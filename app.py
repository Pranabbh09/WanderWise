from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Import configuration
from config import (
    GOOGLE_API_KEY, CUSTOM_TO_GOOGLE_TYPE, SEMANTIC_PLACE_TYPES, 
    RATED_PLACE_TYPES, SENTENCE_TRANSFORMER_MODEL, DEFAULT_SEARCH_RADIUS,
    DEFAULT_MAX_RESULTS, DEFAULT_RATED_COUNT, DEFAULT_SEMANTIC_COUNT,
    get_config_summary, validate_config
)

# Initialize the sentence transformer
embedder = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)

def get_coordinates(city_name):
    """Get coordinates for a city"""
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={GOOGLE_API_KEY}"
        response = requests.get(url).json()
        if response['status'] == 'OK':
            location = response['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            raise Exception(response.get('error_message', 'Failed to get coordinates'))
    except Exception as e:
        logger.error(f"Error getting coordinates: {e}")
        raise

def get_places(lat, lng, place_type='tourist_attraction', max_results=60):
    """Fetch places from Google Places API"""
    try:
        places = []
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': f'{lat},{lng}',
            'radius': 50000,
            'type': place_type,
            'key': GOOGLE_API_KEY
        }
        
        while len(places) < max_results:
            res = requests.get(url, params=params).json()
            places.extend(res.get('results', []))
            next_page_token = res.get('next_page_token')
            if next_page_token:
                time.sleep(2)
                params['pagetoken'] = next_page_token
            else:
                break
        
        return places[:max_results]
    except Exception as e:
        logger.error(f"Error fetching places: {e}")
        raise

def categorize_place(place_types):
    """Categorize a place as 'semantic' or 'rated' based on its types"""
    place_types_set = set(place_types)
    
    if place_types_set.intersection(RATED_PLACE_TYPES):
        return 'rated'
    
    if place_types_set.intersection(SEMANTIC_PLACE_TYPES):
        return 'semantic'
    
    return 'unknown'

def build_enhanced_dataframe(places):
    """Build dataframe with automatic categorization"""
    data = []
    for p in places:
        place_types = p.get('types', [])
        category = categorize_place(place_types)
        
        if category == 'unknown':
            rating = p.get('rating', 0)
            category = 'rated' if rating > 0 else 'semantic'
        
        data.append({
            'name': p.get('name'),
            'address': p.get('vicinity', 'N/A'),
            'rating': p.get('rating', 0),
            'user_ratings_total': p.get('user_ratings_total', 0),
            'types': ", ".join(place_types),
            'category': category,
            'description': f"{p.get('name')} - {', '.join(place_types)}"
        })
    
    return pd.DataFrame(data)

def recommend_rated_places(df, top_k=10):
    """Recommend rated places using rating-based approach"""
    rated_df = df[df['category'] == 'rated'].copy()
    
    if rated_df.empty:
        return pd.DataFrame()
    
    rated_df['score'] = rated_df['rating'] * np.log1p(rated_df['user_ratings_total'])
    return rated_df.sort_values(by='score', ascending=False).head(top_k)

def generate_embeddings_for_semantic(df):
    """Generate embeddings only for semantic places"""
    semantic_df = df[df['category'] == 'semantic'].copy()
    
    if not semantic_df.empty:
        semantic_df['embedding'] = semantic_df['description'].apply(
            lambda x: embedder.encode(x, convert_to_tensor=True)
        )
    
    return semantic_df

def recommend_semantic_places(df, user_query, top_k=5):
    """Recommend semantic places using semantic similarity"""
    semantic_df = generate_embeddings_for_semantic(df)
    
    if semantic_df.empty:
        return pd.DataFrame()
    
    query_vec = embedder.encode(user_query, convert_to_tensor=True)
    semantic_df['similarity'] = semantic_df['embedding'].apply(
        lambda x: util.cos_sim(query_vec, x).item()
    )
    
    return semantic_df.sort_values(by='similarity', ascending=False).head(top_k)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """API endpoint for recommendations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        city = data.get('city', '').strip()
        place_type = data.get('place_type', '').strip().lower()
        method = data.get('method', 'rating').strip().lower()
        
        if not city or not place_type:
            return jsonify({'success': False, 'error': 'City and place type are required'})
        
        # Get coordinates
        lat, lng = get_coordinates(city)
        
        # Get Google Places API type
        google_place_type = CUSTOM_TO_GOOGLE_TYPE.get(place_type, 'tourist_attraction')
        
        # Fetch places
        raw_places = get_places(lat, lng, google_place_type, DEFAULT_MAX_RESULTS)
        df = build_enhanced_dataframe(raw_places)
        
        if df.empty:
            return jsonify({'success': False, 'error': 'No places found for your query'})
        
        # Process based on method
        if method == 'semantic':
            semantic_results = recommend_semantic_places(df, place_type, top_k=10)
            results = {
                'rated': [],
                'semantic': semantic_results.to_dict('records') if not semantic_results.empty else [],
                'stats': {
                    'total_places': len(df),
                    'rated_places': len(df[df['category'] == 'rated']),
                    'semantic_places': len(df[df['category'] == 'semantic'])
                }
            }
            
        else:  # rating method (default)
            rated_results = recommend_rated_places(df, top_k=10)
            results = {
                'rated': rated_results.to_dict('records') if not rated_results.empty else [],
                'semantic': [],
                'stats': {
                    'total_places': len(df),
                    'rated_places': len(df[df['category'] == 'rated']),
                    'semantic_places': len(df[df['category'] == 'semantic'])
                }
            }
        
        return jsonify({'success': True, 'data': results})
        
    except Exception as e:
        logger.error(f"Error in recommend endpoint: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Place Recommendation API is running'})

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get application configuration"""
    config_summary = get_config_summary()
    config_issues = validate_config()
    
    return jsonify({
        'success': True,
        'config': config_summary,
        'issues': config_issues
    })


if __name__ == '__main__':
    from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, APP_NAME, APP_VERSION
    
    print(f"🚀 Starting {APP_NAME} v{APP_VERSION}...")
    print(f"📍 Visit http://{FLASK_HOST}:{FLASK_PORT} for the web interface")
    print(f"🔗 API endpoint: http://{FLASK_HOST}:{FLASK_PORT}/api/recommend")
    print(f"⚙️  Configuration endpoint: http://{FLASK_HOST}:{FLASK_PORT}/api/config")
    
    # Show configuration issues if any
    config_issues = validate_config()
    if config_issues:
        print("\n⚠️  Configuration warnings:")
        for issue in config_issues:
            print(f"   {issue}")
    
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)

