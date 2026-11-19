from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget
)

from components.navbar.topbar import Topbar
from components.sidebar.sidebar import Sidebar
from pages.admin.admin import AdminPage
from pages.configuracion.configuracion import ConfiguracionPage
from pages.dashboard.dashboard import DashboardPage
from pages.inventario.inventario import InventarioPage
from pages.movimientos.movimientos import MovimientosPage
from pages.productos.productos import ProductosPage
from pages.proveedores.proveedores import ProveedoresPage
from pages.reportes.reportes import ReportesPage
from pages.ventas.ventas import VentasPage


class MainWindow(QMainWindow):
    def __init__(self, state, user):
        super().__init__()

        self.setWindowTitle("Tiendita")
        self.resize(1400, 850)
        self.setMinimumSize(1100, 700)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar()

        content = QWidget()
        content.setObjectName("mainContent")

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
            "admin": "Administracion",
            "configuracion": "Configuracion"
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        content_layout.addWidget(self.topbar)
        content_layout.addWidget(self.stack)

        root.addWidget(self.sidebar)
        root.addWidget(content, 1)

        self.sidebar.page_changed.connect(self.change_page)

        self.change_page("dashboard")

    def change_page(self, page):
        widget = self.pages.get(page)

        if widget:
            self.stack.setCurrentWidget(widget)
            self.topbar.set_title(self.titles.get(page, "Tiendita"))