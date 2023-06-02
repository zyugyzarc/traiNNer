from window import *

class ValueNode(Node):

    def __init__(self, scene, id=""):

        self.size = (150, 100)

        super().__init__(scene, "Value")

        Socket(self, "Output", "#fff", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self):

        return eval(self.textedit.toPlainText())

class ViewerNode(Node):

    def __init__(self, scene, id=""):

        self.size = (150, 100)

        super().__init__(scene, "Viewer")

        Socket(self, "Value", "#fff", type=INPUT)

        self.button = self.addWidget(QPushButton("HUNGUS"))
        self.button.clicked.connect(self.eval)

    def __eval__(self, value):

        self.button.setText(repr(value))


class MathNode(Node):

    def __init__(self, scene, id=""):

        super().__init__(scene, "Math")

        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Output","#40d080", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self, val1, val2):

        op = self.textedit.toPlainText()
        return eval(str(val1)+op+str(val2))


import torch
from torch import nn


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

class AdamNode(Node):

    def __init__(self, scene):

        self.size = (150, 100)

        super().__init__(scene, "Adam")

        Socket(self, "Loss", "#40d080", type=INPUT)
        Socket(self, "Optim", "#d0f080", type=OUTPUT)

        #self.button = self.addWidget(QPushButton("OPTIM"))
        #self.button.clicked.connect(self.eval)

    def __eval__(self, loss):

        raise KeyboardInterrupt


View.availableNodes = [j for i, j in globals().items() if i.endswith("Node") and i != 'Node']
print(View.availableNodes)