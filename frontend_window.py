from tkinter import *
from backend_database import Database

class Window(object):
    '''
        Window object GUI for displaying library database and includes the functionality of viewing, clearing,
        searching, adding, updating and deleting.
    '''

    def __init__(self, window, db):
        self._window = window
        self._window.wm_title("Library")

        self._db = database

        # generate labels for Title, Author, Year and ISBN
        labelTitle = Label(self._window, text = "Title")
        labelTitle.grid(row = 0, column = 0)

        labelAuthor = Label(self._window, text = "Author")
        labelAuthor.grid(row = 0, column = 2)

        labelYear = Label(self._window, text = "Year")
        labelYear.grid(row = 1, column = 0)

        labelISBN = Label(self._window, text = "ISBN")
        labelISBN.grid(row = 1, column = 2)

        # generate corresponding entry fields for the labels
        self._titleValue = StringVar()
        self._entryTitle = Entry(self._window, textvariable = self._titleValue)
        self._entryTitle.grid(row = 0, column = 1)

        self._authorValue = StringVar()
        self._entryAuthor = Entry(self._window, textvariable = self._authorValue)
        self._entryAuthor.grid(row = 0, column = 3)

        self._yearValue = StringVar()
        self._entryYear = Entry(self._window, textvariable = self._yearValue)
        self._entryYear.grid(row = 1, column = 1)

        self._isbnValue = StringVar()
        self._entryISBN = Entry(self._window, textvariable = self._isbnValue)
        self._entryISBN.grid(row = 1, column = 3)

        # generate list box for displaying information
        self._listDesc = Listbox(self._window, height = 6, width = 35)
        self._listDesc.grid(row = 2, column = 0, rowspan = 6, columnspan = 2)
        self._listDesc.bind("<<ListboxSelect>>", self.getSelectedRow)

        # create scrollbar for list box window
        scroll = Scrollbar(self._window)
        scroll.grid(row = 2, column = 2, rowspan = 6)

        # configure list box to add scroll bar object
        self._listDesc.configure(yscrollcommand = scroll.set)
        scroll.configure(command = self._listDesc.yview)

        # generate buttons for viewing, clearing searching, adding, updating and deleting
        buttonView = Button(self._window, text = "View All", width = 12, command = self.viewCommand)
        buttonView.grid(row = 2, column = 3)

        buttonClose = Button(self._window, text = "Clear Entry", width = 12, command = self.clearCommand)
        buttonClose.grid(row = 3, column = 3)

        buttonSearch = Button(self._window, text = "Search Entry", width = 12, command = self.searchCommand)
        buttonSearch.grid(row = 4, column = 3)

        buttonAdd = Button(self._window, text = "Add Entry", width = 12, command = self.insertCommand)
        buttonAdd.grid(row = 5, column = 3)

        buttonUpdate = Button(self._window, text = "Update", width = 12, command = self.updateCommand)
        buttonUpdate.grid(row = 6, column = 3)

        buttonDelete = Button(self._window, text = "Delete", width = 12, command = self.deleteCommand)
        buttonDelete.grid(row = 7, column = 3)

    def getSelectedRow(self, event):
        '''
            Fill entries with selected tuple in the list box.
        '''
        try:
            index = self._listDesc.curselection()[0]
            self._selectedTuple = self._listDesc.get(index)

            self._entryTitle.delete(0, END)
            self._entryTitle.insert(END, self._selectedTuple[1])

            self._entryAuthor.delete(0, END)
            self._entryAuthor.insert(END, self._selectedTuple[2])

            self._entryYear.delete(0, END)
            self._entryYear.insert(END, self._selectedTuple[3])

            self._entryISBN.delete(0, END)
            self._entryISBN.insert(END, self._selectedTuple[4])
        except IndexError:
            pass
    
    def clearCommand(self):
        '''
            Clear out all entry fields.
        '''
        self._entryTitle.delete(0, END)
        self._entryAuthor.delete(0, END)
        self._entryYear.delete(0, END)
        self._entryISBN.delete(0, END)

    def viewCommand(self):
        '''
            Get data from backend SQL view query and insert into the list box.
        '''
        # clear list box before displaying data
        self._listDesc.delete(0, END)

        for row in self._db.viewData():
            self._listDesc.insert(END, row)

    def searchCommand(self):
        ''' 
            Get values from entry widgets and insert data from backend SQL search query into the list box.
        '''
        # clear list box before searching data
        self._listDesc.delete(0, END)

        for row in self._db.searchData(self._titleValue.get(), self._authorValue.get(), self._yearValue.get(), self._isbnValue.get()):
            self._listDesc.insert(END, row)

    def insertCommand(self):
        '''
            Inserts data into the books table, using the backend SQL insert query.
        '''
        self._db.insertData(self._titleValue.get(), self._authorValue.get(), self._yearValue.get(), self._isbnValue.get())
        
        # clear list box before displaying data
        self._listDesc.delete(0, END)
        self._listDesc.insert(END, (self._titleValue.get(), self._authorValue.get(), self._yearValue.get(), self._isbnValue.get()))

    def updateCommand(self):
        '''
            Updates data in the books table, using the backend SQL update query.
        '''
        self._db.updateData(self._selectedTuple[0], self._titleValue.get(), self._authorValue.get(), self._yearValue.get(), self._isbnValue.get())
    
    def deleteCommand(self):
        '''
            Deletes data in books table, given an ID and using the backend SQL delete query.
        '''
        self._db.deleteData(self._selectedTuple[0])

if __name__ == "__main__":
    # create empty window object instance
    window = Tk()

    # connect to database and create library table
    database = Database("books.db")

    Window(window, database)

    window.mainloop()