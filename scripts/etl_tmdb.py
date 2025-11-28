import requests
import uuid
import random
import sys
import os
from datetime import datetime, timedelta, time

# Add project root to path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import get_session, engine
from app.core.models.phim import Phim
from app.core.models.lichchieu import LichChieu
from app.core.models.phongphim import PhongPhim

# Configuration
API_KEY = "849b291dac43bbb30be7f24c983169d3"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_genres():
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY, "language": "vi-VN"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {g["id"]: g["name"] for g in genres}
    return {}

def fetch_movies(start_date, end_date):
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "vi-VN",
        "region": "VN",
        "sort_by": "popularity.desc",
        "primary_release_date.gte": start_date,
        "primary_release_date.lte": end_date,
        "with_release_type": "2|3"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    print(f"Error fetching movies: {response.status_code} {response.text}")
    return []

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "vi-VN"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {}

def ensure_rooms(session: Session):
    rooms = session.query(PhongPhim).all()
    if not rooms:
        print("No rooms found. Creating default rooms...")
        default_rooms = [
            PhongPhim(ma_phong="P01", ten_phong="Phòng 1", so_luong_ghe=100),
            PhongPhim(ma_phong="P02", ten_phong="Phòng 2", so_luong_ghe=120),
            PhongPhim(ma_phong="P03", ten_phong="Phòng 3", so_luong_ghe=80),
        ]
        session.add_all(default_rooms)
        session.commit()
        rooms = session.query(PhongPhim).all()
    return rooms

def run_etl():
    session = get_session()
    try:
        # 1. Setup Dates
        today = datetime.now()
        next_week = today + timedelta(days=7)
        start_date_str = today.strftime('%Y-%m-%d')
        end_date_str = next_week.strftime('%Y-%m-%d')
        
        print(f"🚀 Starting ETL for {start_date_str} to {end_date_str}")

        # 2. Fetch Data
        genres_map = fetch_genres()
        movies_data = fetch_movies(start_date_str, end_date_str)
        
        if not movies_data:
            print("No movies found.")
            return

        # 3. Ensure Rooms Exist
        rooms = ensure_rooms(session)
        room_ids = [r.ma_phong for r in rooms]

        # 4. Process Movies
        for m_data in movies_data:
            movie_id = str(m_data["id"])
            
            # Fetch full details for NSX (Production Companies)
            details = get_movie_details(movie_id)
            nsx = details.get("production_companies", [{}])[0].get("name", "Unknown") if details.get("production_companies") else "Unknown"
            
            # Map Genres
            genre_names = [genres_map.get(g_id, "") for g_id in m_data.get("genre_ids", [])]
            genre_str = ", ".join(filter(None, genre_names))

            # Upsert Movie
            existing_movie = session.query(Phim).filter(Phim.ma_phim == movie_id).first()
            if not existing_movie:
                new_movie = Phim(
                    ma_phim=movie_id,
                    ten_phim=m_data["title"],
                    NSX=nsx,
                    nhan="P" if not m_data.get("adult") else "C18", # Simple logic
                    the_loai=genre_str,
                    poster=f"{IMAGE_BASE_URL}{m_data['poster_path']}" if m_data.get('poster_path') else None
                )
                session.add(new_movie)
                print(f"➕ Added movie: {m_data['title']}")
            else:
                # Update existing?
                existing_movie.ten_phim = m_data["title"]
                existing_movie.poster = f"{IMAGE_BASE_URL}{m_data['poster_path']}" if m_data.get('poster_path') else None
                print(f"🔄 Updated movie: {m_data['title']}")
            
            # 5. Generate Schedule (LichChieu)
            # Strategy: For each day in the range, schedule this movie 1-2 times
            current_date = today
            while current_date <= next_week:
                # Randomly decide if movie shows today (70% chance)
                if random.random() > 0.3:
                    # 1-3 shows per day
                    num_shows = random.randint(1, 3)
                    for _ in range(num_shows):
                        # Random time between 9:00 and 23:00
                        hour = random.randint(9, 22)
                        minute = random.choice([0, 15, 30, 45])
                        show_time = time(hour, minute)
                        
                        # Random room
                        room_id = random.choice(room_ids)
                        
                        # Check collision (Simple check, can be improved)
                        # For now, just insert. In real app, check if room is booked.
                        
                        lich_id = str(uuid.uuid4())[:8] # Short ID
                        
                        new_lich = LichChieu(
                            ma_lich_chieu=lich_id,
                            gio=show_time,
                            ngay=current_date.date(),
                            ma_phim=movie_id,
                            ma_phong=room_id
                        )
                        session.add(new_lich)
                
                current_date += timedelta(days=1)
        
        session.commit()
        print("✅ ETL Completed Successfully!")

    except Exception as e:
        session.rollback()
        print(f"❌ ETL Failed: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    run_etl()
