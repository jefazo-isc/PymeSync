<?php
declare(strict_types=1);

class Database
{
    private static ?PDO $instance = null;

    public static function dbPath(): string
    {
        return dirname(__DIR__) . '/data/pymesync.sqlite';
    }

    public static function connect(): PDO
    {
        if (self::$instance !== null) {
            return self::$instance;
        }

        $dbFile = self::dbPath();
        $dataDir = dirname($dbFile);
        if (!is_dir($dataDir) && !mkdir($dataDir, 0775, true) && !is_dir($dataDir)) {
            throw new RuntimeException("No se pudo crear el directorio de base de datos: {$dataDir}");
        }

        $pdo = new PDO('sqlite:' . $dbFile);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        $pdo->exec('PRAGMA foreign_keys = ON;');

        self::initSchemaAndSeed($pdo);
        self::$instance = $pdo;

        return self::$instance;
    }

    public static function initSchemaAndSeed(PDO $pdo): void
    {
        $pdo->exec("
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL DEFAULT '',
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL DEFAULT 'General',
                costo REAL NOT NULL DEFAULT 0,
                precio REAL NOT NULL DEFAULT 0,
                stock INTEGER NOT NULL DEFAULT 0,
                minimo INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folio TEXT NOT NULL,
                fecha TEXT NOT NULL,
                productos INTEGER NOT NULL DEFAULT 0,
                total REAL NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL DEFAULT 0,
                detalle TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS providers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                contacto TEXT NOT NULL DEFAULT '',
                telefono TEXT NOT NULL DEFAULT '',
                productos TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'Cajero',
                estado TEXT NOT NULL DEFAULT 'Activo'
            );

            CREATE TABLE IF NOT EXISTS config (
                clave TEXT PRIMARY KEY,
                valor TEXT NOT NULL DEFAULT ''
            );
        ");

        $productCount = (int) $pdo->query('SELECT COUNT(*) FROM products')->fetchColumn();
        $userCount = (int) $pdo->query('SELECT COUNT(*) FROM users')->fetchColumn();

        if ($productCount === 0 && $userCount === 0) {
            self::seed($pdo);
        }
    }

    public static function seed(PDO $pdo): void
    {
        $now = time();
        $day = 86400;

        $products = [
            ['7501055300012', 'Coca-Cola 600 ml', 'Bebidas', 14.50, 20.00, 80, 15],
            ['7500478020019', 'Sabritas Original 45 g', 'Botanas', 13.00, 18.00, 42, 10],
            ['7501000110019', 'Leche Lala 1 L', 'Lacteos', 23.50, 29.00, 28, 8],
            ['7501031310011', 'Pan Bimbo Grande', 'Panaderia', 39.00, 48.00, 19, 8],
            ['7501005100022', 'Galletas Marias', 'Abarrotes', 15.00, 21.00, 35, 10],
            ['7501025400014', 'Agua Ciel 1 L', 'Bebidas', 9.00, 14.00, 60, 15],
            ['7501000124450', 'Huevo 12 piezas', 'Abarrotes', 39.00, 49.00, 7, 10],
            ['7501011100423', 'Cafe Soluble 100 g', 'Abarrotes', 52.00, 65.00, 12, 5],
        ];

        $stmtProd = $pdo->prepare('
            INSERT INTO products (codigo, nombre, categoria, costo, precio, stock, minimo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ');
        foreach ($products as $p) {
            $stmtProd->execute($p);
        }

        $sales = [
            ['V-1001', date('c', $now - 6 * $day), 8, 420.00],
            ['V-1002', date('c', $now - 5 * $day), 14, 790.00],
            ['V-1003', date('c', $now - 4 * $day), 10, 560.00],
            ['V-1004', date('c', $now - 3 * $day), 18, 940.00],
            ['V-1005', date('c', $now - 2 * $day), 12, 655.00],
            ['V-1006', date('c', $now - 1 * $day), 21, 1180.00],
            ['V-1007', date('c', $now), 9, 510.00],
        ];

        $stmtSale = $pdo->prepare('
            INSERT INTO sales (folio, fecha, productos, total)
            VALUES (?, ?, ?, ?)
        ');
        foreach ($sales as $s) {
            $stmtSale->execute($s);
        }

        // Insertados de más antiguo a más reciente para que ORDER BY id DESC muestre Entrada primero
        $movements = [
            [date('d/m/Y H:i', $now - $day), 'Ajuste', 'Leche Lala 1 L', -2, 'Producto danado'],
            [date('d/m/Y H:i', $now), 'Venta', 'Sabritas Original 45 g', -3, 'Venta registrada'],
            [date('d/m/Y H:i', $now), 'Entrada', 'Coca-Cola 600 ml', 24, 'Recepcion de proveedor'],
        ];

        $stmtMov = $pdo->prepare('
            INSERT INTO movements (fecha, tipo, producto, cantidad, detalle)
            VALUES (?, ?, ?, ?, ?)
        ');
        foreach ($movements as $m) {
            $stmtMov->execute($m);
        }

        $providers = [
            ['Distribuidora Centro', 'Carlos Ramirez', '449 123 4567', 'Bebidas y botanas'],
            ['Abarrotes del Bajio', 'Maria Lopez', '449 222 3344', 'Abarrotes'],
            ['Lacteos del Centro', 'Jorge Hernandez', '449 555 8899', 'Lacteos'],
        ];

        $stmtProv = $pdo->prepare('
            INSERT INTO providers (nombre, contacto, telefono, productos)
            VALUES (?, ?, ?, ?)
        ');
        foreach ($providers as $pr) {
            $stmtProv->execute($pr);
        }

        $users = [
            ['Administrador', 'admin', password_hash('admin123', PASSWORD_DEFAULT), 'Administrador', 'Activo'],
            ['Caja Principal', 'caja1', password_hash('caja123', PASSWORD_DEFAULT), 'Cajero', 'Activo'],
        ];

        $stmtUser = $pdo->prepare('
            INSERT INTO users (nombre, usuario, password_hash, rol, estado)
            VALUES (?, ?, ?, ?, ?)
        ');
        foreach ($users as $u) {
            $stmtUser->execute($u);
        }

        $configs = [
            ['storeName', 'Mi Tiendita · PymeSync'],
            ['owner', 'Propietario'],
            ['phone', '449 000 0000'],
            ['currency', 'MXN - Peso mexicano'],
        ];

        $stmtCfg = $pdo->prepare('
            INSERT OR REPLACE INTO config (clave, valor)
            VALUES (?, ?)
        ');
        foreach ($configs as $c) {
            $stmtCfg->execute($c);
        }
    }

    public static function resetDemo(PDO $pdo): void
    {
        $pdo->beginTransaction();
        try {
            $pdo->exec('DELETE FROM products');
            $pdo->exec('DELETE FROM sales');
            $pdo->exec('DELETE FROM movements');
            $pdo->exec('DELETE FROM providers');
            $pdo->exec('DELETE FROM users');
            $pdo->exec('DELETE FROM config');
            $pdo->exec("DELETE FROM sqlite_sequence WHERE name IN ('products','sales','movements','providers','users')");

            self::seed($pdo);
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            throw $e;
        }
    }
}
