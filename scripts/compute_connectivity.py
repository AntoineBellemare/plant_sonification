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
    preprocess_epoch_infraslow
)

def process_epoch(epoch_idx, epoch_data, keep_idx, metric, preprocess, fs, lowcut, highcut, remove_avg):
    """Worker function to process a single epoch."""
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
    else:
        raise ValueError(f"Metric '{metric}' not implemented.")

    return epoch_idx, results

def main():
    parser = argparse.ArgumentParser(description='Compute plant connectivity metrics.')
    parser.add_argument('--ecosystem', choices=['GulfStLawrence', 'LaurentianMapleGrove'], required=True,
                        help='Name of the ecosystem to process')
    parser.add_argument('--preprocess', action='store_true',
                        help='Whether to preprocess the data')
    parser.add_argument('--metric', choices=['PLV', 'coherence', 'transfer_entropy', 'wpli', 'imag_coherence'], required=True,
                        help='Connectivity metric to compute')
    args = parser.parse_args()

    ecosystem = args.ecosystem
    preprocess = args.preprocess
    metric = args.metric

    if ecosystem == 'GulfStLawrence':
        from GulfStLawrence_info import seasons, SPRING, SUMMER, FALL, WINTER, plant_common_names
    else:
        from LaurentianMapleGrove_info import seasons, SPRING, SUMMER, FALL, WINTER, plant_common_names

    lowcut = 0.1
    highcut = 1.0
    fs = 100
    remove_avg = True
    list_seasons = [SPRING, SUMMER, FALL, WINTER]

    for SEASON in list_seasons:
        season_name = seasons[SEASON]
        folderpath = f'../plant_data_{ecosystem}/{season_name}'
        dates = [d for d in os.listdir(folderpath) if os.path.isdir(os.path.join(folderpath, d))]
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
                        metric, preprocess, fs, lowcut, highcut, remove_avg
                    ): idx
                    for idx in range(epochs)
                }
                for future in tqdm(as_completed(futures),
                                   total=epochs,
                                   desc=f"Epochs in {date_loaded}",
                                   leave=False):
                    epoch_idx, epoch_res = future.result()
                    connectivity_results[epoch_idx] = epoch_res

            # Build DataFrame and collect
            df_results = pd.DataFrame.from_dict({
                (epoch, pair): value
                for epoch, pairs in connectivity_results.items()
                for pair, value in pairs.items()
            }, orient='index', columns=[metric])
            df_results['date'] = date_loaded
            dfs_results.append(df_results)

        output_dir = os.path.join(folderpath)    
        output_path = os.path.join(output_dir, f'connectivity_results_{metric}.pkl')
        with open(output_path, 'wb') as f:
            pickle.dump(dfs_results, f)
if __name__ == "__main__":
    main()

