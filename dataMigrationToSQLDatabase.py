# This Python Code reads a csv file called users_data.csv, iterates through each rows, extracts the data and insert it into a mysql database. 
# It will create 2 tables. This sql database can then be used to pull data for data analytics and visualisation.
# Users table: This table stores information about individual users.
# LoginActivity table: This table records login activity details for each user.

import csv
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='bobTheBuilder',
    password='xMarksTheSpot',
    database='samsungGearPortalDatabase'
)

# Create Users table if it doesn't exist
create_users_table = """
    CREATE TABLE IF NOT EXISTS Users (
        UserID INT PRIMARY KEY AUTO_INCREMENT,
        Name VARCHAR(255),
        Email VARCHAR(255) UNIQUE
    )
"""
cursor = conn.cursor()
cursor.execute(create_users_table)
cursor.close()

# Create LoginActivity table if it doesn't exist
create_login_activity_table = """
    CREATE TABLE IF NOT EXISTS LoginActivity (
        LoginID INT PRIMARY KEY AUTO_INCREMENT,
        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UserID INT,
        Date DATE,
        Latitude DECIMAL(9, 6),
        Longitude DECIMAL(9, 6),
        LastLoginDaysAgo INT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
"""
cursor = conn.cursor()
cursor.execute(create_login_activity_table)
cursor.close()

# Open the CSV file for reading
with open('users_data.csv', 'r') as file:

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

    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Extract the data from the row
        name = row[name_index]
        email = row[email_index]
        date = row[date_index]
        latitude = row[latitude_index]
        longitude = row[longitude_index]
        last_login_days = row[last_login_index]

        # Insert data into Users table using ignore to avoid duplicate inserts
        insert_users_data = """
            INSERT IGNORE INTO Users (Name, Email)
            VALUES (%s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(insert_users_data, (name, email))
        cursor.close()        
        
          # Insert data into LoginActivity table
          # This SQL statement inserts a new row into the 'LoginActivity' table by selecting the 'UserID' from the 'Users' table
          # based on the provided 'Email' value and combining it with the other provided values for 'Date', 'Latitude', 'Longitude'
          # and 'LastLoginDaysAgo'.
        insert_login_activity_data = """
            INSERT INTO LoginActivity (UserID, Date, Latitude, Longitude, LastLoginDaysAgo)
            SELECT UserID, %s, %s, %s, %s
            FROM Users
            WHERE Email = %s
            """
        cursor = conn.cursor()
        cursor.execute(insert_login_activity_data, (date, latitude, longitude, last_login_days, email))
        cursor.close()

    # Commit the changes to the database
    conn.commit()

# Close the connection
conn.close()

