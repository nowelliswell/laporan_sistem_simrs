from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Laporan
from app.forms import LaporanForm, EditStatusForm
from app.utils import save_upload_file, delete_upload_file, sanitize_input, format_datetime
from . import bp

@bp.route("/tambah", methods=["GET", "POST"])
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
            current_app.logger.info(f'New report created by {current_user.username}: {laporan.id}')
            # Redirect to main dashboard
            return redirect(url_for("main.dashboard"))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error creating report: {str(e)}')
            flash('Terjadi kesalahan saat menyimpan laporan', 'error')
    
    return render_template("tambah_laporan.html", form=form)

@bp.route("/detail/<int:id>")
@login_required
def detail(id):
    try:
        laporan = Laporan.query.get_or_404(id)
        return render_template("detail_laporan.html", laporan=laporan, format_datetime=format_datetime)
    except Exception as e:
        current_app.logger.error(f'Error loading report detail: {str(e)}')
        flash('Laporan tidak ditemukan', 'error')
        return redirect(url_for('main.dashboard'))

@bp.route("/edit_status/<int:id>", methods=["GET", "POST"])
@login_required
def edit_status(id):
    """Edit status laporan - accessible by all authenticated users"""
    try:
        laporan = Laporan.query.get_or_404(id)
        form = EditStatusForm()
        
        if form.validate_on_submit():
            # Update status
            laporan.status = form.status.data
            
            # Only admin can assign to other users
            if current_user.is_authenticated and current_user.is_admin():
                if form.assigned_to.data and form.assigned_to.data != 0:
                    laporan.assigned_to = form.assigned_to.data
                else:
                    laporan.assigned_to = None
            
            # Update timestamp
            laporan.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash('Status laporan berhasil diupdate', 'success')
            current_app.logger.info(f'Report {id} status updated by {current_user.username}: {laporan.status}')
            return redirect(url_for('reports.detail', id=id))
        
        # Pre-populate form with current values
        if request.method == 'GET':
            form.status.data = laporan.status
            if current_user.is_authenticated and current_user.is_admin():
                form.assigned_to.data = laporan.assigned_to if laporan.assigned_to else 0
        
        return render_template("edit_status.html", form=form, laporan=laporan, format_datetime=format_datetime)
        
    except Exception as e:
        current_app.logger.error(f'Error editing status: {str(e)}')
        flash('Terjadi kesalahan saat mengedit status', 'error')
        return redirect(url_for('reports.detail', id=id))

@bp.route("/delete_laporan/<int:id>", methods=["POST", "GET"])
@login_required
def delete_laporan(id):
    """Delete laporan - only admin can delete"""
    if not current_user.is_admin():
        flash('Akses ditolak. Hanya admin yang dapat menghapus laporan.', 'error')
        return redirect(url_for('reports.detail', id=id))
    
    try:
        laporan = Laporan.query.get_or_404(id)
        
        # Delete associated file if exists
        if laporan.bukti_file:
            delete_upload_file(laporan.bukti_file)
        
        # Delete laporan
        db.session.delete(laporan)
        db.session.commit()
        
        flash('Laporan berhasil dihapus', 'success')
        current_app.logger.info(f'Report {id} deleted by {current_user.username}')
        return redirect(url_for('main.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error deleting report: {str(e)}')
        flash('Terjadi kesalahan saat menghapus laporan', 'error')
        return redirect(url_for('reports.detail', id=id))
