import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Streamlit UI
st.title("Bond Historical Data Scraper (Selenium Version)")
st.write("This app scrapes and saves historical data from Rava for the bond you specify.")

# Input for the user to enter the bond ticker
bond_ticker = st.text_input("Enter bond ticker (e.g., AL30, AE38, GD35):", "AL30").upper()

# Button to trigger the data scraping
if st.button('Scrape Data'):

    # Selenium WebDriver setup (Automatically downloads the ChromeDriver if not installed)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # URL for the bond profile page on Rava
    url = f'https://www.rava.com/perfil/{bond_ticker.lower()}'
    driver.get(url)

    # Give time for the page to load
    time.sleep(3)

    # Find the table using XPath
    try:
        table = driver.find_element_by_xpath('/html/body/div[1]/main/div/div/div[3]/div[2]/div/div/div[2]')
        
        # Extract rows from the table
        rows = table.find_elements_by_tag_name('tr')
        data = []
        for row in rows[1:]:  # Skip the header
            cells = [cell.text for cell in row.find_elements_by_tag_name('td')]
            if cells:
                data.append(cells)

        # Create a DataFrame
        headers = ['Fecha', 'Apert.', 'Máx', 'Mín', 'Cierre', 'Vol']
        df = pd.DataFrame(data, columns=headers)

        # Display the DataFrame in Streamlit
        st.write(f"Data scraped successfully for {bond_ticker}:")
        st.dataframe(df)

        # Save the DataFrame to a CSV file
        csv_filename = f'historical_data_{bond_ticker}.csv'
        df.to_csv(csv_filename, index=False)

        # Provide a download link
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=csv_filename,
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"Failed to find data: {e}")
    finally:
        # Close the driver
        driver.quit()
