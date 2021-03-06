# -*- coding: utf-8 -*-
"""
Velimir
-Ispravljena pogreška, agreg--- min i std su bili zamjenjeni
-Ispravljena pogreška prilikom inicijalizacije agregatora u testnom dijelu

-ostala samo jedna pogreška/upozorenje

C:\WinPython-32bit-3.3.3.3\python-3.3.3\lib\site-packages\pandas\core\
frame.py:1686: UserWarning: 
Boolean Series key will be reindexed to match DataFrame index.
"DataFrame index.", UserWarning)

Grafikon se iscrtava ok.. nisam 100% siguran na što se upozorenje odnosi.
Potencijalno na određivanje sliceova getSlajs, ili kod auto_validacije
jer se tamo korisit boolean series key da se izvadi slice, ali warning kaže da
se pandas sam pobrinuo za poravnavanje podataka (alignment). Možemo li
ignorirati upozorenje??
"""

import pandas as pd
from datetime import timedelta
from citac import WlReader
import matplotlib.pyplot as plt
import auto_validacija
import uredjaj
from datetime import datetime

class Agregator(object):
    
    uredjaji=[]

    def __init__(self, uredjaji):
        self.uredjaj = uredjaji
        
    def dodajUredjaj(self, uredjaj):
        self.uredjaji.append(uredjaj)
        
            
    def setDataFrame(self, df):
        self.__df = df
        self.pocetak = df.index.min()+pd.DateOffset(hours=1) 
        self.kraj = df.index.max()
        self.sviSati=pd.date_range(self.pocetak, self.kraj, freq='H')
    
    def agreg(self, kraj):
        #modifikacija get slice kopira direktno, bez flag testa
        ddd = self.getSlajs(kraj)
        #selekcija prema flagu za agreg
        ddd=ddd[ddd[u'flag']>0]
        avg=ddd.mean().iloc[0]
        std=ddd.std().iloc[0]
        max=ddd.max().iloc[0]
        min=ddd.min().iloc[0]
        med=ddd.quantile(0.5).iloc[0]
        q95=ddd.quantile(0.05).iloc[0]
        q05=ddd.quantile(0.95).iloc[0]
        count=ddd.count().iloc[0]
        
#        status=self.uredjaj.statusAgregator(ddd[u'status'])
        status=0
        for i in ddd[u'status']:
            """
            Definitivni problem s flagom. Funkcija getSlajs 100% nece uzeti
            u obzir lose (<=0) flagove. Nastaju problemi s plotanjem.
            """
            try:
                status|=int(i)
            except ValueError:
                #ValueError iskace kada int() pokusa convertati np.nan
                #binary or radi samo na int tipu
                status|=int(0)

        data = {'avg':avg,'std':std,'min':min,'max':max,'med':med,'q95':q95,
                'q05':q05,'count':count,'status':status}
        return kraj, data
    
    def getSlajs(self, kraj):
        pocetak= kraj-timedelta(minutes=59)
# koristimo iskljucivo flagove, a ne statuse. Flagove odredjuje AutoValidacija
        #return self.__df[pocetak:kraj][self.__df['flag']>0]
        return self.__df[pocetak:kraj]
    
    def agregirajNiz(self):
        niz = []
        for sat in self.sviSati:
        	vrijeme, vrijednost = self.agreg(sat)
        	niz.append(vrijednost)
        return pd.DataFrame(niz, self.sviSati)
        
    def nizNiz(self):
        niz = []
        for sat in self.sviSati:
            fr = self.getSlajs(sat).iloc[:,0]
            niz.append(fr)
        return niz
    

if __name__ == "__main__":
    data = WlReader().citaj('pj.csv')
    u1 = uredjaj.M100E()
    u2 = uredjaj.M100C()
    u1.pocetak=datetime(2000,1,1)
    u2.pocetak=datetime(2014,2,24,0,10)
    u1.kraj=datetime(2014,2,24,0,10)
    u2.kraj=datetime(2015,1,1)
    a = auto_validacija.AutoValidacija()
    a.dodaj_uredjaj(u2)
    a.dodaj_uredjaj(u1)
    a.validiraj(data['SO2'])
    
    ag = Agregator([u1,u2])
    ag.setDataFrame(data['SO2'])
    agregirani = ag.agregirajNiz()
    nizNizova = ag.nizNiz()

    plt.boxplot(nizNizova)
    plt.plot(agregirani['avg'])
    plt.plot(agregirani['q05'])
    plt.plot(agregirani['q95'])
    plt.show()
    
    for i in nizNizova:
        print('broj podataka ',len(i))
        
        
        