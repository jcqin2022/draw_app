
from PySide6.QtCore import Qt, QPointF, Signal, QObject

class GraphicsSignals(QObject):
    add_shape = Signal(dict)