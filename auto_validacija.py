# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 21:18:45 2014

@author: kraljevic
"""

class AutoValidacija(object):

    __uredjaji=[]
#    def __init__(self):
#        self.__uredjaji.append(uredjaj.M100E())
#        self.__uredjaji.append(uredjaj.M100C())

    def dodaj_uredjaj(self,u):
        self.__uredjaji.append(u)
        
    def validiraj(self,df):
        for u in self.__uredjaji:
            p=max([df.first_valid_index(),u.pocetak])
            k=min([df.last_valid_index(),u.kraj])
            df.loc[p:k,u'flag'] = u.validnost(df.loc[p:k,u'status'])
            #d.flag = u.validnost(d['status'])
        