import requests
import pandas as pd
import random

# Constants
API_URL = "https://www.googleapis.com/books/v1/volumes"
MAX_RESULTS = 20  # Max results per API query

# Fetch books based on genre
def fetch_books(genre):
    try:
        params = {
            'q': f"subject:{genre}",
            'maxResults': MAX_RESULTS,
            'printType': 'books'
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        books = []
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            book = {
                "Title": volume_info.get("title", "N/A"),
                "Authors": ', '.join(volume_info.get("authors", ["Unknown"])),
                "Published Year": volume_info.get("publishedDate", "N/A")[:4],
                "Rating": volume_info.get("averageRating", "N/A"),
                "Genre": genre.title()
            }
            books.append(book)

        return pd.DataFrame(books)

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return pd.DataFrame()

# Filter books based on user input
def filter_books(df, min_rating=None, year=None):
    if min_rating:
        df = df[df["Rating"] != "N/A"]
        df["Rating"] = pd.to_numeric(df["Rating"])
        df = df[df["Rating"] >= min_rating]
    if year:
        df = df[df["Published Year"].str.contains(str(year))]
    return df

# Suggest a random book
def suggest_random_book(df):
    if df.empty:
        print("No books found with the given filters.")
    else:
        book = df.sample(1).iloc[0]
        print("\n📚 Book Suggestion:")
        print(f"Title: {book['Title']}")
        print(f"Authors: {book['Authors']}")
        print(f"Year: {book['Published Year']}")
        print(f"Rating: {book['Rating']}")
        print(f"Genre: {book['Genre']}")

# Main flow
def main():
    print("📖 Welcome to the Book Suggestion App!")
    genre = input("Enter your favorite genre (e.g., fiction, history, science): ").lower()
    df = fetch_books(genre)

    if df.empty:
        print("No books found. Try a different genre.")
        return

    try:
        min_rating = float(input("Enter minimum rating (1 to 5, or leave blank): ") or 0)
    except ValueError:
        min_rating = 0

    year = input("Enter a publication year to filter (or leave blank): ")
    year = year.strip() if year else None

    filtered_df = filter_books(df, min_rating=min_rating if min_rating else None, year=year)
    suggest_random_book(filtered_df)

if __name__ == "__main__":
    main()