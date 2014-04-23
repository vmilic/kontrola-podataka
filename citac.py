# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:01:06 2014

@author: velimir
"""

import pandas as pd
import re

class WlReader:

    def __init__(self):
        self.kanali = {'SO2':'1-SO2-ppb',
                       'CO':'30-CO-ppm',}
        """
        key:regex pattern to match it
        
        pretpostavka je da je naziv kompaktan i da sadrži:
        ime plina i mjernu jedinicu

	pattern je 
	[0-9]+-xxx-yyy

        """
        self.regexKanali={'SO2-ug/m3':r'\b\S*so2\S*ug/m3\b',
                          'NO-ug/m3':r'\b\S*no\S*ug/m3\b',
                          'NOx-ug/m3':r'\b\S*nox\S*ug/m3\b',
                          'NO2-ug/m3':r'\b\S*no2\S*ug/m3\b',
                          'CO-mg/m3':r'\b\S*co\S*mg/m3\b',
                          'O3-ug/m3':r'\b\S*o3\S*ug/m3\b',
                          'PM1-ug/m3':r'\b\S*pm1\S*ug/m3\b',
                          'PM2.5-ug/m3':r'\b\S*(pm2\.5)\S*ug/m3\b',
                          'PM10-ug/m3':r'\b\S*pm10\S*ug/m3\b'}

    def set_kanali_za_citanje(self, mapa):
        self.kanali = mapa
        
    def dodaj_kanal(self,kljuc,kanal):
        if kljuc not in self.kanali.keys():
            self.kanali[kljuc]=kanal
        else:
            raise KeyError('Unable to create new key, it already exists')
   
    def brisi_kanal(self,dkey):
        del self.kanali[dkey]

    def citaj(self, path):
        """reads from CSV file into data frame (path is location of file)"""
        df = pd.read_csv(
            path,
            na_values='-999.00',
            index_col=0,
            parse_dates=[[0,1]],
            dayfirst=True,
            header=0,
            sep=',',
            encoding='latin-1')


        if self.kanali=={}:
            raise KeyError('Neko sranje sa kanalima')
            
        frejmovi={}
        for k in self.kanali:
            v=self.kanali[k]
            i=df.columns.get_loc(v)
            frejmovi[k] = df.iloc[:,i:i+2]
            frejmovi[k][u'flag']=pd.Series(0,index=frejmovi[k].index)
            tmp=frejmovi[k].columns.values
            tmp[0]=u'koncentracija'
            tmp[1]=u'status'
            frejmovi[k].columns=tmp
        
        #regex dio
        for column in df.columns:
            for key in self.regexKanali:
                match=re.search(self.regexKanali[key],column,re.IGNORECASE)
                if match:
                    v=column
                    i=df.columns.get_loc(v)
                    frejmovi[key] = df.iloc[:,i:i+2]
                    frejmovi[key][u'flag']=pd.Series(0,index=frejmovi[key].index)
                    tmp=frejmovi[key].columns.values
                    tmp[0]=u'koncentracija'
                    tmp[1]=u'status'
                    frejmovi[key].columns=tmp
        return frejmovi
        
            
if __name__ == "__main__":
    data = WlReader().citaj('pj.csv')
