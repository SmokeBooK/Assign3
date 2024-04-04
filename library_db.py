import sqlite3
from Book import Book
from tkinter import simpledialog


class LibraryDB:
    def __init__(self, db_path="library.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

    def create_tables(self):
        with self.connection:
            cursor = self.connection.cursor()

            # Book table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    ISBN TEXT NOT NULL,
                    category TEXT NOT NULL,
                    is_borrowed INTEGER DEFAULT 0,
                    borrower TEXT,
                    due_date TEXT
                )
            ''')

            # User table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')

            # Borrow Books table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrowed_books (
                    id INTEGER PRIMARY KEY,
                    book_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

    def add_book(self, book):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, ISBN, category, is_borrowed, borrower)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (book.title, book.author, book.ISBN, book.category, book.is_borrowed, book.borrower))

    def remove_book_by_id(self, book_id):
        with self.connection:
            cursor = self.connection.cursor()

            # ตรวจสอบว่ามีผู้ใช้ยืมหนังสือเล่มนี้หรือไม่
            cursor.execute('SELECT * FROM borrowed_books WHERE book_id=?', (book_id,))
            borrowed_info = cursor.fetchone()

            if borrowed_info:
                print(f"Book with ID {book_id} is borrowed by a user. It cannot be removed.")
                return False
            else:
                # หากไม่มีผู้ใช้ยืมหนังสือ ให้ลบหนังสือออก
                cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
                print(f"Book with ID {book_id} removed from the library.")

                # ลบหนังสือออกจากตาราง
                cursor.execute('DELETE FROM borrowed_books WHERE book_id=?', (book_id,))

                return True

    def toggle_availability(self, book_id):
        with self.connection:
            cursor = self.connection.cursor()

            # เรียกดูค่า is_borrowed ปัจจุบันของหนังสือ
            cursor.execute('SELECT is_borrowed FROM books WHERE id=?', (book_id,))
            current_availability = cursor.fetchone()[0]

            # คำนวณค่า is_borrowed ใหม่และอัปเดตในฐานข้อมูล
            new_availability = 1 if current_availability == 0 else 0
            cursor.execute('UPDATE books SET is_borrowed=? WHERE id=?', (new_availability, book_id))

            # หาก is_borrowed เปลี่ยนจาก 0 เป็น 1 ให้บันทึก ID ผู้ใช้ที่ยืมหนังสือ
            if new_availability == 1:
                borrower_name = simpledialog.askstring("Borrower Information", "Enter the borrower's name:")
                cursor.execute('UPDATE books SET borrower=? WHERE id=?', (borrower_name, book_id))
            else:
                # หาก is_borrowed เปลี่ยนจาก 1 เป็น 0 ให้ล้างค่า ID ผู้ใช้ที่ยืมหนังสือ
                cursor.execute('UPDATE books SET borrower=NULL WHERE id=?', (book_id,))

    def remove_book(self, title):
        # ลบหนังสือออกจากฐานข้อมูลโดยใช้ ID แทนชื่อหนังสือ
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM books WHERE title=?', (title,))
            book_info = cursor.fetchone()

            if book_info:
                book_id = book_info[0]
                return self.remove_book_by_id(book_id)
            else:
                print(f"Book with title {title} not found.")
                return False

    def list_books(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM books')
            books = cursor.fetchall()
            return [self.fetch_book_as_dict(book) for book in books]

    def search_book(self, title):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM books WHERE title=?', (title,))
            result = cursor.fetchone()
            return Book(*result[1:]) if result else None  # ข้ามคอลัมน์แรก (id) ของตาราง
    @staticmethod
    def fetch_book_as_dict(result):
        if result:
            return {
                'id': result[0],
                'title': result[1],
                'author': result[2],
                'ISBN': result[3],
                'category': result[4],
                'is_borrowed': result[5],
                'borrower': result[6],
                'due_date': result[7]
            }
        else:
            return None

    def add_user(self, user):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE name=?', (user.name,))
            existing_user = cursor.fetchone()

            # เพิ่มผู้ใช้ใหม่หากยังไม่มีอยู่
            if existing_user is None:
                cursor.execute('''
                    INSERT INTO users (name, email)
                    VALUES (?, ?)
                ''', (user.name, f"{user.name.lower()}@example.com"))

    def list_users(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            return [{'name': user[1], 'email': user[2]} for user in users]

    def add_borrower(self, book_id, user_id, borrower_name):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO borrowed_books (book_id, user_id)
                VALUES (?, ?)
            ''', (book_id, user_id))

            # อัปเดตสถานะของหนังสือ
            cursor.execute('''
                UPDATE books SET is_borrowed=?, borrower=? WHERE id=?
            ''', (1, borrower_name, book_id))

            print(f"Book with ID {book_id} borrowed by {borrower_name}.")

    def remove_user_by_name(self, username):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM users WHERE name=?', (username,))
            print(f"User with name '{username}' removed from the library.")

    def get_book_by_id(self, book_id):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
            book_info = cursor.fetchone()
            if book_info:
                return {
                    'id': book_info[0],
                    'title': book_info[1],
                    'author': book_info[2],
                    'ISBN': book_info[3],
                    'category': book_info[4],
                    'is_borrowed': book_info[5],
                    'borrower': book_info[6]
                }
            else:
                return None

    def update_book(self, isbn, updated_title, updated_author, updated_isbn, updated_category, updated_is_borrowed,
                    updated_borrower):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE books
                SET title=?, author=?, ISBN=?, category=?, is_borrowed=?, borrower=?
                WHERE ISBN=?
            ''', (
                updated_title, updated_author, updated_isbn, updated_category, updated_is_borrowed, updated_borrower,
                isbn))
