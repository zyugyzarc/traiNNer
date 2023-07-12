from window import *

from torch import Tensor
import numpy as np

import torch
from torch import nn

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class TensorNode(Node):

    def __init__(self, scene, id=""):

        self.size = (150, 100)

        super().__init__(scene, "Tensor")

        Socket(self, "Output", "#fff", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self):

        return eval("torch.Tensor(("+self.textedit.toPlainText()+"))")

class TimePlotNode(Node):

    def __init__(self, scene, id=''):

        self.size = (250, 200)

        super().__init__(scene, "Time Plot")

        Socket(self, "Value", "#0080f0", type=INPUT)
        Socket(self, "Value", "#0080f0", type=OUTPUT)

        self.figure = plt.figure()
        self.canvas = self.addWidget(FigureCanvas(self.figure))

        self.series = []

        self.canvas.draw()

    def __eval__(self, x):

        self.series.append(x)

        self.figure.clear()
        p = self.figure.add_subplot()

        p.plot(self.series)

        self.canvas.draw()

        return x

View.availableNodes[__name__.replace("Nodes", "")] = [j for i, j in globals().items() if i.endswith("Node") and i != 'Node']