# import csv
# import sqlite3

# con = sqlite3.connect("jarvis.db")
# cursor = con.cursor()

# # query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# # cursor.execute(query)

# # query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# # #cursor.execute(query)
# # con.commit()

# # query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# # cursor.execute(query)

# # query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# # cursor.execute(query)
# # con.commit()


# # # testing module
# # app_name = "android studio"
# # cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# # results = cursor.fetchall()
# # print(results[0][0])

# # Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# # Specify the column indices you want to import (0-based index)
# # Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 18]

# # # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#         csvreader = csv.reader(csvfile)
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # # Commit changes and close connection
# con.commit()
# con.close()

# query = "INSERT INTO contacts VALUES (null,'Sagar', '7084706565', 'null')"
# cursor.execute(query)
# con.commit()

# # query = 'kunal'
# # query = query.strip().lower()

# # cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# # results = cursor.fetchall()
# # print(results[0][0])

#delet contacts
# query = "DELETE FROM contacts"
# cursor.execute(query)
# con.commit()




# import sqlite3
# import csv

# # Connect to SQLite database
# con = sqlite3.connect("jarvis.db")
# cursor = con.cursor()

# # Create the table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS contacts (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         mobile_no TEXT NOT NULL
#     );
# ''')
# con.commit()

# # Define the desired column indices (update as per your CSV structure)
# desired_columns_indices = [0, 18]  # Example: Column 0 = name, Column 1 = mobile_no

# # Read data from CSV and insert into SQLite table
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     next(csvreader)  # Skip header row if needed

#     for row in csvreader:  
#         selected_data = [row[i] for i in desired_columns_indices]  # Extract required columns
#         cursor.execute('''INSERT INTO contacts (name, mobile_no) VALUES (?, ?)''', tuple(selected_data))

# # Commit and close connection
# con.commit()
# con.close()

# query = "INSERT INTO contacts VALUES (null,'Mama', '9284470741',null)"
# cursor.execute(query)
# con.commit()

# import sqlite3

# # Connect to SQLite database
# con = sqlite3.connect("jarvis.db")
# cursor = con.cursor()

# # Create the emails table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS emails (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         email TEXT NOT NULL UNIQUE
#     );
# ''')

# con.commit()
# con.close()

# print("Emails table created successfully!")

# import sqlite3


# def store_email(name: str, email: str):
#     """
#     Stores an email address in the database with the corresponding name.
#     """
#     con = sqlite3.connect("jarvis.db")
#     cursor = con.cursor()

#     try:
#         cursor.execute("INSERT INTO emails (name, email) VALUES (?, ?)", (name, email))
#         con.commit()
#         print(f"Email {email} added successfully!")
#     except sqlite3.IntegrityError:
#         print(f"Email {email} already exists!")
#     finally:
#         con.close()

# # store_email("vivek", "vp983351@gmail.com")
# # store_email("omkar",  "omkarchandra206@gmail.com")
# # store_email("sagar", "guptasagar0555@gmail.com")store_email("priti", "pandeyvaibhavi540@gmail.com")
# # store_email("priti", "pandeyvaibhavi540@gmail.com")
# store_email("papa" , "pandeysanjay332211@gmail.com")