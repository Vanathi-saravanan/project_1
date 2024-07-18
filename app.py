import streamlit as st
import pandas as pd
import sqlite3

# Connecting to SQLite database
conn = sqlite3.connect("D:/Redbus proj/Redbus.db")
df = pd.read_sql('SELECT * FROM bus_routes', conn)

# Clean and convert the 'seats_available' column
#df['seats_available'] = df['seats_available'].str.extract('(\d+)').astype(float)
df['seats_available'] = df['seats_available'].str.extract(r'(\d+)').astype(float)


# Convert other columns to appropriate data types
df['star_rating'] = pd.to_numeric(df['star_rating'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Streamlit app
st.title('Redbus Data Filtering')

# Sidebar for filters
route_name_filter = st.sidebar.text_input('Route Name')
busname_filter = st.sidebar.text_input('Bus Name')
bustype_filter = st.sidebar.text_input('Bus Type')
departing_time_filter = st.sidebar.text_input('Departing Time')
duration_filter = st.sidebar.text_input('Duration')
reaching_time_filter = st.sidebar.text_input('Reaching Time')
star_rating_filter = st.sidebar.slider('Rating', 0.0, 5.0, (0.0, 5.0), step=0.1)
price_filter = st.sidebar.slider('Price', 0.0, float(df['price'].max()), (0.0, float(df['price'].max())))
seats_available_filter = st.sidebar.slider('Seats Available', 0, int(df['seats_available'].max()), (0, int(df['seats_available'].max())))

# Apply filters
if route_name_filter:
    df = df[df['route_name'].str.contains(route_name_filter, case=False)]
if busname_filter:
    df = df[df['busname'].str.contains(busname_filter, case=False)]
if bustype_filter:
    df = df[df['bustype'].str.contains(bustype_filter, case=False)]
if departing_time_filter:
    df = df[df['departing_time'].str.contains(departing_time_filter, case=False)]
if duration_filter:
    df = df[df['duration'].str.contains(duration_filter, case=False)]
if reaching_time_filter:
    df = df[df['reaching_time'].str.contains(reaching_time_filter, case=False)]
if star_rating_filter != (0.0, 5.0):
    df = df[(df['star_rating'] >= star_rating_filter[0]) & (df['star_rating'] <= star_rating_filter[1])]
if price_filter != (0.0, float(df['price'].max())):
    df = df[(df['price'] >= price_filter[0]) & (df['price'] <= price_filter[1])]
if seats_available_filter != (0, int(df['seats_available'].max())):
    df = df[(df['seats_available'] >= seats_available_filter[0]) & (df['seats_available'] <= seats_available_filter[1])]

# Display data
st.write(df)

conn.close()
