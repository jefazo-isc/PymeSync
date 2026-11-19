#!/bin/bash
cd "$(dirname "$0")"
echo "=========================================================="
echo "  PymeSync Server (PHP + SQLite) - «Tu tiendita, bien chidita»"
echo "  Acceso Local: http://localhost:8000"
echo "  API Endpoint: http://localhost:8000/api.php"
echo "=========================================================="
php -S 0.0.0.0:8000
