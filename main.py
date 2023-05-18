from window import * 

app = QApplication([])

window = AppWindow()

class TestNode(Node):
	def __init__(self, scene):
		super().__init__(scene, "Add")

		Socket(self, "Value 1", "#4080d0")
		Socket(self, "Value 2", "#4080d0")

		Socket(self, "Output", "#4080d0", type=OUTPUT)


n2 = TestNode(window.scene)
n1 = TestNode(window.scene)

n1.title += " (N1)"
n2.title += " (N2)"

n1.sockets[-1].connect(n2.sockets[1])

print(f"connected n1.{n1.sockets[-1].name} to n2.{n2.sockets[0].name}")

app.exec_()