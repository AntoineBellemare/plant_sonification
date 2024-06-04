# Plant Sonification

<p align="center">
  <img src="https://github.com/AntoineBellemare/plant_sonification/assets/49297774/0b7db764-7aa4-42a3-9fa3-e3de856663ca" width="48%" />
</p>

This repository contains code that converts plant electrophysiology into musical structures. By capturing and analyzing the electrical signals of plants, we can translate these bio-signals into unique and dynamic soundscapes. This project aims to bridge the gap between nature and technology, creating a new way to experience the hidden rhythms of plant life.

## Project Overview

This project involves the sonification of various plant species. The electrophysiological data of the plants are recorded over different periods and then converted into musical structures. Each plant's unique bio-signals are captured, processed, and transformed into sound, allowing us to hear the "music" created by these living organisms.

## Captations ⚡️

🌿 Plants studied during Spring 2024 🌿

1. **Acer rubrum**

2. **Rhododendron groenlandicum**
   
3. **Dryopteris mas**

4. **Polystichum acrostichoides**

5. **Alnus**

6. **Geum rivale**

7. **Myrica gale**

8. **Acer pensylvanicum**

## Getting Started 🔑

To get started with this project, clone this repository and navigate to the project directory. The code is written in Python and requires several libraries, which can be installed using the provided `requirements.txt` file.

```sh
git clone https://github.com/yourusername/plant-sonification.git
cd plant-sonification
pip install -r requirements.txt
```

## 📙 Notebook 1 - Temporal Clustering, Melodies, and Spectral Chords 📙

### Objectives

1. **Identify Temporal Patterns**: Use clustering to find patterns in the data over time.
2. **Analyze Spectral Properties**: Examine the spectral centroid and main spectral peaks.
3. **Generate Musical Structures**: Create melodies and chord progressions in MIDI format.

### 1. Temporal Clustering

We use temporal clustering to identify patterns in the electrophysiological data over time, utilizing the spectral centroid as the main feature.

### 2. Spectral Analysis

We analyze the spectral properties of the data:
- **Spectromorphology**: Examining the spectral centroid.
- **Extraction of Spectral Peaks**: Identifying the main spectral peaks using two different methods (EMD, cepstrum).

### 3. Melodies and Chord Progressions in MIDI

We translate the analyzed data into musical structures:
- **Melody Generation**: Mapping the spectral centroid across segments.
- **Chord Progression**: Using the main spectral peaks in each segment to create chord progressions.

### Audio example of spectral chords : 

[Listen to the Audio](https://github.com/AntoineBellemare/plant_sonification/assets/49297774/46def8f3-1409-44e6-b51f-2175a6d2a509)


## 📒 Notebook 2 - Spectromorphological Curves 📒

### Objectives

1. **Extract Spectral Features**: Analyze key spectral features from plant signals.
2. **Generate Curves**: Create curves showing how these features change over time.
3. **Control Parameters for DAWs**: Use the curves to control music software.

### 1. Load and Normalize Data

Import and normalize plant signal data to ensure consistency.

### 2. Extract Features

Calculate spectral centroid, bandwidth, and flux across time to understand the spectral characteristics of the plant signals.

### 3. Create Curves

Generate and smooth curves from these features to highlight significant trends and patterns.

### 4. Export Curves

Save the generated curves as files for use in Digital Audio Workstations (DAWs), enabling them to be used as control parameters for music production.

### Example of curves for 5 days with the same plant

<p align="center">
  <img src="https://github.com/AntoineBellemare/plant_sonification/assets/49297774/585974fa-9edb-40b7-ba27-2a97f26d610b" width="48%" />
  <img src="https://github.com/AntoineBellemare/plant_sonification/assets/49297774/b22b774c-4c4a-4557-a165-982de16fcc3e" width="48%" />
</p>

## 📗 Notebook 3 - Plant Connectivity Analysis 📗

### Objectives

1. **Measure Connectivity**: Analyze the connectivity between plants over time using time-series data.
2. **Visualize Connectivity**: Create visual and animated representations of connectivity patterns.
3. **One-to-One and One-to-Many Connectivity**: Examine individual and averaged connectivity among plants.

### 1. Setup, Imports, and Data Loading

Initialize the environment, import necessary libraries, and load raw data files for the plants.
- **Libraries**: numpy, matplotlib, custom scripts.
- **Data Path**: Define the folder path for plant data files.
- **File Handling**: Load .raw files, filter out NaNs, and normalize the data.

### 2. Measuring Connectivity

Measure the connectivity between plants over time using predefined methods.
- **Harmonic Connectivity**: Apply harmonic connectivity methods and remove artifacts using filters.
- **Data Segmentation**: Chunk the data into segments and calculate connectivity matrices for each segment.

### 3. Visualize and Animate Connectivity

Create visual and animated representations of connectivity patterns.
- **Time-Series Visualization**: Plot connectivity matrices over time.
- **Animation**: Use Matplotlib's animation functions to animate the connectivity data and save it as a GIF.

### 4. Connectivity Analysis: One-to-One and One-to-Many

Examine individual and averaged connectivity among plants.
- **One-to-One Connectivity**: Extract and plot connectivity matrices for a specific plant, smoothing the data for clarity.
- **One-to-Many Connectivity**: Calculate and visualize the average connectivity for each plant, smoothing the data to highlight trends.

### Example of one-to-many connectivity

![plant_connectivity](https://github.com/AntoineBellemare/plant_sonification/assets/49297774/f3f22abb-ccfb-4a0d-8948-047019c43d42)



