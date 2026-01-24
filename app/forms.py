from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, SelectField, DateTimeLocalField, PasswordField, RadioField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, Optional
from config import Config

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username wajib diisi'),
        Length(min=3, max=50, message='Username harus 3-50 karakter')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password wajib diisi'),
        Length(min=4, message='Password minimal 4 karakter')
    ])

class LaporanForm(FlaskForm):
    unit = SelectField('Unit', 
        choices=[
            ('IGD', 'IGD (Instalasi Gawat Darurat)'),
            ('Rawat Inap', 'Rawat Inap'),
            ('Rawat Jalan', 'Rawat Jalan'),
            ('ICU', 'ICU (Intensive Care Unit)'),
            ('NICU', 'NICU (Neonatal ICU)'),
            ('Kamar Operasi', 'Kamar Operasi'),
            ('Radiologi', 'Radiologi'),
            ('Laboratorium', 'Laboratorium'),
            ('Farmasi', 'Farmasi'),
            ('Rekam Medis', 'Rekam Medis'),
            ('Kasir', 'Kasir'),
            ('Administrasi', 'Administrasi'),
            ('IT', 'IT / Teknologi Informasi'),
            ('Lainnya', 'Lainnya')
        ],
        validators=[DataRequired(message='Unit wajib dipilih')]
    )
    pelapor = StringField('Pelapor', validators=[
        DataRequired(message='Nama pelapor wajib diisi'),
        Length(max=100, message='Nama pelapor maksimal 100 karakter')
    ])
    modul_simrs = RadioField('Modul SIMRS', 
        choices=[
            ('Pendaftaran & Front Office', '📋 Pendaftaran & Front Office'),
            ('Administrasi Pasien', '🏥 Administrasi Pasien'),
            ('Rekam Medis Elektronik (RME/EMR)', '📝 Rekam Medis Elektronik (RME/EMR)'),
            ('Penunjang Medis', '🧪 Penunjang Medis (Lab, Radiologi, Fisioterapi)'),
            ('Farmasi', '💊 Farmasi'),
            ('Keuangan / Billing', '💳 Keuangan / Billing'),
            ('Manajemen Inventaris & Aset', '📦 Manajemen Inventaris & Aset'),
            ('Sumber Daya Manusia (SDM)', '👥 Sumber Daya Manusia (SDM)'),
            ('Laporan & Pelaporan', '📊 Laporan & Pelaporan')
        ],
        validators=[DataRequired(message='Modul SIMRS wajib dipilih')]
    )
    jenis_kesalahan = SelectField('Jenis Kesalahan', 
        choices=[
            ('Data Pasien', 'Data Pasien'),
            ('Transaksi', 'Transaksi'),
            ('Sistem Error', 'Sistem Error'),
            ('Lainnya', 'Lainnya')
        ],
        validators=[DataRequired(message='Jenis kesalahan wajib dipilih')]
    )
    deskripsi = TextAreaField('Deskripsi', validators=[
        DataRequired(message='Deskripsi wajib diisi'),
        Length(max=1000, message='Deskripsi maksimal 1000 karakter')
    ])
    tgl_kejadian = DateTimeLocalField('Tanggal Kejadian', validators=[
        DataRequired(message='Tanggal kejadian wajib diisi')
    ])
    bukti_file = FileField('Bukti File', validators=[
        Optional(),
        FileAllowed(Config.ALLOWED_EXTENSIONS, 
                   message='File harus berformat: txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx'),
        FileSize(max_size=Config.MAX_CONTENT_LENGTH, 
                message='Ukuran file maksimal 16MB')
    ])

class UserForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username wajib diisi'),
        Length(min=3, max=50, message='Username harus 3-50 karakter')
    ])
    email = StringField('Email', validators=[
        Optional(),
        Email(message='Format email tidak valid'),
        Length(max=100, message='Email maksimal 100 karakter')
    ])
    unit = SelectField('Unit', 
        choices=[
            ('', 'Pilih Unit (Opsional)'),
            ('IGD', 'IGD (Instalasi Gawat Darurat)'),
            ('Rawat Inap', 'Rawat Inap'),
            ('Rawat Jalan', 'Rawat Jalan'),
            ('ICU', 'ICU (Intensive Care Unit)'),
            ('NICU', 'NICU (Neonatal ICU)'),
            ('Kamar Operasi', 'Kamar Operasi'),
            ('Radiologi', 'Radiologi'),
            ('Laboratorium', 'Laboratorium'),
            ('Farmasi', 'Farmasi'),
            ('Rekam Medis', 'Rekam Medis'),
            ('Kasir', 'Kasir'),
            ('Administrasi', 'Administrasi'),
            ('IT', 'IT / Teknologi Informasi'),
            ('Lainnya', 'Lainnya')
        ],
        validators=[Optional()]
    )
    password = PasswordField('Password', validators=[
        DataRequired(message='Password wajib diisi'),
        Length(min=6, message='Password minimal 6 karakter')
    ])
    role = SelectField('Role', 
        choices=[
            ('admin', 'Administrator'),
            ('user', 'User')
        ],
        validators=[DataRequired(message='Role wajib dipilih')]
    )

class EditStatusForm(FlaskForm):
    status = SelectField('Status', 
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved')
        ],
        validators=[DataRequired(message='Status wajib dipilih')]
    )
    assigned_to = SelectField('Assign ke', 
        choices=[],  # Will be populated dynamically
        validators=[Optional()],
        coerce=int
    )
    
    def __init__(self, *args, **kwargs):
        super(EditStatusForm, self).__init__(*args, **kwargs)
        # Populate assigned_to choices with users
        from app.models import User
        self.assigned_to.choices = [(0, 'Tidak ada')] + [(u.id, u.username) for u in User.query.all()]

class SearchForm(FlaskForm):
    search_query = StringField('Pencarian', validators=[
        Optional(),
        Length(max=200, message='Pencarian maksimal 200 karakter')
    ])
    unit_filter = SelectField('Unit', 
        choices=[('', 'Semua Unit')],
        validators=[Optional()]
    )
    status_filter = SelectField('Status', 
        choices=[
            ('', 'Semua Status'),
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved')
        ],
        validators=[Optional()]
    )
    jenis_filter = SelectField('Jenis Kesalahan', 
        choices=[
            ('', 'Semua Jenis'),
            ('Data Pasien', 'Data Pasien'),
            ('Transaksi', 'Transaksi'),
            ('Sistem Error', 'Sistem Error'),
            ('Lainnya', 'Lainnya')
        ],
        validators=[Optional()]
    )
    pelapor_filter = StringField('Pelapor', validators=[
        Optional(),
        Length(max=100, message='Nama pelapor maksimal 100 karakter')
    ])
    date_from = DateField('Dari Tanggal', validators=[Optional()])
    date_to = DateField('Sampai Tanggal', validators=[Optional()])
    sort_by = SelectField('Urutkan berdasarkan', 
        choices=[
            ('id', 'ID Laporan'),
            ('created_at', 'Tanggal Dibuat'),
            ('tgl_kejadian', 'Tanggal Kejadian'),
            ('unit', 'Unit'),
            ('pelapor', 'Pelapor'),
            ('status', 'Status'),
            ('jenis_kesalahan', 'Jenis Kesalahan')
        ],
        default='id',
        validators=[Optional()]
    )
    sort_order = SelectField('Urutan', 
        choices=[
            ('asc', 'Terkecil ke Terbesar'),
            ('desc', 'Terbesar ke Terkecil')
        ],
        default='asc',
        validators=[Optional()]
    )

class SaveSearchForm(FlaskForm):
    name = StringField('Nama Pencarian', validators=[
        DataRequired(message='Nama pencarian wajib diisi'),
        Length(min=3, max=100, message='Nama pencarian harus 3-100 karakter')
    ])