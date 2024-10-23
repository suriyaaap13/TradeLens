import streamlit as st
from import_export_scraper import TradeDataScraper

st.title("TradeLens")
st.caption("An Indian trade data Scrapping tool")

# Instructions for users
st.markdown("""
    Instructions: 
""")

# Input from user
hs_code_input = st.text_input("Enter the Commodity HS Code:")
from_year = st.number_input("From Year:", min_value=1997, max_value=2024, value=2020)
to_year = st.number_input("To Year:", min_value=2000, max_value=2024, value=2024)

# Button to fetch data
if st.button("Fetch Data"):
    # Validations
    if len(hs_code_input) < 6 or len(hs_code_input) % 2 != 0:
        st.warning("Please enter a valid HS Code.")
    else:
        # Create an instance of the scraper
        scraper = TradeDataScraper()

        # Get years
        years = [str(i) for i in range(int(from_year), int(to_year) + 1)]

        
        # Run scraping function
        data = scraper.get_trade_qty(hs_code_input, years)

        # Display Data
        st.subheader("Trade Data")
        if not data.empty:
            st.dataframe(data)
        else:
            st.warning("No data found for the provided HS Code.")


        # Cleanup
        scraper.close()
