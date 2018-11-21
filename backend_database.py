import sqlite3

class Database:
    '''
        SQLite database which can be viewed, searched, inserted, deleted, updated and closed upon.
    '''

    def __init__(self, db):
        self._connection = sqlite3.connect(db)
        self._cursor = self._connection.cursor()
        self._cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)")
        self._connection.commit()

    def viewData(self):
        '''
            Fetches and returns all the rows in the books table.
        '''
        self._cursor.execute("SELECT * FROM books")
        rows = self._cursor.fetchall()
        return rows
    
    def insertData(self, title, author, year, isbn):
        '''
            Inserts data into the books table, given user input.
        ''' 
        self._cursor.execute("INSERT INTO books VALUES (NULL, ?, ?, ? , ?)", (title, author, year, isbn))
        self._connection.commit()

    def searchData(self, title = "", author = "", year = "", isbn = ""):
        '''
            Fetchs and returns the rows of the books table that matches the user search query.
        '''
        self._cursor.execute("SELECT * FROM books WHERE title = ? OR author = ? or year = ? or isbn = ?", (title, author, year, isbn))
        rows = self._cursor.fetchall()
        return rows

    def deleteData(self, id):
        '''
            Deletes data from the books table, using the book id.
        '''
        self._cursor.execute("DELETE FROM books WHERE id = ?", (id,))
        self._connection.commit()

    def updateData(self, id, title, author, year, isbn):
        '''
            Updates data from books table, using the book id.
        '''
        self._cursor.execute("UPDATE books SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?", (title, author, year, isbn, id))
        self._connection.commit()

    def __del__(self):
        self._connection.close()