from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

EDGERADIUS = 8
SOCKETRADIUS = 6
INPUT = 0
OUTPUT = 1

class Edge(QGraphicsItem):

    def __init__(self, fromsock, tosock, point=None):
        
        super().__init__(fromsock)

        self.setFlag(QGraphicsItem.ItemStacksBehindParent)
        if tosock: tosock.node.setZValue(fromsock.node.zValue()+1)
        

        self.fr = fromsock
        self.to = tosock
        self.point = point

        self.delta = (self.to.absPos() if self.to else self.point) - (self.fr.absPos() if self.fr else self.point)

    def paint(self, painter, QStyleGraphicsItem, widget=None):

        self.setZValue(-10)

        offset = QPointF(EDGERADIUS+SOCKETRADIUS, 4*EDGERADIUS) - QPointF(*(self.fr.node.size if self.fr else self.to))

        self.setPos(self.fr.pos() + offset)

        self.delta = (self.to.absPos() if self.to else self.point) - (self.fr.absPos() if self.fr else self.point)

        p1 = QPointF(0, 0)
        p2 = self.delta

        #grad = QLinearGradient(p1, p2)
        #grad.setColorAt(0, Qt.red)
        #grad.setColorAt(1, Qt.blue)
        #pen = QPen(QBrush(grad), 1.5)

        pen = QPen(Qt.white, 1.5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        path = QPainterPath(p1)
        path.cubicTo( (1*p1.x()+p2.x())/2, p1.y(), (p1.x()+p2.x()*1)/2, p2.y(), p2.x(), p2.y())

        painter.drawPath(path)

    def boundingRect(self):

        return QRectF(
            QPointF(0, 0),
            self.delta
        )

class Socket(QGraphicsItem):

    def __init__(self, node, name="undefined", color='#ff0000', type=INPUT):

        super().__init__(node)

        self.edges = []

        self.node = node

        self.color = QBrush(QColor(color))
        self.outline = QPen(QColor('#101010'))
        self.outline.setWidthF(2)

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

        painter.setPen(self.outline)
        painter.setBrush(self.color)

        painter.drawEllipse(0, 0, SOCKETRADIUS*2, SOCKETRADIUS*2)

    def connect(self, other, edge=None):

        if not edge: edge = Edge(self, other)
        self.edges.append(edge)
        other.edges.append(edge)

        print(f"connected {self} to {other}")
    
    def absPos(self):
        return self.pos() + self.node.pos()
    
    def __repr__(self):
        return f"<Socket {self.name} at {self.node}>"



class Node(QGraphicsItem):

    def __init__(self, scene, title="Undefined"):

        super().__init__()

        self.scene = scene
        
        self.sockets = []
        self.widgets = []

        self.size = (150, 200)

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



class View(QGraphicsView):

    def __init__(self, graphics, parent=None):

        super().__init__(parent)
        
        self.graphics = graphics
        self.setScene(graphics)

        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            print("clicked on", item)

            if type(item) == Socket:
                for i in self.graphics.selectedItems():
                    i.setSelected(False)
                item.node.setSelected(True)
                return

        if event.button() == Qt.MiddleButton:
            
            #release mmb
            super().mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers()))

            self.setDragMode(QGraphicsView.ScrollHandDrag)
            
            #press lmb and mmb
            super().mousePressEvent(QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers()))            

            return 

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MiddleButton:

            # release lmb
            super().mousePressEvent(QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | -Qt.LeftButton, event.modifiers()))            

            self.setDragMode(QGraphicsView.NoDrag)

            return 

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):

        dzoom = 1 if event.angleDelta().y() > 0 else -1
        dzoom = 1 + dzoom * 0.25

        self.scale(dzoom, dzoom)



class Scene(QGraphicsScene):

    def __init__(self, parent=None):
    
        super().__init__(parent)

        self.nodes = []
        self.edges = []

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



class AppWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.scene = Scene()

        self.view = View(self.scene, self)

        self.layout.addWidget(self.view)

        self.setWindowTitle("traiNNer")
        self.show()

    

