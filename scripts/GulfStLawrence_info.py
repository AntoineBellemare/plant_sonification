# captation_series.py

SPRING = 'Serie 6'
SUMMER = 'Serie 23'
FALL = 'Serie 37'
WINTER = 'Serie 38'

seasons = {
    SPRING: 'Spring 2024',
    SUMMER: 'Summer 2024',
    FALL: 'Fall 2024',
    WINTER: 'Winter 2025',
}

plant_common_names = {
    'Amelanchier canadensis': 'Serviceberry',
    'Dryopteris filix-mas': 'Male Fern',
    'Lysimachia ciliata': 'Fringed Loosestrife',
    'Onoclea sensibilis': 'Sensitive Fern',
    'Diervilla lonicera': 'Bush Honeysuckle',
    'Carex intumescens': 'Bladder Sedge',
    'Vaccinium angustifolium': 'Lowbush Blueberry',
    'Symphiotrum novi-belgii': 'New York Aster',
}

plant_common_names_fr = {
    'Amelanchier canadensis': 'Amélanchier du Canada',
    'Dryopteris filix-mas': 'Fougère mâle',
    'Lysimachia ciliata': 'Lysimaque ciliée',
    'Onoclea sensibilis': 'Onoclée sensible',
    'Diervilla lonicera': 'Dierville chèvrefeuille',
    'Carex intumescens': 'Laîche enflée',
    'Vaccinium angustifolium': 'Bleuet à feuilles étroites',
    'Symphiotrum novi-belgii': 'Aster de Nouvelle-Belgique',
}

plant_distances = {
    (0, 1): 40.0, (0, 2): 99.819, (0, 3): 135.341, (0, 4): 114.927, (0, 5): 168.411,
    (0, 6): 184.897, (0, 7): 80.211, (1, 2): 61.954, (1, 3): 106.234, (1, 4): 136.881,
    (1, 5): 171.512, (1, 6): 174.213, (1, 7): 51.379, (2, 3): 107.564, (2, 4): 165.548,
    (2, 5): 168.839, (2, 6): 149.459, (2, 7): 34.355, (3, 4): 243.108, (3, 5): 269.638,
    (3, 6): 256.786, (3, 7): 131.534, (4, 5): 85.266, (4, 6): 135.399, (4, 7): 131.278,
    (5, 6): 61.243, (5, 7): 138.757, (6, 7): 128.509
}