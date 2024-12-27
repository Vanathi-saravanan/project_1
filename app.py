import streamlit as st
import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("D:/Redbus proj/Redbus.db")

# Streamlit app title
st.title('Redbus Data Filtering')

# Sidebar for filters
route_name_filter = st.sidebar.text_input('Route Name')
busname_filter = st.sidebar.text_input('Bus Name')
bustype_filter = st.sidebar.text_input('Bus Type')
departing_time_filter = st.sidebar.text_input('Departing Time')
duration_filter = st.sidebar.text_input('Duration')
reaching_time_filter = st.sidebar.text_input('Reaching Time')
star_rating_filter = st.sidebar.slider('Rating', 0.0, 5.0, (0.0, 5.0), step=0.1)
price_filter = st.sidebar.slider('Price', 0.0, 1000.0, (0.0, 1000.0))
seats_available_filter = st.sidebar.slider('Seats Available', 0, 100, (0, 100))

# Base SQL query for filtering
query = "SELECT * FROM bus_routes WHERE 1=1"  # Start with a condition that always evaluates to True

# Dynamically modify the SQL query based on user inputs
if route_name_filter:
    query += f" AND route_name LIKE '%{route_name_filter}%'"
if busname_filter:
    query += f" AND busname LIKE '%{busname_filter}%'"
if bustype_filter:
    query += f" AND bustype LIKE '%{bustype_filter}%'"
if departing_time_filter:
    query += f" AND departing_time LIKE '%{departing_time_filter}%'"
if duration_filter:
    query += f" AND duration LIKE '%{duration_filter}%'"
if reaching_time_filter:
    query += f" AND reaching_time LIKE '%{reaching_time_filter}%'"
if star_rating_filter != (0.0, 5.0):  # Check if rating filter is applied
    query += f" AND star_rating BETWEEN {star_rating_filter[0]} AND {star_rating_filter[1]}"
if price_filter != (0.0, 1000.0):  # Check if price filter is applied
    query += f" AND price BETWEEN {price_filter[0]} AND {price_filter[1]}"
if seats_available_filter != (0, 100):  # Check if seats filter is applied
    query += f" AND seats_available BETWEEN {seats_available_filter[0]} AND {seats_available_filter[1]}"

# Execute the SQL query
df = pd.read_sql(query, conn)

# Display the filtered data in Streamlit
st.write(df)

# Close the database connection
conn.close()
