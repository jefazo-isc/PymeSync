<?php
declare(strict_types=1);

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json; charset=utf-8');

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/src/Database.php';
require_once __DIR__ . '/src/Auth.php';
require_once __DIR__ . '/src/StoreRepository.php';

try {
    Auth::ensureSession();
    $db = Database::connect();
    $repo = new StoreRepository($db);

    $rawInput = file_get_contents('php://input');
    $jsonBody = [];
    if (is_string($rawInput) && trim($rawInput) !== '') {
        $decoded = json_decode($rawInput, true);
        if (is_array($decoded)) {
            $jsonBody = $decoded;
        }
    }

    $input = array_merge($_POST, $jsonBody);
    $action = (string) ($_GET['action'] ?? $input['action'] ?? 'state');

    switch ($action) {
        case 'ping':
        case 'state':
            echo json_encode([
                'ok' => true,
                'state' => $repo->getFullState(),
                'user' => Auth::user(),
            ], JSON_UNESCAPED_UNICODE);
            break;

        case 'login':
            $usuario = (string) ($input['usuario'] ?? '');
            $password = (string) ($input['password'] ?? '');
            $user = Auth::login($db, $usuario, $password);
            if ($user === null) {
                http_response_code(401);
                echo json_encode([
                    'ok' => false,
                    'error' => 'Usuario o contraseña incorrectos.',
                ], JSON_UNESCAPED_UNICODE);
                exit;
            }
            echo json_encode([
                'ok' => true,
                'user' => $user,
                'state' => $repo->getFullState(),
            ], JSON_UNESCAPED_UNICODE);
            break;

        case 'logout':
            Auth::logout();
            echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);
            break;

        case 'product_save':
            $state = $repo->saveProduct($input);
            echo json_encode([
                'ok' => true,
                'state' => $state,
            ], JSON_UNESCAPED_UNICODE);
            break;

        case 'stock_add':
            $productId = (int) ($input['product_id'] ?? 0);
            $quantity = (int) ($input['cantidad'] ?? 0);
            $state = $repo->addStock($productId, $quantity);
            echo json_encode([
                'ok' => true,
                'state' => $state,
            ], JSON_UNESCAPED_UNICODE);
            break;

        case 'sale_create':
            $cart = is_array($input['cart'] ?? null) ? $input['cart'] : [];
            $result = $repo->createSale($cart);
            echo json_encode([
                'ok' => true,
                'folio' => $result['folio'],
                'total' => $result['total'],
                'state' => $result['state'],
            ], JSON_UNESCAPED_UNICODE);
            break;

        case 'provider_add':
            $state = $repo->addProvider($input);
            echo json_encode([
                'ok' => true,
                'state' => $state,
            ], JSON_UNESCAPED_UNICODE);
            break;

        case 'user_add':
            $state = $repo->addUser($input);
            echo json_encode([
                'ok' => true,
                'state' => $state,
            ], JSON_UNESCAPED_UNICODE);
            break;

        case 'config_save':
            $state = $repo->saveConfig($input);
            echo json_encode([
                'ok' => true,
                'state' => $state,
            ], JSON_UNESCAPED_UNICODE);
            break;

        case 'reset_demo':
            $state = $repo->resetDemo();
            echo json_encode([
                'ok' => true,
                'state' => $state,
            ], JSON_UNESCAPED_UNICODE);
            break;

        default:
            http_response_code(400);
            echo json_encode([
                'ok' => false,
                'error' => "Acción desconocida: {$action}",
            ], JSON_UNESCAPED_UNICODE);
            break;
    }
} catch (InvalidArgumentException $e) {
    http_response_code(400);
    echo json_encode([
        'ok' => false,
        'error' => $e->getMessage(),
    ], JSON_UNESCAPED_UNICODE);
} catch (Throwable $e) {
    http_response_code(400);
    echo json_encode([
        'ok' => false,
        'error' => $e->getMessage(),
    ], JSON_UNESCAPED_UNICODE);
}
