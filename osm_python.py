# Importing packages for creating webapp
import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def checkdata(propertyType,noBedroom,totalArea,energyRating,postCode,budget):
    """
    In this defined function we are going to check that user input data is valid or not.
    As its non-functional requirement so we are checking with one attributes that is postcode.
    In future, we need to check all passed variable.
    It returns true if user input parameter is valid and returns false if user input parameter is invalid.
    """
    if(postCode == ''):
        st.write('Enter Postcode')
        return False
    else:
        return True

def load_dataset():
    """
    This defined function will load our dataset into dataframe.
    It returns loaded dataframe.
    """
    priceData = pd.read_csv('pp-complete.csv')
    return priceData

def clean_dataset(priceData):
    """
    This defined function takes dataframe as input.
    Here we are going to perform data pre processing and data wrangling process with dataframe.
    It will return dataframe.
    """
    data_columns = ['Transaction_unique_numner','Price','Data_of_transfer','Postcode','Property_type','Old_new',
          'Duration','PAON','SAON','Street','Locality','Town','District','County','PPD_category_type',
           'Record_status_monthly_file']
    priceData.columns = data_columns
    # Drop unnecessary columns which has high number of NaN values
    dropCols = ['SAON','Locality']
    priceData = priceData.drop(columns=dropCols)
    # Drop rows with NaN values
    priceData = priceData.dropna()
    # Drop duplicates data
    priceData = priceData.drop_duplicates()
    # Remove spaces and convert specific data columns to lowercase
    priceData['Postcode'] = priceData['Postcode'].astype(str).str.lower()
    priceData['Postcode'] = priceData['Postcode'].str.replace(' ','')
    priceData['PAON'] = priceData['PAON'].astype(str).str.lower()
    priceData['PAON'] = priceData['PAON'].str.replace(' ','')
    return priceData

def searchData(priceData,propertyType,noBedroom,totalArea,energyRating,postCode,budget):
    """
    This defined function will create Secondary dataframe by checking postcode with main dataset.
    Here we need to add our python script.
    It returns dataframe.
    """
    st.write(postCode)
    postCode = postCode.lower()
    postCode = postCode.replace(' ','')
    searchedData = priceData.query('Postcode == @postCode')
    return searchedData
    
# Listed different type of properties in list    
type_Property = ['Detached','Semi-Detached','Terraced','Flats']

# Get input from Users
propertyType = st.sidebar.radio("Type of Property Type", type_Property)
noBedroom = st.sidebar.slider("Bedrooms",0,10)
totalArea = st.sidebar.slider("Total Area (Sqr ft.)",400,1000)
energyRating = st.sidebar.slider("Energy Rating(EPC)",1,8)
postCode = st.sidebar.text_input("Enter Post Code")
budget = st.sidebar.slider("Choose Budget Price", 150000, 1000000)
calculate = st.sidebar.button("Calculate")

# Executes once user entered all input parameters and wants outputs
if calculate:
    temp = checkdata(propertyType,noBedroom,totalArea,energyRating,postCode,budget)
    if(temp == True):
        st.write('Cheched Data')
        # Call a defined function to load price paid dataset.
        priceData = load_dataset()
        st.write(priceData.count())
        st.write('Loaded Dataset')
        # Call a defined function to clean price paid dataset.
        priceData = clean_dataset(priceData)
        st.write(priceData.count())
        st.write('Cleaned Dataset')
        # Call a defined function to search for property based on user input parameters
        searchedData = searchData(priceData,propertyType,noBedroom,totalArea,energyRating,postCode,budget)
        st.write(searchedData.count())
        st.write('Searching for data')
        st.dataframe(searchedData)
    
# Information regarding Sidebar parameters
st.markdown(" ## **AVM tool for Predicting Property Price**")
st.markdown(" #### Accurate, Transparent and Instantaneous Property Valuation")
st.markdown("  ** Start by defining the property to value on the sidebar: **")
st.write("- Type of Property : Detached, semi detached, terraced or flat")
st.write("- Bedrooms : Number of bedrooms")
st.write("- Total area : the gross internal floor area in sq ft.")
st.write("- Energy rating : Energy Rating of the Property by EPC Cerificate")
st.write("- Postcode : the exact postcode of the property (e.g. HA5 4AY).")
st.write("- Bugdet Price : Price of the property searching for")