from window import *

class ValueNode(Node):

    def __init__(self, scene, id=""):

        self.size = (150, 100)

        super().__init__(scene, "Value")

        Socket(self, "Output", "#fff", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self):

        return self.textedit.toPlainText()

class ViewerNode(Node):

    def __init__(self, scene, id=""):

        self.size = (150, 100)

        super().__init__(scene, "Viewer")

        Socket(self, "Value", "#fff", type=INPUT)

        self.button = self.addWidget(QPushButton("HUNGUS"))
        self.button.clicked.connect(self.eval)

    def __eval__(self, value):

        self.button.setText(value)


class MathNode(Node):

    def __init__(self, scene, id=""):

        super().__init__(scene, "Math")

        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Output","#40d080", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self, val1, val2):
        op = self.textedit.toPlainText()
        return str(eval(val1+op+val2))

View.availableNodes = [j for i, j in globals().items() if i.endswith("Node") and i != 'Node']
print(View.availableNodes)