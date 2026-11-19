<?php
declare(strict_types=1);

class Auth
{
    public static function ensureSession(): void
    {
        if (session_status() === PHP_SESSION_NONE && !headers_sent()) {
            $sessionDir = dirname(__DIR__) . '/data/sessions';
            if (!is_dir($sessionDir)) {
                @mkdir($sessionDir, 0775, true);
            }
            if (is_dir($sessionDir) && is_writable($sessionDir)) {
                session_save_path($sessionDir);
            }
            session_start();
        }
    }

    public static function login(PDO $db, string $username, string $password): ?array
    {
        self::ensureSession();

        $username = trim($username);
        if ($username === '' || $password === '') {
            return null;
        }

        $stmt = $db->prepare('
            SELECT id, nombre, usuario, password_hash, rol, estado
            FROM users
            WHERE usuario = :usuario
            LIMIT 1
        ');
        $stmt->execute([':usuario' => $username]);
        $row = $stmt->fetch();

        if (!$row) {
            return null;
        }

        if (($row['estado'] ?? '') !== 'Activo') {
            return null;
        }

        if (!password_verify($password, (string) $row['password_hash'])) {
            return null;
        }

        $user = [
            'id' => (int) $row['id'],
            'nombre' => (string) $row['nombre'],
            'usuario' => (string) $row['usuario'],
            'rol' => (string) $row['rol'],
            'estado' => (string) $row['estado'],
        ];

        $_SESSION['pymesync_user'] = $user;

        return $user;
    }

    public static function logout(): void
    {
        self::ensureSession();
        unset($_SESSION['pymesync_user']);
    }

    public static function user(): ?array
    {
        self::ensureSession();
        return $_SESSION['pymesync_user'] ?? null;
    }
}
