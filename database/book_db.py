from database.db_connection import DBManager
from schemas import CreateBook, UpdateBook


class BookDB:
    def __init__(self, db:DBManager):
        self.db = db

    def create_book(self, data: CreateBook):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        book_data = data.model_dump()
        cursor.execute("""insert into books (title, author, genre)
                        values (%s, %s, %s);""", (book_data["title"], book_data["author"], book_data["genre"]))
        connection.commit()
        cursor.close()
        return
    
    def get_all_books(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from books;")
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_book_by_id(self, id:int):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from books where id = %s;",(id,))
        result = cursor.fetchone()
        cursor.close()
        return result
   
   
    def update_book(self, id: int, data: UpdateBook):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        book_data = data.model_dump(exclude_unset=True)

        fields = []
        values = []

        for key, value in book_data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        if not fields:
            cursor.close()
            return False

        query = f"""
            UPDATE books
            SET {", ".join(fields)}
            WHERE id = %s
        """

        values.append(id)

        cursor.execute(query, tuple(values))

        connection.commit()
        cursor.close()

        return True
    def set_available(self, id, val, member_id):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        if val == True:
            cursor.execute("""update books 
                           set is_available = %s, 
                           borrowed_by_member_id = %s
                           where id = %s;
            """, (val, None, id))

        else:
            cursor.execute("""update books 
                           set is_available = %s, 
                           borrowed_by_member_id = %s
                           where id = %s;
            """, (val, member_id, id))

        connection.commit()
        cursor.close()
        return    
    
    def count_total_books(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("select count(*) from books;")
        res = cursor.fetchone()[0]
        cursor.close()
        return res
    
    def count_available_books(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("select count(*) from books where is_available = %s;", (True,))

        res = cursor.fetchone()[0]
        cursor.close()
        return res
    
    def count_borrowed_books(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("select count(*) from books where is_available = %s;", (False,))

        res = cursor.fetchone()[0]
        cursor.close()
        return res
    
    def count_by_genre(self, genre):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("select count(*) from books where genre = %s;", (genre,))

        res = cursor.fetchone()[0]
        cursor.close()
        return res
    

    def count_active_borrows_by_member(self, member_id):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM books
            WHERE borrowed_by_member_id = %s
            AND is_available = %s
            """,
            (member_id, False)
        )

        result = cursor.fetchone()[0]
        cursor.close()

        return result