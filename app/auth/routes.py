from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from app import db
from app.models import User
from app.forms import LoginForm
from app.utils import sanitize_input
from . import bp

@bp.route("/", methods=["GET", "POST"])
def login():
    # TEMPORARY: Redirect directly to dashboard (login disabled for testing)
    return redirect(url_for("main.dashboard"))
    
    # Original login code (commented out for testing)
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    
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
                # Ensure next_page is safe or belongs to app, but standard simple check ok for now
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            else:
                flash('Username atau password salah', 'error')
                current_app.logger.warning(f'Failed login attempt for username: {username}')
                
        except Exception as e:
            current_app.logger.error(f'Login error: {str(e)}')
            flash('Terjadi kesalahan saat login', 'error')
    
    return render_template("login.html", form=form)
    """

@bp.route("/logout")
@login_required
def logout():
    current_app.logger.info(f'User {current_user.username} logged out')
    logout_user()
    flash('Anda telah logout', 'info')
    return redirect(url_for("auth.login"))
