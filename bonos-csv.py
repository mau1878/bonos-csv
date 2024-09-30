import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Streamlit UI
st.title("AL30 Historical Data Scraper")
st.write("This app scrapes and saves AL30 historical data from Rava.")

# Button to trigger the data scraping
if st.button('Scrape AL30 Data'):

    # URL for the AL30 profile page
    url = 'https://www.rava.com/perfil/al30'
    
    # Send a GET request to fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table that contains the historical data
    table = soup.find('table', {'id': 'cotizaciones-historicas'})  # Adjust table ID if necessary
    
    if table:
        # Extract table headers
        headers = [th.text.strip() for th in table.find_all('th')]
        
        # Extract table rows
        data = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cells = [cell.text.strip() for cell in row.find_all('td')]
            if cells:
                data.append(cells)
        
        # Convert to a DataFrame for easier manipulation
        df = pd.DataFrame(data, columns=headers)

        # Display the DataFrame in the Streamlit app
        st.write("Data scraped successfully:")
        st.dataframe(df)

        # Save the DataFrame to a CSV file
        csv_filename = 'historical_data_al30.csv'
        df.to_csv(csv_filename, index=False)
        
        # Provide a download link
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=csv_filename,
            mime='text/csv'
        )
    else:
        st.error("Failed to find the data table. Please check the page structure.")
