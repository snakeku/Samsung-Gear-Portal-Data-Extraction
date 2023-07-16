import csv
import mysql.connector

# This Python Code reads a csv file called users_data.csv, iterates through each rows, extracts the data and insert it into a mysql database. 
# It will create 2 tables. This sql database can then be used to pull data for data analytics and visualisation.
# Users table: This table stores information about individual users.
# LoginActivity table: This table records login activity details for each user.

def connect_to_database():
    # This function connects to the MySQL database and returns the connection and cursor.
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='P@ssword1001',
        database='employees_database'
    )
    cursor = conn.cursor()
    return conn, cursor

def create_users_table(cursor):
    # This function creates a Users table if it doesn't exist
    create_users_table_query = """
        CREATE TABLE IF NOT EXISTS Users (
            UserID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(255),
            Email VARCHAR(255) UNIQUE
        )
    """
    cursor.execute(create_users_table_query)

def create_login_activity_table(cursor):
    # This function creates LoginActivity table if it doesn't exist
    create_login_activity_table_query = """
        CREATE TABLE IF NOT EXISTS LoginActivity (
            LoginID INT PRIMARY KEY AUTO_INCREMENT,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UserID INT,
            Email VARCHAR(255),
            Date DATE,
            Latitude DECIMAL(9, 6),
            Longitude DECIMAL(9, 6),
            LastLoginDaysAgo INT,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (Email) REFERENCES Users(Email)
        )
    """
    cursor.execute(create_login_activity_table_query)

def insert_users_data(cursor, name, email):
    # This function inserts data into Users table using ignore to avoid duplicate inserts
    insert_users_data_query = """
        INSERT IGNORE INTO Users (Name, Email)
        VALUES (%s, %s)
    """
    cursor.execute(insert_users_data_query, (name, email))

def insert_login_activity_data(cursor, email, date, latitude, longitude, last_login_days):
    # This function inserts data into LoginActivity table
    insert_login_activity_data_query = """
        INSERT INTO LoginActivity (UserID, Email, Date, Latitude, Longitude, LastLoginDaysAgo)
        SELECT UserID, %s, %s, %s, %s, %s
        FROM Users
        WHERE Email = %s
    """
    cursor.execute(insert_login_activity_data_query, (email, date, latitude, longitude, last_login_days, email))

def process_csv_data(file_path):
    # This function opens the CSV file for reading
    with open(file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Get the column index based on the headers
        headers = next(csv_reader)
        name_index = headers.index('Name')
        email_index = headers.index('Email')
        date_index = headers.index('Date')
        latitude_index = headers.index('Latitude')
        longitude_index = headers.index('Longitude')
        last_login_index = headers.index('LastLogin in Days')

        # Connect to the database
        conn, cursor = connect_to_database()

        # Create Users and LoginActivity tables if it does not exist.
        create_users_table(cursor)
        create_login_activity_table(cursor)

        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Extract the data from the row
            name = row[name_index]
            email = row[email_index]
            date = row[date_index]
            latitude = row[latitude_index]
            longitude = row[longitude_index]
            last_login_days = row[last_login_index]

            # Insert data into Users table if new users
            insert_users_data(cursor, name, email)

            # Insert data into LoginActivity table
            insert_login_activity_data(cursor, email, date, latitude, longitude, last_login_days)

        # Commit the changes to the database
        conn.commit()

        # Close the connection
        conn.close()

# Call the function to process the CSV data
process_csv_data('users_data.csv')
