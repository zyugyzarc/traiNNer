from window import * 
from nodes import *

app = QApplication([])

window = AppWindow()

val2 = ValueNode(window.scene)
val1 = ValueNode(window.scene)
viw = ViewerNode(window.scene)
math = MathNode(window.scene)
#n2 = TestNode(window.scene, '(N2)')
#n1 = TestNode(window.scene, '(N1)')

#n1.sockets[-1].connect(n2.sockets[1])

app.exec_()