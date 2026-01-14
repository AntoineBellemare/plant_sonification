"""
Generate aggregated PhiID metrics CSV files.
One CSV per series with IIT and Information Dynamics metrics averaged across all plants.
"""

import os
import sys
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import argparse

# Add scripts to path
sys.path.append(os.path.dirname(__file__))
from JardinFleuris_info import seasons

# Configuration
SERIES_TO_PROCESS = ["Serie 7", "Serie 40", "Serie 43", "Serie 44", "Serie 45", "Serie 46"]
ECOSYSTEM = "JardinFleuris"
METRIC = "PhiID"
OUTPUT_DIR = "../data/processed/phiid_aggregated_metrics"

# 16 PhiID atoms
ATOM_NAMES = [
    "rtr", "rtx", "rty", "rts",
    "xtr", "xtx", "xty", "xts",
    "ytr", "ytx", "yty", "yts",
    "str", "stx", "sty", "sts"
]

# Aggregated metrics
IIT_METRICS = {
    "IIT_Information_storage": ["xtx", "yty", "rtr", "sts"],
    "IIT_Transfer_entropy": ["xty", "xtr", "str", "sty"],
    "IIT_Causal_density": ["xtr", "ytr", "sty", "str", "xty", "ytx", "stx"],
    "IIT_Integrated_information": ["rts", "xts", "sts", "sty", "str", "yts", "ytx", "stx", "xty"],
}

INFO_DYNAMICS_METRICS = {
    "InfoDyn_Storage": ["rtr", "xtx", "yty", "sts"],
    "InfoDyn_Copy": ["xtx", "yty"],
    "InfoDyn_Transfer": ["xty", "ytx"],
    "InfoDyn_Erasure": ["rtx", "rty"],
    "InfoDyn_Downward_causation": ["sty", "stx", "str"],
    "InfoDyn_Upward_causation": ["xts", "yts", "rts"],
}

# Combine both metric sets
ALL_METRICS = {**IIT_METRICS, **INFO_DYNAMICS_METRICS}


def load_phiid_data(series_code):
    """
    Load PhiID connectivity results for a given series.
    
    Args:
        series_code: Series identifier (e.g., "Serie 7")
    
    Returns:
        List of DataFrames, one per day
    """
    series_folder = seasons[series_code]
    file_path = f"../data/processed/plant_data_{ECOSYSTEM}/{series_folder}/connectivity_results_{METRIC}_tau100_kindgaussian_redMMI.pkl"
    
    try:
        with open(file_path, 'rb') as f:
            dfs_results = pickle.load(f)
        return dfs_results
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


def compute_aggregated_metrics_for_day(df_day):
    """
    Compute aggregated metrics from pairwise PhiID data for one day.
    Average across all plants and connections for each epoch.
    
    Args:
        df_day: DataFrame with columns ['epoch', 'plant', 'rtr', 'rtx', ...]
                where 'plant' contains tuples (plant1, plant2)
    
    Returns:
        DataFrame with columns ['Epoch', 'Date', metric1, metric2, ...]
    """
    if len(df_day) == 0:
        return pd.DataFrame()
    
    df = df_day.copy()
    
    # Get date
    date = df['date'].iloc[0] if 'date' in df.columns else None
    
    # Rename for consistency
    df = df.rename(columns={"epoch": "Epoch"})
    
    # Get atom columns and clean infinities
    atom_cols = [c for c in df.columns if c in ATOM_NAMES]
    for col in atom_cols:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
    
    # For each epoch, average atom values across all pairs
    df_avg_atoms = df.groupby("Epoch")[atom_cols].mean().reset_index()
    
    # Compute aggregated metrics
    for metric_name, atoms in ALL_METRICS.items():
        atoms_present = [a for a in atoms if a in df_avg_atoms.columns]
        metric_sum = df_avg_atoms[atoms_present].sum(axis=1, skipna=True)
        all_nan = df_avg_atoms[atoms_present].isna().all(axis=1)
        metric_sum[all_nan] = np.nan
        
        # Special handling for Integrated information (subtract rtr)
        if "Integrated_information" in metric_name and "rtr" in df_avg_atoms.columns:
            metric_sum = metric_sum - df_avg_atoms["rtr"]
        
        df_avg_atoms[metric_name] = metric_sum
    
    # Keep only Epoch, Date, and aggregated metrics
    metric_cols = list(ALL_METRICS.keys())
    result_cols = ["Epoch"] + metric_cols
    df_result = df_avg_atoms[result_cols].copy()
    df_result['Date'] = date
    
    return df_result


def process_series(series_code, output_dir):
    """
    Process one series and save aggregated metrics to CSV (one per day).
    """
    print(f"Processing {series_code} ({seasons[series_code]})...")
    
    # Load PhiID data
    dfs_results = load_phiid_data(series_code)
    
    if dfs_results is None:
        print(f"  Skipping - data not found")
        return
    
    # Create series subfolder
    series_name = seasons[series_code].replace(" ", "_")
    series_dir = Path(output_dir) / series_name
    series_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each day
    saved_count = 0
    for day_idx, df_day in enumerate(dfs_results):
        if len(df_day) == 0:
            continue
        
        df_metrics = compute_aggregated_metrics_for_day(df_day)
        if len(df_metrics) == 0:
            continue
        
        # Get date for filename
        date = df_metrics['Date'].iloc[0]
        
        # Reorder columns: Date, Epoch, then metrics
        metric_cols = list(ALL_METRICS.keys())
        df_metrics = df_metrics[['Date', 'Epoch'] + metric_cols]
        
        # Save to CSV (one per day)
        output_file = series_dir / f"aggregated_metrics_{date}.csv"
        df_metrics.to_csv(output_file, index=False)
        
        n_epochs = len(df_metrics)
        print(f"  Saved: {output_file.name} ({n_epochs} epochs)")
        saved_count += 1
    
    if saved_count == 0:
        print(f"  No data to save")
    else:
        print(f"  Total: {saved_count} day(s) processed")


def main():
    """Main processing loop."""
    parser = argparse.ArgumentParser(description='Generate aggregated PhiID metrics CSV files.')
    parser.add_argument('--output_dir', type=str, default=OUTPUT_DIR,
                        help='Output directory for CSV files')
    parser.add_argument('--series', type=str, nargs='+', default=SERIES_TO_PROCESS,
                        help='Series to process')
    
    args = parser.parse_args()
    
    print(f"PhiID Aggregated Metrics Generation")
    print(f"=" * 60)
    print(f"Output directory: {args.output_dir}")
    print(f"Series to process: {args.series}")
    print()
    
    for series_code in args.series:
        if series_code not in seasons:
            print(f"Skipping unknown series: {series_code}")
            continue
        
        process_series(series_code, args.output_dir)
        print()
    
    print("Processing complete!")


if __name__ == "__main__":
    main()
