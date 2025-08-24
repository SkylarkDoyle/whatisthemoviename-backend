# 🎬 WhatIsTheMovieName (Backend)

This is the FastAPI backend for **WhatIsTheMovieName**, an API that identifies movies or TV shows from a single screenshot.

It uses:
- **Cloudinary** → to store uploaded images
- **Selenium + Bing Visual Search** → to extract film/show titles from screenshots
- **TMDB API** → to fetch detailed metadata about the movie/show
- **Pydantic Schemas** → for structured JSON responses

---

## 🚀 Features
- Upload a screenshot (JPEG/PNG)
- Extract the film/show title from the image
- Search TMDB (Movies + TV Shows)
- Return metadata: title, overview, release date, poster, backdrop, rating
- Optimized with image compression + async requests

---

## ⚡ Tech Stack
- **Python 3.10+**
- **FastAPI**
- **Selenium (Edge/Chrome Driver)**
- **httpx**
- **Pydantic**
- **Cloudinary SDK**

---

## 🛠 Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/yourusername/whatisthemoviename.git
cd whatisthemoviename

### 2️⃣ Setup environment & dependencies with uv
```bash
uv sync
```


### ▶️ Running the API
```bash
uv run main.py
```

---

## 📝 API Endpoints
- `POST /analyze` → Upload an image and get metadata
- `GET /docs` → Interactive API docs

---


## 🙏 Acknowledgements
- [TMDB API](https://www.themoviedb.org/documentation/api)
- [Cloudinary](https://cloudinary.com/documentation)

