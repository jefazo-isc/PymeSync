FROM php:8.4-apache

# Habilitar mod_rewrite, configurar ServerName y bloquear acceso HTTP directo a /data y /src
RUN a2enmod rewrite \
    && echo "ServerName localhost" > /etc/apache2/conf-available/servername.conf \
    && printf '<Directory /var/www/html/data>\n    Require all denied\n</Directory>\n<Directory /var/www/html/src>\n    Require all denied\n</Directory>\n' > /etc/apache2/conf-available/pymesync-security.conf \
    && a2enconf servername pymesync-security

WORKDIR /var/www/html
COPY . /var/www/html/

# Crear carpeta de datos con permisos de escritura para SQLite y sesiones
RUN mkdir -p /var/www/html/data/sessions \
    && chown -R www-data:www-data /var/www/html/data \
    && chmod -R 775 /var/www/html/data

# Puerto dinámico compatible con Render (default 10000) y Google Cloud Run (8080)
ENV PORT=10000
EXPOSE 10000

CMD ["sh", "-c", "PORT=${PORT:-10000}; echo \"Listen ${PORT}\" > /etc/apache2/ports.conf; sed -i -E \"s|<VirtualHost [*]:[0-9]+>|<VirtualHost *:${PORT}>|g\" /etc/apache2/sites-available/000-default.conf; mkdir -p /var/www/html/data/sessions && chown -R www-data:www-data /var/www/html/data && chmod -R 775 /var/www/html/data; exec apache2-foreground"]
