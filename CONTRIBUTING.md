# Contributing to BAP SIMRS

Terima kasih atas minat Anda untuk berkontribusi pada BAP SIMRS! Kami menyambut kontribusi dari komunitas.

## 🚀 Cara Berkontribusi

### 1. Fork Repository
- Fork repository ini ke akun GitHub Anda
- Clone fork ke local machine Anda

```bash
git clone https://github.com/yourusername/laporan_sistem_simrs.git
cd laporan_sistem_simrs
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run application
python app.py
```

### 3. Create Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 4. Make Changes
- Write clean, readable code
- Follow existing code style
- Add comments where necessary
- Test your changes thoroughly

### 5. Commit Changes

```bash
git add .
git commit -m "Add: amazing feature description"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/amazing-feature
```

Kemudian buat Pull Request di GitHub.

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### HTML/CSS
- Use semantic HTML elements
- Follow consistent indentation (2 spaces)
- Use meaningful class names
- Keep CSS organized and commented

### Database
- Use descriptive table and column names
- Add appropriate indexes
- Include foreign key constraints
- Document schema changes

## 🧪 Testing

Before submitting a pull request:

1. Test all functionality manually
2. Ensure no errors in browser console
3. Test with different user roles
4. Verify file upload functionality
5. Check responsive design

## 📋 Pull Request Guidelines

### PR Title Format
- `Add: new feature description`
- `Fix: bug description`
- `Update: component/feature description`
- `Remove: deprecated feature`

### PR Description
Include:
- What changes were made
- Why the changes were necessary
- How to test the changes
- Screenshots (if UI changes)
- Any breaking changes

### Example PR Description
```markdown
## Changes Made
- Added email notification feature for new reports
- Updated user model to include email field
- Created email templates for notifications

## Why
Users requested email notifications when reports are assigned to them.

## Testing
1. Create new report
2. Assign to user with email
3. Check that email is sent
4. Verify email content and formatting

## Screenshots
[Include relevant screenshots]
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment**: OS, Python version, browser
2. **Steps to reproduce**: Detailed steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Screenshots**: If applicable
6. **Error messages**: Full error text

## 💡 Feature Requests

For new features:

1. **Use case**: Why is this needed?
2. **Proposed solution**: How should it work?
3. **Alternatives**: Other ways to solve the problem
4. **Additional context**: Any other relevant information

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `security`: Security-related issues

## 📞 Getting Help

- Check existing issues and documentation
- Ask questions in GitHub Discussions
- Contact maintainers via email

## 🎯 Development Priorities

Current focus areas:
1. UI/UX improvements
2. Performance optimization
3. Additional security features
4. API development
5. Mobile responsiveness

Thank you for contributing to BAP SIMRS! 🙏