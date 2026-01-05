from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from sqlalchemy import Engine, create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

app = FastAPI()

# Konfiguracja bazy danych
DATABASE_URL = "sqlite:///./movies-extended.db"
engine: Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

db = Session(engine)

# Definicje modeli SQLAlchemy
class Movie(Base):
    __tablename__ = 'movie'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    director = Column(String)
    description = Column(String)

class Actor(Base):
    __tablename__ = 'actor'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)

# Pydantic models do walidacji requestów
class MovieCreate(BaseModel):
    title: str
    year: int
    director: str
    description: str = ""

class MovieUpdate(BaseModel):
    title: str
    year: int
    director: str
    description: str = ""

class ActorCreate(BaseModel):
    name: str
    surname: str

class ActorUpdate(BaseModel):
    name: str
    surname: str

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
    # Budowa URL do Nominatim API (reverse geocoding)
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    
    # Wysłanie zapytania z nagłówkiem User-Agent, żeby API nas nie blokowało
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # Zwrócenie odpowiedzi w formacie JSON
    return response.json()

@app.get('/movies')
def get_movies():
    """Pobiera listę wszystkich filmów"""
    movies = db.query(Movie).all()
    
    return [
        {
            'id': movie.id,
            'title': movie.title,
            'year': movie.year,
            'director': movie.director,
            'description': movie.description
        }
        for movie in movies
    ]

@app.get('/movies/{movie_id}')
def get_single_movie(movie_id: int):
    """Pobiera pojedynczy film po ID"""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Film nie znaleziony")
    
    return {
        'id': movie.id,
        'title': movie.title,
        'year': movie.year,
        'director': movie.director,
        'description': movie.description
    }

@app.post("/movies")
def add_movie(movie: MovieCreate):
    """Dodaje nowy film do bazy"""
    new_movie = Movie(
        title=movie.title,
        year=movie.year,
        director=movie.director,
        description=movie.description
    )
    
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    
    return {"message": "Film dodany pomyślnie", "movie_id": new_movie.id}

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: MovieUpdate):
    """Aktualizuje istniejący film"""
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if not db_movie:
        raise HTTPException(status_code=404, detail="Film nie znaleziony")
    
    db_movie.title = movie.title  # type: ignore
    db_movie.year = movie.year  # type: ignore
    db_movie.director = movie.director  # type: ignore
    db_movie.description = movie.description  # type: ignore
    
    db.commit()
    
    return {"message": f"Film {movie_id} zaktualizowany"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    """Usuwa film z bazy"""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Film nie znaleziony")
    
    db.delete(movie)
    db.commit()
    
    return {"message": f"Film {movie_id} usunięty"}

@app.delete("/movies")
def delete_all_movies():
    """Usuwa wszystkie filmy z bazy"""
    deleted_count = db.query(Movie).delete()
    db.commit()
    
    return {"message": "Wszystkie filmy usunięte", "deleted_count": deleted_count}

# ========== ENDPOINTY DLA AKTORÓW ==========

@app.get('/actors')
def get_actors():
    """Pobiera listę wszystkich aktorów"""
    actors = db.query(Actor).all()
    
    return [
        {
            'id': actor.id,
            'name': actor.name,
            'surname': actor.surname
        }
        for actor in actors
    ]

@app.get('/actors/{actor_id}')
def get_single_actor(actor_id: int):
    """Pobiera pojedynczego aktora po ID"""
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    
    if not actor:
        raise HTTPException(status_code=404, detail="Aktor nie znaleziony")
    
    return {
        'id': actor.id,
        'name': actor.name,
        'surname': actor.surname
    }

@app.post("/actors")
def add_actor(actor: ActorCreate):
    """Dodaje nowego aktora do bazy"""
    new_actor = Actor(
        name=actor.name,
        surname=actor.surname
    )
    
    db.add(new_actor)
    db.commit()
    db.refresh(new_actor)
    
    return {"message": "Aktor dodany pomyślnie", "actor_id": new_actor.id}

@app.put("/actors/{actor_id}")
def update_actor(actor_id: int, actor: ActorUpdate):
    """Aktualizuje istniejącego aktora"""
    db_actor = db.query(Actor).filter(Actor.id == actor_id).first()
    
    if not db_actor:
        raise HTTPException(status_code=404, detail="Aktor nie znaleziony")
    
    db_actor.name = actor.name  # type: ignore
    db_actor.surname = actor.surname  # type: ignore
    
    db.commit()
    
    return {"message": f"Aktor {actor_id} zaktualizowany"}

@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    """Usuwa aktora z bazy"""
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    
    if not actor:
        raise HTTPException(status_code=404, detail="Aktor nie znaleziony")
    
    db.delete(actor)
    db.commit()
    
    return {"message": f"Aktor {actor_id} usunięty"}

# ========== RELACJE FILM-AKTOR ==========

@app.get('/movies/{movie_id}/actors')
def get_movie_actors(movie_id: int):
    """Pobiera aktorów grających w danym filmie"""
    # Sprawdź czy film istnieje
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Film nie znaleziony")
    
    # Pobierz aktorów
    query = text("""
        SELECT a.id, a.name, a.surname
        FROM actor a
        INNER JOIN movie_actor_through ma ON a.id = ma.actor_id
        WHERE ma.movie_id = :movie_id
    """)
    
    result = db.execute(query, {"movie_id": movie_id})
    actors = []
    
    for row in result:
        actors.append({
            'id': row[0],
            'name': row[1],
            'surname': row[2]
        })
    
    return actors