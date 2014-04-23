from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import \
    FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import \
#    NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

class Grafovi(QtGui.QWidget):
    def __init__(self, label="Grafovi", parent=None):
        super(Grafovi,self).__init__(parent)
        
        
        self.satniSrednjaci = QtGui.QWidget()
        self.satniSrednjaci.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)                
        self.satniSrednjaci.setWindowTitle('Satno agregirani podaci')
        self.fig1 = Figure()
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas1.setParent(self.satniSrednjaci)
        self.axes1 = self.fig1.add_subplot(111)
        
        self.satniPodaci = QtGui.QWidget()
        self.satniPodaci.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)       
        self.satniPodaci.setWindowTitle('Podaci u odabranom intervalu')
        self.fig2 = Figure()
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas2.setParent(self.satniPodaci)
        self.axes2 = self.fig2.add_subplot(111)
 
        
        graphLayout = QtGui.QHBoxLayout()
        graphLayout.addWidget(self.satniSrednjaci)
        graphLayout.addWidget(self.satniPodaci)
        self.setLayout(graphLayout)
        
    def draw_request_satni(self):
        """
        boxplot satnih prosjeka
        """
                
        kanal = str(self.trenutniKanal)
        self.axes1.clear()
        
        temp = self.nizNizova[kanal]
        # test
        self.axes1.boxplot(temp)
        self.axes1.plot(self.agdata[kanal]['avg'], picker=5)
        self.axes1.plot(self.agdata[kanal]['q05'], picker=5)
        self.axes1.plot(self.agdata[kanal]['q95'], picker=5)
        self.axes1.set_title('Boxplot satnih podataka s q05.q95 i average')
        self.canvas1.draw()

        
    