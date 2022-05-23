import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

response = requests.get(URL)
website = response.text

soup = BeautifulSoup(website, "html.parser")

movie_titles = soup.find_all(name="h3", class_="title")
# print(movie_titles)
movies = []
for movie in movie_titles:
    movies.append(movie.text)

movies.reverse()

with open("movies.txt", "w") as file:
    for movie in movies:
        file.write(f"{movie}\n")
