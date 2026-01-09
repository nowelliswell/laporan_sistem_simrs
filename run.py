from app import create_app, db
from app.models import User
import os

app = create_app()

def init_db():
    """Initialize database and create default admin user"""
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        # We need to inspect because the table might exist
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
        else:
            # If table doesn't exist, create_all should have created it, 
            # so this block might just be for safety or initial run.
            pass

if __name__ == "__main__":
    # Ensure upload directory exists - Config is loaded in app
    # We can access app.config
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'app/static/uploads'), exist_ok=True)
    
    # Initialize database
    init_db()
    
    app.run(debug=True)
