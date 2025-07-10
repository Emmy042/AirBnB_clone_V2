#!/usr/bin/env bash
# Sets up the web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y nginx
fi

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Create or recreate symbolic link
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
NGINX_CONF="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static/" "$NGINX_CONF"; then
    sudo sed -i "/listen 80 default_server;/a \\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" "$NGINX_CONF"
fi

# Restart Nginx to apply changes
sudo nginx -t && sudo systemctl reload nginx
