import pandas as pd
import numpy as np
import pickle
from compost import CompostBin
import time

if __name__=='__main__':
    # load database
    with open('data/database.pkl', 'rb') as f:
        df = pickle.load(f)

    # instantiate compost bin w/ straw
    bin = CompostBin(volume=0.1, density=203.5, Cfrac=0.056, Nfrac=0.041, wc=0.095)
    bin.load_data(df)
    bin.calc()

    # conversions
    gal_yd3 = 0.00495113

    # volumes
    # volume of 1 square bale bale: 16” high x 22” wide x 44”
    # bale_vol_in3 = 16*22*44
    # bale_vol_yd3 = bale_vol_in3 / 46656
    # volume of 1 PRF bale: 4' x 4' x 3.15' = 50.27 ft3
    bale_vol_ft3 = 4 * 4 * 3.15
    bale_vol_yd3 = bale_vol_ft3 / 27

    # bucket volume: 78.75 inches in width and John Deere’s website claims it carries a heaped load of 14.2 ft^3 or 0.40m^3
    bucket_vol_ft3 = 14.2
    bucket_vol_yd3 = bucket_vol_ft3 / 27

    # add to bin
    #bin.add('Straw-general', 1*bale_vol_yd3)
    #bin.calc()

    #calculate how much browns to add to balance
    bin.set_target_ratio(0.4)

    # add for Feb
    #for i in range(21):
    #bin.add('Straw-general', 1*bale_vol_yd3)

    #add = 4+8+12+8+4+8+4
    #for i in range(add):
    #    bin.add('Sawdust', 1*bucket_vol_yd3)

    # add shedule file
    schd = pd.read_csv('data/additions_schedule_prf_1.csv')
    schd.columns = ['date','bedding_bales','wood_chips_yd3','wood_chips_bucket']

    #schd.columns = ['Date', 'Bedding bales', 'yd3 wood chips',
    #   'Buckets of Large wood chips', 'Buckets of Mixed wood chips']

    # fill in un-recorded days
    dt = pd.to_datetime(schd.date)
    schd.index = dt
    schd.drop('date', axis=1, inplace=True)

    # new dataframe for manure additions
    daily_manure_gal = 1455
    daterange = pd.date_range(start=schd.index[0], end=schd.index[-1])
    manure_xx = np.ones(len(daterange)) * daily_manure_gal
    dd = {'date':daterange, 'manure_gal':manure_xx}
    manure_df = pd.DataFrame(dd)
    manure_df = manure_df.set_index('date')

    # merge
    schd = manure_df.join(schd, how='outer')
    schd.fillna(0, inplace=True)

    # instantiate bin_vol column as empty
    schd['bin_vol'] = None

    #schd['manure_gal'] = schd['manure_gal'] * 1.5 # REMOVE THIS

    # add by day
    bin_vol = []
    bin_ratio = []
    bin_wc = []
    for i in schd.index:
        # values
        #date = schd.loc[i,:]['date']
        manure_gal = schd.loc[i,:]['manure_gal']
        bedding_bales = schd.loc[i,:]['bedding_bales']
        chip_yd3 = schd.loc[i,:]['wood_chips_yd3']
        chip_bucket = schd.loc[i,:]['wood_chips_bucket']

        # add
        bin.add('Cattle', manure_gal * gal_yd3)
        bin.add('Straw-general', bedding_bales * bale_vol_yd3)
        bin.add('Sawdust', chip_yd3)
        bin.add('Sawdust', chip_bucket * bucket_vol_yd3)

        # new columns
        bin_vol.append(bin.vol)
        bin_ratio.append(bin.CNratio)
        bin_wc.append(bin.wc)

    schd['bin_vol'] = bin_vol
    schd['bin_ratio'] = bin_ratio
    schd['bin_wc'] = bin_wc

    # write file
    schd.to_csv('output/output_1455gal_{}.csv'.format(time.strftime('%Y_%m_%d')))

    #bin.calc()
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
