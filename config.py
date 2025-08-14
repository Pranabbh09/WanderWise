"""
🌍 Smart Place Recommender - Configuration
Centralized configuration for the application
"""

import os

# Google Places API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyDzbgxX9OR4-ds2SgMOAGWlhZYRZf9pZIM')

# Flask Configuration
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Application Configuration
APP_NAME = "🌍 Smart Place Recommender"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-powered place recommendations using semantic search and ratings"

# Search Configuration
DEFAULT_SEARCH_RADIUS = 50000  # meters
DEFAULT_MAX_RESULTS = 60
DEFAULT_RATED_COUNT = 10
DEFAULT_SEMANTIC_COUNT = 5

# Place Type Mappings
CUSTOM_TO_GOOGLE_TYPE = {
    'restaurant': 'restaurant',
    'cafe': 'cafe',
    'hotel': 'lodging',
    'Temple': 'temple',
    'hotels': 'lodging',
    'shopping': 'shopping_mall',
    'fort': 'tourist_attraction',
    'museum': 'museum',
    'park': 'park',
    'beach': 'natural_feature',
    'mountain': 'natural_feature',
    'lake': 'natural_feature',
    'airport': 'airport',
    'hospital': 'hospital',
    'school': 'school',
    'university': 'university',
    'bank': 'bank',
    'pharmacy': 'pharmacy',
    'gas_station': 'gas_station',
    'post_office': 'post_office'
}

# Place Categorization
SEMANTIC_PLACE_TYPES = {
    'temple', 'church', 'mosque', 'synagogue', 'hindu_temple',
    'tourist_attraction', 'museum', 'park', 'natural_feature',
    'establishment', 'point_of_interest', 'place_of_worship',
    'historical_site', 'monument', 'landmark', 'fort', 'palace',
    'art_gallery', 'library', 'theater', 'stadium', 'aquarium',
    'zoo', 'botanical_garden', 'national_park', 'beach', 'mountain',
    'lake', 'river', 'waterfall', 'cave', 'volcano'
}

RATED_PLACE_TYPES = {
    'restaurant', 'cafe', 'lodging', 'hotel', 'food', 'meal_takeaway',
    'shopping_mall', 'store', 'spa', 'gym', 'entertainment',
    'night_club', 'bar', 'movie_theater', 'bowling_alley',
    'beauty_salon', 'hair_care', 'car_wash', 'car_rental',
    'real_estate_agency', 'lawyer', 'dentist', 'doctor',
    'veterinary_care', 'pet_store', 'hardware_store', 'electronics_store'
}

# AI Model Configuration
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'
SIMILARITY_THRESHOLD = 0.3

# Cache Configuration
ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'False').lower() == 'true'
CACHE_DURATION = 3600  # 1 hour in seconds

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Rate Limiting
ENABLE_RATE_LIMITING = os.getenv('ENABLE_RATE_LIMITING', 'False').lower() == 'true'
RATE_LIMIT_PER_MINUTE = 60

# Security Configuration
ENABLE_CORS = os.getenv('ENABLE_CORS', 'True').lower() == 'true'
ALLOWED_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']

# Performance Configuration
ENABLE_COMPRESSION = os.getenv('ENABLE_COMPRESSION', 'True').lower() == 'true'
ENABLE_LOGGING = os.getenv('ENABLE_LOGGING', 'True').lower() == 'true'

# Development Configuration
DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'True').lower() == 'true'
SHOW_DEBUG_INFO = os.getenv('SHOW_DEBUG_INFO', 'False').lower() == 'true'

def get_config_summary():
    """Get a summary of the current configuration"""
    return {
        'app_name': APP_NAME,
        'app_version': APP_VERSION,
        'flask_host': FLASK_HOST,
        'flask_port': FLASK_PORT,
        'flask_debug': FLASK_DEBUG,
        'google_api_configured': bool(GOOGLE_API_KEY),
        'search_radius': DEFAULT_SEARCH_RADIUS,
        'max_results': DEFAULT_MAX_RESULTS,
        'caching_enabled': ENABLE_CACHING,
        'rate_limiting_enabled': ENABLE_RATE_LIMITING,
        'development_mode': DEVELOPMENT_MODE
    }

def validate_config():
    """Validate the configuration and return any issues"""
    issues = []
    
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == 'AIzaSyDzbgxX9OR4-ds2SgMOAGWlhZYRZf9pZIM':
        issues.append("⚠️  Using default Google API key. Consider setting your own GOOGLE_API_KEY environment variable.")
    
    if FLASK_DEBUG and not DEVELOPMENT_MODE:
        issues.append("⚠️  Debug mode is enabled but development mode is disabled.")
    
    if FLASK_HOST == '0.0.0.0' and not DEVELOPMENT_MODE:
        issues.append("⚠️  Binding to all interfaces (0.0.0.0) in production mode.")
    
    return issues

