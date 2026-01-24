# BAP SIMRS - Sistem Pelaporan Kesalahan SIMRS

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **Sistem Pelaporan Kesalahan SIMRS** adalah aplikasi web berbasis Flask untuk mengelola dan melacak laporan kesalahan/bug pada Sistem Informasi Manajemen Rumah Sakit (SIMRS). Aplikasi ini menyediakan platform terpusat untuk pelaporan, tracking, dan resolusi masalah teknis dalam lingkungan rumah sakit.

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Teknologi](#-teknologi)
- [Arsitektur](#-arsitektur)
- [Instalasi](#-instalasi)
- [Konfigurasi](#-konfigurasi)
- [Penggunaan](#-penggunaan)
- [API Endpoints](#-api-endpoints)
- [Keamanan](#-keamanan)
- [Kontribusi](#-kontribusi)
- [Roadmap](#-roadmap)

## ✨ Fitur Utama

### 🔐 Autentikasi & Otorisasi
- **Secure Authentication**: Hash password menggunakan bcrypt
- **Role-based Access Control**: Admin dan User dengan hak akses berbeda
- **Session Management**: Timeout otomatis dan secure session handling
- **CSRF Protection**: Perlindungan terhadap Cross-Site Request Forgery

### 📊 Manajemen Laporan
- **CRUD Operations**: Create, Read, Update, Delete laporan kesalahan
- **Status Tracking**: Pending → In Progress → Resolved
- **File Upload**: Upload bukti dengan validasi keamanan
- **Assignment System**: Penugasan laporan ke teknisi/admin
- **Categorization**: Klasifikasi berdasarkan jenis kesalahan

### 👥 Manajemen User
- **User Management**: Kelola user dan role (Admin only)
- **Profile Management**: Update informasi user
- **Activity Tracking**: Log aktivitas dan last login
- **Multi-role Support**: Admin dan User dengan permission berbeda

### 📈 Dashboard & Statistik
- **Real-time Statistics**: Overview laporan dan status
- **Visual Charts**: Grafik berdasarkan jenis kesalahan
- **Recent Activity**: Laporan terbaru dan aktivitas sistem
- **Interactive UI**: Click-to-navigate dan responsive design

### 🛡️ Keamanan & Validasi
- **Input Sanitization**: Pencegahan XSS attacks
- **File Upload Security**: Validasi tipe dan ukuran file
- **Error Handling**: Comprehensive error pages dan logging
- **Audit Trail**: Logging semua aktivitas penting

## 🛠️ Teknologi

### Backend
- **Flask 2.0+** - Web framework
- **SQLAlchemy** - ORM dan database management
- **Flask-Login** - Session management
- **Flask-WTF** - Form handling dan CSRF protection
- **Werkzeug** - WSGI utilities dan security
- **bcrypt** - Password hashing

### Frontend
- **HTML5/CSS3** - Markup dan styling
- **Jinja2** - Template engine
- **Responsive Design** - Mobile-friendly interface
- **Custom CSS** - Modern UI dengan gradients dan animations

### Database
- **SQLite** - Development database
- **PostgreSQL/MySQL** - Production ready (configurable)

### Security
- **CSRF Protection** - Flask-WTF
- **Password Hashing** - bcrypt
- **Input Validation** - WTForms validators
- **File Upload Security** - Type dan size validation

## 🏗️ Arsitektur

```
bap-laporan-simrs/
├── 📁 app.py                 # Main application & routes
├── 📁 config.py              # Configuration management
├── 📁 models.py              # Database models (User, Laporan)
├── 📁 forms.py               # WTF Forms dengan validasi
├── 📁 utils.py               # Utility functions
├── 📁 requirements.txt       # Python dependencies
├── 📁 .env                   # Environment variables
├── 📁 .gitignore            # Git ignore rules
│
├── 📂 templates/             # Jinja2 templates
│   ├── 🔐 login.html
│   ├── 📊 dashboard.html
│   ├── 📈 statistik.html
│   ├── 📝 tambah_laporan.html
│   ├── 📄 detail_laporan.html
│   ├── ✏️ edit_status.html
│   ├── 👥 users.html
│   ├── ➕ add_user.html
│   └── 📂 errors/
│       ├── 404.html
│       └── 500.html
│
├── 📂 static/
│   └── 📂 uploads/           # File uploads storage
│
├── 📂 instance/
│   └── 🗄️ database.db       # SQLite database
│
└── 📂 logs/                  # Application logs
    └── 📋 bap_simrs.log
```

### Database Schema

```sql
-- Users table
User {
  id: Integer (PK)
  username: String(50) UNIQUE
  email: String(100) UNIQUE
  password_hash: String(255)
  role: String(20) DEFAULT 'user'
  is_active: Boolean DEFAULT True
  created_at: DateTime
  last_login: DateTime
}

-- Reports table
Laporan {
  id: Integer (PK)
  unit: String(100)
  pelapor: String(100)
  modul_simrs: String(100)
  jenis_kesalahan: String(50)
  deskripsi: Text
  tgl_kejadian: DateTime
  bukti_file: String(200)
  status: String(20) DEFAULT 'pending'
  created_at: DateTime
  updated_at: DateTime
  created_by: Integer (FK -> User.id)
  assigned_to: Integer (FK -> User.id)
}
```

## 🚀 Instalasi

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Quick Start

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/bap-laporan-simrs.git
   cd bap-laporan-simrs
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env file dengan konfigurasi Anda
   ```

5. **Database Setup**
   ```bash
   # Database akan dibuat otomatis saat pertama kali run
   python app.py
   ```

6. **Access Application**
   ```
   URL: http://127.0.0.1:5000
   Default Login: admin / admin123
   ```

## ⚙️ Konfigurasi

### Environment Variables (.env)

```bash
# Security
SECRET_KEY=your-super-secret-key-here-change-in-production

# Database
DATABASE_URL=sqlite:///instance/database.db
# DATABASE_URL=postgresql://user:password@localhost/bap_simrs  # PostgreSQL
# DATABASE_URL=mysql://user:password@localhost/bap_simrs       # MySQL

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True

# Upload Settings (Optional - defaults in config.py)
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=static/uploads
```

### Production Configuration

```python
# config.py - Production settings
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

## 📖 Penggunaan

### Login & Authentication

```python
# Default credentials
Username: admin
Password: admin123

# Ganti password default di production!
```

### Membuat Laporan Baru

1. Login ke sistem
2. Klik **"+ Tambah Laporan"** di dashboard
3. Isi form dengan informasi lengkap:
   - Unit/Departemen
   - Nama Pelapor
   - Modul SIMRS terkait
   - Jenis kesalahan
   - Deskripsi detail
   - Tanggal kejadian
   - Upload bukti (opsional)
4. Klik **"Simpan Laporan"**

### Mengelola Status Laporan (Admin)

1. Buka detail laporan
2. Klik **"Edit Status"**
3. Ubah status: Pending → In Progress → Resolved
4. Assign ke teknisi/admin
5. Simpan perubahan

### Melihat Statistik

- Akses menu **"Statistik"** untuk melihat:
  - Overview total laporan
  - Breakdown berdasarkan status
  - Chart jenis kesalahan
  - Laporan terbaru

## 🔌 API Endpoints

### Authentication
```http
GET  /                    # Login page
POST /                    # Login process
GET  /logout              # Logout
```

### Dashboard & Reports
```http
GET  /dashboard           # Main dashboard
GET  /statistik           # Statistics page
GET  /tambah              # Add report form
POST /tambah              # Create new report
GET  /detail/<id>         # Report details
GET  /edit_status/<id>    # Edit status form (Admin)
POST /edit_status/<id>    # Update status (Admin)
GET  /delete_laporan/<id> # Delete report (Admin)
```

### User Management (Admin Only)
```http
GET  /users               # User list
GET  /add_user            # Add user form
POST /add_user            # Create new user
```

### File Handling
```http
GET  /static/uploads/<filename>  # Download uploaded files
```

## 🛡️ Keamanan

### Implemented Security Measures

- ✅ **Password Hashing**: bcrypt dengan salt
- ✅ **CSRF Protection**: Flask-WTF tokens
- ✅ **Input Sanitization**: XSS prevention
- ✅ **File Upload Security**: Type & size validation
- ✅ **Session Security**: Secure cookies & timeout
- ✅ **SQL Injection Prevention**: SQLAlchemy ORM
- ✅ **Error Handling**: No sensitive data exposure
- ✅ **Logging**: Audit trail untuk aktivitas penting

### Security Best Practices

```python
# Password requirements
- Minimum 6 characters
- Hash dengan bcrypt
- No password in logs/errors

# File upload restrictions
- Max size: 16MB
- Allowed types: txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx
- Secure filename handling

# Session management
- 1 hour timeout
- Secure cookie settings
- CSRF token validation
```

### Production Security Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure secure headers
- [ ] Set up proper logging
- [ ] Regular security updates
- [ ] Database backup strategy
- [ ] Monitor failed login attempts

## 🤝 Kontribusi

Kami menyambut kontribusi dari komunitas! Berikut cara berkontribusi:

### Development Setup

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Setup development environment
4. Make changes dan test
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Create Pull Request

### Coding Standards

- Follow PEP 8 untuk Python code
- Use meaningful variable names
- Add docstrings untuk functions
- Write unit tests untuk new features
- Update documentation

### Testing

```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Linting
flake8 app.py models.py forms.py utils.py
```

## 🗺️ Roadmap

### Phase 2: UI/UX Enhancement (Q2 2026)
- [ ] Bootstrap 5 integration
- [ ] Responsive mobile design
- [ ] Dark mode support
- [ ] Advanced filtering & search
- [ ] Bulk operations

### Phase 3: Advanced Features (Q3 2026)
- [ ] Email notifications
- [ ] Real-time updates (WebSocket)
- [ ] Advanced reporting & export
- [ ] API endpoints (REST)
- [ ] Integration dengan sistem eksternal

### Phase 4: Enterprise Features (Q4 2026)
- [ ] Multi-tenant support
- [ ] Advanced analytics dashboard
- [ ] Workflow automation
- [ ] Mobile app (React Native)
- [ ] SSO integration

### Long-term Vision
- [ ] AI-powered issue categorization
- [ ] Predictive analytics
- [ ] Integration dengan monitoring tools
- [ ] Microservices architecture
- [ ] Cloud-native deployment

## 📊 Performance & Scalability

### Current Capacity
- **Concurrent Users**: 50-100 users
- **Database**: SQLite (development), PostgreSQL (production)
- **File Storage**: Local filesystem
- **Response Time**: < 200ms average

### Scaling Recommendations
- Use PostgreSQL/MySQL untuk production
- Implement Redis untuk session storage
- Add CDN untuk static files
- Consider load balancer untuk high traffic
- Implement database indexing

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Solution: Check database path dan permissions
chmod 755 instance/
chmod 664 instance/database.db
```

**File Upload Error**
```bash
# Solution: Check upload directory permissions
mkdir -p static/uploads
chmod 755 static/uploads
```

**Login Issues**
```bash
# Reset admin password
python -c "from app import app; from models import db, User; 
with app.app_context(): 
    admin = User.query.filter_by(username='admin').first(); 
    admin.set_password('newpassword'); 
    db.session.commit()"
```

## 🙏 Acknowledgments

- **Flask Community** - Framework yang luar biasa
- **SQLAlchemy Team** - ORM yang powerful
- **Bootstrap Team** - UI components
- **Contributors** - Semua yang berkontribusi pada project ini

---

<div align="center">

**[⬆ Kembali ke atas](#bap-simrs---sistem-pelaporan-kesalahan-simrs)**

</div>
