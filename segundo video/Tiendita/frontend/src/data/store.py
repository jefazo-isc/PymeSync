from datetime import datetime, timedelta

from PySide6.QtCore import QObject, Signal


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

        hoy = datetime.now()

        self.sales = [
            {
                "folio": "V-1001",
                "fecha": hoy - timedelta(days=6),
                "productos": 8,
                "total": 420.00
            },
            {
                "folio": "V-1002",
                "fecha": hoy - timedelta(days=5),
                "productos": 14,
                "total": 790.00
            },
            {
                "folio": "V-1003",
                "fecha": hoy - timedelta(days=4),
                "productos": 10,
                "total": 560.00
            },
            {
                "folio": "V-1004",
                "fecha": hoy - timedelta(days=3),
                "productos": 18,
                "total": 940.00
            },
            {
                "folio": "V-1005",
                "fecha": hoy - timedelta(days=2),
                "productos": 12,
                "total": 655.00
            },
            {
                "folio": "V-1006",
                "fecha": hoy - timedelta(days=1),
                "productos": 21,
                "total": 1180.00
            },
            {
                "folio": "V-1007",
                "fecha": hoy,
                "productos": 9,
                "total": 510.00
            }
        ]

        self.movements = [
            {
                "fecha": hoy.strftime("%d/%m/%Y %H:%M"),
                "tipo": "Entrada",
                "producto": "Coca-Cola 600 ml",
                "cantidad": 24,
                "detalle": "Recepcion de proveedor"
            },
            {
                "fecha": hoy.strftime("%d/%m/%Y %H:%M"),
                "tipo": "Venta",
                "producto": "Sabritas Original 45 g",
                "cantidad": -3,
                "detalle": "Venta registrada"
            },
            {
                "fecha": (hoy - timedelta(days=1)).strftime("%d/%m/%Y %H:%M"),
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

    def sell(self, cart):
        for item in cart:
            product = self.get_product(item["product_id"])

            if product is None:
                return False, "Producto no encontrado"

            if item["cantidad"] > product["stock"]:
                return False, f"Stock insuficiente para {product['nombre']}"

        total = 0
        cantidad_total = 0

        for item in cart:
            product = self.get_product(item["product_id"])

            product["stock"] -= item["cantidad"]

            subtotal = item["cantidad"] * product["precio"]

            total += subtotal
            cantidad_total += item["cantidad"]

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
                "productos": cantidad_total,
                "total": total
            }
        )

        self.updated.emit()

        return True, total

    def add_stock(self, product_id, cantidad):
        product = self.get_product(product_id)

        if product is None:
            return

        product["stock"] += cantidad

        self.movements.insert(
            0,
            {
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tipo": "Entrada",
                "producto": product["nombre"],
                "cantidad": cantidad,
                "detalle": "Entrada de inventario"
            }
        )

        self.updated.emit()

    def add_product(self, product):
        product["id"] = max(
            [product["id"] for product in self.products],
            default=0
        ) + 1

        self.products.append(product)

        self.updated.emit()

    def update_price(self, product_id, costo, precio):
        product = self.get_product(product_id)

        if product is None:
            return

        product["costo"] = costo
        product["precio"] = precio

        self.updated.emit()

    def add_provider(self, provider):
        self.providers.append(provider)
        self.updated.emit()

    def add_user(self, user):
        self.users.append(user)
        self.updated.emit()