import torch
import torch.optim as O
from window import *

optims = [O.SGD, O.Adam, O.Adagrad, O.Adadelta, O.RMSprop, O.ASGD, O.Rprop]

class OptimNode(Node):

    def __init__(self, scene):

        self.size = (150, 150)

        super().__init__(scene, title(self._optim.__name__))

        Socket(self, "Weights", "#d0f080", type=OUTPUT)
        self.loss_sock = Socket(self, "Backward Loss", "#40d080", type=INPUT)

        self.button = self.addWidget(QPushButton("TRAIN EPOCH"))
        self.button.clicked.connect(self.train)

        self.optim = None
        self.update(None)

    def update(self, to):
        
        print('update optim')

        if hasattr(self, 'optim'):
            del self.optim

        for i in self.sockets[0].edges:
            i = i.to.node
            if hasattr(i, 'layer'):
                if hasattr(self, 'optim'):
                    self.optim.add_param_group(i.layer.parameters())
                else:
                    self.optim = self._optim(i.layer.parameters())

    def train(self):

        try:
            
            self.loss_sock.edges[0].fr.node.eval()
            loss = self.loss_sock.edges[0].value

            print(f"Loss: {loss}")

            loss.backward()
            self.optim.step()
        
        except Exception as E:

            self.title_item.setDefaultTextColor(QColor("#ff4040"))
            self.title = self.title.replace(' (!)', '')
            self.title += ' (!)'

            print('=======')
            print(f'During Eval of {self}')
            print(traceback.format_exc())
            print('=======')
            self.title_item.setToolTip(repr(E).split('(')[0] + ': ' + str(E))

    def eval(self):
        pass

        
View.availableNodes[__name__.replace("Nodes", "").replace('_', '.')] = [
	type(title(i.__name__)+"Node", (OptimNode,), dict(_optim=i))
	for i in optims
]