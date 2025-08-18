# captation_series.py


SPRING1 = "Serie 7"
SPRING2 = "Serie 40"
SPRING3 = "Serie 41"
SPRING4 = "Serie 42"
SPRING5 = "Serie 43"
SPRING6 = "Serie 44"
SPRING7 = "Serie 45"
SPRING8 = "Serie 46"
SUMMER1 = "Serie 10"

seasons = {
    SPRING1: 'Spring 2024_01',
    SPRING2: 'Spring 2025_02',
    SPRING3: 'Spring 2025_03',
    SPRING4: 'Spring 2025_04',
    SPRING5: 'Spring 2025_05',
    SPRING6: 'Spring 2025_06',
    SPRING7: 'Spring 2025_07',
    SUMMER1: 'Summer 2024_01'
}

serie_code_map = {
    "Serie 7": "SPRING1",
    "Serie 40": "SPRING2",
    "Serie 41": "SPRING3",
    "Serie 42": "SPRING4",
    "Serie 43": "SPRING5",
    "Serie 44": "SPRING6",
    "Serie 45": "SPRING7",
    "Serie 46": "SPRING8",
    "Serie 10": "SUMMER1"
}

plant_common_names = {
    "SPRING1": {  # Serie 7
        "Iris": "Iris",
        "Asphodeline lutea": "King's spear",
        "Hemerocallis": "Daylily",
        "Lilium candidum": "Madonna lily",
        "Salvia x sylvestris": "Woodland sage",
        "Empty": "Empty channel",
        "Paeonia": "Peony",
        "Lilium henryi var.citrinum": "Henry's lily (yellow form)",
    },
    "SUMMER1": {  # Serie 10
        "Lilium Alexis": "Lily 'Alexis'",
        "Iris setosa": "Beachhead iris",
        "Hemerocallis Ruby spider": "Daylily 'Ruby Spider'",
        "Paeonia lactiflora": "Chinese peony",
        "Hemerocallis Queen Esther": "Daylily 'Queen Esther'",
        "Cephalanthus occidentalis": "Buttonbush",
        "Aconitum lycoctonum": "Wolfsbane",
        "Peaeonia suffruticosa": "Tree peony",
    },
    "SPRING2": {  # Serie 40
        "Actaea simplex atropurpurea": "Bugbane (black cohosh)",
        "Paeonia La Clément": "Peony 'La Clement'",
        "Lilium": "Lily",
        "Paeonia officinalis": "Common peony",
        "Iris spuria": "Spuria iris",
        "Symphyotrichum novae-angliae": "New England aster",
        "Hemerocallis forrestii Mrs. Hugh Johnson": "Daylily 'Mrs. Hugh Johnson'",
        "Allium rosenbachianum": "Rosenbach's onion",
    },
    "SPRING3": {  # Serie 41
        "Astilbe": "Astilbe",
        "Iris 'Regard'": "Iris 'Regard'",
        "Papaver orientale": "Oriental poppy",
        "Iris 'Royal Scot'": "Iris 'Royal Scot'",
        "Paeonia lactiflora": "Chinese peony",
        "Veronica grandis": "Large speedwell",
        "Lilium sargentiae": "Sargent's lily",
        "Hemerocallis forrestii Daylily": "Daylily (H. forrestii)",
    },
    "SPRING4": {  # Serie 42
        "Aster mongolicus": "Mongolian aster",
        "Iris 'Caesar'": "Iris 'Caesar'",
        "Paeonia tenuifolia": "Fernleaf peony",
        "Lilium 'Brenda Watts'": "Lily 'Brenda Watts'",
        "Paeonia lactiflora": "Chinese peony",
        "Iris lutescens": "Dwarf iris",
        "Iris lactea": "Milk iris",
        "Hemerocallis Daylily 'Summer Blush'": "Daylily 'Summer Blush'",
    },
    "SPRING5": {  # Serie 43
        "Echinacea tennesseensis": "Tennessee coneflower",
        "Paeonia 'Yellow Crown'": "Peony 'Yellow Crown'",
        "Doellingeria umbellata": "Flat-topped aster",
        "Miscanthus sinensis 'Rotsilber'": "Chinese silver grass 'Rotsilber'",
        "Iris 'Raspberry Ice'": "Iris 'Raspberry Ice'",
        "Iris 'Borbeleta'": "Iris 'Borbeleta'",
        "Paeonia lactiflora 'Mons. Jules Elie'": "Peony 'Mons. Jules Elie'",
        "Lilium 'Prairie Harlequin'": "Lily 'Prairie Harlequin'",
    },
    "SPRING6": {  # Serie 44
        "Echinops tjanschanicus": "Globe thistle (Tien Shan)",
        "Salvia nemorosa": "Woodland sage",
        "Paeonia 'Legion of Honor'": "Peony 'Legion of Honor'",
        "Paeonia  'Chief Black Hawk'": "Peony 'Chief Black Hawk'",
        "Syringa vulgaris 'Ethiopia'": "Common lilac 'Ethiopia'",
        "Dianthus pinifolius": "Pineleaf pink",
        "Camassia leichtlinii": "Great camas",
        "Lilium 'Royal Delight'": "Lily 'Royal Delight'",
    },
    "SPRING7": {  # Serie 45
        "Iris Sibirica \"Fourfold white'": "Siberian iris 'Fourfold White'",
        "Lilium lancifolium  'Flore pleno'": "Double tiger lily",
        "Paeonia 'Rushkight's grandchild'": "Peony 'Rushkight's Grandchild'",
        "Miscanthus x ogiformis": "Silver grass (Miscanthus)",
        "Solidago rugosa 'Fireworks'": "Goldenrod 'Fireworks'",
        "Hemerocallis 'Chipper cherry'": "Daylily 'Chipper Cherry'",
        "Iris pallida ssp. illiryca": "Sweet iris (Illyrian)",
        "Iris 'Benton rubeo'": "Iris 'Benton Rubeo'",
    },
    "SPRING8": {  # Serie 46
        "Paeonia 'The Mackinac Grand'": "Peony 'The Mackinac Grand'",
        "Hemerocallis 'Rose F. Kennedy'": "Daylily 'Rose F. Kennedy'",
        "Paeonia lactiflora 'Angel Cheeks'": "Peony 'Angel Cheeks'",
        "Iris 'Tree of Songs'": "Iris 'Tree of Songs'",
        "Paeonia 'Ludovica'": "Peony 'Ludovica'",
        "Paeonia 'Garden Treasure'": "Peony 'Garden Treasure'",
        "Paeonia 'Coral Sunset'": "Peony 'Coral Sunset'",
        "Iris 'Coronation anthem'": "Iris 'Coronation Anthem'",
    },
}


plant_distances = {
    (3, 6): 50,
    (7, 6): 275,
    (7, 3): 300,
    (7, 1): 180,
    (1, 6): 290,
    (1, 3): 285
}