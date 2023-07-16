import matplotlib.pyplot as plt
import mysql.connector

# This Python Code pulls data from the relational MySQL database by executing an SQL query
# convert the fetched data and plots the login counts against the month in a bar chart.
# The bar chart is used to analyse user login patterns and identifying trends in user activity so as to 
# provide insights into user engagement and helps in making data-driven decisions. 

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


def fetch_login_activity(cursor):
    # This function fetches and pull the data using an SQL Query.
    sql_statement = """
    SELECT * FROM LoginActivity;
    """
    cursor.execute(sql_statement)
    rows = cursor.fetchall()
    return rows


def month_converter(day_input):
    # This function takes in an argument which is the total number of days, convert the days
    # into month and return that value.
    return day_input // 30


def count_login_by_month(rows):
    # This function returns the number of logins per month in the form of dictionary
    month_count = {}
    for row in rows:
        months = month_converter(row[7])
        if months in month_count:
            month_count[months] += 1
        else:
            month_count[months] = 1
    return month_count


def plot_login_counts(login_counts):
    # This functions takes in the dictionary and plots the data
    """Plots the login counts."""
    months_on_x_axis = list(login_counts.keys())
    login_counter = list(login_counts.values())

    # Create the bar chart
    plt.bar(months_on_x_axis, login_counter)

    # Add labels and title
    plt.xlabel('Months')
    plt.ylabel('Users Last Login Count')
    plt.title('User Login Count by Month')

    # Display the chart
    plt.show()


# Connect to the database
conn, cursor = connect_to_database()

# Fetch the login activity data
rows = fetch_login_activity(cursor)

# Count the logins by month
login_counts = count_login_by_month(rows)

# Plot the login counts
plot_login_counts(login_counts)

# Close the cursor and connection
cursor.close()
conn.close()
