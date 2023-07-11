import torch
import torch.nn.functional as F
from window import *

functions = [F.mse_loss, F.cross_entropy, F.binary_cross_entropy, F.l1_loss]

class ActivationNode(Node):

    def __init__(self, scene):

        self.size = (150, 100)

        super().__init__(scene, title(self.__eval__.__name__))

        Socket(self, "Value", "#40d080", type=INPUT)
        Socket(self, "Target", "#40d080", type=INPUT)
        Socket(self, "Output", "#40d080", type=OUTPUT)

        
View.availableNodes[__name__.replace("Nodes", "").replace('_', '.')] = [
	type(title(i.__name__)+"Node", (ActivationNode,), dict(__eval__=staticmethod(i)))
	for i in functions
]