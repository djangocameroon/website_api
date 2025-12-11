🌍 Available languages: **English** | [Français](README.md)

# Website API

A RESTful API built with Django and Django REST Framework to manage website content, including blog features, events, and user management.

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (for caching and queues)
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/charles-kamga/website_api.git
   cd website_api
   ```

2. **Set up the virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the PostgreSQL database**
   ```sql
   -- Connect to PostgreSQL
   sudo -u postgres psql
   
   -- Create the database
   CREATE DATABASE django_website_db;
   
   -- Create a user (replace values in brackets)
   CREATE USER [db_user] WITH PASSWORD '[your_password]';
   
   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE django_website_db TO [db_user];
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your settings:
   - `DB_*`: Database connection parameters  
   - `SECRET_KEY`: Django secret key (generate a new one for production)  
   - `EMAIL_*`: SMTP configuration for emails  
   - `TWILLIO_*`: Twilio credentials for SMS verification (optional)

6. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at: http://127.0.0.1:8000/  
   The admin interface will be available at: http://127.0.0.1:8000/admin/

## 🏗 Project Structure

```
website_api/
├── apps/                  # Django applications
│   ├── blog/             # Blog article management
│   ├── events/           # Events management
│   └── users/            # User management and authentication
├── config/               # Project configuration
├── documentation/        # Additional documentation
├── middlewares/          # Custom middlewares
├── services/             # Business logic
└── website_api/          # Main project settings
```

## 🔧 Environment Variables

| Variable | Description | Default Value |
|----------|-------------|----------------|
| `DEBUG` | Debug mode | `True` in development, `False` in production |
| `SECRET_KEY` | Django secret key | Must be defined in production |
| `DB_*` | Database settings | See `.env.example` |
| `EMAIL_*` | SMTP configuration | Must be set for emails |
| `REDIS_URL` | Redis connection URL | `redis://127.0.0.1:6379` |
| `TWILLIO_*` | Twilio credentials (SMS) | Optional |

## 📚 API Documentation

The API documentation is available at `/api/docs/` when the server is running.

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.users
```

## 🛠 Development Tools

- **Linting**: `flake8`
- **Formatting**: `black`
- **Import sorting**: `isort`

## 🤝 Contributing

Contributions are welcome! Here’s how to contribute:

1. Fork the project  
2. Create a feature branch (`git checkout -b feature/my-new-feature`)  
3. Commit your changes (`git commit -am 'Add new feature'`)  
4. Push the branch (`git push origin feature/my-new-feature`)  
5. Create a Pull Request  

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For any questions, please open an issue on GitHub or contact the development team.
