from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsPathItem, QVBoxLayout, QWidget
)
from PySide6.QtGui import QPainter, QColor, QPen, QAction, QPainterPath
from PySide6.QtCore import Qt, QPointF, Signal, QObject
from typing import List, Dict
from .menu import WBMenu
from .curve_shap import CurveShap
import json

class WhiteboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scense_reserved = 15
        self.window_height = 600
        self.window_width = 800
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.init_ui()
        self.history: List[Dict] = []
        self.view.setMouseTracking(True)
        self.view.mousePressEvent = self.mousePressEvent
        self.view.mouseMoveEvent = self.mouseMoveEvent
        self.view.mouseReleaseEvent = self.mouseReleaseEvent
        
        # 绘图工具状态
        self.current_tool = "line"
        self.start_point = QPointF()
        self.temp_item = None
        self.color = QColor("#000000")
        self.pen_width = 2  # 默认线宽
        self.dot_interval = 5  # Default dot interval for dotted lines

    def init_ui(self):
        self.setGeometry(100, 
                         100, 
                         self.window_width,
                         self.window_height
                         )
        self.setWindowTitle("Whiteboard")
        self.view.setRenderHint(QPainter.Antialiasing)
        # Add menu bar
        self.menu = WBMenu(self)

    def set_dot_interval(self, interval: float):
        """Set the interval for dotted lines"""
        self.dot_interval = interval

    def add_remote_shape(self, shape_data):
        """处理来自网络的绘图指令"""
        item = None
        color = QColor(shape_data.get('color', '#000000'))
        pen = QPen(color, self.pen_width)

        if shape_data['type'] == 'line':
            x1, y1 = shape_data['start']
            x2, y2 = shape_data['end']
            item = QGraphicsLineItem(x1, y1, x2, y2)
        elif shape_data['type'] == 'dotted_line':
            x1, y1 = shape_data['start']
            x2, y2 = shape_data['end']
            dot_interval = shape_data.get('dot_interval', 5)
            # Create dotted line style
            pen.setStyle(Qt.DotLine)
            pen.setDashPattern([1, dot_interval])  # [dot size, space]
            item = QGraphicsLineItem(x1, y1, x2, y2)
        elif shape_data['type'] == 'circle':
            x1, y1 = shape_data['start']
            x2, y2 = shape_data['end']
            # Handle both explicit radius (from API) and calculated radius (from GUI)
            if 'radius' in shape_data:
                # API call with explicit radius
                radius = shape_data['radius']
                item = QGraphicsEllipseItem(x1, y1, radius * 2, radius * 2)
            else:
                # GUI drawing with start/end points
                radius = ((x2 - x1)**2 + (y2 - y1)**2)**0.5  # Euclidean distance
                item = QGraphicsEllipseItem(x1, y1, radius * 2, radius * 2)
        elif shape_data['type'] == 'rect':
            x1, y1 = shape_data['start']
            x2, y2 = shape_data['end']
            item = QGraphicsRectItem(
                min(x1, x2), min(y1, y2),
                abs(x2 - x1), abs(y2 - y1)
            )
        elif shape_data['type'] == 'curve':
            # 处理曲线绘制逻辑
            # 这里可以使用贝塞尔曲线或其他算法来绘制曲线
            points = shape_data['points']
            if isinstance(points, str):
                shape_data["points"] = json.loads(points) 
            curve = CurveShap.model_validate(shape_data)
            if len(curve.points) > 1:
                path = QPainterPath()
                path.moveTo(curve.points[0].x, curve.points[0].y)
                for point in curve.points[1:]:
                    path.lineTo(point.x, point.y)
                item = self.scene.addPath(path, color)
        
        if item:
            item.setPen(pen)
            self.scene.addItem(item)
            self.history.append(shape_data)

    # 新增工具切换方法
    def set_drawing_tool(self, tool_name):
        """切换绘图工具"""
        self.current_tool = tool_name
        self.setCursor(Qt.CrossCursor)

    # 新增颜色设置方法
    def set_pen_color(self, color_hex):
        """设置画笔颜色 #RRGGBB"""
        self.color = QColor(color_hex)

    def resizeEvent(self, event):
        """Ensure the view resizes with the window."""
        win_rect = self.rect()
        x = win_rect.x()
        y = win_rect.y()
        width = win_rect.width()
        height = win_rect.height()
        self.view.setGeometry(x, y, width, height)  # Set the view's size to match the window's size
        self.scene.setSceneRect(x, 
                                y, 
                                width - self.scense_reserved, 
                                height - self.scense_reserved)
        super().resizeEvent(event)

    # 以下是PyQt的鼠标事件处理
    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.LeftButton:
                widget_pos = event.position().toPoint()
                self.start_point = self.view.mapToScene(widget_pos)
                if self.current_tool in ["line", "dotted_line"]:
                    self.temp_item = QGraphicsLineItem()
                    if self.current_tool == "dotted_line":
                        pen = self.temp_item.pen()
                        pen.setStyle(Qt.DotLine)
                        pen.setDashPattern([1, self.dot_interval])
                        self.temp_item.setPen(pen)
                    self.scene.addItem(self.temp_item)
                elif self.current_tool == "circle":
                    self.temp_item = QGraphicsEllipseItem()
                    self.scene.addItem(self.temp_item)
                elif self.current_tool == "rect":
                    self.temp_item = QGraphicsRectItem()
                    self.scene.addItem(self.temp_item)
                elif self.current_tool == "curve":
                    self.temp_item = QGraphicsPathItem()
                    self.scene.addItem(self.temp_item)
                    self.path = QPainterPath()
                    self.path.moveTo(self.start_point)
                    self.points = [self.start_point]
                # elif self.current_tool == "dotted_line":
                #     # For dotted lines, initialize a temporary line item
                #     self.temp_item = QGraphicsLineItem()
                #     self.scene.addItem(self.temp_item)

        except Exception as e:
            print(f"Error in mousePressEvent: {e}")

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() & Qt.LeftButton and self.temp_item:
                widget_pos = event.position().toPoint()
                end_point = self.view.mapToScene(widget_pos)
                if self.current_tool in ["line", "dotted_line"]:
                    if isinstance(self.temp_item, QGraphicsLineItem):
                        self.temp_item.setLine(
                            self.start_point.x(), self.start_point.y(),
                            end_point.x(), end_point.y()
                        )
                        if self.current_tool == "dotted_line":
                            pen = self.temp_item.pen()
                            pen.setStyle(Qt.DotLine)
                            pen.setDashPattern([1, self.dot_interval])
                            self.temp_item.setPen(pen)
                    else:
                        self.temp_item = QGraphicsLineItem()
                        self.scene.addItem(self.temp_item)
                elif self.current_tool == "circle":
                    # Use Euclidean distance for consistent circle drawing
                    dx = end_point.x() - self.start_point.x()
                    dy = end_point.y() - self.start_point.y()
                    radius = (dx**2 + dy**2)**0.5
                    self.temp_item.setRect(
                        self.start_point.x() - radius,
                        self.start_point.y() - radius,
                        radius * 2,
                        radius * 2
                    )
                elif self.current_tool == "rect":
                        self.temp_item.setRect(
                            min(self.start_point.x(), end_point.x()),
                            min(self.start_point.y(), end_point.y()),
                            abs(end_point.x() - self.start_point.x()),
                            abs(end_point.y() - self.start_point.y())
                        )
                elif self.current_tool == "curve":
                # Add the current point to the path
                    self.path.lineTo(end_point)
                    self.temp_item.setPath(self.path)
                    self.points.append(end_point) 
                # elif self.current_tool == "dotted_line":
                #     # Update the end point of the temporary line item
                #     if isinstance(self.temp_item, QGraphicsLineItem):
                #         self.temp_item.setLine(
                #             self.start_point.x(), self.start_point.y(),
                #             end_point.x(), end_point.y()
                #         )
                #     else:
                #         self.temp_item = QGraphicsLineItem()
                #         self.scene.addItem(self.temp_item)
        except Exception as e:
            print(f"Error in mouseMoveEvent: {e}")

    def mouseReleaseEvent(self, event):
        try:
            if event.button() == Qt.LeftButton and self.temp_item:
                widget_pos = event.position().toPoint()
                end_point = self.view.mapToScene(widget_pos)
                
                # Base shape data
                shape_data = {
                    "type": self.current_tool,
                    "start": (self.start_point.x(), self.start_point.y()),
                    "end": (end_point.x(), end_point.y()),
                    "color": self.color.name() if self.temp_item else "#000000"
                }
                
                # Add points only for curve type
                if self.current_tool == "curve":
                    if hasattr(self, 'points'):
                        shape_data["points"] = [{"x":p.x(), "y":p.y()} for p in self.points]
                        delattr(self, 'points')  # Clean up points after use

                self.scene.removeItem(self.temp_item)  # Remove temporary shape
                self.add_remote_shape(shape_data)  # Add final shape
                self.history.append(shape_data)
                print(f"Shape added to history: {shape_data}")
                self.temp_item = None

        except Exception as e:
            print(f"Error in mouseReleaseEvent: {e}")