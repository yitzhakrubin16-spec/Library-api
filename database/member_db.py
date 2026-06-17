from database.db_connection import DBManager
from schemas import CreateMember, UpdateMember

class MemberDB:
    def __init__(self, db:DBManager):
        self.db = db

    def create_member(self, data: CreateMember):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        member_data = data.model_dump()

        cursor.execute("""insert into members (name, email)
                        values (%s, %s);""", (member_data["name"], member_data["email"]))
        connection.commit()
        cursor.close()
        return
    
    def get_all_members(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("select * from members;")
        res = cursor.fetchall()
        cursor.close()
        return res
    
    def get_member_by_id(self, id):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("select * from members where id = %s;", (id,))
        res = cursor.fetchone()
        cursor.close()
        return res
    
    def update_member(self, id: int, data: UpdateMember):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        member_data = data.model_dump(exclude_unset=True)

        fields_to_update = []
        values = []

        for key, value in member_data.items():
            fields_to_update.append(f"{key} = %s")
            values.append(value)

        if not fields_to_update:
            cursor.close()
            return False

        query = f"""
            UPDATE members
            SET {", ".join(fields_to_update)}
            WHERE id = %s
        """

        values.append(id)

        cursor.execute(query, tuple(values))

        connection.commit()
        cursor.close()

        return True

    def deactivate_member(self, id):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""update members 
                           set is_active = %s
                           where id = %s;
            """, (False, id))

        connection.commit()
        cursor.close()

        return True
    
    def activate_member(self, id):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""update members 
                           set is_active = %s
                           where id = %s;
            """, (True, id))

        connection.commit()
        cursor.close()

        return True
    
    def increment_borrows(self, id):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""update members 
                           set total_borrows = total_borrows + 1
                           where id = %s;
            """, (id,))

        connection.commit()
        cursor.close()

        return True
    
    def count_active_members(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("select count(*) from members where is_active = %s;", (True,))

        res = cursor.fetchone()[0]
        cursor.close()
        return res
    
    def get_top_member(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id AS member_id,
                total_borrows AS borrowed
            FROM members
            ORDER BY total_borrows DESC
            LIMIT 1;
        """)

        result = cursor.fetchone()
        cursor.close()

        return result
    
    def get_member_by_email(self, email: str):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM members
            WHERE email = %s
            """,
            (email,)
        )

        member = cursor.fetchone()
        cursor.close()

        return member