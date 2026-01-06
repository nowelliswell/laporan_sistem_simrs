import os
import secrets
from werkzeug.utils import secure_filename
from flask import current_app, flash
from config import Config

def allowed_file(filename):
    """Check apakah file extension diizinkan"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_upload_file(file):
    """
    Simpan file upload dengan nama yang aman
    Returns: filename jika berhasil, None jika gagal
    """
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        flash('Tipe file tidak diizinkan', 'error')
        return None
    
    # Generate nama file yang unik
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{secrets.token_hex(8)}{ext}"
    
    try:
        # Pastikan direktori upload ada
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Simpan file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        return filename
    except Exception as e:
        current_app.logger.error(f"Error saving file: {str(e)}")
        flash('Gagal menyimpan file', 'error')
        return None

def delete_upload_file(filename):
    """Hapus file upload"""
    if not filename:
        return True
    
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {str(e)}")
        return False

def sanitize_input(text):
    """Sanitize input text"""
    if not text:
        return text
    
    # Basic sanitization - remove dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def format_datetime(dt):
    """Format datetime untuk display"""
    if not dt:
        return '-'
    return dt.strftime('%d/%m/%Y %H:%M')

def get_file_size(file_path):
    """Get ukuran file dalam bytes"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0