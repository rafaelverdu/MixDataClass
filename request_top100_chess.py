from bs4 import BeautifulSoup
import pandas as pd
import requests

# Sample HTML response
url = 'https://ratings.fide.com/a_top.phtml?list=men'

response = requests.get(url, timeout=10)
response.raise_for_status()  # Raise an error for bad status codes
# Parse the HTML response

soup = BeautifulSoup(response.text, "html.parser")

# Locate the table with the players' information
table = soup.find("div", id="top_rating_div").find("table")

# Initialize a list to store the extracted player information
players = []

# Loop through the rows in the table body
for row in table.find_all("tr")[1:]:  # Skip the header row
    cells = row.find_all("td")
    if len(cells) >= 6:  # Ensure the row has enough columns
        player_info = {
            "Rank": cells[0].get_text(strip=True),
            "Name": cells[1].get_text(strip=True),
            "Federation": cells[2].get_text(strip=True),
            "Rating": cells[3].get_text(strip=True),
            "Change": cells[4].get_text(strip=True),
            "Birth Year": cells[5].get_text(strip=True),
        }
        players.append(player_info)

print(players)

# Convert the extracted data to a pandas DataFrame
df = pd.DataFrame(players)

# Save the extracted data to an Excel file
df.to_excel("fide_top_100_players.xlsx", index=False)

# Print a confirmation message
print("Data has been extracted and saved to 'fide_top_100_players.xlsx'")
