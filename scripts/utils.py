import numpy as np
import dit
from dit.inference import dist_from_timeseries
from dit.multivariate import total_correlation as I, intrinsic_total_correlation as IMI
from collections import namedtuple
import numpy as np
from scipy import stats
from scipy import ndimage
import pandas as pd
import os
import pickle

# Function to segment the time series data based on boundary times
def segment_time_series(data, bound_times):
    """
    Segment the time series data based on provided boundary times.
    
    Args:
        data (np.array): The full time series data.
        bound_times (np.array): The boundary times for segmentation.
        
    Returns:
        list of np.array: A list containing each segment of the time series.
    """
    segments = []
    start_time = 0
    # Create segments of the time series
    for end_time in bound_times:
        segments.append(data[int(start_time):int(end_time)])
        start_time = end_time
    # Add the last segment
    segments.append(data[int(start_time):])
    return segments

def average_across_days(dfs_results, metric='transfer_entropy'):
    df_results_final = []
    for i in range(len(dfs_results)):
        if len(dfs_results[i]) == 0:
            continue
        # Reset index to expose the tuple structure
        df_results = dfs_results[i].reset_index()
        #print(df_results.head())
        # Ensure columns are correctly named
        df_results.columns = ["Index", metric, "date"]

        # Extract Epoch, Plant1, and Plant2 from the multi-index tuple
        df_results[["Epoch", "Plant1", "Plant2"]] = pd.DataFrame(df_results["Index"].apply(lambda x: (x[0], x[1][0], x[1][1])).tolist(), index=df_results.index)

        # Drop the original tuple column
        df_results = df_results.drop(columns=["Index"])

        # Reorder columns
        df_results = df_results[["Epoch", "Plant1", "Plant2", metric, "date"]]
        df_results_final.append(df_results)
    df_combined = pd.concat(df_results_final, ignore_index=True)

    # Group by (Epoch, Plant1, Plant2) and compute the mean Transfer Entropy
    df_avg = df_combined.groupby(["Epoch", "Plant1", "Plant2"], as_index=False)[metric].mean()
    return df_combined, df_avg

# Define namedtuple to store transfer entropy results
TimeDelayed = namedtuple('TimeDelayed', ['timedelayedMU', 'transferE'])

# Function to compute time-delayed mutual information and transfer entropy
def get_timedelayed(ts, length=1):
    """
    Computes time-delayed mutual information and transfer entropy.
    
    Parameters:
        ts (numpy array): Time series of shape (T, 2), where columns are variables.
        length (int): History length (default=1).
        
    Returns:
        TimeDelayed: Named tuple with mutual information and transfer entropy values.
    """
    d = dist_from_timeseries(ts, history_length=length)

    i_past, j_past, i_pres, j_pres = [0], [1], [2], [3]

    timedelayedMU = I(d, [i_past, j_pres])
    transferE = I(d, [i_past, j_pres], j_past)

    return TimeDelayed(timedelayedMU, transferE)

# Function to bin continuous data into discrete values
def discretize_data(data, bins=10):
    """
    Discretizes continuous time series data into discrete bins.
    
    Parameters:
        data (numpy array): 1D array of continuous values.
        bins (int): Number of bins (default=10).
        
    Returns:
        numpy array: Discretized version of the data.
    """
    return np.digitize(data, np.linspace(data.min(), data.max(), bins))



def transfer_entropy(X,Y,delay=1,gaussian_sigma=None):
	'''
	TE implementation: asymmetric statistic measuring the reduction in uncertainty
	for a future value of X given the history of X and Y.
	Calculated through the Kullback-Leibler divergence with conditional probabilities

	Quantifies the amount of information from Y to X.

	author: Sebastiano Bontorin
	mail: sbontorin@fbk.eu

	args:
		- X (1D array):
			time series of scalars (1D array)
		- Y (1D array):
			time series of scalars (1D array)
	kwargs:
		- delay (int): 
			step in tuple (x_n, y_{n - delay}, x_(n - delay))
		- gaussian_sigma (int):
			sigma to be used
			default set at None: no gaussian filtering applied
	returns:
		- TE (float):
			transfer entropy between X and Y given the history of X
	'''

	if len(X)!=len(Y):
		raise ValueError('time series entries need to have same length')

	n = float(len(X[delay:]))

	# number of bins for X and Y using Freeman-Diaconis rule
	# histograms built with numpy.histogramdd
	binX = int( (max(X)-min(X))
				/ (2* stats.iqr(X) / (len(X)**(1.0/3))) )
	binY = int( (max(Y)-min(Y))
				/ (2* stats.iqr(Y) / (len(Y)**(1.0/3))) )

	# Definition of arrays of shape (D,N) to be transposed in histogramdd()
	x3 = np.array([X[delay:],Y[:-delay],X[:-delay]])
	x2 = np.array([X[delay:],Y[:-delay]])
	x2_delay = np.array([X[delay:],X[:-delay]])

	p3,bin_p3 = np.histogramdd(
		sample = x3.T,
		bins = [binX,binY,binX])

	p2,bin_p2 = np.histogramdd(
		sample = x2.T,
		bins=[binX,binY])

	p2delay,bin_p2delay = np.histogramdd(
		sample = x2_delay.T,
		bins=[binX,binX])

	p1,bin_p1 = np.histogramdd(
		sample = np.array(X[delay:]),
		bins=binX)

	# Hists normalized to obtain densities
	p1 = p1/n
	p2 = p2/n
	p2delay = p2delay/n
	p3 = p3/n

	# If True apply gaussian filters at given sigma to the distributions
	if gaussian_sigma is not None:
		s = gaussian_sigma
		p1 = ndimage.gaussian_filter(p1, sigma=s)
		p2 = ndimage.gaussian_filter(p2, sigma=s)
		p2delay = ndimage.gaussian_filter(p2delay, sigma=s)
		p3 = ndimage.gaussian_filter(p3, sigma=s)

	# Ranges of values in time series
	Xrange = bin_p3[0][:-1]
	Yrange = bin_p3[1][:-1]
	X2range = bin_p3[2][:-1]

	# Calculating elements in TE summation
	elements = []
	for i in range(len(Xrange)):
		px = p1[i]
		for j in range(len(Yrange)):
			pxy = p2[i][j]

			for k in range(len(X2range)):
				pxx2 = p2delay[i][k]
				pxyx2 = p3[i][j][k]

				arg1 = float(pxy*pxx2)
				arg2 = float(pxyx2*px)

				# Corrections avoding log(0)
				if arg1 == 0.0: arg1 = float(1e-8)
				if arg2 == 0.0: arg2 = float(1e-8)

				term = pxyx2*np.log2(arg2) - pxyx2*np.log2(arg1) 
				elements.append(term)

	# Transfer Entropy
	TE = np.sum(elements)
	return TE

import numpy as np
from scipy.signal import hilbert, coherence
from utils import discretize_data, get_timedelayed
from scipy.signal import butter, filtfilt

def compute_transfer_entropy(epoch_data, keep_idx):
    num_plants = epoch_data.shape[0]
    discrete_data = np.array([discretize_data(epoch_data[i]) for i in range(num_plants)])
    results = {}

    for i in range(num_plants):
        for j in range(num_plants):
            if i != j:
                ts = np.vstack([discrete_data[i], discrete_data[j]]).T
                transfer_info = get_timedelayed(ts, length=1)
                results[(keep_idx[i], keep_idx[j])] = transfer_info.transferE
    return results

def bandpass_filter(signal, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

def preprocess_epoch(epoch_data, fs, lowcut, highcut, remove_avg=True, order=4):
    """
    Applies bandpass filter and optional average signal subtraction to all plant signals.

    Parameters:
        epoch_data : np.array (plants, samples)
        fs : sampling frequency in Hz
        lowcut, highcut : bandpass range in Hz
        remove_avg : if True, subtracts the mean across channels
        order : filter order (default: 4)

    Returns:
        np.array : filtered data (plants, samples)
    """
    nyq = 0.5 * fs
    b, a = butter(order, [lowcut / nyq, highcut / nyq], btype='band')

    if remove_avg:
        epoch_data = epoch_data - np.mean(epoch_data, axis=0)

    filtered = np.array([filtfilt(b, a, epoch_data[i]) for i in range(epoch_data.shape[0])])
    return filtered

from scipy.signal import decimate, butter, sosfiltfilt

def preprocess_epoch_infraslow(epoch_data, fs, lowcut, highcut,
                                remove_avg=True, decim_factor=None, order=4):
    """
    1) Optionally subtract across-channel mean
    2) Decimate to bring fs down so that 0.01–0.1 Hz is in a safe range
    3) SOS IIR band-pass 0.01–0.1 Hz at the new rate
    Returns filtered_data (plants × samples) and fs_new.
    """
    # 1) remove global mean
    if remove_avg:
        epoch_data = epoch_data - epoch_data.mean(axis=0)

    # 2) choose decimation so that new fs >> 2*highcut
    if decim_factor is None:
        # e.g. ensure fs_new ≈ 2–5 Hz
        decim_factor = max(1, int(np.floor(fs / (5 * highcut))))
    fs_new = fs / decim_factor

    # decimate each channel with zero-phase filtering
    data_dec = decimate(epoch_data, decim_factor, axis=1, zero_phase=True)

    # 3) design SOS band-pass at new Nyquist
    nyq_new = 0.5 * fs_new
    sos = butter(order, [lowcut/nyq_new, highcut/nyq_new],
                 btype='band', output='sos')

    filtered = np.array([sosfiltfilt(sos, ch) for ch in data_dec])

    return filtered, fs_new

def compute_plv(filtered_data, keep_idx):
    num_plants = filtered_data.shape[0]
    analytic_signals = np.array([hilbert(filtered_data[i]) for i in range(num_plants)])
    phases = np.angle(analytic_signals)
    results = {}

    for i in range(num_plants):
        for j in range(num_plants):
            if i != j:
                phase_diff = phases[i] - phases[j]
                plv = np.abs(np.sum(np.exp(1j * phase_diff)) / len(phase_diff))
                results[(keep_idx[i], keep_idx[j])] = plv
    return results


def compute_coherence(epoch_data, keep_idx, fs=256):  # Adjust `fs` if needed
    num_plants = epoch_data.shape[0]
    results = {}

    for i in range(num_plants):
        for j in range(num_plants):
            if i != j:
                f, Cxy = coherence(epoch_data[i], epoch_data[j], fs=fs)
                results[(keep_idx[i], keep_idx[j])] = np.mean(Cxy)  # or pick a freq band
    return results

def compute_imaginary_coherence(epoch_data, keep_idx, fs=256):
    num_plants = epoch_data.shape[0]
    results = {}
    for i in range(num_plants):
        for j in range(num_plants):
            if i != j:
                f, Cxy = coherence(epoch_data[i], epoch_data[j], fs=fs)
                iCoh = np.imag(Cxy)
                results[(keep_idx[i], keep_idx[j])] = np.mean(iCoh)
    return results

def compute_wpli(filtered_data, keep_idx):
    """
    Computes the Weighted Phase Lag Index (wPLI) for each pair of signals.

    Parameters:
        filtered_data (ndarray): shape = (n_channels, n_samples), bandpassed signals.
        keep_idx (list): list of indices or labels for each channel.

    Returns:
        dict: {(i, j): wPLI} for all i < j
    """
    num_channels = filtered_data.shape[0]
    results = {}

    # Compute analytic signals
    analytic_signals = np.array([hilbert(filtered_data[i]) for i in range(num_channels)])

    for i in range(num_channels):
        for j in range(i+1, num_channels):
            cross_spectrum = analytic_signals[i] * np.conj(analytic_signals[j])
            imag_cross = np.imag(cross_spectrum)

            num = np.abs(np.mean(np.sign(imag_cross) * np.abs(imag_cross)))
            denom = np.mean(np.abs(imag_cross))

            wpli = num / (denom + 1e-10)  # add epsilon to avoid div-by-zero

            results[(keep_idx[i], keep_idx[j])] = wpli
            results[(keep_idx[j], keep_idx[i])] = wpli  # optional symmetry
    return results

