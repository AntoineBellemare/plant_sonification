# Updated script with argparse, progress bars, and parallel processing

import numpy as np
import os
import pandas as pd
import pickle
import sys
import argparse
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import your utility functions
from utils import segment_time_series, get_timedelayed, discretize_data
from utils import (
    compute_transfer_entropy, compute_plv, compute_coherence,
    preprocess_epoch, compute_wpli, compute_imaginary_coherence,
    preprocess_epoch_infraslow, compute_phiid
)

def process_epoch(epoch_idx, epoch_data, keep_idx, metric, preprocess, fs, lowcut, highcut, remove_avg, tau, kind, redundancy):
    if preprocess:
        epoch_data, fs = preprocess_epoch_infraslow(epoch_data, fs, lowcut, highcut, remove_avg)

    if metric == 'transfer_entropy':
        results = compute_transfer_entropy(epoch_data, keep_idx)
    elif metric == 'PLV':
        results = compute_plv(epoch_data, keep_idx)
    elif metric == 'coherence':
        results = compute_coherence(epoch_data, keep_idx, fs=fs)
    elif metric == 'wpli':
        results = compute_wpli(epoch_data, keep_idx)
    elif metric == 'imag_coherence':
        results = compute_imaginary_coherence(epoch_data, keep_idx, fs=fs)
    elif metric == 'PhiID':
        results = compute_phiid(epoch_data, keep_idx, tau=tau, kind=kind, redundancy=redundancy)

    else:
        raise ValueError(f"Metric '{metric}' not implemented.")

    return epoch_idx, results


def main():
    parser = argparse.ArgumentParser(description='Compute plant connectivity metrics.')
    parser.add_argument('--ecosystem', choices=['GulfStLawrence', 'LaurentianMapleGrove', 'JardinFleuris'], required=True,
                        help='Name of the ecosystem to process')
    parser.add_argument('--preprocess', action='store_true',
                        help='Whether to preprocess the data')
    parser.add_argument('--metric', choices=['PLV', 'coherence', 'transfer_entropy', 'wpli', 'imag_coherence', 'PhiID'], required=True,
                    help='Connectivity metric to compute')
    parser.add_argument('--phiid_tau', type=int, default=30, help='Tau (lag) parameter for PhiID (default=5)')
    parser.add_argument('--phiid_kind', type=str, default='gaussian', choices=['gaussian', 'kernel', 'knn'], help='Kind of estimator for PhiID')
    parser.add_argument('--phiid_redundancy', type=str, default='MMI', help='Redundancy function for PhiID')


    args = parser.parse_args()

    ecosystem = args.ecosystem
    preprocess = args.preprocess
    metric = args.metric
    tau = args.phiid_tau
    kind = args.phiid_kind
    redundancy = args.phiid_redundancy

    if ecosystem == 'GulfStLawrence':
        from GulfStLawrence_info import seasons, SPRING, SUMMER, FALL, WINTER, plant_common_names
        list_seasons = [SPRING, SUMMER, FALL, WINTER]
    if ecosystem == 'LaurentianMapleGrove':
        from LaurentianMapleGrove_info import seasons, SPRING, SUMMER, FALL, WINTER, plant_common_names
        list_seasons = [SPRING, SUMMER, FALL, WINTER]
    if ecosystem == 'JardinFleuris':
        from JardinFleuris_info import seasons, plant_common_names
        list_seasons = list(seasons.keys())

    lowcut = 0.1
    highcut = 1.0
    fs = 100
    remove_avg = True

    for SEASON in list_seasons:
        season_name = seasons[SEASON]
        folderpath = f'../plant_data_{ecosystem}/{season_name}'
        dates = [
            d for d in os.listdir(folderpath)
            if os.path.isdir(os.path.join(folderpath, d)) and not d.startswith('Serie')
        ]
        dfs_results = []
        for date in tqdm(dates, desc=f"Dates in {season_name}"):
            data_path = os.path.join(folderpath, date, 'plant_data.npz')
            loaded = np.load(data_path, allow_pickle=True)
            all_data = loaded["data"]
            keep_idx = loaded["keep_idx"]
            date_loaded = loaded["date"]

            epochs = all_data.shape[0]
            connectivity_results = {}

            # Parallel processing of epochs
            with ProcessPoolExecutor() as executor:
                futures = {
                    executor.submit(
                        process_epoch, idx, all_data[idx], keep_idx,
                        metric, preprocess, fs, lowcut, highcut, remove_avg, tau, kind, redundancy
                    ): idx
                    for idx in range(epochs)
                }
                for future in tqdm(as_completed(futures),
                                   total=epochs,
                                   desc=f"Epochs in {date_loaded}",
                                   leave=False):
                    epoch_idx, epoch_res = future.result()
                    connectivity_results[epoch_idx] = epoch_res

            if metric == "PhiID":
                # Results is: {epoch: {ch: {atom: value, ...}, ...}, ...}
                records = []
                for epoch, ch_dict in connectivity_results.items():
                    for ch, atom_vals in ch_dict.items():
                        record = {"epoch": epoch, "plant": ch, **atom_vals}
                        records.append(record)
                df_results = pd.DataFrame(records)
                df_results['date'] = date_loaded
            else:
                df_results = pd.DataFrame.from_dict({
                    (epoch, pair): value
                    for epoch, pairs in connectivity_results.items()
                    for pair, value in pairs.items()
                }, orient='index', columns=[metric])
                df_results['date'] = date_loaded
            dfs_results.append(df_results)

        output_dir = os.path.join(folderpath)    
        if metric == "PhiID":
            fname = f'connectivity_results_{metric}_tau{args.phiid_tau}_kind{args.phiid_kind}_red{args.phiid_redundancy}.pkl'
        else:
            fname = f'connectivity_results_{metric}.pkl'
        output_path = os.path.join(output_dir, fname)

        with open(output_path, 'wb') as f:
            pickle.dump(dfs_results, f)
if __name__ == "__main__":
    main()

