import pandas as pd
import streamlit as st
import plotly.express as px
import preprocessor

# changing the layout of streamlit
st.set_page_config(layout="wide")

# logo display
st.sidebar.image("logo.jpg")

# Load Crime data
data = pd.read_csv("cleaned_data.csv")

# creating sidebar
st.sidebar.header("Filters")

# year filter
min_year, max_year = int(data['Year'].min()), int(data['Year'].max())
year_range = st.sidebar.slider('Select Year Range', min_year, max_year, (min_year, max_year))

# Sates filter
states = data['STATE/UT'].unique()
selected_state = st.sidebar.selectbox('Select State/UT', options=['All'] + list(states))

# District filter
districts = data[data['STATE/UT'] == selected_state]['DISTRICT'].unique() if selected_state != 'All' else data['DISTRICT'].unique()
selected_district = st.sidebar.selectbox('Select District', options=['All'] + list(districts))

# Crime filter
crime_type = st.sidebar.selectbox('Select Crime Type', options=['All'] + list(data.columns[4:-3]))

# Display an info icon with expandable information
with st.expander("ℹ️  About Dashboard"):
    st.write("This dashboard presents an analysis of caste-related crimes in India, focusing on data from 2001 to 2013. It provides a detailed view of how crimes against Scheduled Castes (SC) and Scheduled Tribes (ST) were distributed across various regions during this period. The dashboard sheds light on the systemic issues tied to the Indian caste system, offering insights into the persistence of caste-based violence despite legal protections such as the SC/ST Act of 1989. The goal is to help understand the historical context of caste-related violence and the ongoing challenges faced by these marginalized communities.")

# Main dashboard
st.title("State & District - wise Crime Analysis Dashbord")
st.markdown('-------') 

# Custom styled title
st.markdown(
    """
    <h1 style="color: #2c3e50; font-size: 30px; text-align: center;">
        Caste Crimes : Crimes Against SC (2001-2013)
    </h1>
    """, unsafe_allow_html=True
)

# Global filtering
filtered_df = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['STATE/UT'] == selected_state]
if selected_district != 'All':
    filtered_df = filtered_df[filtered_df['DISTRICT'] == selected_district]
if crime_type != 'All':
    filtered_df = filtered_df[filtered_df[crime_type] > 0]
   
# Display map 
if (selected_state != 'All') and (crime_type != 'All') and (selected_district == 'All'):
    df = filtered_df[["STATE/UT","DISTRICT",crime_type]].reset_index()
    df.columns = ["index","STATE/UT","DISTRICT","Total Crimes"]
    preprocessor.display(df)
else :
    preprocessor.display(filtered_df)

st.markdown('-------') 

# display bar graph for each state 
if (selected_state == 'All') and (selected_district == 'All'):
    preprocessor.state_crime(filtered_df)
elif (selected_state != 'All') and (crime_type == 'All'):
    preprocessor.district_crime(filtered_df) # gives district wise graph for each state
elif (selected_state != 'All') and (crime_type != 'All'):
    df = filtered_df[["DISTRICT",crime_type]]
    df.columns = ['District', 'Total']
    preprocessor.crime_type(df) # gives specified crime distribution for specified state

st.markdown('-------') 

# Pie chart display for each of filter
if crime_type == 'All':
    preprocessor.Crime_year(filtered_df)

# Crime trends over time
if crime_type == 'All':
    crime_trend = filtered_df.groupby('Year').sum().reset_index()
    preprocessor.Year_crime(crime_trend)
else:
    crime_trend = filtered_df.groupby('Year')[crime_type].sum().reset_index(name="Total Crimes")
    preprocessor.Year_crime(crime_trend)

# description at the bottom of crimes
st.sidebar.markdown('---')  # Optional: Adds a horizontal line
if crime_type:
    with st.sidebar.expander("Types of Crime and Legal Acts/Protections", expanded=False):
        st.markdown(
            """
            <div style="color: black; font-size: 18;">
                <strong>Here :</strong><br>
                1. Violent Crimes: Murder, Assault on Women, Kidnapping and Abduction, Hurt <br>
                2. Property Crimes: Dacoity, Robbery, Arson <br>
                3. Legal Acts and Protections: Prevention of Atrocities (POA) Act, Protection of Civil Rights (PCR) Act, Other Crimes Against SCs
            </div>
            """, unsafe_allow_html=True
        )

# Url to visit 
url = r"https://ncsk.nic.in/sites/default/files/PoA%20Act%20as%20amended-Nov2017.pdf"
st.sidebar.write(f"[Click For More Informtion]({url})")