from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash dan simpan password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifikasi password"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check apakah user adalah admin"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Laporan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(100), nullable=False)
    pelapor = db.Column(db.String(100), nullable=False)
    modul_simrs = db.Column(db.String(100))
    jenis_kesalahan = db.Column(db.String(50), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    tgl_kejadian = db.Column(db.DateTime, nullable=False)
    bukti_file = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key ke user yang membuat laporan
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_reports')
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_reports')
    
    def __repr__(self):
        return f'<Laporan {self.id}: {self.unit}>'

class SearchPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    search_query = db.Column(db.String(200))
    unit_filter = db.Column(db.String(100))
    status_filter = db.Column(db.String(20))
    jenis_filter = db.Column(db.String(50))
    pelapor_filter = db.Column(db.String(100))
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)
    sort_by = db.Column(db.String(50), default='created_at')
    sort_order = db.Column(db.String(10), default='desc')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='search_preferences')
    
    def __repr__(self):
        return f'<SearchPreference {self.name}>'