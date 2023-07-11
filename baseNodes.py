from window import *

class ValueNode(Node):

    def __init__(self, scene, id=""):

        self.size = (150, 100)

        super().__init__(scene, "Value")

        Socket(self, "Output", "#fff", type=OUTPUT)

        self.textedit = self.addWidget(QLineEdit("HUNGUS"))

    def __eval__(self):

        return eval(self.textedit.text())

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

class PythonNode(Node):

    def __init__(self, scene, id=""):

        self.size = (200, 250)

        super().__init__(scene, "Python")

        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Output","#40d080", type=OUTPUT)

        self.textedit = QTextEdit("HUNGUS")
        self.textedit.resize(150, 150)
        self.addWidget(self.textedit, lambda w:w.setFixedHeight(150))
        

    def __eval__(self, val):

        op = self.textedit.toPlainText()
        vars = dict(input=val, output=None)
        exec(op, None, vars)
        return vars['output']

View.availableNodes[__name__.replace("Nodes", "")] = [j for i, j in globals().items() if i.endswith("Node") and i != 'Node']