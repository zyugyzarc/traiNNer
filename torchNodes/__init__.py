from window import *

from torch import Tensor
import numpy as np

import torch
from torch import nn
from torch.optim import Adam

class TensorNode(Node):

    def __init__(self, scene, id=""):

        self.size = (150, 100)

        super().__init__(scene, "Tensor")

        Socket(self, "Output", "#fff", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self):

        return eval("torch.Tensor(("+self.textedit.toPlainText()+"))")

class MSELossNode(Node):

    def __init__(self, scene):

        self.size = (150, 100)

        super().__init__(scene, "MSELoss")

        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Target", "#40d080", type=INPUT)
        Socket(self, "Loss", "#40d080", type=OUTPUT)

    def __eval__(self, x, y):

        return ((x - y)*(x - y)).mean()

class LinearNode(Node):

    def __init__(self, scene):

        super().__init__(scene, "Linear")

        Socket(self, "Optim", "#d0f080", type=INPUT)
        Socket(self, "Input", "#40d080", type=INPUT)
        Socket(self, "Output", "#40d080", type=OUTPUT)

        self.inputsize = self.addWidget(QTextEdit("4"))
        self.outputsize = self.addWidget(QTextEdit("5"))

        self.layer = nn.Linear(4, 4)

    def update(self, sock):
        
        del self.layer
        self.layer = nn.Linear(
            int(self.inputsize.toPlainText()),
            int(self.outputsize.toPlainText())
        )

    def __eval__(self, weights, val):

        return self.layer(val)

View.availableNodes[__name__.replace("Nodes", "")] = [j for i, j in globals().items() if i.endswith("Node") and i != 'Node']