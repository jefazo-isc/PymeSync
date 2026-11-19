# PymeSync · «El control total de tu negocio, sin complicaciones»

**Eslogan:** *«Tu tiendita, bien chidita»*  
**Equipo 3 · Universidad Autónoma de Aguascalientes (UAA)**

Plataforma de gestión comercial diseñada específicamente para tiendas de abarrotes y micronegocios. Incluye tanto la **Web App interactiva** (lista para GitHub Pages o servidor local) como la **aplicación de escritorio en Python (PySide6)**, ambas unificadas bajo la identidad corporativa oficial de **PymeSync** (`#0e498c` Azul Zafiro y `#14b6c4` Turquesa Eléctrico).

---

## 🌐 1. Usar la Web App (`index.html`)

La Web App funciona 100% en el navegador con persistencia local (`localStorage`) y sin requerir conexión a internet ni base de datos externa:

- **En GitHub Pages:** Activa GitHub Pages en la rama `main` (carpeta raíz `/`) y abre `https://jefazo-isc.github.io/PymeSync/`.
- **En tu computadora:** Puedes abrir `index.html` o levantar un servidor local rápido:
  ```bash
  python3 -m http.server 8000
  ```
  Y visitar `http://localhost:8000`.

### Módulos incluidos en la Web App
1. **Inicio (Dashboard):** KPIs del día (`Ventas de hoy`, `Operaciones`, `Productos`, `Stock bajo`), alertas de stock mínimo y ventas recientes.
2. **Ventas (Punto de Venta):** Selección de producto, validación de stock en tiempo real, carrito de compras y cobro automático con folio y descuento de inventario.
3. **Productos:** Catálogo completo con buscador en tiempo real por nombre, código o categoría, y modales para agregar y editar productos.
4. **Inventario:** Registro de entradas de mercancía y estados semánticos (`Disponible`, `Stock bajo`, `Agotado`).
5. **Movimientos:** Historial sincronizado de entradas, ventas y ajustes.
6. **Proveedores:** Directorio de surtidores y registro de nuevos proveedores.
7. **Reportes:** Ingresos acumulados, ventas registradas, ticket promedio y valor total del inventario al costo.
8. **Administración:** Gestión de usuarios y roles (`Administrador`, `Cajero`, `Encargado`).
9. **Configuración:** Datos generales de la tienda y restauración de datos demo.
10. **Business Model Canvas:** Disponible en [`pymesync_canvas.html`](pymesync_canvas.html).

---

## 🖥️ 2. Ejecutar la Desktop App en Python (PySide6)

Para ejecutar la aplicación de escritorio:

```bash
./run_app.sh
```
O directamente con Python:
```bash
python3 pymesync_app.py
```

Para entrar directamente al sistema sin pasar por el login:
```bash
./run_app.sh --autologin
```

---

## 🔐 Credenciales de Acceso Demo

- **Usuario:** `admin`
- **Contraseña:** `admin123`
*(También puedes hacer clic en el botón **Acceso Demo** en la pantalla de inicio de sesión para autocompletar las credenciales).*
