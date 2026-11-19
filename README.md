# PymeSync · «El control total de tu negocio, sin complicaciones»

**Eslogan:** *«Tu tiendita, bien chidita»*  
**Equipo 3 · Universidad Autónoma de Aguascalientes (UAA)**

Plataforma web de gestión comercial diseñada específicamente para tiendas de abarrotes y micronegocios, desarrollada en **PHP 8 + SQLite (PDO)** con una interfaz unificada bajo la identidad corporativa oficial de **PymeSync** (`#0e498c` Azul Zafiro y `#14b6c4` Turquesa Eléctrico).

---

## ⚙️ Arquitectura PHP + SQLite + GitHub Pages

Cada máquina que ejecuta el sistema corre su propio servidor web **PHP 8** con base de datos local **SQLite** (`data/pymesync.sqlite`), sin requerir MySQL ni dependencias externas ni conexión a internet:

- **[`index.php`](index.php):** Interfaz principal renderizada por PHP conectada directamente a SQLite.
- **[`api.php`](api.php):** API REST JSON con soporte CORS para autenticación, ventas, productos, inventario, movimientos, proveedores, usuarios y configuración.
- **[`src/Database.php`](src/Database.php):** Conexión PDO SQLite, creación automática del esquema y datos iniciales demo.
- **[`src/Auth.php`](src/Auth.php):** Manejo de sesiones PHP y autenticación con `password_verify`.
- **[`src/StoreRepository.php`](src/StoreRepository.php):** Repositorio transaccional SQLite (`beginTransaction` / `commit`) para descontar stock, generar folios y registrar movimientos.
- **[`index.html`](index.html):** Cliente estático compatible con **GitHub Pages** (`https://jefazo-isc.github.io/PymeSync/`) que se conecta automáticamente al servidor PHP local (`http://localhost:8000/api.php`) cuando está activo en la máquina.

---

## 🚀 Cómo iniciar el servidor en tu máquina

Ejecuta el script incluido:

```bash
./run_server.sh
```
*(O manualmente con `php -S 0.0.0.0:8000`)*.

Luego abre en tu navegador:
- **Servidor PHP directo:** `http://localhost:8000` (carga `index.php` + SQLite)
- **Desde GitHub Pages conectado a tu máquina:** `https://jefazo-isc.github.io/PymeSync/`

La base de datos `data/pymesync.sqlite` se crea y puebla automáticamente la primera vez que entra una petición.

---

## 📦 Módulos del Sistema

1. **Inicio (Dashboard):** KPIs del día (`Ventas de hoy`, `Operaciones`, `Productos`, `Stock bajo`), alertas de stock mínimo y ventas recientes.
2. **Ventas (Punto de Venta):** Selector de producto, validación de stock en tiempo real, carrito y cobro transaccional con folio (`V-100X`) y descuento automático en SQLite.
3. **Productos:** Catálogo completo con buscador en tiempo real por código, nombre o categoría, y modales para agregar y editar.
4. **Inventario:** Registro de entradas de mercancía y estados semánticos (`Disponible`, `Stock bajo`, `Agotado`).
5. **Movimientos:** Historial sincronizado de entradas, ventas y ajustes.
6. **Proveedores:** Directorio de surtidores y registro de nuevos proveedores.
7. **Reportes:** Ingresos acumulados, ventas registradas, ticket promedio y valor total del inventario al costo.
8. **Administración:** Gestión de usuarios con contraseñas cifradas (`password_hash`) y roles (`Administrador`, `Cajero`, `Encargado`).
9. **Configuración:** Datos generales de la tienda, estado del nodo PHP/SQLite y restauración de datos demo.
10. **Business Model Canvas:** Disponible en [`pymesync_canvas.html`](pymesync_canvas.html).

---

## 🔐 Credenciales de Acceso Demo

- **Usuario:** `admin` | **Contraseña:** `admin123` *(Rol: Administrador)*
- **Usuario:** `caja1` | **Contraseña:** `caja123` *(Rol: Cajero)*
