from fastapi import FastAPI
import requests
import sqlite3
from typing import Any

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
@app.get("/sum")
def sum(x: int = 0, y: int = 10):
    return x+y
@app.get("/subtract")
def subtract(x: int = 0, y: int = 10):
    return x - y
@app.get("/multiply")
def multiply(x: int = 1, y: int = 1):
    return x * y
@app.get("/divide")
def divide(x: int = 1, y: int = 1):
    if y == 0:
        return "Error: Division by zero"
    return x / y

@app.get("/geocode")
def geocode(lat: float, lon: float):
    # Budujemy URL do Nominatim API (reverse geocoding)
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    
    # Wysyłamy zapytanie z nagłówkiem User-Agent, żeby API nas nie blokowało
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # Zwracamy odpowiedź w formacie JSON
    return response.json()

@app.get('/movies')
def get_movies():
    try:
        # Łączymy się z bazą danych
        conn = sqlite3.connect('movies.db')
        conn.row_factory = sqlite3.Row  # Pozwala na dostęp do kolumn po nazwie
        cursor = conn.cursor()
        
        # Pobieramy wszystkie filmy
        cursor.execute("SELECT * FROM movies")
        rows = cursor.fetchall()
        
        # Budujemy listę obiektów
        output = []
        for row in rows:
            movie = {
                'id': row['ID'],
                'title': row['title'],
                'year': row['year'],
                'actors': row['actors']
            }
            output.append(movie)
        
        # Zamykamy połączenie
        conn.close()
        
        return output
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.get('/movies/{movie_id}')
def get_single_movie(movie_id:int):
    try:
        # Łączymy się z bazą danych
        conn = sqlite3.connect('movies.db')
        conn.row_factory = sqlite3.Row  # Pozwala na dostęp do kolumn po nazwie
        cursor = conn.cursor()
        
        # Pobieramy film o podanym ID
        cursor.execute("SELECT * FROM movies WHERE ID=?", (movie_id,))
        row = cursor.fetchone()
        
        if row is None:
            conn.close()
            return {"error": "Movie not found"}
        
        movie = {
            'id': row['ID'],
            'title': row['title'],
            'year': row['year'],
            'actors': row['actors']
        }
        
        # Zamykamy połączenie
        conn.close()
        
        return movie
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.post("/movies")
def add_movie(params: dict[str, Any]):
    title = params.get('title')
    year = params.get('year')
    actors = params.get('actors')
    
    # Walidacja danych wejściowych
    if not title:
        return {"error": "Title is required"}
    if not year:
        return {"error": "Year is required"}
    if not actors:
        return {"error": "Actors is required"}
    
    try:
        # Łączymy się z bazą danych
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        # Wstawiamy nowy film
        cursor.execute("INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)", (title, year, actors))
        conn.commit()
        
        # Pobieramy ID nowo dodanego filmu
        movie_id = cursor.lastrowid
        
        # Sprawdzamy czy film został dodany (cursor.rowcount)
        if cursor.rowcount == 0:
            conn.close()
            return {"error": "Failed to add movie"}
        
        # Zamykamy połączenie
        conn.close()
        
        return {"message": f"Movie added successfully", "movie_id": movie_id}
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any]):
    title = params.get('title')
    year = params.get('year')
    actors = params.get('actors')
    
    # Walidacja danych wejściowych
    if not title:
        return {"error": "Title is required"}
    if not year:
        return {"error": "Year is required"}
    if not actors:
        return {"error": "Actors is required"}
    
    try:
        # Łączymy się z bazą danych
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        # Aktualizujemy film
        cursor.execute("UPDATE movies SET title=?, year=?, actors=? WHERE ID=?", (title, year, actors, movie_id))
        conn.commit()
        
        # Sprawdzamy czy film został zaktualizowany (cursor.rowcount)
        if cursor.rowcount == 0:
            conn.close()
            return {"error": "Movie not found"}
        
        # Zamykamy połączenie
        conn.close()
        
        return {"message": f"Movie {movie_id} updated successfully"}
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    try:
        # Łączymy się z bazą danych
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        # Usuwamy film
        cursor.execute("DELETE FROM movies WHERE ID=?", (movie_id,))
        conn.commit()
        
        # Sprawdzamy czy film został usunięty (cursor.rowcount)
        if cursor.rowcount == 0:
            conn.close()
            return {"error": "Movie not found"}
        
        # Zamykamy połączenie
        conn.close()
        
        return {"message": f"Movie {movie_id} deleted successfully"}
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.delete("/movies")
def delete_all_movies():
    try:
        # Łączymy się z bazą danych
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        
        # Usuwamy wszystkie filmy
        cursor.execute("DELETE FROM movies")
        conn.commit()
        
        # Sprawdzamy ile filmów zostało usuniętych (cursor.rowcount)
        deleted_count = cursor.rowcount
        
        # Zamykamy połączenie
        conn.close()
        
        return {"message": f"All movies deleted successfully", "deleted_count": deleted_count}
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}