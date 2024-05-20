import numpy as np

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