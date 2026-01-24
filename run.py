from app import create_app, db
from app.models import User
import os
from config import DevelopmentConfig, ProductionConfig

# Pilih config berdasarkan environment
config = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig
app = create_app(config)

def init_db():
    """Initialize database and create default admin user"""
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        if inspector.has_table("user"):
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', role='admin')
                admin.set_password('admin123')  # Change this in production!
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created: admin/admin123")

if __name__ == "__main__":
    # Ensure upload directory exists
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'app/static/uploads'), exist_ok=True)
    
    # Initialize database
    init_db()
    
    # Run app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
