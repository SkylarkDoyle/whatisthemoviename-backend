
import httpx
from ..config import settings
from typing import Dict
from ..schemas.film import Film

class TMDBService:
    def __init__(self):
        self.api_key = settings.tmdb_api_key
        self.base_image_url = "https://image.tmdb.org/t/p/original"
        self.client = httpx.AsyncClient(
            base_url="https://api.themoviedb.org/3",
            timeout=httpx.Timeout(15.0, connect=5.0)
        )
        
    async def search_movie(self, title: str) -> Dict[str, any]:
        try:
            endpoint = "/search/movie"
            params = {
                'api_key': self.api_key,
                'query': title
            }
            films = await self.client.get(endpoint, params=params)
            data = films.json()
            return data.get("results", [])
        except httpx.RequestError as e:
            raise Exception(f"TMDB request failed: {str(e)}")
        except httpx.ConnectTimeout as e:
            raise Exception(f"TMDB connection timed out: {str(e)}")
        
    async def search_tvshow(self, title: str) -> Dict[str, any]:
        try:
            endpoint = "/search/tv"
            params = {
                'api_key': self.api_key,
                'query': title
            }
            films = await self.client.get(endpoint, params=params)
            data = films.json()
            return data.get("results", [])
        except httpx.RequestError as e:
            raise Exception(f"TMDB request failed: {str(e)}")
        except httpx.ConnectTimeout as e:
            raise Exception(f"TMDB connection timed out: {str(e)}")

    #schema mapper
    def tmdb_to_film(self, data: dict) -> Film:
        return Film(
            id=data["id"],
            title=data.get("title") or data.get("name"),
            overview=data.get("overview"),
            release_date=data.get("release_date") or data.get("first_air_date"),
            poster_url = f"{self.base_image_url}{data['poster_path']}" if data.get('poster_path') else None,
            backdrop_url = f"{self.base_image_url}{data['backdrop_path']}" if data.get('backdrop_path') else None,
            vote_average=data.get("vote_average"),
        )
    # async def search_person(self, name: str) -> Dict[str, any]:
    #     endpoint = f"{self.base_url}/search/person"
    #     params = {
    #         'api_key': self.api_key,
    #         'query': title
    #     }
        
        