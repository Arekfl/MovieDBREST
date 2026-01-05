# Movie Database REST API

REST API do zarządzania bazą danych filmów i aktorów, zbudowane przy użyciu FastAPI i SQLAlchemy ORM.

## Funkcjonalności

- Pełny CRUD dla filmów (tytuł, rok, reżyser, opis)
- Pełny CRUD dla aktorów (imię, rok urodzenia)
- Relacja wiele-do-wielu między filmami a aktorami
- Endpoint do pobierania aktorów dla danego filmu
- Dodatkowe endpointy: obliczenia matematyczne, geokodowanie

## Technologie

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Baza danych**: SQLite
- **Python**: 3.8+

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
    "name": "Leonardo DiCaprio",
    "birth_year": 1974
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

### Movie
- `ID` (Integer, Primary Key)
- `title` (String, Required)
- `year` (Integer, Required)
- `director` (String, Required)
- `description` (String, Optional)
- `actors` (Relationship - wiele do wielu)

### Actor
- `ID` (Integer, Primary Key)
- `name` (String, Required)
- `birth_year` (Integer, Optional)
- `movies` (Relationship - wiele do wielu)

### MovieActor (Tabela pośrednia)
- `movie_id` (Foreign Key → movies.ID)
- `actor_id` (Foreign Key → actors.ID)

## Przewaga ORM nad surowym SQL

✅ **Bezpieczeństwo** - Ochrona przed SQL Injection  
✅ **Czytelność** - Kod Pythonowy zamiast stringów SQL  
✅ **Maintainability** - Łatwiejsze w utrzymaniu i modyfikacji  
✅ **Relationships** - Automatyczne zarządzanie relacjami  
✅ **Type Safety** - Wsparcie dla type hintów  
✅ **Migrations** - Łatwa ewolucja schematu bazy danych
