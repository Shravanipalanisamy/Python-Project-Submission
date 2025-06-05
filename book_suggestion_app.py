import requests
import pandas as pd
import random

# API URL
API_URL = "https://www.googleapis.com/books/v1/volumes"

# Function to get books using genre
def get_books(genre):
    try:
        params = {
            'q': f"subject:{genre}",
            'maxResults': 20
        }
        response = requests.get(API_URL, params=params)
        data = response.json()
        books = []

        for item in data.get("items", []):
            info = item.get("volumeInfo", {})
            title = info.get("title", "No Title")
            authors = info.get("authors", ["Unknown"])
            published = info.get("publishedDate", "N/A")
            rating = info.get("averageRating", "N/A")

            book = {
                "Title": title,
                "Authors": ", ".join(authors),
                "Published Year": published[:4],
                "Rating": rating,
                "Genre": genre
            }
            books.append(book)

        return pd.DataFrame(books)

    except requests.exceptions.RequestException:
        print("There was a network error. Please check your internet.")
        return pd.DataFrame()
    except:
        print("Something went wrong while getting data.")
        return pd.DataFrame()

# Function to filter books by rating and year
def filter_books(data, min_rating=None, year=None):
    if min_rating:
        data = data[data["Rating"] != "N/A"]
        data["Rating"] = pd.to_numeric(data["Rating"], errors='coerce')
        data = data[data["Rating"] >= min_rating]
    if year:
        data = data[data["Published Year"].str.contains(str(year), na=False)]
    return data

# Function to suggest a random book
def suggest_book(data):
    if data.empty:
        print("No books found with the selected filters.")
    else:
        chosen = data.sample(1).iloc[0]
        print("\n📚 Book Suggestion:")
        print("Title:", chosen["Title"])
        print("Authors:", chosen["Authors"])
        print("Year:", chosen["Published Year"])
        print("Rating:", chosen["Rating"])
        print("Genre:", chosen["Genre"])

# Main code
def main():
    print("📖 Welcome to the Book Suggestion App!")

    genre = input("Enter your favorite genre (e.g. fiction, history, science): ").lower()
    books_df = get_books(genre)

    if books_df.empty:
        print("No books found. Try a different genre.")
        return

    try:
        rating_input = input("Enter minimum rating (1 to 5, or leave blank): ")
        min_rating = float(rating_input) if rating_input else None
    except ValueError:
        print("Invalid rating. Skipping rating filter.")
        min_rating = None

    year_input = input("Enter a publication year to filter (or leave blank): ")
    year = year_input.strip() if year_input else None

    filtered = filter_books(books_df, min_rating, year)
    suggest_book(filtered)

# Run the app
if __name__ == "__main__":
    main()
input("\nPress Enter to exit...")  # <-- This keeps the window open