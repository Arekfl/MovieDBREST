# Movie Database REST API

REST API do zarządzania bazą danych filmów i aktorów, zbudowane przy użyciu FastAPI i SQLAlchemy ORM.

## Funkcjonalności

- Pełny CRUD dla filmów (tytuł, rok, reżyser, opis)
- Pełny CRUD dla aktorów (imię, nazwisko)
- Relacja wiele-do-wielu między filmami a aktorami
- Endpoint do pobierania aktorów dla danego filmu
- Dodatkowe endpointy: obliczenia matematyczne, geokodowanie

## Technologie

- **Framework**: FastAPI
- **ORM**: SQLAlchemy (prosty setup podobny do Peewee)
- **Baza danych**: SQLite (movies-extended.db)
- **Python**: 3.12+

## Instalacja

1. Sklonuj repozytorium i przejdź do katalogu projektu:
```bash
cd MovieDBREST
```

2. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

## Uruchomienie

Uruchom serwer FastAPI:
```bash
fastapi dev main.py
```

Lub:
```bash
uvicorn main:app --reload --port 8000
```

Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:8000`

Dokumentacja API (Swagger): `http://127.0.0.1:8000/docs`

## Endpointy API

### Filmy

- `GET /movies` - Pobierz wszystkie filmy
- `GET /movies/{id}` - Pobierz film po ID
- `POST /movies` - Dodaj nowy film
  ```json
  {
    "title": "Inception",
    "year": 2010,
    "director": "Christopher Nolan",
    "description": "A thief who steals corporate secrets..."
  }
  ```
- `PUT /movies/{id}` - Zaktualizuj film
- `DELETE /movies/{id}` - Usuń film
- `DELETE /movies` - Usuń wszystkie filmy

### Aktorzy

- `GET /actors` - Pobierz wszystkich aktorów
- `GET /actors/{id}` - Pobierz aktora po ID
- `POST /actors` - Dodaj nowego aktora
  ```json
  {
    "name": "Leonardo",
    "surname": "DiCaprio"
  }
  ```
- `PUT /actors/{id}` - Zaktualizuj aktora
- `DELETE /actors/{id}` - Usuń aktora

### Relacje

- `GET /movies/{movie_id}/actors` - Pobierz aktorów dla danego filmu

### Inne

- `GET /` - Hello World
- `GET /sum?x=5&y=3` - Dodawanie
- `GET /subtract?x=10&y=3` - Odejmowanie
- `GET /multiply?x=5&y=3` - Mnożenie
- `GET /divide?x=10&y=2` - Dzielenie
- `GET /geocode?lat=52.237049&lon=21.017532` - Geokodowanie (OpenStreetMap)

## Struktura projektu

```
MovieDBREST/
├── main.py                 # Główna aplikacja FastAPI z ORM
├── movies-extended.db      # Baza danych SQLite
├── requirements.txt        # Zależności projektu
├── .gitignore             # Pliki ignorowane przez git
└── api-tests.http         # Testy API
```

## Modele ORM

### Movie (tabela: movie)
- `id` (Integer, Primary Key)
- `title` (String)
- `year` (Integer)
- `director` (String)
- `description` (String)

### Actor (tabela: actor)
- `id` (Integer, Primary Key)
- `name` (String)
- `surname` (String)

### movie_actor_through (Tabela pośrednia)
- `movie_id` (Foreign Key → movie.id)
- `actor_id` (Foreign Key → actor.id)

**Uwaga**: Modele ORM są uproszczone - bez definicji relacji (relationships). Połączenie między filmami a aktorami odbywa się przez surowe zapytanie SQL z JOIN.

## Cechy implementacji ORM

✅ **Prosty setup** - Jedna globalna sesja `db = Session(engine)` podobnie do Peewee  
✅ **Bezpieczeństwo** - Ochrona przed SQL Injection  
✅ **Czytelność** - Kod Pythonowy zamiast stringów SQL  
✅ **Pydantic validation** - Walidacja requestów przez modele Pydantic  
✅ **Type hints** - Wsparcie dla adnotacji typów  
✅ **Poziom junior** - Prosty kod bez zaawansowanych wzorców (bez Depends, bez relationship)
