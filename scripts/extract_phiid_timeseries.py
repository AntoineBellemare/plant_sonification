"""
Extract PhiID atom time series from connectivity results.

Two extraction modes:
1. Per-plant: Average atom values across all connections for each plant
2. Pairwise: Keep the full pairwise plant connection structure

Generates CSV files with 16 atom time series per series per day.
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
OUTPUT_DIR = "../data/processed/phiid_timeseries"
MODE = "per_plant"  # Options: "per_plant" or "pairwise"

# 16 PhiID atoms
ATOM_NAMES = [
    "rtr", "rtx", "rty", "rts",
    "xtr", "xtx", "xty", "xts",
    "ytr", "ytx", "yty", "yts",
    "str", "stx", "sty", "sts"
]


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


def extract_plant_timeseries(df_day):
    """
    Extract time series for each plant from pairwise PhiID data.
    For each plant at each epoch, average the atom values across all its connections.
    
    Args:
        df_day: DataFrame with columns ['epoch', 'plant', 'rtr', 'rtx', ...]
                where 'plant' contains tuples (plant1, plant2)
    
    Returns:
        DataFrame with columns ['Epoch', 'Plant', 'rtr', 'rtx', ...]
    """
    if len(df_day) == 0:
        return pd.DataFrame()
    
    df = df_day.copy()
    
    # Split plant tuple into Plant1 and Plant2
    df[["Plant1", "Plant2"]] = pd.DataFrame(df["plant"].tolist(), index=df.index)
    df = df.rename(columns={"epoch": "Epoch"})
    
    # Get atom columns
    atom_cols = [c for c in df.columns if c in ATOM_NAMES]
    
    # Create two views: one for each direction of the connection
    # Plant1 perspective
    df_p1 = df[["Epoch", "Plant1"] + atom_cols].copy()
    df_p1 = df_p1.rename(columns={"Plant1": "Plant"})
    
    # Plant2 perspective
    df_p2 = df[["Epoch", "Plant2"] + atom_cols].copy()
    df_p2 = df_p2.rename(columns={"Plant2": "Plant"})
    
    # Combine both perspectives
    df_combined = pd.concat([df_p1, df_p2], ignore_index=True)
    
    # For each (Epoch, Plant), average across all connections
    df_plant_ts = df_combined.groupby(["Epoch", "Plant"], as_index=False)[atom_cols].mean()
    
    return df_plant_ts


def extract_pairwise_timeseries(df_day):
    """
    Keep the pairwise structure of PhiID data.
    
    Args:
        df_day: DataFrame with columns ['epoch', 'plant', 'rtr', 'rtx', ...]
                where 'plant' contains tuples (plant1, plant2)
    
    Returns:
        DataFrame with columns ['Epoch', 'Plant1', 'Plant2', 'rtr', 'rtx', ...]
    """
    if len(df_day) == 0:
        return pd.DataFrame()
    
    df = df_day.copy()
    
    # Split plant tuple into Plant1 and Plant2
    df[["Plant1", "Plant2"]] = pd.DataFrame(df["plant"].tolist(), index=df.index)
    df = df.rename(columns={"epoch": "Epoch"})
    
    # Get atom columns
    atom_cols = [c for c in df.columns if c in ATOM_NAMES]
    
    # Return clean pairwise structure
    df_pairwise = df[["Epoch", "Plant1", "Plant2"] + atom_cols]
    
    return df_pairwise


def save_timeseries_csv(df_ts, series_code, day_idx, output_dir, mode, date=None):
    """
    Save time series to CSV.
    
    Args:
        df_ts: DataFrame with time series data
        series_code: Series identifier
        day_idx: Day index
        output_dir: Output directory path
        mode: "per_plant" or "pairwise"
        date: Date string (optional)
    """
    if len(df_ts) == 0:
        print(f"  No data for {series_code}, day {day_idx}")
        return
    
    # Create series subfolder
    series_name = seasons[series_code].replace(" ", "_")
    series_dir = Path(output_dir) / mode / series_name
    series_dir.mkdir(parents=True, exist_ok=True)
    
    # Save CSV with date if available
    if date:
        output_file = series_dir / f"phiid_atoms_{date}.csv"
    else:
        output_file = series_dir / f"phiid_atoms_day{day_idx:02d}.csv"
    
    df_ts.to_csv(output_file, index=False)
    
    if mode == "per_plant":
        n_plants = df_ts["Plant"].nunique()
        n_epochs = df_ts["Epoch"].nunique()
        print(f"  Saved: {output_file.name} ({n_plants} plants, {n_epochs} epochs)")
    else:
        n_pairs = len(df_ts.groupby(["Plant1", "Plant2"]))
        n_epochs = df_ts["Epoch"].nunique()
        print(f"  Saved: {output_file.name} ({n_pairs} pairs, {n_epochs} epochs)")


def main():
    """Main processing loop."""
    parser = argparse.ArgumentParser(description='Extract PhiID time series from connectivity results.')
    parser.add_argument('--mode', choices=['per_plant', 'pairwise'], default='per_plant',
                        help='Extraction mode: per_plant (averaged) or pairwise (full structure)')
    parser.add_argument('--output_dir', type=str, default=OUTPUT_DIR,
                        help='Output directory for CSV files')
    
    args = parser.parse_args()
    mode = args.mode
    output_dir = args.output_dir
    
    print(f"PhiID Time Series Extraction")
    print(f"=" * 60)
    print(f"Mode: {mode}")
    print(f"Output directory: {output_dir}")
    print(f"Series to process: {SERIES_TO_PROCESS}")
    print()
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Process each series
    for series_code in SERIES_TO_PROCESS:
        print(f"Processing {series_code} ({seasons[series_code]})...")
        
        # Load PhiID data
        dfs_results = load_phiid_data(series_code)
        
        if dfs_results is None:
            print(f"  Skipping {series_code} - data not found")
            continue
        
        # Process each day
        for day_idx, df_day in enumerate(dfs_results):
            if len(df_day) == 0:
                continue
            
            # Extract date if available
            date = df_day['date'].iloc[0] if 'date' in df_day.columns else None
            
            # Extract time series based on mode
            if mode == 'per_plant':
                df_ts = extract_plant_timeseries(df_day)
            else:  # pairwise
                df_ts = extract_pairwise_timeseries(df_day)
            
            # Save to CSV
            save_timeseries_csv(df_ts, series_code, day_idx, output_dir, mode, date)
        
        print()
    
    print("Processing complete!")


if __name__ == "__main__":
    main()
