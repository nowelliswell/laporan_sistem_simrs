#!/bin/bash

# BAP SIMRS Deployment Script
# Script untuk mempermudah deployment ke berbagai platform

set -e

echo "🚀 BAP SIMRS Deployment Helper"
echo "================================"
echo ""

# Function untuk generate SECRET_KEY
generate_secret_key() {
    python3 -c 'import secrets; print(secrets.token_hex(32))'
}

# Function untuk deploy ke Heroku
deploy_heroku() {
    echo "📦 Deploying to Heroku..."
    
    # Check if heroku CLI installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Please install: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    read -p "Enter app name (or press Enter for random): " APP_NAME
    
    if [ -z "$APP_NAME" ]; then
        heroku create
    else
        heroku create "$APP_NAME"
    fi
    
    echo "Adding PostgreSQL..."
    heroku addons:create heroku-postgresql:essential-0
    
    echo "Setting environment variables..."
    SECRET_KEY=$(generate_secret_key)
    heroku config:set SECRET_KEY="$SECRET_KEY"
    heroku config:set FLASK_ENV=production
    
    echo "Deploying..."
    git push heroku main || git push heroku master
    
    echo "Initializing database..."
    heroku run python init_db.py
    
    echo "✅ Deployment complete!"
    heroku open
}

# Function untuk deploy ke Railway
deploy_railway() {
    echo "🚂 Deploying to Railway..."
    
    if ! command -v railway &> /dev/null; then
        echo "Installing Railway CLI..."
        npm i -g @railway/cli
    fi
    
    railway login
    railway init
    railway up
    
    echo "✅ Deployment complete!"
    echo "Don't forget to:"
    echo "1. Add PostgreSQL database in Railway dashboard"
    echo "2. Set SECRET_KEY environment variable"
    echo "3. Run: railway run python init_db.py"
}

# Function untuk setup Docker
deploy_docker() {
    echo "🐳 Setting up Docker deployment..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker first."
        exit 1
    fi
    
    echo "Generating SECRET_KEY..."
    SECRET_KEY=$(generate_secret_key)
    
    echo "Creating .env file..."
    cat > .env.docker << EOF
SECRET_KEY=$SECRET_KEY
FLASK_ENV=production
DATABASE_URL=postgresql://bapuser:bappassword@db:5432/bap_simrs
EOF
    
    echo "Building and starting containers..."
    docker-compose up -d --build
    
    echo "Waiting for database to be ready..."
    sleep 10
    
    echo "Initializing database..."
    docker-compose exec web python init_db.py
    
    echo "✅ Docker deployment complete!"
    echo "Application running at: http://localhost"
}

# Function untuk VPS setup
deploy_vps() {
    echo "🖥️  VPS Deployment Guide"
    echo ""
    echo "This will guide you through VPS deployment."
    echo "Make sure you have:"
    echo "- Ubuntu 20.04+ server"
    echo "- Root or sudo access"
    echo "- Domain name (optional)"
    echo ""
    read -p "Continue? (y/n): " CONTINUE
    
    if [ "$CONTINUE" != "y" ]; then
        exit 0
    fi
    
    read -p "Enter your server IP: " SERVER_IP
    read -p "Enter your domain (or press Enter to skip): " DOMAIN
    
    echo ""
    echo "📋 Follow these steps on your VPS:"
    echo ""
    echo "1. SSH to your server:"
    echo "   ssh root@$SERVER_IP"
    echo ""
    echo "2. Run the setup commands:"
    cat << 'EOF'
   
   # Update system
   apt update && apt upgrade -y
   
   # Install dependencies
   apt install python3 python3-pip python3-venv nginx supervisor postgresql postgresql-contrib -y
   
   # Setup PostgreSQL
   sudo -u postgres psql << SQL
   CREATE DATABASE bap_simrs;
   CREATE USER bapuser WITH PASSWORD 'strongpassword123';
   GRANT ALL PRIVILEGES ON DATABASE bap_simrs TO bapuser;
   \q
SQL
   
   # Create app user
   adduser bapapp
   su - bapapp
   
   # Clone and setup
   git clone YOUR_REPO_URL bap-laporan-simrs
   cd bap-laporan-simrs
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Create .env
   cat > .env << ENVEOF
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
DATABASE_URL=postgresql://bapuser:strongpassword123@localhost/bap_simrs
FLASK_ENV=production
ENVEOF
   
   # Initialize database
   python init_db.py
   
   exit  # Exit from bapapp user
EOF
    
    echo ""
    echo "3. Setup Supervisor (copy config from DEPLOYMENT.md)"
    echo "4. Setup Nginx (copy config from DEPLOYMENT.md)"
    echo "5. Setup SSL with Let's Encrypt"
    echo ""
    echo "For detailed instructions, see DEPLOYMENT.md"
}

# Main menu
echo "Select deployment platform:"
echo "1) Heroku (Easiest)"
echo "2) Railway (Modern)"
echo "3) Docker (Local/VPS)"
echo "4) VPS Manual Setup"
echo "5) Exit"
echo ""
read -p "Enter choice [1-5]: " CHOICE

case $CHOICE in
    1)
        deploy_heroku
        ;;
    2)
        deploy_railway
        ;;
    3)
        deploy_docker
        ;;
    4)
        deploy_vps
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
