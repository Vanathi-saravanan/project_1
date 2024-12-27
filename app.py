import streamlit as st
import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("D:/Redbus proj/Redbus.db")

# Fetch distinct values for selectboxes (for each column)
route_names = pd.read_sql("SELECT DISTINCT route_name FROM bus_routes", conn)['route_name'].dropna().tolist()
busnames = pd.read_sql("SELECT DISTINCT busname FROM bus_routes", conn)['busname'].dropna().tolist()
bustypes = pd.read_sql("SELECT DISTINCT bustype FROM bus_routes", conn)['bustype'].dropna().tolist()
departing_times = pd.read_sql("SELECT DISTINCT departing_time FROM bus_routes", conn)['departing_time'].dropna().tolist()
durations = pd.read_sql("SELECT DISTINCT duration FROM bus_routes", conn)['duration'].dropna().tolist()
reaching_times = pd.read_sql("SELECT DISTINCT reaching_time FROM bus_routes", conn)['reaching_time'].dropna().tolist()

# Streamlit app
st.title('Redbus Data Filtering')

# Sidebar for filters with selectbox
route_name_filter = st.sidebar.selectbox('Route Name', ['All'] + route_names)
busname_filter = st.sidebar.selectbox('Bus Name', ['All'] + busnames)
bustype_filter = st.sidebar.selectbox('Bus Type', ['All'] + bustypes)
departing_time_filter = st.sidebar.selectbox('Departing Time', ['All'] + departing_times)
duration_filter = st.sidebar.selectbox('Duration', ['All'] + durations)
reaching_time_filter = st.sidebar.selectbox('Reaching Time', ['All'] + reaching_times)

# Filter for rating and price (using slider, same as before)
star_rating_filter = st.sidebar.slider('Rating', 0.0, 5.0, (0.0, 5.0), step=0.1)
price_filter = st.sidebar.slider('Price', 0.0, float(pd.read_sql("SELECT MAX(price) FROM bus_routes", conn).iloc[0, 0]), (0.0, float(pd.read_sql("SELECT MAX(price) FROM bus_routes", conn).iloc[0, 0])))
seats_available_filter = st.sidebar.slider('Seats Available', 0, 100, (0, 100))

# Base SQL query
query = "SELECT * FROM bus_routes WHERE 1=1"  # Start with a condition that always evaluates to True

# Dynamically modify the SQL query based on selectbox input
if route_name_filter != 'All':
    query += f" AND route_name = '{route_name_filter}'"
if busname_filter != 'All':
    query += f" AND busname = '{busname_filter}'"
if bustype_filter != 'All':
    query += f" AND bustype = '{bustype_filter}'"
if departing_time_filter != 'All':
    query += f" AND departing_time = '{departing_time_filter}'"
if duration_filter != 'All':
    query += f" AND duration = '{duration_filter}'"
if reaching_time_filter != 'All':
    query += f" AND reaching_time = '{reaching_time_filter}'"
if star_rating_filter != (0.0, 5.0):
    query += f" AND star_rating BETWEEN {star_rating_filter[0]} AND {star_rating_filter[1]}"
if price_filter != (0.0, float(pd.read_sql("SELECT MAX(price) FROM bus_routes", conn).iloc[0, 0])):
    query += f" AND price BETWEEN {price_filter[0]} AND {price_filter[1]}"
if seats_available_filter != (0, 100):
    query += f" AND seats_available BETWEEN {seats_available_filter[0]} AND {seats_available_filter[1]}"

# Execute the SQL query
df = pd.read_sql(query, conn)

# Display the filtered data in Streamlit
st.write(df)

# Close the database connection
conn.close()
