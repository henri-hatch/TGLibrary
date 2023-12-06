import sqlite3

class Database:
    def __init__(self, db_file="tgl.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()


    def get_all_books_data(self):
        query = """
            SELECT
                Books.title,
                Books.author,
                GROUP_CONCAT(Subjects.subject_name, ', ') AS subjects,
                Libraries.name AS location,
                Books.isbn,
                Books.copies,
                Books.loaned
            FROM
                Books
            LEFT JOIN BookSubjects ON Books.book_id = BookSubjects.book_id
            LEFT JOIN Subjects ON BookSubjects.subject_id = Subjects.subject_id
            LEFT JOIN Libraries ON Books.library_id = Libraries.library_id
            GROUP BY
                Books.book_id, Books.library_id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_books_by_title(self, title):
        query = f"""
            SELECT
                Books.title,
                Books.author,
                GROUP_CONCAT(Subjects.subject_name, ', ') AS subjects,
                Libraries.name AS location,
                Books.isbn,
                Books.copies,
                Books.loaned
            FROM
                Books
            LEFT JOIN BookSubjects ON Books.book_id = BookSubjects.book_id
            LEFT JOIN Subjects ON BookSubjects.subject_id = Subjects.subject_id
            LEFT JOIN Libraries ON Books.library_id = Libraries.library_id
            WHERE
                Books.title LIKE ?
            GROUP BY
                Books.book_id, Books.library_id
        """
        self.cursor.execute(query, ("%" + title + "%",))
        return self.cursor.fetchall()


    def get_books_by_author(self, author):
        query = """
            SELECT
                Books.title,
                Books.author,
                GROUP_CONCAT(Subjects.subject_name, ', ') AS subjects,
                Libraries.name AS location,
                Books.isbn,
                Books.copies,
                Books.loaned

            FROM
                Books
            LEFT JOIN BookSubjects ON Books.book_id = BookSubjects.book_id
            LEFT JOIN Subjects ON BookSubjects.subject_id = Subjects.subject_id
            LEFT JOIN Libraries ON Books.library_id = Libraries.library_id
            WHERE
                Books.author LIKE ?
            GROUP BY
                Books.book_id, Books.library_id
        """
        self.cursor.execute(query, ("%" + author + "%",))
        return self.cursor.fetchall()


    def get_books_by_subject(self, subject):
        query = """
            SELECT
                Books.title,
                Books.author,
                GROUP_CONCAT(Subjects.subject_name, ', ') AS subjects,
                Libraries.name AS location,
                Books.isbn,
                Books.copies,
                Books.loaned
            FROM
                Books
            LEFT JOIN BookSubjects ON Books.book_id = BookSubjects.book_id
            LEFT JOIN Subjects ON BookSubjects.subject_id = Subjects.subject_id
            LEFT JOIN Libraries ON Books.library_id = Libraries.library_id
            WHERE
                Subjects.subject_name LIKE ?
            GROUP BY
                Books.book_id, Books.library_id
        """
        self.cursor.execute(query, ("%" + subject + "%",))
        return self.cursor.fetchall()


    def get_books_by_location(self, location):
        query = """
            SELECT
                Books.title,
                Books.author,
                GROUP_CONCAT(Subjects.subject_name, ', ') AS subjects,
                Libraries.name AS location,
                Books.isbn,
                Books.copies,
                Books.loaned
            FROM
                Books
            LEFT JOIN BookSubjects ON Books.book_id = BookSubjects.book_id
            LEFT JOIN Subjects ON BookSubjects.subject_id = Subjects.subject_id
            LEFT JOIN Libraries ON Books.library_id = Libraries.library_id
            WHERE
                Libraries.name LIKE ?
            GROUP BY
                Books.book_id, Books.library_id
        """
        self.cursor.execute(query, ("%" + location + "%",))
        return self.cursor.fetchall()


    def get_books_by_isbn(self, isbn):
        query = """
            SELECT
                Books.title,
                Books.author,
                GROUP_CONCAT(Subjects.subject_name, ', ') AS subjects,
                Libraries.name AS location,
                Books.isbn,
                Books.copies,
                Books.loaned
            FROM
                Books
            LEFT JOIN BookSubjects ON Books.book_id = BookSubjects.book_id
            LEFT JOIN Subjects ON BookSubjects.subject_id = Subjects.subject_id
            LEFT JOIN Libraries ON Books.library_id = Libraries.library_id
            WHERE
                Books.isbn LIKE ?
            GROUP BY
                Books.book_id, Books.library_id
        """
        self.cursor.execute(query, ("%" + isbn + "%",))
        return self.cursor.fetchall()


    def add_library(self, library_name):
        query = """
            INSERT INTO Libraries (name)
            VALUES (?)
        """
        self.cursor.execute(query, (library_name,))
        self.conn.commit()


    def add_subject(self, subject_name):
        query = """
            INSERT INTO Subjects (subject_name)
            VALUES (?)
        """
        self.cursor.execute(query, (subject_name,))
        self.conn.commit()


    def add_book(self, title, author, location_id, isbn, copies, loaned, notes):
        query = """
            INSERT INTO Books (title, author, library_id, isbn, copies, loaned, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        # Commit and then return the book ID of the new book
        self.cursor.execute(query, (title, author, location_id, isbn, copies, loaned, notes))
        self.conn.commit()
        return self.cursor.lastrowid


    def get_libraries(self):
        query = """
            SELECT
                name
            FROM
                Libraries
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_library_id(self, library_name):
        query = """
            SELECT
                library_id
            FROM
                Libraries
            WHERE
                name = ?
        """
        self.cursor.execute(query, (library_name.strip("{}"),))
        num = self.cursor.fetchone()
        return num[0]


    def get_subjects(self):
        query = """
            SELECT
                subject_name
            FROM
                Subjects
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_subject_id(self, subject_name):
        query = """
            SELECT
                subject_id
            FROM
                Subjects
            WHERE
                subject_name = ?
        """
        self.cursor.execute(query, (subject_name[0],))
        num = self.cursor.fetchone()
        return num[0]


    def add_book_subject(self, book_id, subject_id):
        query = """
            INSERT INTO BookSubjects (book_id, subject_id)
            VALUES (?, ?)
        """
        self.cursor.execute(query, (book_id, subject_id))
        self.conn.commit()


    def close_connection(self):
        self.conn.close()


# Example usage:
if __name__ == "__main__":
    db = Database()
    books_data = db.get_all_books_data()
    db.close_connection()

    for book in books_data:
        print(book)
