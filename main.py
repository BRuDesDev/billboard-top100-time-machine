from bs4 import BeautifulSoup
import requests

date = input("What date would you like to travel back in time to? (YYYY-mm-dd): ")

url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url)
website = response.text

soup = BeautifulSoup(website, "html-parser")

