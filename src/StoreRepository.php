<?php
declare(strict_types=1);

class StoreRepository
{
    private PDO $db;

    public function __construct(PDO $db)
    {
        $this->db = $db;
    }

    public function getFullState(): array
    {
        $productsRaw = $this->db->query('SELECT id, codigo, nombre, categoria, costo, precio, stock, minimo FROM products ORDER BY id ASC')->fetchAll();
        $products = array_map(static function (array $row): array {
            return [
                'id' => (int) $row['id'],
                'codigo' => (string) $row['codigo'],
                'nombre' => (string) $row['nombre'],
                'categoria' => (string) $row['categoria'],
                'costo' => (float) $row['costo'],
                'precio' => (float) $row['precio'],
                'stock' => (int) $row['stock'],
                'minimo' => (int) $row['minimo'],
            ];
        }, $productsRaw);

        $salesRaw = $this->db->query('SELECT id, folio, fecha, productos, total FROM sales ORDER BY id ASC')->fetchAll();
        $sales = array_map(static function (array $row): array {
            return [
                'id' => (int) $row['id'],
                'folio' => (string) $row['folio'],
                'fecha' => (string) $row['fecha'],
                'productos' => (int) $row['productos'],
                'total' => (float) $row['total'],
            ];
        }, $salesRaw);

        $movementsRaw = $this->db->query('SELECT id, fecha, tipo, producto, cantidad, detalle FROM movements ORDER BY id DESC')->fetchAll();
        $movements = array_map(static function (array $row): array {
            return [
                'id' => (int) $row['id'],
                'fecha' => (string) $row['fecha'],
                'tipo' => (string) $row['tipo'],
                'producto' => (string) $row['producto'],
                'cantidad' => (int) $row['cantidad'],
                'detalle' => (string) $row['detalle'],
            ];
        }, $movementsRaw);

        $providers = $this->db->query('SELECT id, nombre, contacto, telefono, productos FROM providers ORDER BY id ASC')->fetchAll();
        $users = $this->db->query('SELECT id, nombre, usuario, rol, estado FROM users ORDER BY id ASC')->fetchAll();

        $configRows = $this->db->query('SELECT clave, valor FROM config')->fetchAll();
        $config = [
            'storeName' => 'Mi Tiendita · PymeSync',
            'owner' => 'Propietario',
            'phone' => '449 000 0000',
            'currency' => 'MXN - Peso mexicano',
        ];
        foreach ($configRows as $c) {
            $config[(string) $c['clave']] = (string) $c['valor'];
        }

        return [
            'products' => $products,
            'sales' => $sales,
            'movements' => $movements,
            'providers' => $providers,
            'users' => $users,
            'config' => $config,
            'server_info' => [
                'php_version' => PHP_VERSION,
                'engine' => 'PHP ' . PHP_VERSION . ' + SQLite3',
                'host' => gethostname() ?: 'localhost',
                'timestamp' => date('c'),
            ],
        ];
    }

    public function saveProduct(array $data): array
    {
        $id = isset($data['id']) ? (int) $data['id'] : 0;
        $codigo = trim((string) ($data['codigo'] ?? ''));
        $nombre = trim((string) ($data['nombre'] ?? ''));
        $categoria = trim((string) ($data['categoria'] ?? ''));
        if ($categoria === '') {
            $categoria = 'General';
        }
        $costo = max(0.0, (float) ($data['costo'] ?? 0));
        $precio = max(0.0, (float) ($data['precio'] ?? 0));
        $stock = max(0, (int) ($data['stock'] ?? 0));
        $minimo = max(0, (int) ($data['minimo'] ?? 0));

        if ($nombre === '') {
            throw new InvalidArgumentException('Ingresa el nombre del producto.');
        }

        if ($id > 0) {
            $stmt = $this->db->prepare('
                UPDATE products
                SET codigo = ?, nombre = ?, categoria = ?, costo = ?, precio = ?, stock = ?, minimo = ?
                WHERE id = ?
            ');
            $stmt->execute([$codigo, $nombre, $categoria, $costo, $precio, $stock, $minimo, $id]);
        } else {
            $stmt = $this->db->prepare('
                INSERT INTO products (codigo, nombre, categoria, costo, precio, stock, minimo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ');
            $stmt->execute([$codigo, $nombre, $categoria, $costo, $precio, $stock, $minimo]);
        }

        return $this->getFullState();
    }

    public function addStock(int $productId, int $quantity): array
    {
        if ($quantity <= 0) {
            throw new InvalidArgumentException('La cantidad debe ser mayor a cero.');
        }

        $this->db->beginTransaction();
        try {
            $stmt = $this->db->prepare('SELECT id, nombre, stock FROM products WHERE id = ? LIMIT 1');
            $stmt->execute([$productId]);
            $product = $stmt->fetch();

            if (!$product) {
                throw new RuntimeException('Producto no encontrado.');
            }

            $upd = $this->db->prepare('UPDATE products SET stock = stock + ? WHERE id = ?');
            $upd->execute([$quantity, $productId]);

            $mov = $this->db->prepare('
                INSERT INTO movements (fecha, tipo, producto, cantidad, detalle)
                VALUES (?, ?, ?, ?, ?)
            ');
            $mov->execute([
                date('d/m/Y H:i'),
                'Entrada',
                (string) $product['nombre'],
                $quantity,
                'Entrada de inventario',
            ]);

            $this->db->commit();
        } catch (Throwable $e) {
            if ($this->db->inTransaction()) {
                $this->db->rollBack();
            }
            throw $e;
        }

        return $this->getFullState();
    }

    public function createSale(array $cart): array
    {
        if (empty($cart)) {
            throw new InvalidArgumentException('Agrega al menos un producto al carrito.');
        }

        $this->db->beginTransaction();
        try {
            $total = 0.0;
            $units = 0;
            $resolvedItems = [];

            $stmtFind = $this->db->prepare('SELECT id, nombre, precio, stock FROM products WHERE id = ? LIMIT 1');

            foreach ($cart as $item) {
                $productId = (int) ($item['product_id'] ?? 0);
                $qty = (int) ($item['cantidad'] ?? 0);

                if ($qty <= 0) {
                    throw new InvalidArgumentException('La cantidad de producto debe ser mayor a cero.');
                }

                $stmtFind->execute([$productId]);
                $product = $stmtFind->fetch();

                if (!$product) {
                    throw new RuntimeException('Producto no encontrado.');
                }

                $available = (int) $product['stock'];
                if ($qty > $available) {
                    throw new RuntimeException("Stock insuficiente para {$product['nombre']} (disponible: {$available}).");
                }

                $resolvedItems[] = [
                    'id' => $productId,
                    'nombre' => (string) $product['nombre'],
                    'precio' => (float) $product['precio'],
                    'qty' => $qty,
                ];
            }

            $stmtUpd = $this->db->prepare('UPDATE products SET stock = stock - ? WHERE id = ?');
            $stmtMov = $this->db->prepare('
                INSERT INTO movements (fecha, tipo, producto, cantidad, detalle)
                VALUES (?, ?, ?, ?, ?)
            ');
            $nowDisplay = date('d/m/Y H:i');

            foreach ($resolvedItems as $line) {
                $stmtUpd->execute([$line['qty'], $line['id']]);
                $total += $line['precio'] * $line['qty'];
                $units += $line['qty'];

                $stmtMov->execute([
                    $nowDisplay,
                    'Venta',
                    $line['nombre'],
                    -$line['qty'],
                    'Venta registrada',
                ]);
            }

            $salesCount = (int) $this->db->query('SELECT COUNT(*) FROM sales')->fetchColumn();
            $folio = 'V-' . (1000 + $salesCount + 1);

            $stmtSale = $this->db->prepare('
                INSERT INTO sales (folio, fecha, productos, total)
                VALUES (?, ?, ?, ?)
            ');
            $stmtSale->execute([
                $folio,
                date('c'),
                $units,
                $total,
            ]);

            $this->db->commit();

            return [
                'folio' => $folio,
                'total' => $total,
                'state' => $this->getFullState(),
            ];
        } catch (Throwable $e) {
            if ($this->db->inTransaction()) {
                $this->db->rollBack();
            }
            throw $e;
        }
    }

    public function addProvider(array $data): array
    {
        $nombre = trim((string) ($data['nombre'] ?? ''));
        $contacto = trim((string) ($data['contacto'] ?? ''));
        $telefono = trim((string) ($data['telefono'] ?? ''));
        $productos = trim((string) ($data['productos'] ?? ''));

        if ($nombre === '') {
            throw new InvalidArgumentException('Ingresa el nombre del proveedor.');
        }

        $stmt = $this->db->prepare('
            INSERT INTO providers (nombre, contacto, telefono, productos)
            VALUES (?, ?, ?, ?)
        ');
        $stmt->execute([$nombre, $contacto, $telefono, $productos]);

        return $this->getFullState();
    }

    public function addUser(array $data): array
    {
        $nombre = trim((string) ($data['nombre'] ?? ''));
        $usuario = trim((string) ($data['usuario'] ?? ''));
        $password = (string) ($data['password'] ?? '');
        $rol = trim((string) ($data['rol'] ?? 'Cajero'));

        if ($nombre === '' || $usuario === '' || $password === '') {
            throw new InvalidArgumentException('Completa todos los datos del usuario.');
        }

        $check = $this->db->prepare('SELECT COUNT(*) FROM users WHERE usuario = ?');
        $check->execute([$usuario]);
        if ((int) $check->fetchColumn() > 0) {
            throw new InvalidArgumentException("El usuario '{$usuario}' ya existe.");
        }

        $stmt = $this->db->prepare('
            INSERT INTO users (nombre, usuario, password_hash, rol, estado)
            VALUES (?, ?, ?, ?, ?)
        ');
        $stmt->execute([
            $nombre,
            $usuario,
            password_hash($password, PASSWORD_DEFAULT),
            $rol !== '' ? $rol : 'Cajero',
            'Activo',
        ]);

        return $this->getFullState();
    }

    public function saveConfig(array $data): array
    {
        $allowed = ['storeName', 'owner', 'phone', 'currency'];
        $stmt = $this->db->prepare('INSERT OR REPLACE INTO config (clave, valor) VALUES (?, ?)');

        foreach ($allowed as $key) {
            if (array_key_exists($key, $data)) {
                $stmt->execute([$key, trim((string) $data[$key])]);
            }
        }

        return $this->getFullState();
    }

    public function resetDemo(): array
    {
        Database::resetDemo($this->db);
        return $this->getFullState();
    }
}
