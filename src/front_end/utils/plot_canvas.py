from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QSizePolicy
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from matplotlib import gridspec
from matplotlib.colors import ListedColormap
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=10, dpi=100, title=''):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.title = title

        self.axes_result = self.fig.add_subplot(1, 1, 1)
        self.axes_result.set_title(title)
        # self.axes_result.SubplotParams(bottom=2)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, value):
        self.axes_result.clear()
        self.axes_result.plot(value)
        self.axes_result.set_ylabel('Magnitude (V)')
        self.axes_result.set_xlabel('Time')
        self.draw()

    def plot_x_y(self, x, y):
        self.axes_result.clear()
        self.axes_result.plot(x, y)

        self.axes_result.set_xlim([30000, 50000])
        self.axes_result.set_ylabel('FFT')

        self.axes_result.set_xlabel('Frequency')
        self.draw()

    def plot_confusion_matrix(self, y_test, result, labels=['HUMAN', 'NON_HUMAN']
                              ):
        # self.axes_result.clear()
        self.axes_result.remove()
        self.axes_result = self.fig.add_subplot(1, 1, 1)
        cm = confusion_matrix(y_test, result)
        labels.sort()
        recall = np.diag(cm) / np.sum(cm, axis=1)
        recall = np.around(recall, decimals=2)
        precision = np.diag(cm) / np.sum(cm, axis=0)
        precision = np.around(precision, decimals=2)
        sum = np.sum(cm)
        score = accuracy_score(y_test, result)
        length = len(cm)
        actual_cm = [[]]*(length+1)
        for i in range(0, length):
            actual_cm[i] = np.append(cm[i], recall[i])
        actual_cm[length] = np.append(precision, score)

        cm = np.array(actual_cm)
        sns.heatmap(cm, annot=True, ax=self.axes_result, linewidths=.5,
                    fmt='g', cmap="Reds")  # annot=True to annotate cells

        # labels, title and ticks
        self.axes_result.set_xlabel('Predicted labels')
        self.axes_result.set_ylabel('True labels')
        self.axes_result.set_title(self.title)
        counter = 0
        for i in range(0, length):
            for j in range(0, length+1):
                print(cm[i, j])
                percentage = cm[i, j]/sum
                t = self.axes_result.texts[counter]
                if j == length:
                    t.set_text(str(cm[i, j]))
                else:
                    t.set_text(str(cm[i, j]) + '\n' +
                               str(round(percentage*100, 2)) + " %")
                counter = counter + 1
        self.axes_result.xaxis.set_ticklabels(labels)
        self.axes_result.yaxis.set_ticklabels(labels)
        self.draw()

    def plot_prediction(self, value):
        self.axes_result.clear()
        self.axes_result.plot(value)
        self.draw()
