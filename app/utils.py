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

def build_search_query(form_data):
    """Build SQLAlchemy query berdasarkan search criteria"""
    from app.models import Laporan, User
    from sqlalchemy import and_, or_, desc, asc
    from datetime import datetime, timedelta
    
    query = Laporan.query
    
    # Text search - search in multiple fields
    if form_data.get('search_query'):
        search_term = f"%{form_data['search_query']}%"
        query = query.filter(
            or_(
                Laporan.unit.ilike(search_term),
                Laporan.pelapor.ilike(search_term),
                Laporan.modul_simrs.ilike(search_term),
                Laporan.deskripsi.ilike(search_term)
            )
        )
    
    # Unit filter
    if form_data.get('unit_filter'):
        query = query.filter(Laporan.unit == form_data['unit_filter'])
    
    # Status filter
    if form_data.get('status_filter'):
        query = query.filter(Laporan.status == form_data['status_filter'])
    
    # Jenis kesalahan filter
    if form_data.get('jenis_filter'):
        query = query.filter(Laporan.jenis_kesalahan == form_data['jenis_filter'])
    
    # Pelapor filter
    if form_data.get('pelapor_filter'):
        pelapor_term = f"%{form_data['pelapor_filter']}%"
        query = query.filter(Laporan.pelapor.ilike(pelapor_term))
    
    # Date range filter
    if form_data.get('date_from'):
        query = query.filter(Laporan.tgl_kejadian >= form_data['date_from'])
    
    if form_data.get('date_to'):
        # Add one day to include the end date
        try:
            date_to_str = form_data['date_to']
            # Parse string to date if it's a string
            if isinstance(date_to_str, str):
                date_to_obj = datetime.strptime(date_to_str, '%Y-%m-%d')
            else:
                date_to_obj = date_to_str
                
            end_date = date_to_obj + timedelta(days=1)
            query = query.filter(Laporan.tgl_kejadian < end_date)
        except Exception as e:
            current_app.logger.error(f"Date filter error: {e}")
            pass
    
    # Sorting
    sort_by = form_data.get('sort_by', 'id')
    sort_order = form_data.get('sort_order', 'asc')
    
    if hasattr(Laporan, sort_by):
        sort_column = getattr(Laporan, sort_by)
        if sort_order == 'asc':
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
    
    return query

def export_search_results(laporan_list, format='csv'):
    """Export search results to CSV or Excel"""
    import csv
    import io
    from datetime import datetime
    
    if format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'ID', 'Unit', 'Pelapor', 'Modul SIMRS', 'Jenis Kesalahan',
            'Deskripsi', 'Tanggal Kejadian', 'Status', 'Tanggal Dibuat',
            'Dibuat Oleh', 'Ditugaskan Ke'
        ])
        
        # Data rows
        for laporan in laporan_list:
            writer.writerow([
                laporan.id,
                laporan.unit,
                laporan.pelapor,
                laporan.modul_simrs or '',
                laporan.jenis_kesalahan,
                laporan.deskripsi,
                laporan.tgl_kejadian.strftime('%Y-%m-%d %H:%M') if laporan.tgl_kejadian else '',
                laporan.status,
                laporan.created_at.strftime('%Y-%m-%d %H:%M') if laporan.created_at else '',
                laporan.creator.username if laporan.creator else '',
                laporan.assignee.username if laporan.assignee else ''
            ])
        
        output.seek(0)
        return output.getvalue()
    
    return None

def get_search_statistics(query):
    """Get statistics for current search results"""
    total = query.count()
    
    # Status breakdown
    status_stats = {}
    for status in ['pending', 'in_progress', 'resolved']:
        status_stats[status] = query.filter_by(status=status).count()
    
    # Jenis kesalahan breakdown
    jenis_stats = {}
    for jenis in ['Data Pasien', 'Transaksi', 'Sistem Error', 'Lainnya']:
        jenis_stats[jenis] = query.filter_by(jenis_kesalahan=jenis).count()
    
    return {
        'total': total,
        'status_stats': status_stats,
        'jenis_stats': jenis_stats
    }