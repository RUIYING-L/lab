import requests
from bs4 import BeautifulSoup
import csv

# 1. Access the website and get page content
def get_page_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    return response.content

# 2. Extract movie data from HTML
def scrape_movies(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    movie_elements = soup.find_all("div", class_="el-card__body")

    movie_list = []
    for movie in movie_elements:
        # Get title
        title = movie.find("h2").get_text(strip=True)

        # Get score (SAFE CHECK)
        score_tag = movie.find("p", class_="score")
        score = score_tag.get_text(strip=True) if score_tag else "0.0"

        # Get genres
        genres = [g.get_text(strip=True) for g in movie.find_all("span", class_="genre")]
        genres_str = " / ".join(genres)

        # Get date
        date_tag = movie.find("span", class_="date")
        date = date_tag.get_text(strip=True) if date_tag else "Unknown"

        # Get cover image
        cover = movie.find("img")["src"]

        movie_list.append({
            "title": title,
            "score": score,
            "genres": genres_str,
            "date": date,
            "cover": cover
        })
    return movie_list

# 3. Print all scraped movies
def print_movies(movie_list):
    print("\n===== Scraped Movie Information =====")
    for i, movie in enumerate(movie_list, 1):
        print(f"Movie {i}")
        print(f"Title: {movie['title']}")
        print(f"Score: {movie['score']}")
        print(f"Genres: {movie['genres']}")
        print(f"Release Date: {movie['date']}")
        print(f"Cover Link: {movie['cover']}")
        print("-" * 50)

# 4. Filter high-score movies (score >= 9.0)
def filter_high_score_movies(movie_list):
    high_score = []
    for m in movie_list:
        try:
            if float(m["score"]) >= 9.0:
                high_score.append(m)
        except:
            continue
    return high_score

# 5. Save data to CSV file
def save_to_csv(movie_list, filename="movie_data.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = ["title", "score", "genres", "date", "cover"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movie_list)
    print(f"\nData saved to: {filename}")

# 6. Main function to run the whole program
def main():
    url = "https://ssr1.scrape.center/"
    html = get_page_content(url)
    movies = scrape_movies(html)
    print_movies(movies)

    high_movies = filter_high_score_movies(movies)
    print("\n===== High Score Movies (>= 9.0) =====")
    for m in high_movies:
        print(f"{m['title']} | Score: {m['score']}")

    save_to_csv(movies)
    print("\n*** Scraping Successfully Completed ***")

# Run the program
if __name__ == "__main__":
    main()
