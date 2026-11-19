FROM php:8.4-apache

# Habilitar extensiones necesarias (PDO SQLite ya viene en php:8.4-apache)
RUN a2enmod rewrite

WORKDIR /var/www/html
COPY . /var/www/html/

# Crear carpeta de datos con permisos de escritura para SQLite y sesiones
RUN mkdir -p /var/www/html/data/sessions \
    && chown -R www-data:www-data /var/www/html/data \
    && chmod -R 775 /var/www/html/data

# Configurar Apache para escuchar en el puerto dinámico $PORT de Google Cloud Run (default 8080)
ENV PORT=8080
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

EXPOSE 8080
CMD ["apache2-foreground"]
