from window import * 

app = QApplication([])

window = AppWindow()

class TestNode(Node):
	def __init__(self, scene, id=""):

		super().__init__(scene, "Add"+(" "+id if id else ""))

		Socket(self, "Value 1", "#4080d0")
		Socket(self, "Value 2", "#4080d0")

		Socket(self, "Output", "#4080d0", type=OUTPUT)


n2 = TestNode(window.scene, '(N2)')
n1 = TestNode(window.scene, '(N1)')

n1.sockets[-1].connect(n2.sockets[1])



app.exec_()