import streamlit as st
from import_export_scraper import TradeDataScraper

# Sidebar inputs
with st.sidebar:
    # Title and caption
    st.title("TradeLens")
    st.caption("An Indian trade data Scraping tool")
    
    # Input from user
    hs_code_input = st.text_input("Enter the Commodity HS Code:")
    from_year = st.number_input("From Year:", min_value=1997, max_value=2024, value=2024)
    to_year = st.number_input("To Year:", min_value=1997, max_value=2024, value=2024)

    # Instructions for users
    st.caption("""
        **Instructions:** Year 2023 gives you data from FY 2022 - 23.   
    """)

# Button to fetch data
if st.sidebar.button("Fetch Data"):

    # Validations
    if not hs_code_input:
        st.warning("Please enter a valid HS Code.")
    else:
        # Display a spinner while processing the scraping
        with st.spinner("Fetching trade data..."):
            # Create an instance of the scraper
            scraper = TradeDataScraper()

            # Get years
            years = [str(i) for i in range(int(from_year), int(to_year) + 1)]

            # Run scraping function
            data = scraper.get_trade_data(hs_code_input, years)

            # Cleanup
            scraper.close()

        # Display Data
        st.subheader("Trade Data")
        if not data.empty:
            st.dataframe(data, width=900)  # Make sure the table width fits larger space
        else:
            st.warning("No data found for the provided HS Code.")
