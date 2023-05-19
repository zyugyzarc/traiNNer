from window import * 

app = QApplication([])

window = AppWindow()

class ValueNode(Node):

    def __init__(self, scene, id=""):

        super().__init__(scene, "Value")

        Socket(self, "Output", "#4080d0", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self):

        return self.textedit.toPlainText()

class ViewerNode(Node):

    def __init__(self, scene, id=""):

        super().__init__(scene, "Viewer")

        Socket(self, "Value", "#4080d0", type=INPUT)

        self.button = self.addWidget(QPushButton("HUNGUS"))
        self.button.clicked.connect(self.eval)

    def __eval__(self, value):

        self.button.setText(value)


class MathNode(Node):

    def __init__(self, scene, id=""):

        super().__init__(scene, "Math")

        Socket(self, "Value", "#4080d0", type=INPUT)
        Socket(self, "Value", "#4080d0", type=INPUT)
        Socket(self, "Output", "#4080d0", type=OUTPUT)

        self.textedit = self.addWidget(QTextEdit("HUNGUS"))

    def __eval__(self, val1, val2):
        op = self.textedit.toPlainText()
        return str(eval(val1+op+val2))

val2 = ValueNode(window.scene)
val1 = ValueNode(window.scene)
viw = ViewerNode(window.scene)
math = MathNode(window.scene)
#n2 = TestNode(window.scene, '(N2)')
#n1 = TestNode(window.scene, '(N1)')

#n1.sockets[-1].connect(n2.sockets[1])

app.exec_()