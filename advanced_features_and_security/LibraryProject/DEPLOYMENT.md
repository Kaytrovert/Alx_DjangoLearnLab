# Deployment Configuration for HTTPS

This document provides instructions for configuring your web server to serve the Django application over HTTPS. The Django `settings.py` is configured with `SECURE_SSL_REDIRECT`, HSTS, and secure cookies; the web server must terminate SSL/TLS and forward requests to the application.

## Prerequisites

- Valid SSL/TLS certificates (e.g., from Let's Encrypt)
- Certificate file and private key
- Web server: Nginx or Apache

## Option 1: Nginx Configuration

Configure Nginx to terminate SSL and proxy to Django (e.g., via Gunicorn):

```nginx
# /etc/nginx/sites-available/libraryproject

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server block
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificate paths (e.g., Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_cache shared:SSL:10m;

    # Django static and media
    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }
    location /media/ {
        alias /path/to/your/project/media/;
    }

    # Proxy to Gunicorn/Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site and reload Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Option 2: Apache Configuration

Configure Apache with mod_ssl to terminate SSL and proxy to Django (e.g., via mod_wsgi):

```apache
# /etc/apache2/sites-available/libraryproject.conf

# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS VirtualHost
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf

    WSGIDaemonProcess libraryproject python-path=/path/to/your/project
    WSGIProcessGroup libraryproject
    WSGIScriptAlias / /path/to/your/project/LibraryProject/wsgi.py

    Alias /static/ /path/to/your/project/staticfiles/
    Alias /media/ /path/to/your/project/media/

    <Directory /path/to/your/project/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

Enable modules and site:

```bash
sudo a2enmod ssl rewrite
sudo a2ensite libraryproject
sudo apache2ctl configtest
sudo systemctl reload apache2
```

## Obtaining SSL Certificates (Let's Encrypt)

Using Certbot:

```bash
# Nginx
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Apache
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
```

Certbot will configure SSL and set up automatic renewal.

## Environment Variables for Production

Set these before running the application:

```bash
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY="your-secure-secret-key"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
```

## Running the Application (Gunicorn example)

```bash
gunicorn --bind 127.0.0.1:8000 --workers 3 LibraryProject.wsgi:application
```

Ensure the reverse proxy forwards `X-Forwarded-Proto: https` so Django's `SECURE_SSL_REDIRECT` and secure cookie logic work correctly.
