from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sip
import traceback

EDGERADIUS = 8
SOCKETRADIUS = 6
INPUT = 0
OUTPUT = 1

def uuid():
    from uuid import uuid4
    return str(uuid4())

class Edge(QGraphicsItem):

    def __init__(self, fromsock, tosock, point=None):
        
        super().__init__(fromsock)

        self.id = "edge-"+uuid()

        self.setFlag(QGraphicsItem.ItemStacksBehindParent)
        if tosock: tosock.node.setZValue(fromsock.node.zValue()+1)
        
        self.selected = False

        self.fr = fromsock
        self.to = tosock
        self.point = point

        self.delta = (self.to.absPos() if self.to else self.point) - (self.fr.absPos() if self.fr else self.point)

        self.value = None

        (self.fr if self.fr else self.to).node.scene.edges.append(self)

    def paint(self, painter, QStyleGraphicsItem, widget=None):

        self.setZValue(-10)

        offset = QPointF(EDGERADIUS+SOCKETRADIUS, 4*EDGERADIUS) - QPointF(*(self.fr.node.size if self.fr else self.to.node.size))
        poff = -QPointF(EDGERADIUS, EDGERADIUS)
        sock_off = 4*self.fr.index*SOCKETRADIUS
        #print((self.fr if self.fr else self.to).node.scene.window.view.zoom)

        self.delta = (self.to.absPos() if self.to else self.point+poff) - (self.fr.absPos() if self.fr else self.point+poff)
        #self.delta = (self.to.absPos() if self.to else self.point) - (self.fr.absPos() if self.fr else self.point)

        self.setPos(self.fr.pos() + offset)

        p1 = QPointF(0, sock_off)
        p2 = self.delta

        grad = QLinearGradient(p1, p2)
        grad.setColorAt(0, self.fr.color.color() if self.fr else QColor('#ffffff'))
        grad.setColorAt(1, self.to.color.color() if self.to else QColor('#ffffff'))

        pen = QPen(QBrush(grad), 2)

        path = QPainterPath(p1)

        cutoff = 7

        if p1.x() - p2.x() < -EDGERADIUS*cutoff:

            path.cubicTo( (1*p1.x()+p2.x())/2, p1.y(), (p1.x()+p2.x()*1)/2, p2.y(), p2.x(), p2.y())
        else:
            path.cubicTo( 2*p1.x() - (1*p1.x()+p2.x())/2 + EDGERADIUS*cutoff, p1.y(), p2.x() + (p1.x()+p2.x()*1)/2 - EDGERADIUS*cutoff, p2.y(), p2.x(), p2.y())


        outlinePen = QPen(QColor("#000"), 5)

        painter.setBrush(Qt.NoBrush)
        
        painter.setPen(outlinePen)
        painter.drawPath(path)

        painter.setPen(pen)
        painter.drawPath(path)

    def updateNodes(self):
        self.fr.node.update(self.fr)
        self.to.node.update(self.to)

    def boundingRect(self):

        return QRectF(
            QPointF(0, 0),
            self.delta
        )

    def save(self, d):

        d[self.id] = dict(
            to = self.to.node.id,
            fr = self.fr.node.id,
            to_index = self.to.node.sockets.index(self.to),
            fr_index = self.fr.node.sockets.index(self.fr)
        )
        return d


class Socket(QGraphicsItem):

    def __init__(self, node, name="undefined", color='#ff0000', type=INPUT):

        super().__init__(node)

        self.edges = []

        self.node = node

        self.color = QBrush(QColor(color))
        self.outline = QPen(QColor('#101010'))
        self.outline_sel = QPen(QColor('#FFB040'))
        self.outline.setWidthF(2)
        self.outline_sel.setWidthF(2)
        self.selected = False

        self.type = type
        self.name = name
        self.index = len([i for i in self.node.sockets if self.type == i.type])

        self.text_item = QGraphicsTextItem(self.name, self)
        self.text_item.setFont(QFont("DejaVu Sans", 12))
        self.text_item.setDefaultTextColor(Qt.white)
        width = min(QFontMetrics(QFont("DejaVu Sans", 12)).width(self.name), self.node.size[0] - EDGERADIUS*3)
        self.text_item.setTextWidth(width + 2*SOCKETRADIUS)
        self.text_item.setPos(EDGERADIUS*2 if self.type == INPUT else (-EDGERADIUS*1 - width), -EDGERADIUS)
        self.node.scene.addItem(self.text_item)

        self.node.sockets.append(self)
        self.set_position()

    def set_position(self):

        ypos = EDGERADIUS*3+4*self.index*SOCKETRADIUS

        if self.type==INPUT:
            self.setPos(-SOCKETRADIUS, EDGERADIUS*2 + ypos)

        else:
            self.setPos(self.node.size[0] - SOCKETRADIUS, self.node.size[1] - ypos)

    def boundingRect(self):
        return QRectF(0, 0, self.node.size[0]+SOCKETRADIUS, EDGERADIUS).normalized()

    def paint(self, painter, QStyleGraphicsItem, widget=None):

        painter.setPen(self.outline_sel if self.selected else self.outline)
        painter.setBrush(self.color)

        painter.drawEllipse(0, 0, SOCKETRADIUS*2, SOCKETRADIUS*2)

    def connect(self, other, edge=None):

        if not edge: edge = Edge(self, other)
        self.edges.append(edge)
        
        if other:
            other.edges.append(edge)
        else:
            sock = (edge.fr if edge.fr != self else edge.to)
            sock.edges.append(edge)

            edge.updateNodes()

        print(f"connected {self} to {other}")
    
    def absPos(self):
        return self.pos() + self.node.pos()
    
    def __repr__(self):
        return f"<Socket {self.name} at {self.node}>"



class Node(QGraphicsItem):

    def __init__(self, scene, title="Undefined"):

        super().__init__()

        self.id = str(type(self))[8:-2].split('.')[-1]+"-"+uuid()

        self.scene = scene
        
        self.sockets = []
        self.widgets = []

        if not hasattr(self, 'size'): self.size = (150, 200)

        self._title = title

        self.title_item = QGraphicsTextItem(self)
        self.title_item.setFont(QFont("DejaVu Sans", 12))
        self.title_item.setDefaultTextColor(Qt.white)
        self.title_item.setPos(EDGERADIUS//2, 0)
        self.title_item.setTextWidth(self.size[0] - EDGERADIUS*3)
        
        self.title = title
        self.scene.addNode(self)

        self._outline_pen = QPen(QColor(0x10, 0x10, 0x10, 0xff))
        self._outline_selected_pen = QPen(QColor(0xff, 0xb0, 0x40, 0xff))

        self._outline_pen.setWidthF(1.5)
        self._outline_selected_pen.setWidthF(2)

        self._heading_brush = QBrush(QColor(0x40, 0x40, 0x40, 0xd0))
        self._bg_brush = QBrush(QColor(0x20, 0x20, 0x20, 0xb0))

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def eval(self):
        
        print("eval", self._title)

        check = []
        inputs = []
        for sock in self.sockets:
            if sock.type == INPUT:
                try:
                    edge = sock.edges[0]

                    if edge.fr.node not in check:
                        edge.fr.node.eval()
                        check.append(edge.fr.node)
                    
                    inputs.append(edge.value)
                except IndexError:
                    inputs.append(None)

        try:
            outputs = self.__eval__(*inputs)
            self.title_item.setDefaultTextColor(QColor("#fff"))
            self.title = self.title.replace(' (!)', '')
            self.title_item.setToolTip("")

        except KeyboardInterrupt:
            print(self,": stop eval")

        except Exception as E:
            
            outputs = (E,)*10
            self.title_item.setDefaultTextColor(QColor("#ff4040"))
            self.title = self.title.replace(' (!)', '')
            self.title += ' (!)'

            print('=======')
            print(f'During Eval of {self}')
            print(traceback.format_exc())
            print('=======')
            self.title_item.setToolTip(repr(E).split('(')[0] + ': ' + str(E))

        n = 0
        
        if type(outputs) != tuple: outputs = (outputs,)

        for sock in self.sockets:
            if sock.type == OUTPUT:
                for edge in sock.edges:
                    edge.value = outputs[n]
                n+=1


    def paint(self, painter, QStyleGraphicsItem, widget=None):

        fill = QPainterPath()
        fill.setFillRule(Qt.WindingFill)
        fill.addRoundedRect(0, 0, self.size[0], EDGERADIUS*3, EDGERADIUS, EDGERADIUS)
        fill.addRect(0, EDGERADIUS, self.size[0], EDGERADIUS*2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._heading_brush)
        painter.drawPath(fill.simplified())

        fill = QPainterPath()
        fill.setFillRule(Qt.WindingFill)
        fill.addRoundedRect(0, self.size[1] - EDGERADIUS*2, self.size[0], EDGERADIUS*2, EDGERADIUS, EDGERADIUS)
        fill.addRect(0, EDGERADIUS*3, self.size[0], self.size[1] - EDGERADIUS*4)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._bg_brush)
        painter.drawPath(fill.simplified())

        outline = QPainterPath()
        outline.addRoundedRect(0, 0, *self.size, EDGERADIUS, EDGERADIUS)
        painter.setPen(self._outline_selected_pen if self.isSelected() else self._outline_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(outline.simplified())

    def boundingRect(self):
        return QRectF(0, 0, self.size[0] + EDGERADIUS * 2, self.size[1] + EDGERADIUS * 2).normalized()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title=value; self.title_item.setPlainText(self._title)

    def __repr__(self):
        return f"<Node {self._title}>"

    def __eval__(self, *_):

        print("INVALID __EVAL__()")
        return tuple()

    def addWidget(self, widget, height=30):

        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(widget)

        self.widgets.append(proxy)

        widget.setFixedHeight(height)
        widget.setFixedWidth(self.size[0] - EDGERADIUS*3)

        ypos = EDGERADIUS*3+4*(len([0 for i in self.sockets if i.type == INPUT]) + len(self.widgets) - 1)*SOCKETRADIUS
        
        proxy.setPos(EDGERADIUS, EDGERADIUS*2 + ypos)

        return widget

    def update(self, sock):
        pass

    def save(self, d):

        d[self.id] = dict(
            pos=[self.pos().x(), self.pos().y()],
            title=self.title,
            sockets=[
                dict(type=i.type, name=i.name, color=(
                        i.color.color().red(),
                        i.color.color().green(),
                        i.color.color().blue(),
                    )
                )
                for i in self.sockets
            ],
            widgets=[
                (i.widget().toPlainText() if type(i.widget()) in (QTextEdit,) else None) for i in self.widgets 
            ]
        )

        return d


class View(QGraphicsView):

    availableNodes = []

    def add_nodes(*nodes):
        View.availableNodes += list(nodes)

    def __init__(self, graphics, parent=None):

        super().__init__(parent)
        
        self.graphics = graphics
        self.setScene(graphics)
        self.zoom = 1

        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.currentEdge = None
        self.currentSocket = None

    def contextMenuEvent(self, event):

        addMenu = QMenu("Add Node")

        adds = {}

        for node in self.availableNodes:
            adds[
                addMenu.addAction(str(node).split('.')[-1].replace('Node\'>', ''))
            ] = node


        menu = QMenu()
        menu.addMenu(addMenu)

        item = self.itemAt(event.pos())
        delaction = None

        if isinstance(item, Node) or isinstance(item, Socket):
            delaction = menu.addAction("Delete")
        
        saveaction = menu.addAction("Save")
        loadaction = menu.addAction("Load")

        action = menu.exec(event.globalPos())
        
        if action in adds:

            print("added", adds[action])
            n = adds[action](self.graphics)
            
            n.setPos(
                self.mapToScene(event.globalPos())
            )

        elif action == delaction:

            if isinstance(item, Socket):
                item = item.node

            for sock in item.sockets:
                while sock.edges:
                    edge = sock.edges.pop()
                    self.graphics.edges.remove(edge)
                    
                    self.graphics.removeItem(edge)
                    del edge
            
                self.graphics.removeItem(sock)
                del sock
            
            self.graphics.nodes.remove(item)
            self.graphics.removeItem(item)
            del item

        elif action == saveaction:

            self.graphics.save()

        elif action == loadaction:

            self.graphics.load()


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            print("clicked on", item)

            if type(item) == Socket and item.type == OUTPUT:
                for i in self.graphics.selectedItems():
                    i.setSelected(False)
                item.node.setSelected(True)
                item.selected = True

                self.currentSocket = item
                self.currentEdge = Edge(item, None, self.mapToScene(event.pos()))
                self.currentEdge.selected = True

                return

            elif type(item) == Socket and item.type == INPUT:

                self.currentEdge = item.edges.pop()
                self.currentEdge.fr.edges.pop()

                self.currentEdge.selected = True
                self.currentEdge.to = None

                self.currentEdge.point = self.mapToScene(event.pos())

                print("unlink", self.currentEdge)

            else:

                for node in self.graphics.nodes:
                    for sock in node.sockets:    
                        sock.selected = False

        if event.button() == Qt.MiddleButton:
            
            #release mmb
            super().mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers()))

            self.setDragMode(QGraphicsView.ScrollHandDrag)
            
            #press lmb and mmb
            super().mousePressEvent(QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers()))            

            return 

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if self.currentEdge:

            item = self.itemAt(event.pos())

            if type(item) == Socket and item != self.currentSocket:
                self.currentEdge.to = item
                self.currentEdge.point = None

                for node in self.graphics.nodes:
                    for sock in node.sockets:
                        if sock != item or sock != self.currentSocket:
                            sock.selected = False

                item.selected = True

            else:
                self.currentEdge.to = None
                self.currentEdge.point = self.mapToScene(event.pos())

            self.viewport().repaint()
            #print(self.currentEdge.delta, self.currentEdge.to)


        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        if self.currentEdge:
            if self.currentEdge.to and self.currentEdge.fr:

                self.currentSocket.connect(None, self.currentEdge)

                for node in self.graphics.nodes:
                    for sock in node.sockets:    
                        sock.selected = False

                self.currentEdge.selected = False
            
            else:
                self.graphics.edges.remove(self.currentEdge)
                sip.delete(self.currentEdge)
                del self.currentEdge

            self.currentEdge = None

            print("mouse release")

        if event.button() == Qt.MiddleButton:

            # release lmb
            super().mousePressEvent(QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | -Qt.LeftButton, event.modifiers()))            

            self.setDragMode(QGraphicsView.NoDrag)

            return 

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):

        dzoom = 1 if event.angleDelta().y() > 0 else -1
        dzoom = 1 + dzoom * 0.25

        self.zoom += dzoom

        self.scale(dzoom, dzoom)


class Scene(QGraphicsScene):

    def __init__(self, window, parent=None):
    
        super().__init__(parent)

        self.window = window
        self.nodes = []
        self.edges = []

        self.filename = None

        self.init_graphics()

    def addNode(self, node):

        self.nodes.append(node)
        self.addItem(node)

    def init_graphics(self):

        self.gridSize = 20
        self.gridSquares = 5

        self._color_background = QColor("#303030")
        self._color_light = QColor("#282828")
        self._color_dark = QColor("#202020")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)
        self.scene_width, self.scene_height = 64000, 64000
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(rect.left())
        right = int(rect.right()+1)
        top = int(rect.top())
        bottom = int(rect.bottom()+1)

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % (self.gridSize*self.gridSquares) != 0): lines_light.append(QLine(x, top, x, bottom))
            else: lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if (y % (self.gridSize*self.gridSquares) != 0): lines_light.append(QLine(left, y, right, y))
            else: lines_dark.append(QLine(left, y, right, y))


        # draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)

    def save(self):

        data = {}

        for node in self.nodes:
            data = node.save(data)

        for edge in self.edges:
            data = edge.save(data)

        import json

        print(data)

        if self.filename is None:
            self.filename, _ = QFileDialog.getSaveFileName(None, 'Save File', "", "traiNNer Files (*.nod)")
            self.filename += ".nod" if not self.filename.endswith(".nod") else ""

        print(self.filename)

        with open(self.filename, 'w') as f:
            json.dump(data, f)

        self.window.setWindowTitle(f"{self.filename} - traiNNer")

    def load(self):

        import json

        #if self.filename is None:
        self.filename, _ = QFileDialog.getOpenFileName(None, 'Open File', "", "traiNNer Files (*.nod)")

        with open(self.filename) as f:
            data = json.load(f)

        for i in data:
            if not i.startswith("edge"): # Node

                print("creating", i)
                cls = [j for j in self.window.view.availableNodes if i.startswith(str(j)[8:-2].split('.')[-1])]
                print(cls)
                cls = cls[0]
                inst = cls(self)
                inst.id = i
                inst.setPos(*data[i]['pos'])
                
                for j, w in enumerate(inst.widgets):
                    if type(w.widget()) in (QTextEdit,):
                        w.widget().setPlainText(data[i]['widgets'][j])

            else: # Edge

                i = data[i]

                print([j.id for j in self.nodes])

                Edge(
                    [j for j in self.nodes if j.id == i['fr']][0].sockets[i['fr_index']],
                    [j for j in self.nodes if j.id == i['to']][0].sockets[i['to_index']]
                )

        self.window.setWindowTitle(f"{self.filename} - traiNNer")




class AppWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.scene = Scene(self)

        self.view = View(self.scene, self)

        self.layout.addWidget(self.view)

        self.setWindowTitle("Untitled - traiNNer")
        self.show()