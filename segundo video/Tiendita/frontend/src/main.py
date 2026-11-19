import sys
from datetime import datetime, timedelta
from pathlib import Path

from PySide6.QtCore import QObject, QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QIcon,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget
)


# ==============================================================================
# PALETA CORPORATIVA OFICIAL PYMESYNC (Basada en logo_horizontal_clean.png)
# ==============================================================================
BRAND_BLUE = "#0e498c"         # Azul Zafiro Corporativo ("Pyme" y flecha superior)
BRAND_BLUE_DARK = "#0a3666"    # Azul Profundo Hover / Cabeceras
BRAND_NAVY = "#072448"         # Fondo Oscuro Institucional (Sidebar / Login Hero)
BRAND_BLUE_LIGHT = "#eff6ff"   # Fondo Suave Azul
BRAND_CYAN = "#14b6c4"         # Turquesa Eléctrico ("Sync" y flecha inferior)
BRAND_CYAN_DARK = "#0e8a94"    # Turquesa Oscuro para bordes/texto activo
BRAND_CYAN_LIGHT = "#e6fafc"   # Fondo Suave Turquesa


STYLE = """
QWidget {
    font-family: "Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif;
    font-size: 14px;
    color: #1e293b;
}

QMainWindow, #mainContent, #pageRoot {
    background: #f1f5f9;
}

/* ================= SIDEBAR CORPORATIVO ================= */
#sidebar {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #072448,
        stop: 0.55 #0a3161,
        stop: 1 #061d3b
    );
    border-right: 1px solid #0e498c;
}

#sidebarBrandCard {
    background: #ffffff;
    border: 2px solid #14b6c4;
    border-radius: 13px;
}

#brand {
    color: #0e498c;
    font-size: 24px;
    font-weight: 800;
}

#brandSlogan {
    color: #0e8a94;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.4px;
}

#brandSub {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 600;
}

#sidebarSectionLabel {
    color: #64748b;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
    padding-left: 8px;
}

#sidebarButton {
    background: transparent;
    color: #cbd5e1;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 11px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 13.5px;
}

#sidebarButton:hover {
    background: rgba(20, 182, 196, 0.14);
    color: #ffffff;
    border: 1px solid rgba(20, 182, 196, 0.30);
}

#sidebarButton:checked {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #0e498c,
        stop: 1 #14b6c4
    );
    color: #ffffff;
    border: 1px solid #5eead4;
    font-weight: 800;
}

#sidebarStatusCard {
    background: rgba(14, 73, 140, 0.32);
    border: 1px solid rgba(20, 182, 196, 0.28);
    border-radius: 10px;
}

#sidebarStatusDot {
    color: #5eead4;
    font-size: 11px;
    font-weight: 800;
}

#sidebarFooter {
    color: #94a3b8;
    font-size: 11px;
}

/* ================= TOPBAR ================= */
#topbar {
    background: #ffffff;
    border-bottom: 2px solid #e2e8f0;
}

#topbarAccent {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #0e498c,
        stop: 0.5 #14b6c4,
        stop: 1 #0e498c
    );
}

#pageTitle {
    font-size: 20px;
    font-weight: 800;
    color: #0e498c;
}

#topbarBadge {
    background: #e6fafc;
    color: #0e8a94;
    border: 1px solid #99f6e4;
    border-radius: 6px;
    padding: 3px 9px;
    font-size: 11px;
    font-weight: 800;
}

#userName {
    font-weight: 800;
    color: #0e498c;
    font-size: 13.5px;
}

#userRole {
    color: #0e8a94;
    font-size: 11px;
    font-weight: 700;
}

/* ================= ENCABEZADOS DE SECCION ================= */
#sectionTitle {
    font-size: 25px;
    font-weight: 800;
    color: #0a3666;
}

#sectionSubtitle {
    color: #64748b;
    font-size: 13px;
    font-weight: 500;
}

/* ================= TARJETAS Y KPI STAT CARDS ================= */
#card, #loginCard {
    background: #ffffff;
    border: 1px solid #dbe4f0;
    border-radius: 14px;
}

#statCardBlue {
    background: #ffffff;
    border: 1px solid #dbe4f0;
    border-top: 4px solid #0e498c;
    border-radius: 14px;
}

#statCardCyan {
    background: #ffffff;
    border: 1px solid #dbe4f0;
    border-top: 4px solid #14b6c4;
    border-radius: 14px;
}

#statCardAlert {
    background: #ffffff;
    border: 1px solid #fde68a;
    border-top: 4px solid #f59e0b;
    border-radius: 14px;
}

#statTitle {
    color: #475569;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}

#statValue {
    color: #0e498c;
    font-size: 27px;
    font-weight: 800;
}

#statValueCyan {
    color: #0e8a94;
    font-size: 27px;
    font-weight: 800;
}

#statValueAlert {
    color: #d97706;
    font-size: 27px;
    font-weight: 800;
}

#statDetail {
    color: #64748b;
    font-size: 11.5px;
    font-weight: 600;
}

#cardTitle {
    font-size: 16px;
    font-weight: 800;
    color: #0e498c;
}

/* ================= INPUTS Y CONTROLES ================= */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 9px;
    padding: 8px 12px;
    min-height: 22px;
    color: #0f172a;
    font-weight: 500;
}

QLineEdit:hover, QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border: 1.5px solid #0e498c;
    background: #ffffff;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #14b6c4;
    background: #ffffff;
}

QComboBox::drop-down {
    border: none;
    width: 26px;
}

QCheckBox {
    color: #475569;
    font-weight: 600;
    spacing: 8px;
}

/* ================= BOTONES ================= */
QPushButton {
    border-radius: 9px;
    padding: 9px 16px;
    font-weight: 700;
    font-size: 13.5px;
}

#primaryButton {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #0e498c,
        stop: 1 #14b6c4
    );
    color: #ffffff;
    border: none;
}

#primaryButton:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #0a3666,
        stop: 1 #0e8a94
    );
}

#primaryButton:pressed {
    background: #072448;
}

#secondaryButton {
    background: #ffffff;
    color: #0e498c;
    border: 1.5px solid #0e498c;
}

#secondaryButton:hover {
    background: #eff6ff;
    border: 1.5px solid #14b6c4;
    color: #0a3666;
}

/* ================= TABLAS DE DATOS ================= */
QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    color: #1e293b;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    gridline-color: #f1f5f9;
    selection-background-color: #e6fafc;
    selection-color: #0e498c;
}

QHeaderView::section {
    background-color: #f0f7ff;
    color: #0e498c;
    border: none;
    border-bottom: 2px solid #14b6c4;
    padding: 11px 10px;
    font-weight: 800;
    font-size: 12.5px;
}

QTableWidget::item {
    background-color: transparent;
    color: #1e293b;
    padding: 8px 10px;
    border-bottom: 1px solid #f1f5f9;
}

QTableWidget::item:selected {
    background-color: #e6fafc;
    color: #0e498c;
    font-weight: 700;
}

#saleTotal {
    font-size: 24px;
    font-weight: 800;
    color: #0e498c;
    background: #e6fafc;
    border: 1.5px solid #14b6c4;
    border-radius: 10px;
    padding: 6px 16px;
}

#stockOk {
    color: #0e8a94;
    background: #e6fafc;
    border: 1px solid #99f6e4;
    border-radius: 8px;
    padding: 6px 12px;
    font-weight: 800;
}

#stockLow {
    color: #b45309;
    background: #fef3c7;
    border: 1px solid #fde68a;
    border-radius: 8px;
    padding: 6px 12px;
    font-weight: 800;
}

/* ================= LOGIN WINDOW ================= */
#loginLeft {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #072448,
        stop: 0.6 #0e498c,
        stop: 1 #0b7a8c
    );
}

#loginLogoCard {
    background: #ffffff;
    border: 2px solid #14b6c4;
    border-radius: 16px;
}

#loginRight {
    background: #f1f5f9;
}

#loginBrand {
    color: #ffffff;
    font-size: 28px;
    font-weight: 900;
}

#loginSloganPill {
    background: rgba(20, 182, 196, 0.22);
    color: #5eead4;
    border: 1px solid #14b6c4;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 800;
}

#loginHero {
    color: #ffffff;
    font-size: 36px;
    font-weight: 900;
}

#loginText {
    color: #e2e8f0;
    font-size: 15px;
    line-height: 1.4;
}

#loginFeature {
    color: #f0fdfa;
    font-size: 13.5px;
    font-weight: 600;
}

#loginTitle {
    color: #0e498c;
    font-size: 28px;
    font-weight: 800;
}

#loginSub {
    color: #64748b;
    font-size: 13.5px;
    font-weight: 500;
}

#loginDemo {
    background: #eff6ff;
    color: #0e498c;
    border: 1px dashed #14b6c4;
    border-radius: 8px;
    padding: 8px;
    font-size: 12px;
    font-weight: 700;
}

#loginDemo:hover {
    background: #e6fafc;
}

QDialog {
    background: #f8fafc;
}
"""


# ==============================================================================
# MOTOR DE ICONOS VECTORIALES Y LOGO HORIZONTAL DE PYMESYNC
# ==============================================================================
def find_logo_path():
    here = Path(__file__).resolve().parent
    candidates = [
        here / "logo_horizontal_clean.png",
        here / "assets" / "logo_horizontal_clean.png",
        here.parent.parent.parent.parent / "logo_horizontal_clean.png",
        here.parent.parent.parent / "logo_horizontal_clean.png",
        Path("/home/yahir/2EMPRENDEDORES/logo_horizontal_clean.png"),
        Path("/home/yahir/2EMPRENDEDORES/logo_horizontal.png"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def load_clean_horizontal_logo(max_width=200, max_height=48):
    """Carga el logo horizontal oficial recortando bordes residuales y escalando con proporción exacta."""
    logo_path = find_logo_path()
    if logo_path:
        img = QImage(str(logo_path))
        if not img.isNull():
            w, h = img.width(), img.height()
            # Recorta márgenes blancos exteriores y líneas grises de corte en los extremos del PNG
            x0 = int(w * 0.035)
            y0 = int(h * 0.11)
            cw = max(1, int(w * 0.907))
            ch = max(1, int(h * 0.79))
            cropped = img.copy(x0, y0, cw, ch)
            pix = QPixmap.fromImage(cropped)
            return pix.scaled(
                max_width,
                max_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

    # Fallback vectorial idéntico al logo horizontal PymeSync
    pix = QPixmap(max_width, max_height)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    draw_sync_emblem(p, QRectF(2, 2, max_height - 4, max_height - 4))
    font = QFont("Plus Jakarta Sans", int(max_height * 0.44), QFont.ExtraBold)
    p.setFont(font)
    p.setPen(QColor(BRAND_BLUE))
    p.drawText(QRectF(max_height + 4, 0, max_width * 0.45, max_height), Qt.AlignVCenter | Qt.AlignLeft, "Pyme")
    p.setPen(QColor(BRAND_CYAN))
    p.drawText(QRectF(max_height + max_width * 0.36, 0, max_width * 0.45, max_height), Qt.AlignVCenter | Qt.AlignLeft, "Sync")
    p.end()
    return pix


def draw_sync_emblem(painter, rect):
    """Dibuja el isotipo oficial de PymeSync: doble flecha circular en Azul Zafiro (#0e498c) y Turquesa (#14b6c4)."""
    painter.save()
    painter.setRenderHint(QPainter.Antialiasing)
    cx = rect.center().x()
    cy = rect.center().y()
    r = min(rect.width(), rect.height()) * 0.36
    pen_w = max(2.2, min(rect.width(), rect.height()) * 0.13)

    arc_rect = QRectF(cx - r, cy - r, r * 2, r * 2)

    # Arco superior (Azul Zafiro #0e498c)
    pen_blue = QPen(QColor(BRAND_BLUE), pen_w, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
    painter.setPen(pen_blue)
    painter.drawArc(arc_rect, 25 * 16, 145 * 16)

    # Punta de flecha superior derecha
    head_size = pen_w * 1.55
    p1 = QPointF(cx + r * 0.92, cy - r * 0.18)
    poly_top = QPolygonF([
        p1,
        QPointF(p1.x() - head_size * 1.15, p1.y() - head_size * 0.25),
        QPointF(p1.x() - head_size * 0.15, p1.y() - head_size * 1.25),
    ])
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor(BRAND_BLUE))
    painter.drawPolygon(poly_top)

    # Arco inferior (Turquesa Eléctrico #14b6c4)
    pen_cyan = QPen(QColor(BRAND_CYAN), pen_w, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
    painter.setPen(pen_cyan)
    painter.setBrush(Qt.NoBrush)
    painter.drawArc(arc_rect, 205 * 16, 145 * 16)

    # Punta de flecha inferior izquierda
    p2 = QPointF(cx - r * 0.92, cy + r * 0.18)
    poly_bot = QPolygonF([
        p2,
        QPointF(p2.x() + head_size * 1.15, p2.y() + head_size * 0.25),
        QPointF(p2.x() + head_size * 0.15, p2.y() + head_size * 1.25),
    ])
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor(BRAND_CYAN))
    painter.drawPolygon(poly_bot)
    painter.restore()


def make_app_icon():
    pix = QPixmap(64, 64)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(QPen(QColor(BRAND_CYAN), 2))
    p.setBrush(QColor("#ffffff"))
    p.drawRoundedRect(QRectF(2, 2, 60, 60), 16, 16)
    draw_sync_emblem(p, QRectF(6, 6, 52, 52))
    p.end()
    return QIcon(pix)


def make_vector_pixmap(name, size=24, primary=BRAND_BLUE, accent=BRAND_CYAN, bg=None):
    """Genera iconos vectoriales coherentes con la identidad PymeSync."""
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)

    if bg:
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(bg))
        p.drawRoundedRect(QRectF(0, 0, size, size), size * 0.26, size * 0.26)

    pad = size * (0.24 if bg else 0.12)
    r = QRectF(pad, pad, size - pad * 2, size - pad * 2)
    w = r.width()
    h = r.height()
    x = r.left()
    y = r.top()

    pen_p = QPen(QColor(primary), max(1.8, size * 0.085), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
    pen_a = QPen(QColor(accent), max(1.8, size * 0.085), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

    if name == "dashboard":
        gap = w * 0.14
        hw = (w - gap) / 2
        hh = (h - gap) / 2
        p.setPen(pen_p)
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(x, y, hw, hh), 2.5, 2.5)
        p.drawRoundedRect(QRectF(x + hw + gap, y + hh + gap, hw, hh), 2.5, 2.5)
        p.setPen(pen_a)
        p.drawRoundedRect(QRectF(x + hw + gap, y, hw, hh), 2.5, 2.5)
        p.drawRoundedRect(QRectF(x, y + hh + gap, hw, hh), 2.5, 2.5)

    elif name == "ventas":
        p.setPen(pen_p)
        path = QPainterPath()
        path.moveTo(x, y + h * 0.12)
        path.lineTo(x + w * 0.18, y + h * 0.12)
        path.lineTo(x + w * 0.32, y + h * 0.68)
        path.lineTo(x + w * 0.84, y + h * 0.68)
        path.lineTo(x + w * 0.95, y + h * 0.28)
        path.lineTo(x + w * 0.23, y + h * 0.28)
        p.drawPath(path)
        p.setPen(pen_a)
        p.setBrush(QColor(accent))
        p.drawEllipse(QPointF(x + w * 0.38, y + h * 0.88), w * 0.08, w * 0.08)
        p.drawEllipse(QPointF(x + w * 0.78, y + h * 0.88), w * 0.08, w * 0.08)

    elif name == "productos":
        p.setPen(pen_p)
        poly = QPolygonF([
            QPointF(x + w * 0.5, y + h * 0.05),
            QPointF(x + w * 0.92, y + h * 0.28),
            QPointF(x + w * 0.92, y + h * 0.74),
            QPointF(x + w * 0.5, y + h * 0.95),
            QPointF(x + w * 0.08, y + h * 0.74),
            QPointF(x + w * 0.08, y + h * 0.28),
        ])
        p.drawPolygon(poly)
        p.setPen(pen_a)
        p.drawLine(QPointF(x + w * 0.08, y + h * 0.28), QPointF(x + w * 0.5, y + h * 0.5))
        p.drawLine(QPointF(x + w * 0.92, y + h * 0.28), QPointF(x + w * 0.5, y + h * 0.5))
        p.drawLine(QPointF(x + w * 0.5, y + h * 0.5), QPointF(x + w * 0.5, y + h * 0.95))

    elif name == "inventario":
        p.setPen(pen_p)
        p.drawRoundedRect(QRectF(x + w * 0.08, y + h * 0.12, w * 0.84, h * 0.78), 3, 3)
        p.setPen(pen_a)
        p.drawLine(QPointF(x + w * 0.28, y + h * 0.38), QPointF(x + w * 0.72, y + h * 0.38))
        p.drawLine(QPointF(x + w * 0.28, y + h * 0.58), QPointF(x + w * 0.58, y + h * 0.58))

    elif name == "movimientos":
        draw_sync_emblem(p, r)

    elif name == "proveedores":
        p.setPen(pen_p)
        p.drawRoundedRect(QRectF(x + w * 0.04, y + h * 0.22, w * 0.58, h * 0.48), 2, 2)
        p.setPen(pen_a)
        cab = QPolygonF([
            QPointF(x + w * 0.62, y + h * 0.34),
            QPointF(x + w * 0.82, y + h * 0.34),
            QPointF(x + w * 0.94, y + h * 0.52),
            QPointF(x + w * 0.94, y + h * 0.70),
            QPointF(x + w * 0.62, y + h * 0.70),
        ])
        p.drawPolygon(cab)
        p.setBrush(QColor(primary))
        p.drawEllipse(QPointF(x + w * 0.28, y + h * 0.78), w * 0.09, w * 0.09)
        p.drawEllipse(QPointF(x + w * 0.78, y + h * 0.78), w * 0.09, w * 0.09)

    elif name == "reportes":
        p.setPen(pen_p)
        p.drawLine(QPointF(x + w * 0.1, y + h * 0.88), QPointF(x + w * 0.9, y + h * 0.88))
        p.drawLine(QPointF(x + w * 0.25, y + h * 0.85), QPointF(x + w * 0.25, y + h * 0.55))
        p.drawLine(QPointF(x + w * 0.50, y + h * 0.85), QPointF(x + w * 0.50, y + h * 0.38))
        p.setPen(pen_a)
        p.drawLine(QPointF(x + w * 0.75, y + h * 0.85), QPointF(x + w * 0.75, y + h * 0.18))
        p.drawLine(QPointF(x + w * 0.20, y + h * 0.46), QPointF(x + w * 0.75, y + h * 0.15))

    elif name == "admin":
        p.setPen(pen_p)
        p.drawEllipse(QPointF(x + w * 0.5, y + h * 0.32), w * 0.20, w * 0.20)
        p.setPen(pen_a)
        p.drawArc(QRectF(x + w * 0.16, y + h * 0.58, w * 0.68, h * 0.52), 0, 180 * 16)

    elif name == "configuracion":
        p.setPen(pen_p)
        p.drawLine(QPointF(x + w * 0.12, y + h * 0.26), QPointF(x + w * 0.88, y + h * 0.26))
        p.drawLine(QPointF(x + w * 0.12, y + h * 0.52), QPointF(x + w * 0.88, y + h * 0.52))
        p.drawLine(QPointF(x + w * 0.12, y + h * 0.78), QPointF(x + w * 0.88, y + h * 0.78))
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(accent))
        p.drawEllipse(QPointF(x + w * 0.34, y + h * 0.26), w * 0.11, w * 0.11)
        p.drawEllipse(QPointF(x + w * 0.68, y + h * 0.52), w * 0.11, w * 0.11)
        p.drawEllipse(QPointF(x + w * 0.42, y + h * 0.78), w * 0.11, w * 0.11)

    elif name == "cash":
        p.setPen(pen_p)
        p.drawRoundedRect(QRectF(x + w * 0.06, y + h * 0.22, w * 0.88, h * 0.56), 3, 3)
        p.setPen(pen_a)
        p.drawEllipse(QPointF(x + w * 0.5, y + h * 0.5), w * 0.15, w * 0.15)

    elif name == "alert":
        p.setPen(QPen(QColor("#d97706"), max(1.8, size * 0.085), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        tri = QPolygonF([
            QPointF(x + w * 0.5, y + h * 0.12),
            QPointF(x + w * 0.90, y + h * 0.86),
            QPointF(x + w * 0.10, y + h * 0.86),
        ])
        p.drawPolygon(tri)
        p.drawLine(QPointF(x + w * 0.5, y + h * 0.40), QPointF(x + w * 0.5, y + h * 0.62))
        p.drawPoint(QPointF(x + w * 0.5, y + h * 0.74))

    elif name == "plus":
        p.setPen(pen_p)
        p.drawLine(QPointF(x + w * 0.5, y + h * 0.18), QPointF(x + w * 0.5, y + h * 0.82))
        p.drawLine(QPointF(x + w * 0.18, y + h * 0.5), QPointF(x + w * 0.82, y + h * 0.5))

    elif name == "check":
        p.setPen(pen_p)
        p.drawLine(QPointF(x + w * 0.18, y + h * 0.52), QPointF(x + w * 0.42, y + h * 0.76))
        p.drawLine(QPointF(x + w * 0.42, y + h * 0.76), QPointF(x + w * 0.84, y + h * 0.24))

    elif name == "edit":
        p.setPen(pen_p)
        p.drawLine(QPointF(x + w * 0.20, y + h * 0.80), QPointF(x + w * 0.78, y + h * 0.22))
        p.setPen(pen_a)
        p.drawLine(QPointF(x + w * 0.16, y + h * 0.84), QPointF(x + w * 0.34, y + h * 0.80))

    elif name == "remove":
        p.setPen(pen_p)
        p.drawLine(QPointF(x + w * 0.22, y + h * 0.5), QPointF(x + w * 0.78, y + h * 0.5))

    p.end()
    return pix


def make_section_header(icon_name, title_text, subtitle_text):
    """Crea un encabezado de página con icono corporativo PymeSync."""
    container = QHBoxLayout()
    container.setSpacing(14)

    icon_lbl = QLabel()
    icon_lbl.setFixedSize(44, 44)
    icon_lbl.setPixmap(
        make_vector_pixmap(
            icon_name,
            size=44,
            primary=BRAND_BLUE,
            accent=BRAND_CYAN,
            bg=BRAND_CYAN_LIGHT
        )
    )

    text_box = QVBoxLayout()
    text_box.setSpacing(2)

    title = QLabel(title_text)
    title.setObjectName("sectionTitle")

    subtitle = QLabel(subtitle_text)
    subtitle.setObjectName("sectionSubtitle")

    text_box.addWidget(title)
    text_box.addWidget(subtitle)

    container.addWidget(icon_lbl)
    container.addLayout(text_box)
    container.addStretch()
    return container


class StoreState(QObject):
    updated = Signal()

    def __init__(self):
        super().__init__()

        self.products = [
            {
                "id": 1,
                "codigo": "7501055300012",
                "nombre": "Coca-Cola 600 ml",
                "categoria": "Bebidas",
                "costo": 14.50,
                "precio": 20.00,
                "stock": 80,
                "minimo": 15
            },
            {
                "id": 2,
                "codigo": "7500478020019",
                "nombre": "Sabritas Original 45 g",
                "categoria": "Botanas",
                "costo": 13.00,
                "precio": 18.00,
                "stock": 42,
                "minimo": 10
            },
            {
                "id": 3,
                "codigo": "7501000110019",
                "nombre": "Leche Lala 1 L",
                "categoria": "Lacteos",
                "costo": 23.50,
                "precio": 29.00,
                "stock": 28,
                "minimo": 8
            },
            {
                "id": 4,
                "codigo": "7501031310011",
                "nombre": "Pan Bimbo Grande",
                "categoria": "Panaderia",
                "costo": 39.00,
                "precio": 48.00,
                "stock": 19,
                "minimo": 8
            },
            {
                "id": 5,
                "codigo": "7501005100022",
                "nombre": "Galletas Marias",
                "categoria": "Abarrotes",
                "costo": 15.00,
                "precio": 21.00,
                "stock": 35,
                "minimo": 10
            },
            {
                "id": 6,
                "codigo": "7501025400014",
                "nombre": "Agua Ciel 1 L",
                "categoria": "Bebidas",
                "costo": 9.00,
                "precio": 14.00,
                "stock": 60,
                "minimo": 15
            },
            {
                "id": 7,
                "codigo": "7501000124450",
                "nombre": "Huevo 12 piezas",
                "categoria": "Abarrotes",
                "costo": 39.00,
                "precio": 49.00,
                "stock": 7,
                "minimo": 10
            },
            {
                "id": 8,
                "codigo": "7501011100423",
                "nombre": "Cafe Soluble 100 g",
                "categoria": "Abarrotes",
                "costo": 52.00,
                "precio": 65.00,
                "stock": 12,
                "minimo": 5
            }
        ]

        now = datetime.now()

        self.sales = [
            {
                "folio": "V-1001",
                "fecha": now - timedelta(days=6),
                "productos": 8,
                "total": 420.00
            },
            {
                "folio": "V-1002",
                "fecha": now - timedelta(days=5),
                "productos": 14,
                "total": 790.00
            },
            {
                "folio": "V-1003",
                "fecha": now - timedelta(days=4),
                "productos": 10,
                "total": 560.00
            },
            {
                "folio": "V-1004",
                "fecha": now - timedelta(days=3),
                "productos": 18,
                "total": 940.00
            },
            {
                "folio": "V-1005",
                "fecha": now - timedelta(days=2),
                "productos": 12,
                "total": 655.00
            },
            {
                "folio": "V-1006",
                "fecha": now - timedelta(days=1),
                "productos": 21,
                "total": 1180.00
            },
            {
                "folio": "V-1007",
                "fecha": now,
                "productos": 9,
                "total": 510.00
            }
        ]

        self.movements = [
            {
                "fecha": now.strftime("%d/%m/%Y %H:%M"),
                "tipo": "Entrada",
                "producto": "Coca-Cola 600 ml",
                "cantidad": 24,
                "detalle": "Recepcion de proveedor"
            },
            {
                "fecha": now.strftime("%d/%m/%Y %H:%M"),
                "tipo": "Venta",
                "producto": "Sabritas Original 45 g",
                "cantidad": -3,
                "detalle": "Venta registrada"
            },
            {
                "fecha": (now - timedelta(days=1)).strftime("%d/%m/%Y %H:%M"),
                "tipo": "Ajuste",
                "producto": "Leche Lala 1 L",
                "cantidad": -2,
                "detalle": "Producto danado"
            }
        ]

        self.providers = [
            {
                "nombre": "Distribuidora Centro",
                "contacto": "Carlos Ramirez",
                "telefono": "449 123 4567",
                "productos": "Bebidas y botanas"
            },
            {
                "nombre": "Abarrotes del Bajio",
                "contacto": "Maria Lopez",
                "telefono": "449 222 3344",
                "productos": "Abarrotes"
            },
            {
                "nombre": "Lacteos del Centro",
                "contacto": "Jorge Hernandez",
                "telefono": "449 555 8899",
                "productos": "Lacteos"
            }
        ]

        self.users = [
            {
                "nombre": "Administrador",
                "usuario": "admin",
                "rol": "Administrador",
                "estado": "Activo"
            },
            {
                "nombre": "Caja Principal",
                "usuario": "caja1",
                "rol": "Cajero",
                "estado": "Activo"
            }
        ]

    def get_product(self, product_id):
        for product in self.products:
            if product["id"] == product_id:
                return product

        return None

    def add_product(self, product):
        product["id"] = max(
            [p["id"] for p in self.products],
            default=0
        ) + 1

        self.products.append(product)
        self.updated.emit()

    def update_product(self, product_id, data):
        product = self.get_product(product_id)

        if product:
            product.update(data)
            self.updated.emit()

    def add_stock(self, product_id, quantity):
        product = self.get_product(product_id)

        if not product:
            return False

        product["stock"] += quantity

        self.movements.insert(
            0,
            {
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tipo": "Entrada",
                "producto": product["nombre"],
                "cantidad": quantity,
                "detalle": "Entrada de inventario"
            }
        )

        self.updated.emit()

        return True

    def sell(self, cart):
        for item in cart:
            product = self.get_product(item["product_id"])

            if not product:
                return False, "Producto no encontrado"

            if item["cantidad"] > product["stock"]:
                return False, f"Stock insuficiente para {product['nombre']}"

        total = 0
        units = 0

        for item in cart:
            product = self.get_product(item["product_id"])

            product["stock"] -= item["cantidad"]

            subtotal = product["precio"] * item["cantidad"]

            total += subtotal
            units += item["cantidad"]

            self.movements.insert(
                0,
                {
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "tipo": "Venta",
                    "producto": product["nombre"],
                    "cantidad": -item["cantidad"],
                    "detalle": "Venta registrada"
                }
            )

        folio = f"V-{1000 + len(self.sales) + 1}"

        self.sales.append(
            {
                "folio": folio,
                "fecha": datetime.now(),
                "productos": units,
                "total": total
            }
        )

        self.updated.emit()

        return True, total

    def add_provider(self, provider):
        self.providers.append(provider)
        self.updated.emit()

    def add_user(self, user):
        self.users.append(user)
        self.updated.emit()


class StatCard(QFrame):
    def __init__(self, title, value, detail="", icon_name="cash", variant="blue"):
        super().__init__()

        if variant == "cyan":
            self.setObjectName("statCardCyan")
            val_obj = "statValueCyan"
            bg_col = BRAND_CYAN_LIGHT
            pri_col = BRAND_CYAN_DARK
            acc_col = BRAND_BLUE
        elif variant == "alert":
            self.setObjectName("statCardAlert")
            val_obj = "statValueAlert"
            bg_col = "#fef3c7"
            pri_col = "#d97706"
            acc_col = "#b45309"
        else:
            self.setObjectName("statCardBlue")
            val_obj = "statValue"
            bg_col = BRAND_BLUE_LIGHT
            pri_col = BRAND_BLUE
            acc_col = BRAND_CYAN

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        top_row = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("statTitle")

        icon_label = QLabel()
        icon_label.setFixedSize(34, 34)
        icon_label.setPixmap(
            make_vector_pixmap(
                icon_name,
                size=34,
                primary=pri_col,
                accent=acc_col,
                bg=bg_col
            )
        )

        top_row.addWidget(title_label)
        top_row.addStretch()
        top_row.addWidget(icon_label)

        self.value_label = QLabel(value)
        self.value_label.setObjectName(val_obj)

        detail_label = QLabel(detail)
        detail_label.setObjectName("statDetail")

        layout.addLayout(top_row)
        layout.addWidget(self.value_label)
        layout.addWidget(detail_label)

    def set_value(self, value):
        self.value_label.setText(value)


def setup_table(table, headers):
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.verticalHeader().setVisible(False)
    table.verticalHeader().setDefaultSectionSize(40)
    table.setShowGrid(False)

    table.setEditTriggers(
        QAbstractItemView.NoEditTriggers
    )

    table.setSelectionBehavior(
        QAbstractItemView.SelectRows
    )

    table.setAlternatingRowColors(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.horizontalHeader().setStretchLastSection(True)


def style_table_item(item, value):
    text = str(value).strip()
    if text in ("Disponible", "Activo", "Entrada"):
        item.setForeground(QColor("#0e8a94"))
        font = item.font()
        font.setBold(True)
        item.setFont(font)
    elif text in ("Stock bajo", "Ajuste"):
        item.setForeground(QColor("#d97706"))
        font = item.font()
        font.setBold(True)
        item.setFont(font)
    elif text in ("Agotado",):
        item.setForeground(QColor("#dc2626"))
        font = item.font()
        font.setBold(True)
        item.setFont(font)
    elif text in ("Venta",):
        item.setForeground(QColor(BRAND_BLUE))
        font = item.font()
        font.setBold(True)
        item.setFont(font)
    elif text.startswith("$") or text.startswith("V-"):
        item.setForeground(QColor(BRAND_BLUE))
        font = item.font()
        font.setBold(True)
        item.setFont(font)


def fill_table(table, rows):
    table.setRowCount(len(rows))

    for row_index, row_data in enumerate(rows):
        for column_index, value in enumerate(row_data):
            item = QTableWidgetItem(str(value))
            style_table_item(item, value)
            table.setItem(
                row_index,
                column_index,
                item
            )


class LoginWindow(QWidget):
    login_success = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PymeSync · Tu tiendita, bien chidita")
        self.setWindowIcon(make_app_icon())
        self.resize(1100, 690)
        self.setMinimumSize(920, 610)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        left = QFrame()
        left.setObjectName("loginLeft")

        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(56, 52, 56, 52)
        left_layout.setSpacing(14)

        # Contenedor blanco para el logo horizontal oficial
        logo_card = QFrame()
        logo_card.setObjectName("loginLogoCard")
        logo_card_layout = QHBoxLayout(logo_card)
        logo_card_layout.setContentsMargins(18, 12, 18, 12)
        logo_lbl = QLabel()
        logo_lbl.setPixmap(load_clean_horizontal_logo(270, 56))
        logo_card_layout.addWidget(logo_lbl)
        logo_card_layout.addStretch()

        slogan_pill = QLabel("«TU TIENDITA, BIEN CHIDITA»  ·  SaaS B2B")
        slogan_pill.setObjectName("loginSloganPill")
        slogan_pill.setMaximumWidth(330)

        hero = QLabel(
            "El control total de tu negocio, sin complicaciones"
        )
        hero.setObjectName("loginHero")
        hero.setWordWrap(True)

        text = QLabel(
            "Controla ventas, inventario, precios, entradas, proveedores y reportes desde una interfaz simple, coherente y profesional."
        )
        text.setObjectName("loginText")
        text.setWordWrap(True)

        feat1 = QLabel("✓  Punto de venta ágil y corte de caja automático")
        feat1.setObjectName("loginFeature")
        feat2 = QLabel("✓  Alertas de stock mínimo y control de entradas")
        feat2.setObjectName("loginFeature")
        feat3 = QLabel("✓  Funciona localmente sin depender de internet")
        feat3.setObjectName("loginFeature")

        left_layout.addWidget(logo_card)
        left_layout.addSpacing(8)
        left_layout.addWidget(slogan_pill)
        left_layout.addStretch()
        left_layout.addWidget(hero)
        left_layout.addSpacing(8)
        left_layout.addWidget(text)
        left_layout.addSpacing(14)
        left_layout.addWidget(feat1)
        left_layout.addWidget(feat2)
        left_layout.addWidget(feat3)
        left_layout.addStretch()

        right = QFrame()
        right.setObjectName("loginRight")

        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(72, 52, 72, 52)

        card = QFrame()
        card.setObjectName("loginCard")

        form = QVBoxLayout(card)
        form.setContentsMargins(36, 34, 36, 34)
        form.setSpacing(13)

        mini_logo = QLabel()
        mini_logo.setPixmap(load_clean_horizontal_logo(190, 42))
        mini_logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        title = QLabel("Bienvenido")
        title.setObjectName("loginTitle")

        subtitle = QLabel(
            "Inicia sesión en PymeSync para administrar tu negocio"
        )
        subtitle.setObjectName("loginSub")

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingresa tu usuario (ej. admin)")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(
            "Ingresa tu contraseña"
        )
        self.password_input.setEchoMode(
            QLineEdit.Password
        )
        self.password_input.returnPressed.connect(
            self.login
        )

        show = QCheckBox(
            "Mostrar contraseña"
        )

        show.toggled.connect(
            lambda checked:
            self.password_input.setEchoMode(
                QLineEdit.Normal
                if checked
                else QLineEdit.Password
            )
        )

        button = QPushButton(
            "Iniciar sesión"
        )
        button.setObjectName("primaryButton")
        button.setIcon(QIcon(make_vector_pixmap("check", 18, "#ffffff", "#ffffff")))
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.login)

        demo = QPushButton(
            "Acceso Demo   ·   Usuario: admin   |   Contraseña: admin123"
        )
        demo.setObjectName("loginDemo")
        demo.setCursor(Qt.PointingHandCursor)
        demo.clicked.connect(self.fill_demo)

        form.addWidget(mini_logo)
        form.addSpacing(4)
        form.addWidget(title)
        form.addWidget(subtitle)
        form.addSpacing(8)
        form.addWidget(QLabel("Usuario"))
        form.addWidget(self.user_input)
        form.addWidget(QLabel("Contraseña"))
        form.addWidget(self.password_input)
        form.addWidget(show)
        form.addSpacing(6)
        form.addWidget(button)
        form.addSpacing(4)
        form.addWidget(demo)

        right_layout.addStretch()
        right_layout.addWidget(card)
        right_layout.addStretch()

        root.addWidget(left, 1)
        root.addWidget(right, 1)

    def fill_demo(self):
        self.user_input.setText("admin")
        self.password_input.setText("admin123")

    def login(self):
        user = self.user_input.text().strip()
        password = self.password_input.text()

        if (
            user == "admin"
            and password == "admin123"
        ):
            self.login_success.emit(
                "Administrador"
            )

        else:
            QMessageBox.warning(
                self,
                "Acceso denegado",
                "Usuario o contraseña incorrectos."
            )


class Sidebar(QFrame):
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")
        self.setFixedWidth(262)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 18)
        layout.setSpacing(6)

        # Tarjeta blanca superior con el Logo Horizontal Oficial de PymeSync
        brand_card = QFrame()
        brand_card.setObjectName("sidebarBrandCard")
        brand_card_layout = QVBoxLayout(brand_card)
        brand_card_layout.setContentsMargins(12, 10, 12, 10)
        brand_card_layout.setSpacing(4)

        logo_label = QLabel()
        logo_label.setPixmap(load_clean_horizontal_logo(202, 46))
        logo_label.setAlignment(Qt.AlignCenter)

        slogan = QLabel("«Tu tiendita, bien chidita»")
        slogan.setObjectName("brandSlogan")
        slogan.setAlignment(Qt.AlignCenter)

        brand_card_layout.addWidget(logo_label)
        brand_card_layout.addWidget(slogan)

        sub = QLabel("PLATAFORMA DE GESTIÓN COMERCIAL")
        sub.setObjectName("sidebarSectionLabel")

        layout.addWidget(brand_card)
        layout.addSpacing(12)
        layout.addWidget(sub)
        layout.addSpacing(4)

        self.buttons = {}
        self.icons_normal = {}
        self.icons_active = {}

        pages = [
            ("dashboard", "Inicio"),
            ("ventas", "Ventas"),
            ("productos", "Productos"),
            ("inventario", "Inventario"),
            ("movimientos", "Movimientos"),
            ("proveedores", "Proveedores"),
            ("reportes", "Reportes"),
            ("admin", "Administración"),
            ("configuracion", "Configuración")
        ]

        for key, text in pages:
            button = QPushButton(f"  {text}")
            button.setObjectName("sidebarButton")
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)

            self.icons_normal[key] = QIcon(
                make_vector_pixmap(key, 20, "#cbd5e1", BRAND_CYAN)
            )
            self.icons_active[key] = QIcon(
                make_vector_pixmap(key, 20, "#ffffff", "#e0f2fe")
            )

            button.setIcon(self.icons_normal[key])
            button.setIconSize(QSize(20, 20))

            button.clicked.connect(
                lambda checked=False, page=key:
                self.select_page(page)
            )

            self.buttons[key] = button
            layout.addWidget(button)

        layout.addStretch()

        status_card = QFrame()
        status_card.setObjectName("sidebarStatusCard")
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(12, 10, 12, 10)
        status_layout.setSpacing(2)

        status_dot = QLabel("●  Modo Local Activo (Sin Internet)")
        status_dot.setObjectName("sidebarStatusDot")

        footer = QLabel("PymeSync SaaS · Equipo 3 UAA")
        footer.setObjectName("sidebarFooter")

        status_layout.addWidget(status_dot)
        status_layout.addWidget(footer)

        layout.addWidget(status_card)

    def select_page(self, page):
        for key, button in self.buttons.items():
            is_selected = key == page
            button.setChecked(is_selected)
            button.setIcon(
                self.icons_active[key]
                if is_selected
                else self.icons_normal[key]
            )

        self.page_changed.emit(page)


class Topbar(QFrame):
    def __init__(self, user):
        super().__init__()

        self.setObjectName("topbar")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Barra superior degradada corporativa (Azul Zafiro -> Turquesa -> Azul Zafiro)
        accent_bar = QFrame()
        accent_bar.setObjectName("topbarAccent")
        accent_bar.setFixedHeight(4)
        outer.addWidget(accent_bar)

        layout = QHBoxLayout()
        layout.setContentsMargins(28, 12, 28, 12)
        layout.setSpacing(12)

        self.page_icon = QLabel()
        self.page_icon.setFixedSize(32, 32)
        self.page_icon.setPixmap(
            make_vector_pixmap("dashboard", 32, BRAND_BLUE, BRAND_CYAN, BRAND_CYAN_LIGHT)
        )

        self.title = QLabel("Inicio")
        self.title.setObjectName("pageTitle")

        badge = QLabel("«Tu tiendita, bien chidita»")
        badge.setObjectName("topbarBadge")

        avatar = QLabel()
        avatar.setFixedSize(36, 36)
        avatar.setPixmap(
            make_vector_pixmap("admin", 36, "#ffffff", BRAND_CYAN_LIGHT, BRAND_BLUE)
        )

        user_box = QVBoxLayout()
        user_box.setSpacing(0)

        user_name = QLabel(user)
        user_name.setObjectName("userName")

        user_role = QLabel("Administrador · PymeSync")
        user_role.setObjectName("userRole")

        user_box.addWidget(user_name)
        user_box.addWidget(user_role)

        layout.addWidget(self.page_icon)
        layout.addWidget(self.title)
        layout.addSpacing(6)
        layout.addWidget(badge)
        layout.addStretch()
        layout.addWidget(avatar)
        layout.addLayout(user_box)

        outer.addLayout(layout)

    def set_title(self, title, page_key="dashboard"):
        self.title.setText(title)
        self.page_icon.setPixmap(
            make_vector_pixmap(page_key, 32, BRAND_BLUE, BRAND_CYAN, BRAND_CYAN_LIGHT)
        )


class DashboardPage(QWidget):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.state.updated.connect(
            self.refresh
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        layout.addLayout(
            make_section_header(
                "dashboard",
                "Resumen del negocio",
                "Estado actual de ventas, productos, operaciones e inventario en tiempo real"
            )
        )

        cards = QGridLayout()
        cards.setSpacing(16)

        self.sales_card = StatCard(
            "Ventas de hoy",
            "$0.00",
            "Ingresos registrados hoy",
            icon_name="cash",
            variant="blue"
        )

        self.operations_card = StatCard(
            "Operaciones",
            "0",
            "Tickets cobrados hoy",
            icon_name="ventas",
            variant="cyan"
        )

        self.products_card = StatCard(
            "Productos",
            "0",
            "Productos activos en catálogo",
            icon_name="productos",
            variant="blue"
        )

        self.low_card = StatCard(
            "Stock bajo",
            "0",
            "Requieren reabastecimiento",
            icon_name="alert",
            variant="alert"
        )

        cards.addWidget(self.sales_card, 0, 0)
        cards.addWidget(self.operations_card, 0, 1)
        cards.addWidget(self.products_card, 0, 2)
        cards.addWidget(self.low_card, 0, 3)

        layout.addLayout(cards)

        content = QHBoxLayout()
        content.setSpacing(18)

        low_card = QFrame()
        low_card.setObjectName("card")

        low_layout = QVBoxLayout(low_card)
        low_layout.setContentsMargins(20, 18, 20, 20)
        low_layout.setSpacing(12)

        low_title = QLabel("⚠  Productos con stock bajo")
        low_title.setObjectName("cardTitle")

        self.low_table = QTableWidget()

        setup_table(
            self.low_table,
            [
                "Producto",
                "Stock",
                "Mínimo"
            ]
        )

        low_layout.addWidget(low_title)
        low_layout.addWidget(self.low_table)

        recent_card = QFrame()
        recent_card.setObjectName("card")

        recent_layout = QVBoxLayout(recent_card)
        recent_layout.setContentsMargins(20, 18, 20, 20)
        recent_layout.setSpacing(12)

        recent_title = QLabel("🧾  Ventas recientes")
        recent_title.setObjectName("cardTitle")

        self.recent_table = QTableWidget()

        setup_table(
            self.recent_table,
            [
                "Folio",
                "Fecha",
                "Productos",
                "Total"
            ]
        )

        recent_layout.addWidget(recent_title)
        recent_layout.addWidget(self.recent_table)

        content.addWidget(low_card, 1)
        content.addWidget(recent_card, 2)

        layout.addLayout(content)

        self.refresh()

    def refresh(self):
        today = datetime.now().date()

        today_sales = [
            sale
            for sale in self.state.sales
            if sale["fecha"].date() == today
        ]

        total = sum(
            sale["total"]
            for sale in today_sales
        )

        low = [
            product
            for product in self.state.products
            if product["stock"] <= product["minimo"]
        ]

        self.sales_card.set_value(f"${total:,.2f}")
        self.operations_card.set_value(str(len(today_sales)))
        self.products_card.set_value(str(len(self.state.products)))
        self.low_card.set_value(str(len(low)))

        fill_table(
            self.low_table,
            [
                [
                    product["nombre"],
                    product["stock"],
                    product["minimo"]
                ]
                for product in low
            ]
        )

        recent = list(
            reversed(
                self.state.sales[-6:]
            )
        )

        fill_table(
            self.recent_table,
            [
                [
                    sale["folio"],
                    sale["fecha"].strftime("%d/%m/%Y %H:%M"),
                    sale["productos"],
                    f"${sale['total']:,.2f}"
                ]
                for sale in recent
            ]
        )


class VentasPage(QWidget):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.cart = []

        self.state.updated.connect(
            self.load_products
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        layout.addLayout(
            make_section_header(
                "ventas",
                "Nueva venta · Punto de Venta",
                "Registra productos en el carrito y actualiza el inventario automáticamente"
            )
        )

        entry = QFrame()
        entry.setObjectName("card")

        entry_layout = QHBoxLayout(entry)
        entry_layout.setContentsMargins(20, 16, 20, 16)
        entry_layout.setSpacing(12)

        self.product_combo = QComboBox()
        self.product_combo.currentIndexChanged.connect(
            self.update_stock
        )

        self.quantity = QSpinBox()
        self.quantity.setRange(1, 99999)

        self.stock_label = QLabel("Stock: 0")
        self.stock_label.setObjectName("stockOk")

        add_button = QPushButton("Agregar al carrito")
        add_button.setObjectName("primaryButton")
        add_button.setIcon(QIcon(make_vector_pixmap("plus", 18, "#ffffff", "#ffffff")))
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.clicked.connect(self.add_item)

        entry_layout.addWidget(QLabel("Producto:"))
        entry_layout.addWidget(self.product_combo, 3)
        entry_layout.addWidget(QLabel("Cantidad:"))
        entry_layout.addWidget(self.quantity)
        entry_layout.addWidget(self.stock_label)
        entry_layout.addWidget(add_button)

        layout.addWidget(entry)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 20)
        card_layout.setSpacing(14)

        self.table = QTableWidget()

        setup_table(
            self.table,
            [
                "Producto",
                "Cantidad",
                "Precio",
                "Subtotal",
                "Stock"
            ]
        )

        bottom = QHBoxLayout()

        remove = QPushButton("Quitar seleccionado")
        remove.setObjectName("secondaryButton")
        remove.setIcon(QIcon(make_vector_pixmap("remove", 18, BRAND_BLUE, BRAND_CYAN)))
        remove.setCursor(Qt.PointingHandCursor)
        remove.clicked.connect(self.remove_item)

        self.total_label = QLabel("Total: $0.00")
        self.total_label.setObjectName("saleTotal")

        finish = QPushButton("Finalizar venta")
        finish.setObjectName("primaryButton")
        finish.setIcon(QIcon(make_vector_pixmap("check", 18, "#ffffff", "#ffffff")))
        finish.setCursor(Qt.PointingHandCursor)
        finish.clicked.connect(self.finish_sale)

        bottom.addWidget(remove)
        bottom.addStretch()
        bottom.addWidget(self.total_label)
        bottom.addSpacing(8)
        bottom.addWidget(finish)

        card_layout.addWidget(self.table)
        card_layout.addLayout(bottom)

        layout.addWidget(card)

        self.load_products()

    def load_products(self):
        current = self.product_combo.currentData()

        self.product_combo.blockSignals(True)
        self.product_combo.clear()

        for product in self.state.products:
            self.product_combo.addItem(
                f"{product['nombre']} - ${product['precio']:.2f}",
                product["id"]
            )

        if current is not None:
            index = self.product_combo.findData(current)
            if index >= 0:
                self.product_combo.setCurrentIndex(index)

        self.product_combo.blockSignals(False)

        self.update_stock()
        self.refresh_cart()

    def update_stock(self):
        product = self.state.get_product(
            self.product_combo.currentData()
        )

        if not product:
            self.stock_label.setText("Stock: 0")
            return

        self.stock_label.setText(f"Stock: {product['stock']}")

        self.stock_label.setObjectName(
            "stockLow"
            if product["stock"] <= product["minimo"]
            else "stockOk"
        )

        self.stock_label.style().unpolish(self.stock_label)
        self.stock_label.style().polish(self.stock_label)

        self.quantity.setMaximum(max(product["stock"], 1))

    def add_item(self):
        product = self.state.get_product(
            self.product_combo.currentData()
        )

        if not product:
            return

        quantity = self.quantity.value()

        existing = next(
            (
                item
                for item in self.cart
                if item["product_id"] == product["id"]
            ),
            None
        )

        current = existing["cantidad"] if existing else 0

        if current + quantity > product["stock"]:
            QMessageBox.warning(
                self,
                "Stock insuficiente",
                "La cantidad supera el stock disponible."
            )
            return

        if existing:
            existing["cantidad"] += quantity
        else:
            self.cart.append(
                {
                    "product_id": product["id"],
                    "cantidad": quantity
                }
            )

        self.refresh_cart()

    def refresh_cart(self):
        rows = []
        total = 0

        for item in self.cart:
            product = self.state.get_product(item["product_id"])
            if not product:
                continue

            subtotal = product["precio"] * item["cantidad"]
            total += subtotal

            rows.append(
                [
                    product["nombre"],
                    item["cantidad"],
                    f"${product['precio']:.2f}",
                    f"${subtotal:.2f}",
                    product["stock"]
                ]
            )

        fill_table(self.table, rows)
        self.total_label.setText(f"Total: ${total:,.2f}")

    def remove_item(self):
        row = self.table.currentRow()
        if row >= 0:
            self.cart.pop(row)
            self.refresh_cart()

    def finish_sale(self):
        if not self.cart:
            QMessageBox.warning(
                self,
                "Venta vacía",
                "Agrega al menos un producto."
            )
            return

        success, result = self.state.sell(self.cart)

        if not success:
            QMessageBox.warning(self, "Error", result)
            return

        QMessageBox.information(
            self,
            "Venta registrada",
            f"Venta realizada correctamente.\nTotal cobrado: ${result:,.2f}"
        )

        self.cart = []
        self.refresh_cart()


class ProductDialog(QDialog):
    def __init__(self, product=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Producto · PymeSync")
        self.setWindowIcon(make_app_icon())
        self.setMinimumWidth(440)

        form = QFormLayout(self)
        form.setContentsMargins(24, 24, 24, 24)
        form.setSpacing(12)

        self.codigo = QLineEdit(product["codigo"] if product else "")
        self.nombre = QLineEdit(product["nombre"] if product else "")
        self.categoria = QLineEdit(product["categoria"] if product else "")

        self.costo = QDoubleSpinBox()
        self.costo.setRange(0, 999999)
        self.costo.setDecimals(2)
        self.costo.setValue(product["costo"] if product else 0)

        self.precio = QDoubleSpinBox()
        self.precio.setRange(0, 999999)
        self.precio.setDecimals(2)
        self.precio.setValue(product["precio"] if product else 0)

        self.stock = QSpinBox()
        self.stock.setRange(0, 999999)
        self.stock.setValue(product["stock"] if product else 0)

        self.minimo = QSpinBox()
        self.minimo.setRange(0, 999999)
        self.minimo.setValue(product["minimo"] if product else 0)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        save_btn = buttons.button(QDialogButtonBox.Save)
        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
        if save_btn:
            save_btn.setText("Guardar")
            save_btn.setObjectName("primaryButton")
        if cancel_btn:
            cancel_btn.setText("Cancelar")
            cancel_btn.setObjectName("secondaryButton")

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        form.addRow("Código:", self.codigo)
        form.addRow("Nombre:", self.nombre)
        form.addRow("Categoría:", self.categoria)
        form.addRow("Costo ($):", self.costo)
        form.addRow("Precio ($):", self.precio)
        form.addRow("Stock actual:", self.stock)
        form.addRow("Stock mínimo:", self.minimo)
        form.addRow(buttons)

    def data(self):
        return {
            "codigo": self.codigo.text().strip(),
            "nombre": self.nombre.text().strip(),
            "categoria": self.categoria.text().strip(),
            "costo": self.costo.value(),
            "precio": self.precio.value(),
            "stock": self.stock.value(),
            "minimo": self.minimo.value()
        }


class ProductosPage(QWidget):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.state.updated.connect(self.refresh)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        header = QHBoxLayout()
        header.addLayout(
            make_section_header(
                "productos",
                "Catálogo de Productos",
                "Administra catálogo, códigos de barras, costos, precios y existencias"
            )
        )

        add = QPushButton("Agregar producto")
        add.setObjectName("primaryButton")
        add.setIcon(QIcon(make_vector_pixmap("plus", 18, "#ffffff", "#ffffff")))
        add.setCursor(Qt.PointingHandCursor)
        add.clicked.connect(self.add_product)

        header.addWidget(add)
        layout.addLayout(header)

        tools = QFrame()
        tools.setObjectName("card")

        tools_layout = QHBoxLayout(tools)
        tools_layout.setContentsMargins(18, 14, 18, 14)
        tools_layout.setSpacing(12)

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "🔍  Buscar por nombre, código de barras o categoría..."
        )
        self.search.textChanged.connect(self.refresh)

        edit = QPushButton("Editar seleccionado")
        edit.setObjectName("secondaryButton")
        edit.setIcon(QIcon(make_vector_pixmap("edit", 18, BRAND_BLUE, BRAND_CYAN)))
        edit.setCursor(Qt.PointingHandCursor)
        edit.clicked.connect(self.edit_product)

        tools_layout.addWidget(self.search, 1)
        tools_layout.addWidget(edit)

        layout.addWidget(tools)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 20)

        self.table = QTableWidget()

        setup_table(
            self.table,
            [
                "Código",
                "Producto",
                "Categoría",
                "Costo",
                "Precio",
                "Stock",
                "Mínimo"
            ]
        )

        card_layout.addWidget(self.table)
        layout.addWidget(card)

        self.refresh()

    def visible_products(self):
        text = self.search.text().strip().lower()

        return [
            product
            for product in self.state.products
            if (
                text in product["nombre"].lower()
                or text in product["codigo"].lower()
                or text in product["categoria"].lower()
            )
        ]

    def refresh(self):
        if not hasattr(self, "table"):
            return

        products = self.visible_products()
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            values = [
                product["codigo"],
                product["nombre"],
                product["categoria"],
                f"${product['costo']:.2f}",
                f"${product['precio']:.2f}",
                product["stock"],
                product["minimo"]
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setData(Qt.UserRole, product["id"])
                style_table_item(item, value)
                if col == 5 and product["stock"] <= product["minimo"]:
                    item.setForeground(QColor("#d97706"))
                    f = item.font()
                    f.setBold(True)
                    item.setFont(f)
                self.table.setItem(row, col, item)

    def add_product(self):
        dialog = ProductDialog(parent=self)

        if dialog.exec() == QDialog.Accepted:
            data = dialog.data()

            if not data["nombre"]:
                QMessageBox.warning(
                    self,
                    "Datos incompletos",
                    "Ingresa el nombre del producto."
                )
                return

            self.state.add_product(data)

    def edit_product(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Selección requerida",
                "Selecciona un producto de la tabla para editarlo."
            )
            return

        product_id = self.table.item(row, 0).data(Qt.UserRole)
        product = self.state.get_product(product_id)

        dialog = ProductDialog(product, self)

        if dialog.exec() == QDialog.Accepted:
            self.state.update_product(product_id, dialog.data())


class InventarioPage(QWidget):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.state.updated.connect(self.refresh)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        layout.addLayout(
            make_section_header(
                "inventario",
                "Control de Inventario",
                "Consulta niveles de stock y registra entradas de mercancía"
            )
        )

        entry = QFrame()
        entry.setObjectName("card")

        entry_layout = QHBoxLayout(entry)
        entry_layout.setContentsMargins(20, 16, 20, 16)
        entry_layout.setSpacing(12)

        self.combo = QComboBox()

        self.quantity = QSpinBox()
        self.quantity.setRange(1, 999999)

        button = QPushButton("Registrar entrada")
        button.setObjectName("primaryButton")
        button.setIcon(QIcon(make_vector_pixmap("plus", 18, "#ffffff", "#ffffff")))
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.add_stock)

        entry_layout.addWidget(QLabel("Producto:"))
        entry_layout.addWidget(self.combo, 3)
        entry_layout.addWidget(QLabel("Cantidad a ingresar:"))
        entry_layout.addWidget(self.quantity)
        entry_layout.addWidget(button)

        layout.addWidget(entry)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 20)

        self.table = QTableWidget()

        setup_table(
            self.table,
            [
                "Producto",
                "Categoría",
                "Stock actual",
                "Stock mínimo",
                "Precio",
                "Estado"
            ]
        )

        card_layout.addWidget(self.table)
        layout.addWidget(card)

        self.refresh()

    def refresh(self):
        current = (
            self.combo.currentData()
            if hasattr(self, "combo")
            else None
        )

        self.combo.blockSignals(True)
        self.combo.clear()

        for product in self.state.products:
            self.combo.addItem(product["nombre"], product["id"])

        if current is not None:
            index = self.combo.findData(current)
            if index >= 0:
                self.combo.setCurrentIndex(index)

        self.combo.blockSignals(False)

        rows = []

        for product in self.state.products:
            if product["stock"] == 0:
                status = "Agotado"
            elif product["stock"] <= product["minimo"]:
                status = "Stock bajo"
            else:
                status = "Disponible"

            rows.append(
                [
                    product["nombre"],
                    product["categoria"],
                    product["stock"],
                    product["minimo"],
                    f"${product['precio']:.2f}",
                    status
                ]
            )

        fill_table(self.table, rows)

    def add_stock(self):
        if self.state.add_stock(
            self.combo.currentData(),
            self.quantity.value()
        ):
            QMessageBox.information(
                self,
                "Inventario actualizado",
                "La entrada de mercancía fue registrada correctamente."
            )


class MovimientosPage(QWidget):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.state.updated.connect(self.refresh)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        layout.addLayout(
            make_section_header(
                "movimientos",
                "Movimientos de Mercancía",
                "Historial sincronizado de entradas, ventas y ajustes de inventario"
            )
        )

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 20)

        self.table = QTableWidget()

        setup_table(
            self.table,
            [
                "Fecha",
                "Tipo",
                "Producto",
                "Cantidad",
                "Detalle"
            ]
        )

        card_layout.addWidget(self.table)
        layout.addWidget(card)

        self.refresh()

    def refresh(self):
        fill_table(
            self.table,
            [
                [
                    movement["fecha"],
                    movement["tipo"],
                    movement["producto"],
                    movement["cantidad"],
                    movement["detalle"]
                ]
                for movement in self.state.movements
            ]
        )


class ProveedoresPage(QWidget):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.state.updated.connect(self.refresh)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        header = QHBoxLayout()
        header.addLayout(
            make_section_header(
                "proveedores",
                "Directorio de Proveedores",
                "Administra contactos, teléfonos y surtidores de tu tienda"
            )
        )

        add = QPushButton("Agregar proveedor")
        add.setObjectName("primaryButton")
        add.setIcon(QIcon(make_vector_pixmap("plus", 18, "#ffffff", "#ffffff")))
        add.setCursor(Qt.PointingHandCursor)
        add.clicked.connect(self.add_provider)

        header.addWidget(add)
        layout.addLayout(header)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 20)

        self.table = QTableWidget()

        setup_table(
            self.table,
            [
                "Proveedor",
                "Contacto",
                "Teléfono",
                "Productos que surte"
            ]
        )

        card_layout.addWidget(self.table)
        layout.addWidget(card)

        self.refresh()

    def refresh(self):
        fill_table(
            self.table,
            [
                [
                    provider["nombre"],
                    provider["contacto"],
                    provider["telefono"],
                    provider["productos"]
                ]
                for provider in self.state.providers
            ]
        )

    def add_provider(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo proveedor · PymeSync")
        dialog.setWindowIcon(make_app_icon())
        dialog.setMinimumWidth(420)

        form = QFormLayout(dialog)
        form.setContentsMargins(24, 24, 24, 24)
        form.setSpacing(12)

        name = QLineEdit()
        contact = QLineEdit()
        phone = QLineEdit()
        products = QLineEdit()

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        save_btn = buttons.button(QDialogButtonBox.Save)
        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
        if save_btn:
            save_btn.setText("Guardar")
            save_btn.setObjectName("primaryButton")
        if cancel_btn:
            cancel_btn.setText("Cancelar")
            cancel_btn.setObjectName("secondaryButton")

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        form.addRow("Proveedor:", name)
        form.addRow("Contacto:", contact)
        form.addRow("Teléfono:", phone)
        form.addRow("Productos:", products)
        form.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            self.state.add_provider(
                {
                    "nombre": name.text().strip(),
                    "contacto": contact.text().strip(),
                    "telefono": phone.text().strip(),
                    "productos": products.text().strip()
                }
            )


class ReportesPage(QWidget):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.state.updated.connect(self.refresh)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        layout.addLayout(
            make_section_header(
                "reportes",
                "Reportes Financieros y de Ventas",
                "Consulta ingresos acumulados, ticket promedio e historial detallado"
            )
        )

        cards = QGridLayout()
        cards.setSpacing(16)

        self.income = StatCard(
            "Ingresos acumulados",
            "$0.00",
            "Total histórico de ventas",
            icon_name="cash",
            variant="blue"
        )

        self.sales_count = StatCard(
            "Ventas registradas",
            "0",
            "Tickets emitidos",
            icon_name="ventas",
            variant="cyan"
        )

        self.average = StatCard(
            "Ticket promedio",
            "$0.00",
            "Promedio por operación",
            icon_name="reportes",
            variant="blue"
        )

        self.inventory_value = StatCard(
            "Valor de inventario",
            "$0.00",
            "Capital en mercancía (al costo)",
            icon_name="inventario",
            variant="cyan"
        )

        cards.addWidget(self.income, 0, 0)
        cards.addWidget(self.sales_count, 0, 1)
        cards.addWidget(self.average, 0, 2)
        cards.addWidget(self.inventory_value, 0, 3)

        layout.addLayout(cards)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 20)

        self.table = QTableWidget()

        setup_table(
            self.table,
            [
                "Folio",
                "Fecha",
                "Productos",
                "Total"
            ]
        )

        card_layout.addWidget(self.table)
        layout.addWidget(card)

        self.refresh()

    def refresh(self):
        total = sum(
            sale["total"]
            for sale in self.state.sales
        )

        count = len(self.state.sales)
        average = total / count if count else 0

        inventory = sum(
            product["costo"] * product["stock"]
            for product in self.state.products
        )

        self.income.set_value(f"${total:,.2f}")
        self.sales_count.set_value(str(count))
        self.average.set_value(f"${average:,.2f}")
        self.inventory_value.set_value(f"${inventory:,.2f}")

        sales = list(reversed(self.state.sales))

        fill_table(
            self.table,
            [
                [
                    sale["folio"],
                    sale["fecha"].strftime("%d/%m/%Y %H:%M"),
                    sale["productos"],
                    f"${sale['total']:,.2f}"
                ]
                for sale in sales
            ]
        )


class AdminPage(QWidget):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.state.updated.connect(self.refresh)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        header = QHBoxLayout()
        header.addLayout(
            make_section_header(
                "admin",
                "Administración de Usuarios",
                "Gestiona el personal, cajeros y permisos de acceso al sistema"
            )
        )

        add = QPushButton("Nuevo usuario")
        add.setObjectName("primaryButton")
        add.setIcon(QIcon(make_vector_pixmap("plus", 18, "#ffffff", "#ffffff")))
        add.setCursor(Qt.PointingHandCursor)
        add.clicked.connect(self.add_user)

        header.addWidget(add)
        layout.addLayout(header)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 20)

        self.table = QTableWidget()

        setup_table(
            self.table,
            [
                "Nombre",
                "Usuario",
                "Rol",
                "Estado"
            ]
        )

        card_layout.addWidget(self.table)
        layout.addWidget(card)

        self.refresh()

    def refresh(self):
        fill_table(
            self.table,
            [
                [
                    user["nombre"],
                    user["usuario"],
                    user["rol"],
                    user["estado"]
                ]
                for user in self.state.users
            ]
        )

    def add_user(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo usuario · PymeSync")
        dialog.setWindowIcon(make_app_icon())
        dialog.setMinimumWidth(420)

        form = QFormLayout(dialog)
        form.setContentsMargins(24, 24, 24, 24)
        form.setSpacing(12)

        name = QLineEdit()
        username = QLineEdit()

        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)

        role = QComboBox()
        role.addItems(
            [
                "Administrador",
                "Cajero",
                "Encargado"
            ]
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        save_btn = buttons.button(QDialogButtonBox.Save)
        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
        if save_btn:
            save_btn.setText("Guardar")
            save_btn.setObjectName("primaryButton")
        if cancel_btn:
            cancel_btn.setText("Cancelar")
            cancel_btn.setObjectName("secondaryButton")

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        form.addRow("Nombre:", name)
        form.addRow("Usuario:", username)
        form.addRow("Contraseña:", password)
        form.addRow("Rol:", role)
        form.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            if (
                not name.text().strip()
                or not username.text().strip()
                or not password.text()
            ):
                QMessageBox.warning(
                    self,
                    "Datos incompletos",
                    "Completa todos los datos."
                )
                return

            self.state.add_user(
                {
                    "nombre": name.text().strip(),
                    "usuario": username.text().strip(),
                    "rol": role.currentText(),
                    "estado": "Activo"
                }
            )


class ConfiguracionPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(18)

        layout.addLayout(
            make_section_header(
                "configuracion",
                "Configuración del Negocio",
                "Datos generales de tu tienda y preferencias de PymeSync"
            )
        )

        card = QFrame()
        card.setObjectName("card")
        card.setMaximumWidth(680)

        form = QFormLayout(card)
        form.setContentsMargins(28, 28, 28, 28)
        form.setSpacing(16)

        logo_preview = QLabel()
        logo_preview.setPixmap(load_clean_horizontal_logo(210, 46))

        self.store_name = QLineEdit("Mi Tiendita · PymeSync")
        self.owner = QLineEdit("Propietario")
        self.phone = QLineEdit("449 000 0000")

        self.currency = QComboBox()
        self.currency.addItems(
            [
                "MXN - Peso mexicano",
                "USD - Dólar"
            ]
        )

        save = QPushButton("Guardar configuración")
        save.setObjectName("primaryButton")
        save.setIcon(QIcon(make_vector_pixmap("check", 18, "#ffffff", "#ffffff")))
        save.setCursor(Qt.PointingHandCursor)
        save.clicked.connect(self.save)

        form.addRow("Identidad corporativa:", logo_preview)
        form.addRow("Nombre de la tienda:", self.store_name)
        form.addRow("Propietario:", self.owner)
        form.addRow("Teléfono / WhatsApp:", self.phone)
        form.addRow("Moneda:", self.currency)
        form.addRow(save)

        layout.addWidget(card)
        layout.addStretch()

    def save(self):
        QMessageBox.information(
            self,
            "Configuración guardada",
            "La configuración de PymeSync fue guardada correctamente."
        )


class MainWindow(QMainWindow):
    def __init__(self, state, user):
        super().__init__()

        self.setWindowTitle(
            "PymeSync · El control total de tu negocio, sin complicaciones"
        )
        self.setWindowIcon(make_app_icon())

        self.resize(1400, 850)
        self.setMinimumSize(1100, 700)

        central = QWidget()
        central.setObjectName("mainContent")
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar()

        content = QWidget()
        content.setObjectName("pageRoot")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.topbar = Topbar(user)
        self.stack = QStackedWidget()

        self.pages = {
            "dashboard": DashboardPage(state),
            "ventas": VentasPage(state),
            "productos": ProductosPage(state),
            "inventario": InventarioPage(state),
            "movimientos": MovimientosPage(state),
            "proveedores": ProveedoresPage(state),
            "reportes": ReportesPage(state),
            "admin": AdminPage(state),
            "configuracion": ConfiguracionPage()
        }

        self.titles = {
            "dashboard": "Inicio",
            "ventas": "Ventas",
            "productos": "Productos",
            "inventario": "Inventario",
            "movimientos": "Movimientos",
            "proveedores": "Proveedores",
            "reportes": "Reportes",
            "admin": "Administración",
            "configuracion": "Configuración"
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        content_layout.addWidget(self.topbar)
        content_layout.addWidget(self.stack)

        root.addWidget(self.sidebar)
        root.addWidget(content, 1)

        self.sidebar.page_changed.connect(self.change_page)
        self.sidebar.select_page("dashboard")

    def change_page(self, page):
        widget = self.pages.get(page)

        if widget:
            self.stack.setCurrentWidget(widget)
            self.topbar.set_title(
                self.titles.get(page, "PymeSync"),
                page
            )


app = QApplication(sys.argv)
app.setWindowIcon(make_app_icon())
app.setStyleSheet(STYLE)

state = StoreState()
login = LoginWindow()
main_window = None


def open_system(user):
    global main_window

    main_window = MainWindow(state, user)
    main_window.showMaximized()
    login.close()


login.login_success.connect(open_system)

if "--autologin" in sys.argv:
    open_system("Administrador")
else:
    login.show()

sys.exit(app.exec())
