# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 08:32:47 2014

@author: velimir

Izdvajanje grafova u pojedine klase. Dodana je mini aplikacija za testiranje kao klasa...
"""

#import statements
import sys
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector

from PyQt4 import QtGui
import pandas as pd
import numpy as np


###############################################################################
class MPLCanvas(FigureCanvas):
    """
    matplotlib canvas class, generalni
    """
    def __init__(self,parent=None,width=6,height=5,dpi=100):
        fig=Figure(figsize=(width,height),dpi=dpi)
        self.axes=fig.add_subplot(111)
        FigureCanvas.__init__(self,fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(
            self,
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def crtaj(self):
        #metoda za crtanje, specifična klasa za pojedini graf je overloada
        pass


###############################################################################    
class GrafSatniSrednjaci(MPLCanvas):
    """
    subklasa MPLCanvas, ona definira detalje crtanja isl.
    """
    def __init__(self,*args,**kwargs):
        MPLCanvas.__init__(self,*args,**kwargs)
        #inicijalizacija span selectora
        self.span=SpanSelector(self.axes,
                               self.nakon_odabira,
                               'horizontal',
                               useblit=True,
                               rectprops=dict(alpha=0.4,facecolor='tomato')
                               )
    
    def nakon_odabira(self,xmin,xmax):
        """
        samo kao koncept...trebalo bi srediti bolji dialog        
        """
        opis='Podaci od '+str(xmin)+' do '+str(xmax)
        tekst='Odaberi int vrijednost flaga:'
        flag,ok=QtGui.QInputDialog.getDouble(self,opis,tekst)
        #samo print output... ti podatci trebaju ići prema nekom backendu
        if ok:
            print('min: ',xmin)
            print('max: ',xmax)
            print('novi flag: ',flag)
        else:
            print('bez promjene')
        #selector radi problem...ne vraca datetime... izgleda kao unix timestamp
        #ali nije...
        
        
    def crtaj(self,data):
        """
        data je dictionary pandas datafrejmova koji izbacuje agregator
        """
        #clear canvas i postavi naslov
        self.axes.clear()
        self.axes.set_title('Graf agregiranih satnih podataka')
        
        #x-os grafa        
        vrijeme=data['avg'].index
                
        #naredbe za crtanje pojedinih elemenata
        #srednja vrijednost
        self.axes.plot(vrijeme,data['avg'].values,
                       marker='d',
                       color='blue',
                       lw=1.5,
                       alpha=0.6,
                       label='average')
        #minimalne vrijednosti
        self.axes.scatter(vrijeme,data['min'].values,
                          marker='+',
                          color='black',
                          lw=0.3,
                          label='min/max')
        #maksimalne vrijednosti
        self.axes.scatter(vrijeme,data['max'].values,
                          marker='+',
                          color='black',
                          lw=0.3)
        #medijan
        self.axes.plot(vrijeme,data['med'].values,
                       marker='x',
                       color='black',
                       lw=0.3,
                       label='median')
        #prostor izmedju q05 i q95
        self.axes.fill_between(vrijeme,data['q05'].values,data['q95'].values,
                               facecolor='green',
                               alpha=0.4)
        #rotacija x tickova za 30 stupnjeva i smnjivanje fonta zbog preglednosti
        xLabels=self.axes.get_xticklabels()
        for label in xLabels:
            label.set_rotation(30)
            label.set_fontsize(6)
        
        
        """
        #legenda--- pitanje je da li je bitna..
        legend=self.axes.legend(loc='best',fancybox=True)
        legend.get_frame().set_alpha(0.2)
        
        for label in legend.get_texts():
            label.set_fontsize(6)

        for label in legend.get_lines():
            label.set_linewidth(0.5)
        """
        #naredba za crtanje na ekran
        self.draw()

###############################################################################        
        
class ApplicationMain(QtGui.QMainWindow):
    """
    Testna aplikacija za provjeru ispravnosti MPL klasa za Qt
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Testna aplikacija")
        self.mainWidget=QtGui.QWidget(self)
        #kreiranje canvasa satnih srednjaka
        canvasSatni=GrafSatniSrednjaci(self.mainWidget,width=6,height=5,dpi=150)
        #basic layout
        mainLayout=QtGui.QVBoxLayout(self.mainWidget)
        mainLayout.addWidget(canvasSatni)
        self.setCentralWidget(self.mainWidget)
        
        """
        Testni podaci, dictionary pandas datafrejmova koji je rezultat agregatora.
        Koristim istu strukturu podataka ali random vrijednosti
        """
        vrijeme=pd.date_range('2014-03-15 12:00:00',periods=36,freq='H')
        avg=10+np.random.rand(len(vrijeme))
        min=6+np.random.rand(len(vrijeme))
        max=14+np.random.rand(len(vrijeme))
        median=10+np.random.rand(len(vrijeme))
        q05=12+np.random.rand(len(vrijeme))
        q95=8+np.random.rand(len(vrijeme))
        
        ts1=pd.Series(avg,vrijeme)
        ts2=pd.Series(min,vrijeme)
        ts3=pd.Series(max,vrijeme)
        ts4=pd.Series(median,vrijeme)
        ts5=pd.Series(q05,vrijeme)
        ts6=pd.Series(q95,vrijeme)
        
        data={'avg':ts1,'min':ts2,'max':ts3,'med':ts4,'q05':ts5,'q95':ts6}
                
        #naredba za plot
        canvasSatni.crtaj(data)
        
if __name__=='__main__':
    aplikacija=QtGui.QApplication(sys.argv)
    app=ApplicationMain()
    app.show()
    sys.exit(aplikacija.exec_())
