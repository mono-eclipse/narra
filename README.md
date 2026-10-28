# Narra — Project and Material Management Application

## About the Project

**Narra** is a desktop application for viewing and managing projects and related materials. The project is developed in Python with a PySide6 graphical user interface and uses Microsoft SQL Server for data storage.

The application is intended for educational use and demonstrating work with a relational database, a graphical user interface, and CRUD operations (Create, Read, Update, Delete).

## Key Features

- Authentication via a SQL Server account.
- Viewing and searching for projects.
- Adding and editing projects.
- Viewing all materials and materials of a specific project.
- Filtering materials by type.
- Adding materials with automatic creation of related records.
- Editing and deleting materials.
- Checking for dependencies before deleting a project.
- Using transactions for related write and delete operations.

## Technologies Used

- **Python** — core development language.
- **PySide6** — graphical user interface.
- **pyodbc** — SQL Server connection.
- **Microsoft SQL Server** — data storage.
- **Microsoft ODBC Driver for SQL Server** — database connection driver.
- **Git and GitHub** — version control and source code hosting.

## Project Structure

```text
narra/
├── app/
│   ├── __init__.py
│   ├── login_window.py
│   └── main_window.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── schema.sql
│   ├── seed.sql
│   └── setup_demo_accounts.sql
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

To run the application, you need:

- Windows and Python 3.10 or a compatible Python version.
- Microsoft SQL Server.
- Microsoft ODBC Driver for SQL Server.
- A SQL Server account with the necessary database access permissions.
- Access to a SQL Server instance where the database will be hosted.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <URL-репозитория>
cd narra
```

Replace `<URL-репозитория>` with your GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If using Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create the database

In Microsoft SQL Server Management Studio (SSMS), open and execute the SQL scripts from the `database` directory in the following order:

1. **`schema.sql`** — creates the `NarraDB` database, tables, and integrity constraints.
2. **`seed.sql`** — adds initial values to the material types reference table.
3. **`setup_demo_accounts.sql`** — creates demo SQL Server accounts, database users, and assigns roles.

Before executing the last script, read the instructions inside it and replace all placeholder passwords with your own test values. Do not use real passwords and do not publish them in the repository.

For the demo accounts to work, SQL Server Authentication (Mixed Mode) must be enabled. After changing the authentication mode, a restart of the SQL Server service may be required.

The scripts are intended for the initial database deployment. Do not run them again without checking their contents and the database state.

### 5. Connection configuration

The application uses the following environment variables:

| Variable | Purpose | Default value |
|---|---|---|
| `NARRA_DB_SERVER` | SQL Server name or address | `localhost` |
| `NARRA_DB_NAME` | Database name | `NarraDB` |
| `NARRA_ODBC_DRIVER` | Name of the installed ODBC driver | `ODBC Driver 18 for SQL Server` |

If necessary, set the environment variable values according to your SQL Server configuration.

For example, in PowerShell:

```powershell
$env:NARRA_DB_SERVER = "localhost"
$env:NARRA_DB_NAME = "NarraDB"
$env:NARRA_ODBC_DRIVER = "ODBC Driver 18 for SQL Server"
```

If SQL Server is installed on another computer or uses a named instance, specify the corresponding server address.

The application login uses SQL Server credentials. Enter the credentials created for your environment or the demo credentials from `setup_demo_accounts.sql`.

Do not store passwords in source code, configuration files intended for publication, or in plain text in the repository.

### 6. Run the application

From the project root directory, run:

```bash
python main.py
```

After launching, the authorization window will open. To work with the application, a connection to SQL Server and a database with the prepared structure are required.

## Theoretical Analysis of Potential Vulnerabilities

Below are three potential security risks to consider during further development of the application. Their description does not imply that the exploitation of each risk has been confirmed by practical testing.

### 1. Insufficient data isolation between users

**Risk description:** the application displays the username of the logged-in user, but this alone does not provide separation of projects and materials by owner. If users work with a shared database and have the same access rights, a user could potentially access data not intended exclusively for them.

**Potential consequences:** unauthorized reading, modification, or deletion of other users' data within the rights granted to the account.

**Mitigation measures:**

- Implement a data ownership model and operation-level rights checking.
- Restrict SQL Server rights to the minimum necessary permissions.
- Do not rely solely on hiding buttons or UI elements.
- Check user rights before every sensitive operation.

### 2. Insufficient server authentication in secure connections

**Risk description:** if the `TrustServerCertificate=yes` parameter is used to connect to SQL Server, the connection is encrypted, but the verification of trust in the server certificate is bypassed. Under certain conditions, this increases the risk of connecting to a spoofed server and a Man-in-the-Middle (MITM) attack.

**Potential consequences:** in a successful attack, an attacker located in the data transmission path could potentially intercept or modify the exchange between the client and the server.

**Mitigation measures:**

- Configure a valid SQL Server certificate trusted by the client system.
- Use `TrustServerCertificate=no`.
- Verify that the server name matches the name in the certificate.
- Do not connect to untrusted servers and networks without the necessary protection measures.

### 3. Disclosure of technical details through error messages

**Risk description:** if the application shows the user the full text of SQL Server and driver exceptions, the messages may reveal the internal structure of the database, object names, access rights information, and configuration details.

**Potential consequences:** it may become easier for an attacker to determine the database structure and choose a further attack vector.

**Mitigation measures:**

- Show the user brief and understandable error messages.
- Save exception details in a secure log.
- Exclude passwords, connection strings, and other secrets from the logs.
- Restrict access to diagnostic logs.

## Project Limitations

Narra is intended for educational purposes and demonstrating the interaction of a desktop application with a relational database.

Before use in a real organization, a full security audit must be conducted, the data access model must be reviewed, SQL Server certificate verification must be configured, and a backup procedure must be prepared.

## Conclusion

Narra demonstrates the basic principles of desktop application development, interaction with a relational database, and the execution of related operations with data integrity in mind.

The SQL scripts in the `database` directory allow you to prepare the database structure, populate the material types reference table, and set up demo accounts. The listed security risks require further analysis and testing in a controlled educational environment.