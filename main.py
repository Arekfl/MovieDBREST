from fastapi import FastAPI, Depends, HTTPException
import requests
from typing import Any, List, Optional
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

app = FastAPI()

# Database configuration
DATABASE_URL = "sqlite:///./movies-extended.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for many-to-many relationship between movies and actors
movie_actors = Table(
    'movie_actor_through',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actor.id'), primary_key=True)
)

# ORM Models
class Movie(Base):
    __tablename__ = 'movie'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    director = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    actors = relationship("Actor", secondary=movie_actors, back_populates="movies")

class Actor(Base):
    __tablename__ = 'actor'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    
    movies = relationship("Movie", secondary=movie_actors, back_populates="actors")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Note: Database tables already exist, no need to create them
# If you need to create tables, uncomment the following:
# @app.on_event("startup")
# def startup_event():
#     Base.metadata.create_all(bind=engine)

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
def get_movies(db: Session = Depends(get_db)):
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
def get_single_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return {
        'id': movie.id,
        'title': movie.title,
        'year': movie.year,
        'director': movie.director,
        'description': movie.description
    }

@app.post("/movies")
def add_movie(params: dict[str, Any], db: Session = Depends(get_db)):
    title = params.get('title')
    year = params.get('year')
    director = params.get('director')
    description = params.get('description', '')  # Default to empty string
    
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    if not year:
        raise HTTPException(status_code=400, detail="Year is required")
    if not director:
        raise HTTPException(status_code=400, detail="Director is required")
    
    movie = Movie(
        title=str(title),
        year=int(year),
        director=str(director),
        description=str(description) if description else ''
    )
    
    db.add(movie)
    db.commit()
    db.refresh(movie)
    
    return {"message": "Movie added successfully", "movie_id": movie.id}

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any], db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    title = params.get('title')
    year = params.get('year')
    director = params.get('director')
    description = params.get('description')
    
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    if not year:
        raise HTTPException(status_code=400, detail="Year is required")
    if not director:
        raise HTTPException(status_code=400, detail="Director is required")
    
    movie.title = str(title)  # type: ignore
    movie.year = int(year)  # type: ignore
    movie.director = str(director)  # type: ignore
    if description is not None:
        movie.description = str(description)  # type: ignore
    
    db.commit()
    
    return {"message": f"Movie {movie_id} updated successfully"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(movie)
    db.commit()
    
    return {"message": f"Movie {movie_id} deleted successfully"}

@app.delete("/movies")
def delete_all_movies(db: Session = Depends(get_db)):
    deleted_count = db.query(Movie).delete()
    db.commit()
    
    return {"message": "All movies deleted successfully", "deleted_count": deleted_count}

# ========== ACTORS ENDPOINTS ==========

@app.get('/actors')
def get_actors(db: Session = Depends(get_db)):
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
def get_single_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    
    return {
        'id': actor.id,
        'name': actor.name,
        'surname': actor.surname
    }

@app.post("/actors")
def add_actor(params: dict[str, Any], db: Session = Depends(get_db)):
    name = params.get('name')
    surname = params.get('surname')
    
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    if not surname:
        raise HTTPException(status_code=400, detail="Surname is required")
    
    actor = Actor(
        name=str(name),
        surname=str(surname)
    )
    
    db.add(actor)
    db.commit()
    db.refresh(actor)
    
    return {"message": "Actor added successfully", "actor_id": actor.id}

@app.put("/actors/{actor_id}")
def update_actor(actor_id: int, params: dict[str, Any], db: Session = Depends(get_db)):
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    
    name = params.get('name')
    surname = params.get('surname')
    
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    if not surname:
        raise HTTPException(status_code=400, detail="Surname is required")
    
    actor.name = str(name)  # type: ignore
    actor.surname = str(surname)  # type: ignore
    
    db.commit()
    
    return {"message": f"Actor {actor_id} updated successfully"}

@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    
    db.delete(actor)
    db.commit()
    
    return {"message": f"Actor {actor_id} deleted successfully"}

# ========== MOVIE-ACTORS RELATIONSHIP ==========

@app.get('/movies/{movie_id}/actors')
def get_movie_actors(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return [
        {
            'id': actor.id,
            'name': actor.name,
            'surname': actor.surname
        }
        for actor in movie.actors
    ]