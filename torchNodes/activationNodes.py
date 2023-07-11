import torch
import torch.nn.functional as F
from window import *

functions = [F.relu, F.softmax, F.sigmoid, F.tanh, F.log_softmax]

class ActivationNode(Node):

    def __init__(self, scene):

        self.size = (150, 100)

        super().__init__(scene, self.__eval__.__name__.title())

        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Output", "#40d080", type=OUTPUT)

        
View.availableNodes[__name__.replace("Nodes", "").replace('_', '.')] = [
	type(i.__name__.title()+"Node", (ActivationNode,), dict(__eval__=staticmethod(i)))
	for i in functions
]