from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import logging
from logging.handlers import RotatingFileHandler

# Import local modules
from config import Config
from models import db, User, Laporan
from forms import LoginForm, LaporanForm, UserForm, EditStatusForm
from utils import save_upload_file, delete_upload_file, sanitize_input, format_datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Setup logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/bap_simrs.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('BAP SIMRS startup')
    
    return app

app = create_app()

# ======================
# ERROR HANDLERS
# ======================
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return render_template('errors/500.html'), 500

@app.errorhandler(413)
def too_large(error):
    flash('File terlalu besar. Maksimal 16MB.', 'error')
    return redirect(request.url)

# ======================
# AUTHENTICATION ROUTES
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            username = sanitize_input(form.username.data)
            password = form.password.data
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password) and user.is_active:
                # Update last login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                login_user(user, remember=True, duration=timedelta(hours=1))
                flash(f'Selamat datang, {user.username}!', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Username atau password salah', 'error')
                app.logger.warning(f'Failed login attempt for username: {username}')
                
        except Exception as e:
            app.logger.error(f'Login error: {str(e)}')
            flash('Terjadi kesalahan saat login', 'error')
    
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    app.logger.info(f'User {current_user.username} logged out')
    logout_user()
    flash('Anda telah logout', 'info')
    return redirect(url_for("login"))

# ======================
# DASHBOARD
# ======================
@app.route("/dashboard")
@login_required
def dashboard():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        laporan = Laporan.query.order_by(Laporan.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template("dashboard.html", laporan=laporan, format_datetime=format_datetime)
    except Exception as e:
        app.logger.error(f'Dashboard error: {str(e)}')
        flash('Terjadi kesalahan saat memuat dashboard', 'error')
        return render_template("dashboard.html", laporan=None)

# ======================
# LAPORAN ROUTES
# ======================
@app.route("/tambah", methods=["GET", "POST"])
@login_required
def tambah_laporan():
    form = LaporanForm()
    
    if form.validate_on_submit():
        try:
            # Handle file upload
            filename = None
            if form.bukti_file.data:
                filename = save_upload_file(form.bukti_file.data)
                if not filename:
                    return render_template("tambah_laporan.html", form=form)
            
            # Create laporan
            laporan = Laporan(
                unit=sanitize_input(form.unit.data),
                pelapor=sanitize_input(form.pelapor.data),
                modul_simrs=sanitize_input(form.modul_simrs.data) if form.modul_simrs.data else None,
                jenis_kesalahan=form.jenis_kesalahan.data,
                deskripsi=sanitize_input(form.deskripsi.data),
                tgl_kejadian=form.tgl_kejadian.data,
                bukti_file=filename,
                created_by=current_user.id
            )
            
            db.session.add(laporan)
            db.session.commit()
            
            flash('Laporan berhasil ditambahkan', 'success')
            app.logger.info(f'New report created by {current_user.username}: {laporan.id}')
            return redirect(url_for("dashboard"))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating report: {str(e)}')
            flash('Terjadi kesalahan saat menyimpan laporan', 'error')
    
    return render_template("tambah_laporan.html", form=form)

@app.route("/detail/<int:id>")
@login_required
def detail(id):
    try:
        laporan = Laporan.query.get_or_404(id)
        return render_template("detail_laporan.html", laporan=laporan, format_datetime=format_datetime)
    except Exception as e:
        app.logger.error(f'Error loading report detail: {str(e)}')
        flash('Laporan tidak ditemukan', 'error')
        return redirect(url_for('dashboard'))

@app.route("/edit_status/<int:id>", methods=["GET", "POST"])
@login_required
def edit_status(id):
    if not current_user.is_admin():
        flash('Akses ditolak. Hanya admin yang dapat mengedit status laporan.', 'error')
        return redirect(url_for('detail', id=id))
    
    try:
        laporan = Laporan.query.get_or_404(id)
        form = EditStatusForm()
        
        if form.validate_on_submit():
            # Update status
            laporan.status = form.status.data
            
            # Update assigned_to
            if form.assigned_to.data and form.assigned_to.data != 0:
                laporan.assigned_to = form.assigned_to.data
            else:
                laporan.assigned_to = None
            
            # Update timestamp
            laporan.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash('Status laporan berhasil diupdate', 'success')
            app.logger.info(f'Report {id} status updated by {current_user.username}: {laporan.status}')
            return redirect(url_for('detail', id=id))
        
        # Pre-populate form with current values
        if request.method == 'GET':
            form.status.data = laporan.status
            form.assigned_to.data = laporan.assigned_to if laporan.assigned_to else 0
        
        return render_template("edit_status.html", form=form, laporan=laporan, format_datetime=format_datetime)
        
    except Exception as e:
        app.logger.error(f'Error editing status: {str(e)}')
        flash('Terjadi kesalahan saat mengedit status', 'error')
        return redirect(url_for('detail', id=id))

@app.route("/delete_laporan/<int:id>", methods=["POST", "GET"])
@login_required
def delete_laporan(id):
    if not current_user.is_admin():
        flash('Akses ditolak. Hanya admin yang dapat menghapus laporan.', 'error')
        return redirect(url_for('detail', id=id))
    
    try:
        laporan = Laporan.query.get_or_404(id)
        
        # Delete associated file if exists
        if laporan.bukti_file:
            delete_upload_file(laporan.bukti_file)
        
        # Delete laporan
        db.session.delete(laporan)
        db.session.commit()
        
        flash('Laporan berhasil dihapus', 'success')
        app.logger.info(f'Report {id} deleted by {current_user.username}')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting report: {str(e)}')
        flash('Terjadi kesalahan saat menghapus laporan', 'error')
        return redirect(url_for('detail', id=id))

# ======================
# USER MANAGEMENT (Admin Only)
# ======================
@app.route("/users")
@login_required
def users():
    if not current_user.is_admin():
        flash('Akses ditolak. Hanya admin yang dapat mengakses halaman ini.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        users = User.query.all()
        return render_template("users.html", users=users, format_datetime=format_datetime)
    except Exception as e:
        app.logger.error(f'Error loading users: {str(e)}')
        flash('Terjadi kesalahan saat memuat data user', 'error')
        return redirect(url_for('dashboard'))

@app.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    if not current_user.is_admin():
        flash('Akses ditolak', 'error')
        return redirect(url_for('dashboard'))
    
    form = UserForm()
    
    if form.validate_on_submit():
        try:
            # Check if username already exists
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username sudah digunakan', 'error')
                return render_template("add_user.html", form=form)
            
            user = User(
                username=sanitize_input(form.username.data),
                email=sanitize_input(form.email.data) if form.email.data else None,
                role=form.role.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'User {user.username} berhasil ditambahkan', 'success')
            app.logger.info(f'New user created by {current_user.username}: {user.username}')
            return redirect(url_for('users'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating user: {str(e)}')
            flash('Terjadi kesalahan saat membuat user', 'error')
    
    return render_template("add_user.html", form=form)

# ======================
# STATISTIK ROUTE
# ======================
@app.route("/statistik")
@login_required
def statistik():
    try:
        # Get statistics data
        total_laporan = Laporan.query.count()
        pending_count = Laporan.query.filter_by(status='pending').count()
        in_progress_count = Laporan.query.filter_by(status='in_progress').count()
        resolved_count = Laporan.query.filter_by(status='resolved').count()
        
        # Get laporan by jenis kesalahan
        from sqlalchemy import func
        jenis_stats = db.session.query(
            Laporan.jenis_kesalahan, 
            func.count(Laporan.id).label('count')
        ).group_by(Laporan.jenis_kesalahan).all()
        
        # Get recent activity (last 10 reports)
        recent_reports = Laporan.query.order_by(Laporan.created_at.desc()).limit(10).all()
        
        stats_data = {
            'total_laporan': total_laporan,
            'pending_count': pending_count,
            'in_progress_count': in_progress_count,
            'resolved_count': resolved_count,
            'jenis_stats': jenis_stats,
            'recent_reports': recent_reports
        }
        
        return render_template("statistik.html", stats=stats_data, format_datetime=format_datetime)
        
    except Exception as e:
        app.logger.error(f'Error loading statistics: {str(e)}')
        flash('Terjadi kesalahan saat memuat statistik', 'error')
        return redirect(url_for('dashboard'))

# ======================
# INITIALIZATION
# ======================
def init_db():
    """Initialize database and create default admin user"""
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: admin/admin123")

if __name__ == "__main__":
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    init_db()
    
    app.run(debug=True)