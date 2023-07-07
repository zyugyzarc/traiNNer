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


View.add_nodes(*[j for i, j in globals().items() if i.endswith("Node") and i != 'Node'])