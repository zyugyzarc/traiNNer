from window import *

from torch import Tensor
import numpy as np

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

    def update(self, to):
        try:
            self.button.setText(repr(
                self.sockets[0].edges[0].value
            ))
            print(repr(
                self.sockets[0].edges[0].value
            ))
        except:
            self.button.setText("None")

    def __eval__(self, value):
        self.update(None)


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
from torch.optim import Adam

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

class AdamNode(Node):

    def __init__(self, scene):

        self.size = (150, 150)

        super().__init__(scene, "Adam")

        Socket(self, "Weights", "#d0f080", type=OUTPUT)
        self.loss_sock = Socket(self, "Backward Loss", "#40d080", type=INPUT)

        self.button = self.addWidget(QPushButton("TRAIN EPOCH"))
        self.button.clicked.connect(self.train)

        self.adam = None
        self.update(None)

    def update(self, to):
        
        print('update adam')

        if hasattr(self, 'adam'):
            del self.adam

        for i in self.sockets[0].edges:
            i = i.to.node
            if hasattr(i, 'layer'):
                if hasattr(self, 'adam'):
                    self.adam.add_param_group(i.layer.parameters())
                else:
                    self.adam = Adam(i.layer.parameters())

    def train(self):

        try:
            
            self.loss_sock.edges[0].fr.node.eval()
            loss = self.loss_sock.edges[0].value

            print(f"Loss: {loss}")

            loss.backward()
            self.adam.step()
        
        except Exception as E:

            self.title_item.setDefaultTextColor(QColor("#ff4040"))
            self.title = self.title.replace(' (!)', '')
            self.title += ' (!)'

            print('=======')
            print(f'During Eval of {self}')
            print(traceback.format_exc())
            print('=======')
            self.title_item.setToolTip(repr(E).split('(')[0] + ': ' + str(E))

    def eval(self):
        pass

class ReLUNode(Node):
    def __init__(self, scene, id=""):

        self.size = (100, 90)

        super().__init__(scene, "ReLU")

        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Value", "#40d080", type=OUTPUT)

    def __eval__(self, val):
        return (val + abs(val))/2

class PythonNode(Node):

    def __init__(self, scene, id=""):

        self.size = (200, 250)

        super().__init__(scene, "Python")

        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Output","#40d080", type=OUTPUT)

        self.textedit = QTextEdit("HUNGUS")
        self.textedit.resize(150, 150)
        self.addWidget(self.textedit, height=150)
        

    def __eval__(self, val):

        op = self.textedit.toPlainText()
        vars = dict(input=val, output=None)
        exec(op, None, vars)
        return vars['output']


View.availableNodes = [j for i, j in globals().items() if i.endswith("Node") and i != 'Node']
print(View.availableNodes)