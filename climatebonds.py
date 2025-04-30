from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the Edge WebDriver
edge_options = Options()
edge_options.add_argument("--headless")  
edge_options.add_argument("--disable-gpu")

service = EdgeService(executable_path = r"C:\Users\sansk\Downloads\edgedriver_win64\msedgedriver.exe")

driver = webdriver.Edge(service=service, options = edge_options)

url = "https://www.climatebonds.net/cbi/pub/data/bonds?items_per_page=All"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")[1:]

data = []
for row in rows:
    cols = [col.get_text(strip=True) for col in row.find_all("td")]
    data.append(cols)

columns = ["BondID", "Entity", "Amount Issued", "Currency", "Issue Date", "Maturity Date", "CBI Certified", "SPO Provider"]
df = pd.DataFrame(data, columns=columns)

df.to_csv("green_bonds.csv", index=False)
print("Data has been scraped and saved.")

driver.quit()
