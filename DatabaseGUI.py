# Schyler Lowry
# 3-4-2023
# CRN: 23199
# CIS 226: Advanced Python Programming
# Time Spent: 3 hours

"""
I took the same code from my previous assignment, and slightly modified the functions to return values that can then be displayed in the GUI.
What took me the longest was figuring out the pysimplegui functions, and troubleshooting an issue with the window resizing weirdly.

My goal was to have a central screen, e.g., the 'main menu' that has all the same menu options from the console version of this program. 
From there, I wanted the program to show a different window whenever you click on one of the five options.
I opted for creating several layouts and then incorporating them into the main layout list as columns. 
It's an odd approach, but this was the simplest way. 

Each time you click on one of the GUI elements, it changes the visibility state of the previous column to 'false', meaning it won't show, and subsequently,
it changes the column state associated with the clicked GUI element, to 'true'. Thus, giving the illusion of each button click bringing you to a different menu.
"""



import PySimpleGUI as sg
import sqlite3

menu_def = [
    ['&File', ['&Quit']]
]


initialscreen = [
            [sg.Text('Select the database to connect to:')],
            [sg.Button('Vegetables')]
           ]

mainmenu = [
            [sg.Button('Show all vegetables', key='1')],
            [sg.Button('Lookup vegetable', key='2')],
            [sg.Button('Insert vegetable', key='3')],
            [sg.Button('Update vegetable', key='4')],
            [sg.Button('Remove vegetable', key='5')],                       
           ]


records = []            # declared these here, for use in the 'showall' layout.
toprow = ['ID', 'Name', 'Quantity']
showall = [
            [sg.Text(key='showall')],
            [sg.Table(values = records, headings = toprow, auto_size_columns=False, key='-TABLE-')],            
            [sg.Button('Home',key='home1')]
]

lookup = [
            [sg.Text('Enter ID of vegetable:')],
            [sg.Input(size=(5,1), key='lookupInput')],
            [sg.Button('Lookup', key ='lookup')],
            [sg.Table(values = records, headings = toprow, auto_size_columns=False, key='-TABLE2-')], 
            [sg.Button('Home', key='home2')]
]

insert = [
            [sg.Text('Enter name of vegetable to insert:')],
            [sg.Input(size=(20,1),key = 'insertInputName')],
            [sg.Text('Enter quantity')],
            [sg.Input(size=(5,1),key = 'insertInputQuantity')],
            [sg.Button('Insert',key = 'insert')],
            [sg.Button('Home', key='home3')]
]

update = [
            [sg.Text('Enter ID of vegetable to update:')],
            [sg.Input(size=(5,1),key = 'updateInputID')],
            [sg.Text('Enter new quantity:')],
            [sg.Input(size=(5,1),key = 'updateInputQuantity')],
            [sg.Button('Update',key = 'update')],
            [sg.Button('Home', key='home4')] 
]

remove = [
            [sg.Text('Enter ID of vegetable to remove:')],
            [sg.Input(size=(5,1), key='removeInputID')],
            [sg.Button('Remove', key ='remove')],
            [sg.Button('Home', key='home5')]
]

layout = [
        [sg.Menu(menu_def)],
        [sg.Column(initialscreen, key='-COL1-')],
        [sg.pin(sg.Column(mainmenu, visible=False, key='-COL2-'))],
        [sg.pin(sg.Column(showall, visible=False, key='-COL3-'))],
        [sg.pin(sg.Column(lookup, visible=False, key='-COL4-'))],
        [sg.pin(sg.Column(insert, visible=False, key='-COL5-'))],
        [sg.pin(sg.Column(update, visible=False, key='-COL6-'))],
        [sg.pin(sg.Column(remove, visible=False, key='-COL7-'))],
        [sg.StatusBar('Waiting for selection', key='status')]
        ]

window = sg.Window('Database', layout, resizable=True)


# creates table, so long as it doesn't already exist
def create_table(conn, c):
    c.execute("CREATE TABLE IF NOT EXISTS Vegetables (vegID INTEGER PRIMARY KEY,name text, quantity integer)")
    # pretty straight forward, but I added a primary key so that you can select records accurately. 
    # the PK is identity
    # the PK increases incrementally
    conn.commit()


# inserts a record
def insertrecord(conn,c, vegetable, quantity):
    
    c.execute("INSERT INTO Vegetables VALUES (NULL,?, ?)", [vegetable, quantity])
    # have to pass in NULL in order to have the vegID generate automatically
    conn.commit()
    



# shows all records in table
def readtable(c):
    print("ID:   Name:   Quantity:")
    table = []
    for row in c.execute("SELECT * FROM Vegetables"):
        vegID = row[0]
        vegetable = row[1]
        quantity = row[2]
        print(vegID, " "*3, vegetable, " "*3, quantity)
        list1 = vegID, vegetable, quantity
        table.append(list1)
    return table
    

                                    


# shows single record
def showrecord(c,vegID):
    table = []
    print("ID:   Name:   Quantity:")
    for row in c.execute("SELECT * FROM Vegetables WHERE vegID=?",[vegID]):
        vegID = row[0]
        vegetable = row[1]
        quantity = row[2]
        print(vegID, " "*3, vegetable, " "*3, quantity)
        list1 = vegID, vegetable, quantity
        table.append(list1)
    return table

# updates a record
# can only update the quantity of a vegetable
def updaterecord(conn, c,vegID, quantity):
    
    c.execute("UPDATE Vegetables SET quantity=? WHERE vegID=?", [quantity, vegID])
    conn.commit()


def deleterecord(conn, c, vegID):
    
    c.execute("DELETE FROM Vegetables WHERE vegID=?", [vegID])
    conn.commit()


def main():
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        elif event == 'Vegetables':
            conn = sqlite3.connect('vegetables.db')
            c = conn.cursor()
            create_table(conn,c)
            window['-COL1-'].update(visible=False)
            window['-COL2-'].update(visible=True)
        elif event == '1':
            window['-COL2-'].update(visible=False)
            window['-COL3-'].update(visible=True)
            records = readtable(c)
            window['-TABLE-'].update(records)
            window['status'].update("Showing all records in table")
        elif event == '2':
            window['-COL2-'].update(visible=False)
            window['-COL4-'].update(visible=True)
            window['status'].update("Waiting for entry")
        elif event == 'lookup':
            try:
                vegID = int(values['lookupInput'])
                records = showrecord(c,vegID)
                window['-TABLE2-'].update(records)
                print('lookup pressed') # just for debugging
                window['status'].update("Record displayed with ID of " + str(vegID))
            except ValueError:
                result = 'Invalid entry.'
                window['status'].update(result)
                sg.popup('ERROR', 'Entry must be an integer')
        elif event == '3':
            window['-COL2-'].update(visible=False)
            window['-COL5-'].update(visible=True)
            window['status'].update("Waiting for entry")
        elif event == 'insert':
            try:
                vegetable = values['insertInputName']
                quantity = int(values['insertInputQuantity'])
                insertrecord(conn,c,vegetable,quantity)
                window['status'].update("Record inserted")
            except ValueError:
                result = 'Invalid entry.'
                window['status'].update(result)
                sg.popup('ERROR', 'Entry must be an integer')
        elif event == '4':
            window['-COL2-'].update(visible=False)
            window['-COL6-'].update(visible=True)
            window['status'].update("Waiting for entry")
        elif event == 'update':
            try:
                vegID = int(values['updateInputID'])
                quantity = int(values['updateInputQuantity'])
                updaterecord(conn,c,vegID,quantity)
                window['status'].update("Record updated")
            except ValueError:
                result = 'Invalid entry.'
                window['status'].update(result)
                sg.popup('ERROR', 'Entry must be an integer')
        elif event == '5':
            window['-COL2-'].update(visible=False)
            window['-COL7-'].update(visible=True)
            window['status'].update("Waiting for entry")
        elif event == 'remove':
            try:
                vegID = int(values['removeInputID'])
                deleterecord(conn,c,vegID)
                window['status'].update("Record deleted")
            except ValueError:
                result = 'Invalid entry.'
                window['status'].update(result)
                sg.popup('ERROR', 'Entry must be an integer')
        elif event == 'home1' or event == 'home2' or event == 'home3' or event == 'home4' or event == 'home5':    #this seems like a heavy handed approach, but I couldn't figure out how to close the columns without writing it like this
            window['-COL3-'].update(visible=False)
            window['-COL4-'].update(visible=False)
            window['-COL5-'].update(visible=False)
            window['-COL6-'].update(visible=False)
            window['-COL7-'].update(visible=False)
            window['-COL2-'].update(visible=True)
            window['status'].update("Main Menu")
            print("pressed home")
            
    window.close()

if __name__ == '__main__':
    main()
