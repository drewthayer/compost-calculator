import numpy as np

class CompostBin(object):
    def __init__(self, volume, density, Cfrac, Nfrac, wc):
        self.vol = volume # yd3
        self.dense = density # lb per yd3
        self.Cfrac = Cfrac # fraction of dry weight
        self.Nfrac = Nfrac # fraction of dry weight
        self.wc = wc # fractional water content by weight
        # calculate:
        self.weight =  self.vol * self.dense
        self.dry_weight = self.weight * (1 - self.wc)
        self.C = self.Cfrac * self.dry_weight
        self.N = self.Nfrac * self.dry_weight
        self.CNratio = self.C/self.N

    def load_data(self, dataframe):
        ''' loads dataframe of item data '''
        self.df = dataframe

    def add(self, item, volume):
        ''' add an item, at a specific volume'''
        data = self.df.loc[item]
        weight = data['density'] * volume
        wc = data['wc']/100 # wc by weight of addition
        dry_weight = weight * (1 - wc)
        c = dry_weight * data['C_pct']/100 # dry weight of carbon in addition
        n = dry_weight * data['N_pct']/100 # dry weight of N in addition

        print('\nadd {} yd3 of {}'.format(volume, item))

        # update pile
        self.wc = (self.weight*self.wc + weight*wc)/(self.weight + weight)
        self.vol += volume
        self.weight += weight
        self.dense = self.weight/self.vol
        self.C += c
        self.N += n
        self.CNratio = self.C/self.N


    def calc(self):
        print('\n bin contents:')
        print('C/N ratio = {:0.2f}'.format(self.CNratio))
        print('volume = {:0.2f} yd3'.format(self.vol))
        print('density = {:0.2f} lb/yd3'.format(self.dense))
        print('water content = {:0.2f}'.format(self.wc))
