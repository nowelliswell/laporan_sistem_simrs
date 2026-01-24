"""
Database Initialization Script
Run this after deployment to setup database and create admin user
"""
from app import create_app, db
from app.models import User
from config import ProductionConfig
import os

def init_database():
    """Initialize database and create default admin user"""
    # Use production config if in production
    config = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else None
    app = create_app(config)
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating default admin user...")
            admin = User(username='admin', role='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created")
            print("  Username: admin")
            print("  Password: admin123")
            print("  ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!")
        else:
            print("✓ Admin user already exists")
        
        print("\n✅ Database initialization complete!")

if __name__ == '__main__':
    init_database()
