from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication

class CrosshairOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initProperties()

    def initUI(self):
        # Set window flags for overlay
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # No window frame
            Qt.WindowStaysOnTopHint | # Always on top
            Qt.Tool |                 # No taskbar icon
            Qt.WindowTransparentForInputs  # Click-through
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set fullscreen
        screen = QApplication.primaryScreen()
        self.setGeometry(screen.geometry())

    def initProperties(self):
        # Basic properties
        self.crosshair_size = 20
        self.crosshair_gap = 5
        self.crosshair_thickness = 2
        self.crosshair_color = QColor(Qt.red)
        self.center_dot = False
        
        # Outline properties
        self.outline_enabled = False
        self.outline_thickness = 2
        self.outline_color = QColor(Qt.black)
        
        # Style properties
        self.style = 'cross'  # 'cross', 'dot', 'circle', 'triangle'
        self.circle_radius = 10
        self.is_dynamic = False
        self.dynamic_scale = 1.0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Get center position
        center = QPoint(self.width() // 2, self.height() // 2)

        if self.style == 'cross':
            self.drawCross(painter, center)
        elif self.style == 'dot':
            self.drawDot(painter, center)
        elif self.style == 'circle':
            self.drawCircle(painter, center)
        elif self.style == 'triangle':
            self.drawTriangle(painter, center)

    def drawCross(self, painter, center):
        x, y = center.x(), center.y()
        
        # Draw outline if enabled
        if self.outline_enabled:
            outline_pen = QPen(
                self.outline_color,
                self.crosshair_thickness + self.outline_thickness,
                Qt.SolidLine
            )
            painter.setPen(outline_pen)
            # Horizontal outline segments
            painter.drawLine(x - self.crosshair_size, y, x - self.crosshair_gap, y)
            painter.drawLine(x + self.crosshair_gap, y, x + self.crosshair_size, y)
            # Vertical outline segments
            painter.drawLine(x, y - self.crosshair_size, x, y - self.crosshair_gap)
            painter.drawLine(x, y + self.crosshair_gap, x, y + self.crosshair_size)

        # Main crosshair lines
        pen = QPen(self.crosshair_color, self.crosshair_thickness, Qt.SolidLine)
        painter.setPen(pen)
        
        # Apply dynamic scaling if enabled
        size = self.crosshair_size * self.dynamic_scale if self.is_dynamic else self.crosshair_size
        gap = self.crosshair_gap * self.dynamic_scale if self.is_dynamic else self.crosshair_gap
        
        # Horizontal segments
        painter.drawLine(x - size, y, x - gap, y)
        painter.drawLine(x + gap, y, x + size, y)
        # Vertical segments
        painter.drawLine(x, y - size, x, y - gap)
        painter.drawLine(x, y + gap, x, y + size)

        # Draw center dot if enabled
        if self.center_dot:
            dot_diameter = max(2, int(self.crosshair_thickness * 0.7))
            dot_x = int(x - dot_diameter / 2)
            dot_y = int(y - dot_diameter / 2)
            painter.setBrush(self.crosshair_color)
            painter.drawEllipse(dot_x, dot_y, dot_diameter, dot_diameter)

    def drawDot(self, painter, center):
        x, y = center.x(), center.y()
        
        if self.outline_enabled:
            painter.setPen(QPen(self.outline_color, self.outline_thickness))
            painter.setBrush(self.crosshair_color)
            size = self.crosshair_size / 2
            painter.drawEllipse(x - size, y - size, size * 2, size * 2)
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.crosshair_color)
        size = (self.crosshair_size / 2) - (self.outline_thickness if self.outline_enabled else 0)
        painter.drawEllipse(x - size, y - size, size * 2, size * 2)

    def drawCircle(self, painter, center):
        x, y = center.x(), center.y()
        
        if self.outline_enabled:
            painter.setPen(QPen(self.outline_color, self.outline_thickness))
            painter.setBrush(Qt.NoBrush)
            size = self.circle_radius + self.outline_thickness
            painter.drawEllipse(x - size, y - size, size * 2, size * 2)
        
        painter.setPen(QPen(self.crosshair_color, self.crosshair_thickness))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(x - self.circle_radius, y - self.circle_radius,
                          self.circle_radius * 2, self.circle_radius * 2)

    def drawTriangle(self, painter, center):
        x, y = center.x(), center.y()
        size = self.crosshair_size / 2
        
        path = QPainterPath()
        path.moveTo(x, y - size)
        path.lineTo(x - size, y + size)
        path.lineTo(x + size, y + size)
        path.lineTo(x, y - size)
        
        if self.outline_enabled:
            painter.setPen(QPen(self.outline_color, self.outline_thickness))
            painter.setBrush(self.crosshair_color)
            painter.drawPath(path)
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.crosshair_color)
        painter.drawPath(path)

    def setDynamicScaling(self, enabled, scale=1.0):
        self.is_dynamic = enabled
        self.dynamic_scale = scale
        self.update()

    def setStyle(self, style):
        self.style = style
        self.update()
