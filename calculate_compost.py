import pandas as pd
import numpy as np
import pickle
from compost import CompostBin

if __name__=='__main__':
    # load database
    with open('data/database.pkl', 'rb') as f:
        df = pickle.load(f)

    # instantiate compost bin
    bin = CompostBin(volume=10, density=800, Cfrac=0.4, Nfrac=0.02, wc=0.3)
    bin.load_data(df)
    bin.calc()

    # add to bin
    bin.add('Vegetable produce', 3)
    bin.calc()

    # calculate how much browns to add to balance
    bin.set_target_ratio(0.4)

    # example query
    #query = 'Yard trimmings'
    #print(query)
    #print(df.loc[query])

    # columns
    ''' ['Nitrogen (%dry weight)', 'Carbon (% dry weight',
       'C:N ratio (weight to weight)', 'Moisture content % (wet weight)',
       'Bulk density (pounds per cubic yard)', 'NH4-N %'] '''

    # classes
    ''' ['Apple filter cake', 'Apple pomace', 'Apple-processing sludge',
       'Broiler litter', 'Cattle', 'Cocoa shells', 'Corn cobs', 'Corn stalks',
       'Corrugated cardboard', 'Crab and lobster wastes',
       'Cranberry filter cake', 'Cranberry filter cake (with rice hulls)',
       'Dairy solids', 'Fair waste', 'Horse-general ', 'Laying hens',
       'Newsprint', 'Paper pulp', 'Paunch manure', 'Poultry manure broiler',
       'Rice hulls', 'Sawdust', 'Sewage sludge', 'Shrub trimmings',
       'Straw-general', 'Telephone books', 'Tree trimmings', 'Turkey litter',
       'Vegetable produce', 'Yard trimmings'] '''



    # mix: {item, volume (yd3)}
    mix_volume = {'Yard trimmings': 2, 'Corn cobs':1, 'Newsprint':1, 'Broiler litter':0.3}
