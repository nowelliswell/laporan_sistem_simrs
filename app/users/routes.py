from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.forms import UserForm
from app.utils import sanitize_input, format_datetime
from . import bp

@bp.route("/users")
# @login_required  # TEMPORARY: Login disabled for testing
def users():
    # TEMPORARY FIX: Skip admin check when login disabled
    # if not current_user.is_admin():
    #     flash('Akses ditolak. Hanya admin yang dapat mengakses halaman ini.', 'error')
    #     return redirect(url_for('main.dashboard'))
    
    try:
        users = User.query.all()
        return render_template("users.html", users=users, format_datetime=format_datetime)
    except Exception as e:
        current_app.logger.error(f'Error loading users: {str(e)}')
        flash('Terjadi kesalahan saat memuat data user', 'error')
        return redirect(url_for('main.dashboard'))

@bp.route("/add_user", methods=["GET", "POST"])
# @login_required  # TEMPORARY: Login disabled for testing
def add_user():
    # TEMPORARY FIX: Skip admin check when login disabled
    # if not current_user.is_admin():
    #     flash('Akses ditolak', 'error')
    #     return redirect(url_for('main.dashboard'))
    
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
                unit=sanitize_input(form.unit.data) if form.unit.data else None,
                role=form.role.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'User {user.username} berhasil ditambahkan', 'success')
            creator = current_user.username if current_user.is_authenticated else 'anonymous'  # TEMPORARY FIX
            current_app.logger.info(f'New user created by {creator}: {user.username}')
            return redirect(url_for('users.users'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error creating user: {str(e)}')
            flash('Terjadi kesalahan saat membuat user', 'error')
    
    return render_template("add_user.html", form=form)
