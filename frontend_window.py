from tkinter import *
from backend_database import Database

class Window(object):
    '''
        Window object GUI for displaying library database and includes the functionality of viewing, clearing,
        searching, adding, updating and deleting.
    '''

    def __init__(self, window, db):
        self.window = window
        self.window.wm_title("Library")

        self.db = database

        # generate labels for Title, Author, Year and ISBN
        labelTitle = Label(self.window, text="Title")
        labelTitle.grid(row=0, column=0)

        labelAuthor = Label(self.window, text="Author")
        labelAuthor.grid(row=0, column=2)

        labelYear = Label(self.window, text="Year")
        labelYear.grid(row=1, column=0)

        labelISBN = Label(self.window, text="ISBN")
        labelISBN.grid(row=1, column=2)

        # generate corresponding entry fields for the labels
        self.titleValue = StringVar()
        self.entryTitle = Entry(self.window, textvariable=self.titleValue)
        self.entryTitle.grid(row=0, column=1)

        self.authorValue = StringVar()
        self.entryAuthor = Entry(self.window, textvariable=self.authorValue)
        self.entryAuthor.grid(row=0, column=3)

        self.yearValue = StringVar()
        self.entryYear = Entry(self.window, textvariable=self.yearValue)
        self.entryYear.grid(row=1, column=1)

        self.isbnValue = StringVar()
        self.entryISBN = Entry(self.window, textvariable=self.isbnValue)
        self.entryISBN.grid(row=1, column=3)

        # generate list box for displaying information
        self.listDesc = Listbox(self.window, height=6, width=35)
        self.listDesc.grid(row=2, column=0, rowspan=6, columnspan=2)
        self.listDesc.bind("<<ListboxSelect>>", self.getSelectedRow)

        # create scrollbar for list box window
        scroll = Scrollbar(self.window)
        scroll.grid(row=2, column=2, rowspan=6)

        # configure list box to add scroll bar object
        self.listDesc.configure(yscrollcommand=scroll.set)
        scroll.configure(command=self.listDesc.yview)

        # generate buttons for viewing, clearing searching, adding, updating and deleting
        buttonView = Button(self.window, text="View All", width=12, command=self.viewCommand)
        buttonView.grid(row=2, column=3)

        buttonClose = Button(self.window, text= "Clear Entry", width=12, command=self.clearCommand)
        buttonClose.grid(row=3, column=3)

        buttonSearch = Button(self.window, text="Search Entry", width=12, command=self.searchCommand)
        buttonSearch.grid(row=4, column=3)

        buttonAdd = Button(self.window, text="Add Entry", width=12, command=self.insertCommand)
        buttonAdd.grid(row=5, column=3)

        buttonUpdate = Button(self.window, text="Update", width=12, command=self.updateCommand)
        buttonUpdate.grid(row=6, column=3)

        buttonDelete = Button(self.window, text="Delete", width=12, command=self.deleteCommand)
        buttonDelete.grid(row=7, column=3)

    def getSelectedRow(self, event):
        '''
            Fill entries with selected tuple in the list box.
        '''
        try:
            index = self.listDesc.curselection()[0]
            self.selectedTuple = self.listDesc.get(index)

            self.entryTitle.delete(0, END)
            self.entryTitle.insert(END, self.selectedTuple[1])

            self.entryAuthor.delete(0, END)
            self.entryAuthor.insert(END, self.selectedTuple[2])

            self.entryYear.delete(0, END)
            self.entryYear.insert(END, self.selectedTuple[3])

            self.entryISBN.delete(0, END)
            self.entryISBN.insert(END, self.selectedTuple[4])
        except IndexError:
            pass
    
    def clearCommand(self):
        '''
            Clear out all entry fields.
        '''
        self.entryTitle.delete(0, END)
        self.entryAuthor.delete(0, END)
        self.entryYear.delete(0, END)
        self.entryISBN.delete(0, END)

    def viewCommand(self):
        '''
            Get data from backend SQL view query and insert into the list box.
        '''
        # clear list box before displaying data
        self.listDesc.delete(0, END)
        for row in self.db.viewData():
            self.listDesc.insert(END, row)

    def searchCommand(self):
        ''' 
            Get values from entry widgets and insert data from backend SQL search query into the list box.
        '''
        # clear list box before searching data
        self.listDesc.delete(0, END)
        for row in self.db.searchData(self.titleValue.get(), self.authorValue.get(), self.yearValue.get(), self.isbnValue.get()):
            self.listDesc.insert(END, row)

    def insertCommand(self):
        '''
            Inserts data into the books table, using the backend SQL insert query.
        '''
        self.db.insertData(self.titleValue.get(), self.authorValue.get(), self.yearValue.get(), self.isbnValue.get())
        
        # clear list box before displaying data
        self.listDesc.delete(0, END)
        self.listDesc.insert(END, (self.titleValue.get(), self.authorValue.get(), self.yearValue.get(), self.isbnValue.get()))

    def updateCommand(self):
        '''
            Updates data in the books table, using the backend SQL update query.
        '''
        self.db.updateData(self.selectedTuple[0], self.titleValue.get(), self.authorValue.get(), self.yearValue.get(), self.isbnValue.get())
    
    def deleteCommand(self):
        '''
            Deletes data in books table, given an ID and using the backend SQL delete query.
        '''
        self.db.deleteData(self.selectedTuple[0])

if __name__ == "__main__":
    # create empty window object instance
    window = Tk()

    # connect to database and create library table
    database = Database("books.db")

    Window(window, database)
    window.mainloop()