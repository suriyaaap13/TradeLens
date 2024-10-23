import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class TradeDataScraper:
    def __init__(self):
        self.url_import = 'https://tradestat.commerce.gov.in/eidb/icomq.asp'
        self.url_export = 'https://tradestat.commerce.gov.in/eidb/ecomq.asp'
        chrome_options = Options()
        chrome_options.use_chromium = True
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def get_trade_data(self, hsn_code, year_range):
        """
        Scrape both import and export data and merge the results into a single DataFrame.
        """
        
        
        if len(hsn_code) > 4:
            
            import_data_qty = self.get_import_qty(hsn_code, year_range)
            export_data_qty = self.get_export_qty(hsn_code, year_range)
            import_data_usd = self.get_import_value_USD(hsn_code, year_range)
            export_data_usd = self.get_export_value_USD(hsn_code, year_range)


            # Merge import and export data on 'Year' and 'HS_Code'
            combined_data = pd.merge(import_data_qty, export_data_qty, on=['Year', 'HS_Code'], how='outer')
            combined_data = pd.merge(combined_data, import_data_usd, on=['Year', 'HS_Code'], how='outer')
            combined_data = pd.merge(combined_data, export_data_usd, on=['Year', 'HS_Code'], how='outer')
            combined_data.fillna(0, inplace=True)  # Fill missing values with 0
            return combined_data
        
        else:

            import_data_usd = self.get_import_value_USD(hsn_code, year_range)
            export_data_usd = self.get_export_value_USD(hsn_code, year_range)
            combined_data = pd.merge(import_data_usd, export_data_usd, on=['Year', 'HS_Code'], how='outer')
            combined_data.fillna(0, inplace=True)  # Fill missing values with 0
            return combined_data



    def get_import_qty(self, code, year_range):
        """
        Scrape import data for the given HS code(s) and year range.
        """
        self.driver.get(self.url_import)
        data = []
        
        for year in year_range:
            # Select the year
            select_element_year = self.driver.find_element(By.ID, "select2")
            dropdown_year = Select(select_element_year)
            dropdown_year.select_by_value(year)

            # Enter HS code
            input_field = self.driver.find_element(By.NAME, 'hscode')
            input_field.clear()
            input_field.send_keys(code)

            # Select the HS code length
            select_element = self.driver.find_element(By.ID, "select1")
            dropdown = Select(select_element)
            dropdown.select_by_value(str(len(code)))

            # Choose quantity (radio button)
            qty = self.driver.find_element(By.ID, 'radioqty')
            qty.click()

            # Submit
            submit_btn = self.driver.find_element(By.ID, 'button1')
            submit_btn.click()

            # Scrape the table data
            table_data = self.driver.find_elements(By.TAG_NAME, 'td')
            table_header = self.driver.find_elements(By.TAG_NAME, 'th')

            qty_text = 0
            hs_code = code
            y1 = int(year) - 1
            y2 = year
            year_text = str(y1)+'-'+str(y2)
            qty_text = 0

            if table_header:
                arr_th = [th.text for th in table_header]
                year_text = arr_th[4]

            if table_data:
                arr_td = [td.text for td in table_data]
                qty_text = arr_td[4].replace(',', '') if arr_td[4] != ' ' else 0

            if qty_text == '' or qty_text == ' ':
                qty_text = '0'

            
            # Add the row to the data list
            row = [year_text, hs_code, float(qty_text)]
            data.append(row)

            # Go back to the main page
            back_btn = self.driver.find_element(By.ID, 'IMG1')
            back_btn.click()

        return pd.DataFrame(data, columns=['Year', 'HS_Code', 'Import_Qty_thousand_units'])

    def get_export_qty(self, code, year_range):
        """
        Scrape export data for the given HS code(s) and year range.
        """
        self.driver.get(self.url_export)
        data = []
        for year in year_range:
            # Select the year
            select_element_year = self.driver.find_element(By.ID, "select2")
            dropdown_year = Select(select_element_year)
            dropdown_year.select_by_value(year)

            # Enter HS code
            input_field = self.driver.find_element(By.NAME, 'hscode')
            input_field.clear()
            input_field.send_keys(code)

            # Select the HS code length
            select_element = self.driver.find_element(By.ID, "select1")
            dropdown = Select(select_element)
            dropdown.select_by_value(str(len(code)))

            # Choose quantity (radio button)
            qty = self.driver.find_element(By.ID, 'radioqty')
            qty.click()

            # Submit
            submit_btn = self.driver.find_element(By.ID, 'button1')
            submit_btn.click()
            time.sleep(1)

            # Scrape the table data
            table_data = self.driver.find_elements(By.TAG_NAME, 'td')
            table_header = self.driver.find_elements(By.TAG_NAME, 'th')

            qty_text = 0
            hs_code = code
            y1 = int(year) - 1
            y2 = year
            year_text = str(y1)+'-'+str(y2)
            qty_text = 0
            

            if table_header:
                arr_th = [th.text for th in table_header]
                year_text = arr_th[4]

            if table_data:
                arr_td = [td.text for td in table_data]
                qty_text = arr_td[4].replace(',', '') if arr_td[4] != ' ' else 0


            if qty_text == '' or qty_text == ' ':
                qty_text = '0'

            # Add the row to the data list
            row = [year_text, hs_code, float(qty_text)]
            data.append(row)

            # Go back to the main page
            back_btn = self.driver.find_element(By.ID, 'IMG1')
            back_btn.click()

        return pd.DataFrame(data, columns=['Year', 'HS_Code', 'Export_Qty_thousand_units'])

    
    def get_export_value_USD(self, code, year):
        """
        Scrape export value (USD) data for the given HS code and year range.
        """
        self.driver.get(self.url_export)

        data = []
        
        for j in year:
            select_element_year = self.driver.find_element(By.ID, "select2")
            dropdown_year = Select(select_element_year)
    
            # Selecting the year for which we need to fetch data
            dropdown_year.select_by_value(j)
    
            input = self.driver.find_element(By.NAME, 'hscode')
            input.clear()
            input.send_keys(code)
            
            select_element = self.driver.find_element(By.ID, "select1")
            dropdown = Select(select_element)
            
            # Select hsn_code digit
            dropdown.select_by_value(str(len(code)))
            
            
            # Pressing USD Radio button
            usd_btn = self.driver.find_element(By.ID, 'radiousd')
            usd_btn.click()

            # Pressing Submit Button
            submit_btn = self.driver.find_element(By.ID, 'button1')
            submit_btn.click()
            
            table_data = self.driver.find_elements(By.TAG_NAME, 'td')
            header = self.driver.find_elements(By.TAG_NAME, 'th')
            
            arr_hd = [i for i in header]
            arr_td = [i for i in table_data]

            y1 = int(j)-1
            y2 = j
            year_text = str(y1)+'-'+str(y2)
            value_text = '0'
            
            if arr_td:
                value_text = arr_td[3].text.replace(',','').strip()
                
            if arr_hd:
                year_text = arr_hd[3].text

            if value_text == '' or value_text == ' ':
                value_text = '0'
            
            row = [year_text, code, float(value_text)]
            data.append(row)
            
            # Back Button
            back_btn = self.driver.find_element(By.ID, 'IMG1')
            back_btn.click()

        # Convert the array into a Dataframe
        return pd.DataFrame(data, columns=['Year', 'HS_Code', 'Export_$_millions'])


    def get_import_value_USD(self, code, year):
            """
            Scrape export value (USD) data for the given HS code and year range.
            """
            self.driver.get(self.url_import)

            data = []
            
            for j in year:
                select_element_year = self.driver.find_element(By.ID, "select2")
                dropdown_year = Select(select_element_year)
        
                # Selecting the year for which we need to fetch data
                dropdown_year.select_by_value(j)
        
                input = self.driver.find_element(By.NAME, 'hscode')
                input.clear()
                input.send_keys(code)
                
                select_element = self.driver.find_element(By.ID, "select1")
                dropdown = Select(select_element)
                
                # Select hsn_code digit
                dropdown.select_by_value(str(len(code)))
                
                
                # Pressing USD Radio button
                usd_btn = self.driver.find_element(By.ID, 'radiousd')
                usd_btn.click()

                # Pressing Submit Button
                submit_btn = self.driver.find_element(By.ID, 'button1')
                submit_btn.click()
                time.sleep(1)
                header = self.driver.find_elements(By.TAG_NAME, 'th')
                table_data = self.driver.find_elements(By.TAG_NAME, 'td')
                
                arr_hd = [i for i in header]
                arr_td = [i for i in table_data]

                y1 = int(j)-1
                y2 = j
                year_text = str(y1)+'-'+str(y2)
                value_text = 0
                
                if arr_td:
                    value_text = arr_td[3].text.replace(',','').strip()
                
                if arr_hd:
                    year_text = arr_hd[3].text

                if value_text == '' or value_text == ' ':
                    value_text = '0'
                
                row = [year_text, code, float(value_text)]
                data.append(row)
                
                # Back Button
                back_btn = self.driver.find_element(By.ID, 'IMG1')
                back_btn.click()

            # Convert the array into a Dataframe
            return pd.DataFrame(data, columns=['Year', 'HS_Code', 'Import_$_millions'])
    
    def close(self):
        # Close the scraper and the database connection
        self.driver.quit()
