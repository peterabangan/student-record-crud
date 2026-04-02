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
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()
    def add_student(self, name, age, grade):
        self.cursor.execute(
            "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
            (name, age, grade)
        )
        self.conn.commit()
    def delete_student(self, id):
        self.cursor.execute("DELETE FROM students WHERE id=%s", (id,))
        self.conn.commit()

    def update_student(self, id, name, age, grade):
        self.cursor.execute(
            "UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s",
            (name, age, grade, id)
        )
        self.conn.commit()