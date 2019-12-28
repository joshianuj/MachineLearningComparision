from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QSizePolicy
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from matplotlib import gridspec
from matplotlib.colors import ListedColormap


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=10, dpi=100, title=''):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes_result = fig.add_subplot(1, 1, 1)
        self.axes_result.set_title(title)
        # self.axes_result.SubplotParams(bottom=2)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, value):
        self.axes_result.clear()
        self.axes_result.plot(value)
        self.draw()

    def plot_x_y(self, x, y):
        self.axes_result.clear()
        self.axes_result.plot(x, y)
        self.axes_result.set_xlim([30000, 50000])
        self.draw()
