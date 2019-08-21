from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
import numpy as np

class Sparkline(QWidget):
    def __init__(self, series):
        super().__init__()
        self.series = np.array(series)

    def paintEvent(self, event):
        if len(self.series) < 2:
            return

        painter = QPainter(self)
        x = self.width()/len(self.series) * np.linspace(0, len(self.series), len(self.series))
        y = self.height()/2* (1 - (self.series-self.series.min())/(self.series.max()-self.series.min()) )

        painter.drawPoint(x[0], y[0])   # draw first point
        for i in range(1, len(x)):
            painter.drawLine(x[i-1], y[i-1], x[i], y[i])
        painter.end()

    def append(self, data):
        ''' Add new data to plot '''
        self.series = np.append(self.series, data)
        self.repaint()
