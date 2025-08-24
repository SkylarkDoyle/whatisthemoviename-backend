import os
import asyncio
import time
import cloudinary
# import httpx
from fastapi import APIRouter, UploadFile, File

from ..utils.image_utils import *
from typing import List
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus

from ..services.ollama_service import describe_image
from ..services.tmdb_service import TMDBService
from ..services.scrapers import scrape_bing_sync

router = APIRouter()
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

tmdb_service = TMDBService()
MAX_IMAGES = 3

# run blocking Selenium inside thread
executor = ThreadPoolExecutor(max_workers=2)


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # uploaded_urls = []
    start_time = time.time()
    #read file before passing to cloudinary
    content = await file.read()
        
    #send to cloudinary
    result = cloudinary.uploader.upload(content, folder="film_uploads", resource_type="image")
        
    #get the cloudinary url back
    upload_url = result["secure_url"]
        
    print("uploaded_urls[0]", upload_url)
    
    #append to bing visual image
    bing_url = f"https://www.bing.com/images/search?view=detailv2&iss=SBI&form=SBIHMP&sbisrc=UrlPaste&q=imgurl:{upload_url}&idpbck=1&vsimg={upload_url}&selectedindex=0&id={upload_url}"
     
    print("bing_url", bing_url)
    
    #scrape bing visual image text and return it 
    loop = asyncio.get_event_loop()
    film_title = await loop.run_in_executor(executor, scrape_bing_sync, bing_url)

    print("film_title", film_title)
    #send to tmdb 
    tmdb_results = await tmdb_service.search_movie(film_title)
    
    if not tmdb_results:
        tmdb_results = await tmdb_service.search_tvshow(film_title)
    
    print("tmdb_results", tmdb_results)
    end_time = time.time()

    elapsed_time = round(end_time - start_time, 3)
    print(f"\n\n Total time: {elapsed_time} seconds")
    
    # parse and map the film data 
    if tmdb_results:
        film = tmdb_service.tmdb_to_film(tmdb_results[0])
        return film.model_dump()
    return {"error": "No results from the Movie database"}
        
     
    # print("public id", result["public_id"])
    
    #delete from cloudinary
    
    # await delete_upload(result["public_id"])
    
    
