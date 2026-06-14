# Project Library-api

## System description

מערכת לניהול ספרייה
המערכת עובדת באמצעות שרת API שמתחבר למסד נתונים MySQL המכיל 2 טבלאות נתונים.

טבלת נתונים אחד הוא של הספרים בספרייה (Books).
לכל ספר יש מספר מזהה, כותרת, מחבר, ז'אנר, סטטוס השאלה ובמידה והוא מושאל, מספר המזהה של החבר ספרייה שמחזיק אותו.

טבלת הנתונים השני הוא של חברי הספרייה (Members).
לכל חבר יש מספר מזהה, שם, אימייל, סטטוס פעילות ומונה השאלות.

## Creating MySQL with docker
בcmd, הרץ את הפקודה:
```text
docker run --name my-mysql 
-e MYSQL_ROOT_PASSWORD=secret 
-e MYSQL_DATABASE=library_db 
-p 3306:3306 
-v project_api_db:/var/lib/mysql 
-d mysql:latest
```

## File structure

```text
library-api/
│
├── main.py
│
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
│
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
│
├── logs/
│   └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Tables structure


### Books

| id | title | author | genere | is_avaliable | borrowed_by_member_id |
|----|-------|--------|--------|--------------|-----------------------|
|מפתח לכל ספר|כותרת הספר|שם המחבר|ז'אנר|האם הספר זמין להשאלה|מספר החבר ששואל את הספר|



### Members

| id | name | email | is_active | total_borrows |
|----|------|-------|-----------|---------------|
|מפתח לכל משתמש|שם המשתמש| כתובת המייל| האם המשתמש פעיל|מונה השאלות|

## System rules

 ### 1. יצירת ספר
 המשתמש שולח כותרת, שם המחבר וז'אנר.
 המערכת מגדירה בעצמה את מפתח הספר, שהוא זמין ושהוא לא מושאל כרגע.

 ### 2. הז'אנר
  הז'אנר חייב להיות אחד מהבאים: 
  Fiction / Non-Fiction / Science / History / Other
  כל ערך אחר מחזיר שגיאה.
  מוודאים בהוספה ועדכון של ספר.

  ### 3. יצירת חבר
  המשתמש שולח שם ואימייל
  המערכת מגדירה מפתח חבר, שהוא פעיל ושהוא משאיל 0 ספרים

  ### 4. אימייל
  חייב להיות ייחודי, אם לא מחזיר שגיאה

  ### 5. חבר לא פעיל 
  אם החבר לא פעיל, אי אפשר להשאיל לו ספר

  ### 6. ספר לא זמין
  אי אפשר להשאיל ספר מושאל

  ### 7. מקסימום ספרים
  חבר ישאל מקסימום 3 ספרים בו זמנית

  ### 8. החזרת ספר
  חבר יכול להחזיר ספר רק אם הוא מושאל לאותו חבר

## Endpoints

### Books
| Method | Endpoint | Description | 
|--------|----------|-------------|
| POST | `/books` | יצירת ספר | 
| GET | `/books` | כל הספרים | 
| GET | `/books/{id}` | ספר לפי מפתח |
| PATCH | `/books/{id}` | עדכון ספר לפי מפתח | 
| PATCH | `/books/{id}/borrow/{member_id}` | השאלת ספר לחבר |
| PATCH | `/books/{id}/return/{member_id}` | החזרת ספר מחבר |


### Members

| Method | Endpoint | Description | 
|--------|----------|-------------|
| POST | `/members` | יצירת חבר |
| GET | `/members` | כל החברים |
| GET | `/members/{id}` | חבר לפי מפתח | 
| PATCH | `/members{id}/deactivate` |השבתת חבר |
| PATCH | `/members{id}/activate` |הפעלת חבר |

### Reports

| Method | Endpoint | Description | 
|--------|----------|-------------|
| GET | `/reports/summary` | דו"ח כללי |
| GET | `/reports/books-by-genre` | ספרים לפי ז'אנר | 
| GET | `/reports/top-member` | החבר הכי פעיל | 

## System flow

General flow:

```text
Client sends HTTP request
        ↓
FastAPI endpoint receives the request
        ↓
System checks the request data
        ↓
System applies the business rules
        ↓
The relevant database class is called
        ↓
SQL query runs on MySQL
        ↓
The API returns a response to the client
```

## Running Instructions

### 1. Open terminal in the project folder

Run the following commands from the main project folder:

```text
library-api/
```

Example:

```bash
cd library-api
```

---

### 2. Create a virtual environment

Run from the project root folder:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

---

### 3. Install requirements

Run from the project root folder:

```bash
pip install -r requirements.txt
```

---

### 4. Run MySQL with Docker

This command can be run from any terminal, but it is recommended to run it from the project root folder.

```bash
docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=library_db -p 3306:3306 -v project_api_db:/var/lib/mysql -d mysql:latest
```

Database details:

```text
Container name: my-mysql
Database name: library_db
Root password: secret
Port: 3306
Volume: project_api_db
```

Make sure the database connection settings in:

```text
database/db_connection.py
```

match these Docker settings.

---

### 5. Run the FastAPI server

Run from the project root folder:

```bash
uvicorn main:app --reload
```

---

### 6. Open Swagger

After the server is running, open the following address in the browser:

```text
http://127.0.0.1:8000/docs
```

The API can be tested from Swagger or Postman.

