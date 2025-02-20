# Home Server WOL

**Home Server WOL** is a web application designed to manage **Wake-on-LAN (WOL)** services for devices within the local network. It allows you to remotely power on computers via a secure and user-friendly web interface.

## 🚀 Features
- ✅ Turn on devices in the local network using WOL.
- 🔑 Authentication via access key.
- 🏗 Flask-based architecture for a lightweight and efficient implementation.
- 🗃 Local database for managing registered devices.

## 📋 Requirements
### Necessary installations:
- 🐍 Python 3.x
- 🔥 Flask
- 🛢 SQLite (for the local database)
- 📦 Project dependencies (specified in `requirements.txt`)

### Environment Configuration
To ensure the application works correctly, create a `.env` file in the root of the project with the following variables:

```ini
DB_PATH=path_to_database.db
AUTH_KEY=authentication_key
SECRET_KEY=session_secret_key
ADMIN_USER=admin_username
ADMIN_AUTH=admin_authentication_key
ADMIN_EMAIL=admin_email@example.com
```

## 📌 User Configuration
Currently, users must be manually inserted into the database. In a future update, user management will be available from an administrator role.

To manually add users, you can use SQLite:
```sh
sqlite3 path_to_database.db
```
Then execute `INSERT` commands to add records to the users table.

## 🛠 Installation
Clone the repository and navigate to the project directory:
```sh
git clone https://github.com/pruden96/wol-home-server.git
cd wol-home-server
```
Install dependencies:
```sh
pip install -r requirements.txt
```
Run the application:
```sh
python app.py
```

## 🔐 Security
- ⚠️ It is recommended to change the default keys in the `.env` file before deploying the application.
- 🔒 In production, consider using **HTTPS** for secure requests.

## 📢 Upcoming Improvements
- [ ] Implement user management from the admin interface.
- [ ] Enhance authentication with advanced roles and permissions.
- [ ] Add support for more devices and configuration options.

---
📌 **Author:** [Carlos Prudencio](https://github.com/pruden96)

