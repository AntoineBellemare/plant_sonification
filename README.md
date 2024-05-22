# Plant Sonification

This repository contains code that converts plant electrophysiology into musical structures. By capturing and analyzing the electrical signals of plants, we can translate these bio-signals into unique and dynamic soundscapes. This project aims to bridge the gap between nature and technology, creating a new way to experience the hidden rhythms of plant life.

## Project Overview

This project involves the sonification of various plant species. The electrophysiological data of the plants are recorded over different periods and then converted into musical structures. Each plant's unique bio-signals are captured, processed, and transformed into sound, allowing us to hear the "music" created by these living organisms.

## Captations

The following list outlines the plants studied during Spring 2024.

1. **Acer rubrum**

2. **Rhododendron groenlandicum**
   
3. **Dryopteris mas**

4. **Polystichum acrostichoides**

5. **Alnus**

6. **Geum rivale**

7. **Myrica gale**

8. **Acer pensylvanicum**

## Getting Started

To get started with this project, clone this repository and navigate to the project directory. The code is written in Python and requires several libraries, which can be installed using the provided `requirements.txt` file.

```sh
git clone https://github.com/yourusername/plant-sonification.git
cd plant-sonification
pip install -r requirements.txt
```

## Notebook 1 - Temporal Clustering, Melodies and Spectral Chords

### 1. Temporal Clustering

We use temporal clustering to identify patterns in the electrophysiological data over time, utilizing the spectral centroid as the main feature.

### 2. Spectral Analysis

We analyze the spectral properties of the data:
- **Spectromorphology**: Examining the spectral centroid.
- **Cepstrum Analysis**: Identifying the main cepstral peaks.

### 3. Melodies and Chord Progressions in MIDI

We translate the analyzed data into musical structures:
- **Melody Generation**: Mapping the spectral centroid across segments.
- **Chord Progression**: Using the main cepstral peaks in each segment to create chord progressions.

## Notebook 2 - Spectromorphological Curves

### Overview

This notebook explores how to turn plant bio-signals into music using their spectral characteristics. We generate curves that can be used as control parameters in Digital Audio Workstations (DAWs) to create unique soundscapes.

### Objectives

1. **Extract Spectral Features**: Analyze key spectral features from plant signals.
2. **Generate Curves**: Create curves showing how these features change over time.
3. **Control Parameters for DAWs**: Use the curves to control music software.

### Procedure

1. **Load and Normalize Data**: Import and normalize plant signal data.
2. **Extract Features**: Calculate spectral centroid, bandwidth, and flux across time.
3. **Create Curves**: Generate and smooth curves from these features.
4. **Export Curves**: Save the curves as files for DAWs.

