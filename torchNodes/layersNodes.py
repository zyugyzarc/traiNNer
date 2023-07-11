import torch
import torch.nn as nn
from window import *

import inspect

layers = [nn.Linear, nn.Conv1d, nn.Conv2d, nn.Conv3d]

class LayerNode(Node):

    def __init__(self, scene):

        super().__init__(scene, title(self._layer.__name__))

        Socket(self, "Optim", "#d0f080", type=INPUT)
        Socket(self, "Input", "#40d080", type=INPUT)
        Socket(self, "Output", "#40d080", type=OUTPUT)

        self.args = self.add_args()
        #self.inputsize = self.addWidget(QLineEdit("4"))
        #self.outputsize = self.addWidget(QLineEdit("5"))

    def update(self, sock):
        
        if hasattr(self, 'layer'): del self.layer

        #print(self.args[0].text)

        self.layer = self._layer(
            *[eval(i.text()) for i in self.args]
        )

    def __eval__(self, weights, val):

        return self.layer(val)



View.availableNodes[__name__.replace("Nodes", "").replace('_', '.')] = [
	type(
		title(i.__name__)+"Node",
		(LayerNode,),
		dict(
			_layer = i,
			add_args = lambda self:(
				[
					self.addWidget(QLineEdit(""), lambda w:w.setPlaceholderText(param))
					for param, j in inspect.signature(i.__init__).parameters.items()
					if j.default == inspect.Parameter.empty and param != "self"
				]
			)
		))
	for i in layers
]