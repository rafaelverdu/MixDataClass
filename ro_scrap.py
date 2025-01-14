from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd  # Import pandas for data handling
import time

def main():
    # 1. Specify the path to the WebDriver if needed
    service = Service("./chromedriver")  # "chromedriver.exe" on Windows or full path if not on PATH
    driver = webdriver.Chrome(service=service)

    try:
        # 2. Go to the website
        url = "https://legislacao.sefin.ro.gov.br/textoLegislacao.jsp?texto=2498"
        driver.get(url)

        # 3. Wait for the page to load
        time.sleep(4)  # Adjust as needed

        # 4. Get the HTML source
        html_source = driver.page_source

        # 5. Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_source, "html.parser")

        # Save the parsed HTML to a file (optional)
        with open("output.html", "w", encoding="utf-8") as file:
            file.write(soup.prettify())

        # Initialize a list to store results
        results = []

        # Loop through each <tr> in the table
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 4:  # Ensure there are enough cells
                # Extract the relevant data
                name = cells[0].get_text(strip=True)  # First cell
                value = cells[3].get_text(strip=True)  # Fourth cell, keep as string

                # Append to results
                results.append({
                    "name": name,
                    "value": value  # Store as string
                })

        # 6. Convert the results to a pandas DataFrame
        df = pd.DataFrame(results)

        # 7. Save the DataFrame to an Excel file
        df.to_excel("results.xlsx", index=False)

        print("Data has been saved to 'results.xlsx'.")

    finally:
        # 8. Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
