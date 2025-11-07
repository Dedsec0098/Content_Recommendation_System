import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API with error handling"""
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=f91112461a37120e904df8eff7657381&language=en-US".format(movie_id)
        response = requests.get(url, timeout=5)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                return full_path
            else:
                print(f"No poster_path for movie_id {movie_id}")
        elif response.status_code == 404:
            print(f"Movie ID {movie_id} not found on TMDB (404)")
        else:
            print(f"Error {response.status_code} for movie_id {movie_id}")
    except requests.exceptions.Timeout:
        print(f"Timeout fetching poster for movie_id {movie_id}")
    except requests.exceptions.RequestException as e:
        print(f"Request error for movie_id {movie_id}: {e}")
    except Exception as e:
        print(f"Unexpected error fetching poster for movie_id {movie_id}: {e}")
    return None

def fetch_trailer(movie_id):
    """Fetch movie trailer from TMDB API"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=f91112461a37120e904df8eff7657381&language=en-US"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get('results', [])
            
            # Find the first trailer (preferably YouTube)
            for video in videos:
                if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                    youtube_key = video['key']
                    return f"https://www.youtube.com/watch?v={youtube_key}"
            
            print(f"No trailer found for movie_id {movie_id}")
        else:
            print(f"Error {response.status_code} fetching trailer for movie_id {movie_id}")
    except Exception as e:
        print(f"Error fetching trailer for movie_id {movie_id}: {e}")
    return None

def recommend(movie):
    """Get movie recommendations"""
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_trailers = []
        
        for i in distances[1:6]:
            # Fetch the movie poster and trailer
            movie_id = movies.iloc[i[0]].movie_id
            movie_title = movies.iloc[i[0]].title
            
            print(f"Fetching data for: {movie_title} (ID: {movie_id})")
            poster = fetch_poster(movie_id)
            trailer = fetch_trailer(movie_id)
            
            if poster:
                print(f"✓ Successfully fetched poster for {movie_title}")
            else:
                print(f"✗ Failed to fetch poster for {movie_title}")
            
            if trailer:
                print(f"✓ Successfully fetched trailer for {movie_title}")
            else:
                print(f"✗ No trailer available for {movie_title}")
            
            recommended_movie_posters.append(poster)
            recommended_movie_trailers.append(trailer)
            recommended_movie_names.append(movie_title)

        return recommended_movie_names, recommended_movie_posters, recommended_movie_trailers
    except Exception as e:
        st.error(f"Error getting recommendations: {e}")
        return [], [], []


st.header('🎬 Movie Recommender System')
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    with st.spinner('Recommending you similar movies...'):
        recommended_movie_names, recommended_movie_posters, recommended_movie_trailers = recommend(selected_movie)
    
    if recommended_movie_names:
        st.success(f"Top 5 movies similar to '{selected_movie}':")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        columns = [col1, col2, col3, col4, col5]
        
        for idx, col in enumerate(columns):
            with col:
                st.markdown(f"**{recommended_movie_names[idx]}**")
                if recommended_movie_posters[idx]:
                    st.image(recommended_movie_posters[idx], use_column_width=True)
                else:
                    # Show a placeholder for missing posters
                    st.markdown(
                        """
                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    padding: 60px 20px; 
                                    text-align: center; 
                                    border-radius: 10px; 
                                    color: white; 
                                    font-size: 48px;'>
                            🎬
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    st.caption("Poster not available")
                
                # Add trailer button if available
                if recommended_movie_trailers[idx]:
                    st.markdown(
                        f'<a href="{recommended_movie_trailers[idx]}" target="_blank">'
                        f'<button style="background-color: #FF0000; color: white; padding: 8px 16px; '
                        f'border: none; border-radius: 5px; cursor: pointer; width: 100%; '
                        f'font-weight: bold;">▶ Watch Trailer</button></a>',
                        unsafe_allow_html=True
                    )
                else:
                    st.caption("🎥 Trailer not available")
    else:
        st.error("Could not get recommendations. Please try again.")

# Add info section
st.markdown("---")
st.info("""
**Note about posters & trailers:**
- Some movie posters or trailers may not load if:
  - The movie ID in the dataset doesn't match TMDB's database
  - The movie has been removed from TMDB
  - Network connection issues
  - TMDB API rate limits
  - Some older movies may not have trailers available on YouTube
  
The recommendations are still accurate even without posters or trailers! 🎬
""")





