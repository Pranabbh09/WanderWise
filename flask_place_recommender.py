from flask import Flask, request, jsonify, render_template_string
import requests
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration (from your provided code)
GOOGLE_API_KEY = 'AIzaSyDzbgxX9OR4-ds2SgMOAGWlhZYRZf9pZIM'
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Place Type Mapper
custom_to_google_type = {
    'restaurant': 'restaurant',
    'cafe': 'cafe',
    'hotel': 'lodging',
    'Temple': 'temple',
    'hotels': 'lodging',
    'shopping': 'shopping_mall',
    'fort': 'tourist_attraction'
}

# Place categorization based on type
SEMANTIC_PLACE_TYPES = {
    'temple', 'church', 'mosque', 'synagogue', 'hindu_temple',
    'tourist_attraction', 'museum', 'park', 'natural_feature',
    'establishment', 'point_of_interest', 'place_of_worship',
    'historical_site', 'monument', 'landmark', 'fort', 'palace'
}

RATED_PLACE_TYPES = {
    'restaurant', 'cafe', 'lodging', 'hotel', 'food', 'meal_takeaway',
    'shopping_mall', 'store', 'spa', 'gym', 'entertainment',
    'night_club', 'bar', 'movie_theater', 'bowling_alley'
}

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
    """
    Categorize a place as 'semantic' or 'rated' based on its types
    """
    place_types_set = set(place_types)
    
    # Check if any type matches rated categories
    if place_types_set.intersection(RATED_PLACE_TYPES):
        return 'rated'
    
    # Check if any type matches semantic categories
    if place_types_set.intersection(SEMANTIC_PLACE_TYPES):
        return 'semantic'
    
    # Default fallback: if it has a rating > 0, consider it rated, otherwise semantic
    return 'unknown'

def build_enhanced_dataframe(places):
    """
    Build dataframe with automatic categorization
    """
    data = []
    for p in places:
        place_types = p.get('types', [])
        category = categorize_place(place_types)
        
        # If category is unknown, use rating as fallback
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
    """
    Recommend rated places using rating-based approach
    """
    rated_df = df[df['category'] == 'rated'].copy()
    
    if rated_df.empty:
        return pd.DataFrame()
    
    # Calculate score for rated places
    rated_df['score'] = rated_df['rating'] * np.log1p(rated_df['user_ratings_total'])
    return rated_df.sort_values(by='score', ascending=False).head(top_k)[
        ['name', 'address', 'rating', 'user_ratings_total', 'category']
    ]

def generate_embeddings_for_semantic(df):
    """
    Generate embeddings only for semantic places
    """
    semantic_df = df[df['category'] == 'semantic'].copy()
    
    if not semantic_df.empty:
        semantic_df['embedding'] = semantic_df['description'].apply(
            lambda x: embedder.encode(x, convert_to_tensor=True)
        )
    
    return semantic_df

def recommend_semantic_places(df, user_query, top_k=5):
    """
    Recommend semantic places using semantic similarity
    """
    semantic_df = generate_embeddings_for_semantic(df)
    
    if semantic_df.empty:
        return pd.DataFrame()
    
    query_vec = embedder.encode(user_query, convert_to_tensor=True)
    semantic_df['similarity'] = semantic_df['embedding'].apply(
        lambda x: util.cos_sim(query_vec, x).item()
    )
    
    return semantic_df.sort_values(by='similarity', ascending=False).head(top_k)[
        ['name', 'address', 'types', 'similarity', 'category']
    ]

def get_comprehensive_recommendations(lat, lng, user_query=None, rated_count=10, semantic_count=5):
    """
    Get comprehensive recommendations with automatic categorization
    """
    try:
        logger.info("Fetching places...")
        places = get_places(lat, lng)
        
        logger.info("Building enhanced dataframe...")
        df = build_enhanced_dataframe(places)
        
        logger.info(f"Found {len(df)} total places:")
        logger.info(f"- Rated places: {len(df[df['category'] == 'rated'])}")
        logger.info(f"- Semantic places: {len(df[df['category'] == 'semantic'])}")
        
        results = {}
        
        # Get rated recommendations
        logger.info("Getting rated place recommendations...")
        rated_recommendations = recommend_rated_places(df, rated_count)
        results['rated'] = rated_recommendations.to_dict('records') if not rated_recommendations.empty else []
        
        # Get semantic recommendations
        if user_query:
            logger.info(f"Getting semantic recommendations for query: '{user_query}'")
            semantic_recommendations = recommend_semantic_places(df, user_query, semantic_count)
            results['semantic'] = semantic_recommendations.to_dict('records') if not semantic_recommendations.empty else []
        else:
            logger.info("No query provided for semantic search. Skipping semantic recommendations.")
            results['semantic'] = []
        
        # Add statistics
        results['stats'] = {
            'total_places': len(df),
            'rated_places': len(df[df['category'] == 'rated']),
            'semantic_places': len(df[df['category'] == 'semantic'])
        }
        
        return results
        
    except Exception as e:
        logger.error(f"Error in comprehensive recommendations: {e}")
        raise

# HTML Template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌟 Place Recommendation System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .form-section {
            padding: 40px;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .form-group {
            position: relative;
        }
        
        .form-group.full-width {
            grid-column: 1 / -1;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2d3748;
            font-size: 1.1em;
        }
        
        input, select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #f7fafc;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
        }
        
        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px 40px;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        }
        
        .submit-btn:active {
            transform: translateY(-1px);
        }
        
        .results {
            padding: 0 40px 40px;
        }
        
        .stats-card {
            background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #4a5568;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: #2d3748;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: inline-block;
        }
        
        .places-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .place-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid #e2e8f0;
            position: relative;
            overflow: hidden;
        }
        
        .place-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .place-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        
        .place-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 15px;
            line-height: 1.3;
        }
        
        .place-address {
            color: #4a5568;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            font-size: 0.95em;
        }
        
        .place-address::before {
            content: '📍';
            margin-right: 8px;
        }
        
        .place-metrics {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .metric-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            display: flex;
            align-items: center;
        }
        
        .rating-badge {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }
        
        .similarity-badge {
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            color: white;
        }
        
        .reviews-badge {
            background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
            color: white;
        }
        
        .place-types {
            margin-top: 15px;
            padding: 10px;
            background: #f7fafc;
            border-radius: 8px;
            font-size: 0.9em;
            color: #4a5568;
            border-left: 3px solid #667eea;
        }
        
        .loading {
            text-align: center;
            padding: 60px 20px;
            color: #4a5568;
            font-size: 1.2em;
        }
        
        .loading::before {
            content: '🔍';
            font-size: 3em;
            display: block;
            margin-bottom: 20px;
            animation: spin 2s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
            color: #c53030;
            padding: 25px;
            border-radius: 15px;
            margin-top: 20px;
            border-left: 5px solid #e53e3e;
            font-weight: 600;
        }
        
        .no-results {
            text-align: center;
            padding: 60px 20px;
            color: #4a5568;
            font-size: 1.2em;
        }
        
        .no-results::before {
            content: '😔';
            font-size: 3em;
            display: block;
            margin-bottom: 20px;
        }
        
        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .places-grid {
                grid-template-columns: 1fr;
            }
            
            .container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .header {
                padding: 30px 20px;
            }
            
            .form-section, .results {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 Place Recommendation System</h1>
            <p>Discover amazing places with AI-powered recommendations</p>
        </div>
        
        <div class="form-section">
            <form id="recommendationForm">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="city">🏙️ City Name</label>
                        <input type="text" id="city" name="city" required placeholder="e.g., Indore, Mumbai, Delhi">
                    </div>
                    
                    <div class="form-group">
                        <label for="place_type">📍 Place Type</label>
                        <input type="text" id="place_type" name="place_type" required placeholder="e.g., restaurant, temple, cafe, hotel">
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="method">🔍 Recommendation Method</label>
                        <select id="method" name="method">
                            <option value="auto">🤖 Auto (Smart Categorization)</option>
                            <option value="rating">⭐ Rating-based</option>
                            <option value="semantic">🧠 Semantic Search</option>
                        </select>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn">
                    Get Recommendations
                </button>
            </form>
        </div>
        
        <div id="results" class="results" style="display: none;"></div>
    </div>

    <script>
        document.getElementById('recommendationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = '<div class="loading">Searching for amazing places...</div>';
            
            try {
                const response = await fetch('/api/recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    displayResults(result.data);
                } else {
                    resultsDiv.innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                }
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">❌ Network error: ${error.message}</div>`;
            }
        });
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            let html = '';
            
            // Add statistics
            if (data.stats) {
                html += `
                    <div class="stats-card">
                        <h3>📊 Search Statistics</h3>
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-number">${data.stats.total_places}</div>
                                <div class="stat-label">Total Places</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number">${data.stats.rated_places}</div>
                                <div class="stat-label">Rated Places</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number">${data.stats.semantic_places}</div>
                                <div class="stat-label">Semantic Places</div>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            // Add rated results
            if (data.rated && data.rated.length > 0) {
                html += '<h2 class="section-title">🌟 Top Rated Places</h2>';
                html += '<div class="places-grid">';
                data.rated.forEach(place => {
                    html += `
                        <div class="place-card">
                            <div class="place-name">${place.name}</div>
                            <div class="place-address">${place.address}</div>
                            <div class="place-metrics">
                                <span class="metric-badge rating-badge">⭐ ${place.rating}</span>
                                <span class="metric-badge reviews-badge">👥 ${place.user_ratings_total} reviews</span>
                            </div>
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            // Add semantic results
            if (data.semantic && data.semantic.length > 0) {
                html += '<h2 class="section-title">🔍 Semantic Matches</h2>';
                html += '<div class="places-grid">';
                data.semantic.forEach(place => {
                    html += `
                        <div class="place-card">
                            <div class="place-name">${place.name}</div>
                            <div class="place-address">${place.address}</div>
                            <div class="place-metrics">
                                <span class="metric-badge similarity-badge">🎯 ${(place.similarity * 100).toFixed(1)}% match</span>
                            </div>
                            <div class="place-types">🏷️ ${place.types}</div>
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            if (html === '' || ((!data.rated || data.rated.length === 0) && (!data.semantic || data.semantic.length === 0))) {
                html += '<div class="no-results">No places found. Try a different search term or city.</div>';
            }
            
            resultsDiv.innerHTML = html;
        }
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    """Home page with web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """API endpoint for recommendations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        city = data.get('city', '').strip()
        place_type = data.get('place_type', '').strip().lower()
        method = data.get('method', 'auto').strip().lower()
        
        if not city or not place_type:
            return jsonify({'success': False, 'error': 'City and place type are required'})
        
        # Get coordinates
        lat, lng = get_coordinates(city)
        
        # Get Google Places API type
        google_place_type = custom_to_google_type.get(place_type, 'tourist_attraction')
        
        # Fetch places
        raw_places = get_places(lat, lng, google_place_type)
        df = build_enhanced_dataframe(raw_places)
        
        if df.empty:
            return jsonify({'success': False, 'error': 'No places found for your query'})
        
        # Process based on method
        if method == 'semantic':
            # Semantic search only
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
            
        else:  # rating method
            # Rating-based only
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

if __name__ == '__main__':
    print("🚀 Starting Place Recommendation Flask App...")
    print("📍 Visit http://localhost:5000 for the web interface")
    print("🔗 API endpoint: http://localhost:5000/api/recommend")
    app.run(debug=True, host='0.0.0.0', port=5000)