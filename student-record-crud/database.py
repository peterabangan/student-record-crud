#MySQL database connection and operations for the Student Record CRUD App

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.conn.cursor()

    def get_all_students(self):
        self.cursor.execute("SELECT id, first_name, last_name, age, grade, section, gender FROM students")
        return self.cursor.fetchall()
    def add_student(self, first_name, last_name, age, grade, section, gender):
        self.cursor.execute(
            "INSERT INTO students (first_name, last_name, age, grade, section, gender) VALUES (%s, %s, %s, %s, %s, %s)",
            (first_name, last_name, age, grade, section, gender)
        )
        self.conn.commit()
    def delete_student(self, id):
        self.cursor.execute("DELETE FROM students WHERE id=%s", (id,))
        self.conn.commit()

    def update_student(self, id, first_name, last_name, age, grade, section, gender):
        self.cursor.execute(
            "UPDATE students SET first_name=%s, last_name=%s, age=%s, grade=%s, section=%s, gender=%s WHERE id=%s",
            (first_name, last_name, age, grade, section, gender, id)  
        )
        self.conn.commit()

    def get_all_students_sorted(self):
        self.cursor.execute("SELECT * FROM students ORDER BY name ASC")
        return self.cursor.fetchall() 
    
    def get_all_students_by_id(self):
        self.cursor.execute("SELECT * FROM students ORDER BY id ASC")
        return self.cursor.fetchall() 