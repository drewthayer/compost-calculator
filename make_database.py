import sqlite3
import pandas as pd
import numpy as np
import pickle

import matplotlib.pyplot as plt
from sqlite3 import Error

def connect_to_sql(db_file):
    """ create a database connection to a SQLite database
    input: path to database file
    output: sql connection
    """
    try:
        conn = sqlite3.connect(db_file)
        print('sqlite {}'.format(sqlite3.version))
        return conn
    except Error as e:
        print(e)

if __name__=='__main__':
    params = {'header':2, 'sep':',','thousands':','}
    chars_df = pd.read_csv('feedstock_characteristics_clean.csv', **params)
    chars_df.infer_objects() # infers float

    # clean file
    drop = []
    for i in [11,10,0]: # indices of cols to drop, last to first
        drop.append(chars_df.columns[i])
        chars_df.drop(chars_df.columns[i], axis=1, inplace=True)

    chars_df.drop(chars_df.index[53:], inplace=True)

    # average rows with multiple entries
    average_chars_df = chars_df.groupby(['Material']).mean()

    # rename columns
    average_chars_df.columns = ['N_pct', 'C_pct',
       'CN_ratio', 'wc', 'density', 'NH4_pct']

    # save dataframe to pickle
    with open('data/database.pkl', 'wb') as f:
        pickle.dump(average_chars_df, f)

    # example query
    query = 'Yard trimmings'
    #print(query)
    #print(average_chars_df.loc[query])


    # columns
    ''' ['Nitrogen (%dry weight)', 'Carbon (% dry weight',
       'C:N ratio (weight to weight)', 'Moisture content % (wet weight)',
       'Bulk density (pounds per cubic yard)', 'NH4-N %'] '''

    # options
    ''' ['Apple filter cake', 'Apple pomace', 'Apple-processing sludge',
       'Broiler litter', 'Cattle', 'Cocoa shells', 'Corn cobs', 'Corn stalks',
       'Corrugated cardboard', 'Crab and lobster wastes',
       'Cranberry filter cake', 'Cranberry filter cake (with rice hulls)',
       'Dairy solids', 'Fair waste', 'Horse-general ', 'Laying hens',
       'Newsprint', 'Paper pulp', 'Paunch manure', 'Poultry manure broiler',
       'Rice hulls', 'Sawdust', 'Sewage sludge', 'Shrub trimmings',
       'Straw-general', 'Telephone books', 'Tree trimmings', 'Turkey litter',
       'Vegetable produce', 'Yard trimmings'] '''
