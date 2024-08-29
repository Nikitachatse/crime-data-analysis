import pandas as pd
import preprocessor
import streamlit as st
import plotly.express as px

# changing the layout of streamlit
st.set_page_config(layout="wide")
st.sidebar.image("Screenshot 2024-08-27 194014.png")
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
preprocessor.display(filtered_df)

# display bar graph for each state 
if (selected_state == 'All') and (selected_district == 'All'):
    preprocessor.state_crime(filtered_df)
elif selected_state != 'All':
    preprocessor.district_crime(filtered_df) # gives district wise graph for each state
st.markdown('-------') 
# Pie chart display for each of filter
preprocessor.Crime_year(filtered_df)

# description at the bottom of crimes
st.sidebar.markdown('---')  # Optional: Adds a horizontal line
if crime_type:
    with st.sidebar.expander("Types of Crime and Legal Acts/Protections", expanded=False):
        st.markdown(
            """
            <div style="color: black; font-size: 18;">
                <strong>Here :</strong><br>
                 
                1. Violent Crimes: Murder, Assault on Women, Kidnapping and Abduction, Hurt 
                2. Property Crimes: Dacoity, Robbery, Arson 
                3. Legal Acts and Protections: Prevention of Atrocities (POA) Act, Protection of Civil Rights (PCR) Act, Other Crimes Against SCs
            </div>
            """, unsafe_allow_html=True
        )

