# Simple Student Record CRUD App

A desktop application for managing student records, built with Python and MySQL.

## Features
- Add, update, and delete student records
- View all records in a sortable table
- Input validation for all fields
- Click a record to auto-fill the input fields
- Secure database credentials using environment variables

## Tech Stack
- Python 3
- Tkinter (GUI)
- MySQL (Database)
- mysql-connector-python
- python-dotenv

## Getting Started

### Prerequisites
Make sure you have the following installed:
- Python 3
- MySQL Server
- MySQL Workbench (optional)

### Installation

1. Clone the repository
```
   git clone https://github.com/peterabangan/student-record-crud.git
```

2. Install dependencies
```
   pip install mysql-connector-python python-dotenv
```

3. Set up the database — open MySQL Workbench and run:
```sql
   CREATE DATABASE student_db;
   USE student_db;
   CREATE TABLE students (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       age INT,
       grade VARCHAR(10)
   );
```

4. Create a `.env` file in the project root:
```
   DB_HOST=localhost
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_NAME=student_db
```

5. Run the app
```
   python main.py
```

## Project Structure
```
student-record-crud/
├── main.py          # Entry point
├── ui.py            # GUI and application logic
├── database.py      # Database connection and queries
├── .env             # Your credentials (not uploaded to GitHub)
├── .env.example     # Template for setting up .env
└── README.md
```

## Author
Peter Abangan — [@peterabangan](https://github.com/peterabangan)