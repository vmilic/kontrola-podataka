'''
Created on Apr 21, 2014

@author: kraljevic
'''

class Dokument(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.agregirani={}
        self.nizNizova = {}
        
    def setPodaci(self, frejmovi):
        self.agregirani = {}
        self.nizNizova = {}
        # autovalidacija i agregiranje
        for i in list(frejmovi):
            # agregator mora biti unutar petlje ili ga treba inicijalizirati za 
            # svaku komponentu unutar petlje jer nacelno nije isti validator za 
            # svaku komponentu.
            # Ako je unutar petlje onda ne treba biti member varijable, a ako postoji
            # dobar razlog da bude member (a postoji zbog ragregacije) onda mora biti 
            # mapa (komponenta, agregator)
            ag = agregator.Agregator(listaUredjaja)  # izbaciti izvan petlje?
            autoValidator.validiraj(self.data[i])                
            ag.setDataFrame(self.data[i])
            self.agregirani[i] = ag.agregirajNiz()
            self.nizNizova[i] = ag.nizNiz()
            
            