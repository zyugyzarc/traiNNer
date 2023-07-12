from window import *

from torch import Tensor
import numpy as np

import torch
from torch import nn

class TensorNode(Node):

    def __init__(self, scene, id=""):

        self.size = (150, 100)

        super().__init__(scene, "Tensor")

        Socket(self, "Output", "#fff", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self):

        return eval("torch.Tensor(("+self.textedit.toPlainText()+"))")


View.availableNodes[__name__.replace("Nodes", "")] = [j for i, j in globals().items() if i.endswith("Node") and i != 'Node']