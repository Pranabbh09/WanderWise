# 🌍 WanderWise - AI-Powered Place Recommender

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)](https://flask.palletsprojects.com/)

**WanderWise** is an intelligent place recommendation system that combines the power of Google Places API with AI-driven semantic search to provide personalized place suggestions in any city. Whether you're looking for restaurants, tourist attractions, or hidden gems, WanderWise uses advanced natural language processing to understand your preferences and deliver relevant recommendations.

## ✨ Features

- **🌍 City-based Search**: Find places in any city worldwide
- **🤖 AI-Powered Recommendations**: Uses sentence transformers for semantic understanding
- **⭐ Smart Categorization**: Automatically categorizes places as 'rated' or 'semantic'
- **🔍 Multiple Search Methods**: Choose between rating-based or semantic search
- **📱 Modern Web Interface**: Beautiful, responsive UI with real-time results
- **🚀 RESTful API**: Easy integration with other applications
- **⚡ Fast & Efficient**: Optimized search algorithms with intelligent caching

## 🏗️ Architecture

The system uses a hybrid approach combining:
- **Rating-based recommendations** for places with user ratings
- **Semantic search** using sentence transformers for places without ratings
- **Google Places API** for comprehensive place data
- **Flask backend** with modern web technologies

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Places API key
- Modern web browser

### Installation
1. **Create a virtual environment**
   ```bash
   python -m venv myenv
   
   # On Windows
   myenv\Scripts\activate
   
   # On macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Google API Key**
   
   Get your API key from [Google Cloud Console](https://console.cloud.google.com/):
   - Enable Places API
   - Create credentials
   - Set environment variable:
     ```bash
     # Windows
     set GOOGLE_API_KEY=your_api_key_here
     
     # macOS/Linux
     export GOOGLE_API_KEY=your_api_key_here
     ```
   
   Or edit `config.py` directly (not recommended for production)

5. **Run the application**
   ```bash
   # Option 1: Use the startup script
   python run.py
   
   # Option 2: Run directly
   python app.py
   
   # Option 3: Use batch/shell scripts
   # Windows: run.bat
   # macOS/Linux: run.sh
   ```

6. **Open your browser**
   
   The application will automatically open at `http://localhost:5000`

## 🎯 How to Use

### Web Interface

1. **Enter a city name** (e.g., "Paris", "New York", "Tokyo")
2. **Select a place type** (restaurant, museum, park, etc.)
3. **Choose search method**:
   - **Rating**: Get top-rated places
   - **Semantic**: AI-powered recommendations based on descriptions
4. **Click Search** to get personalized recommendations

### API Usage

The system provides a RESTful API for programmatic access:

```bash
# Get recommendations
POST /api/recommend
{
    "city": "Paris",
    "place_type": "restaurant",
    "method": "semantic"
}

# Health check
GET /api/health

# Configuration info
GET /api/config
```

## 🔧 Configuration

Key configuration options in `config.py`:

- **Search Radius**: Default 50km search area
- **Max Results**: Limit of 60 places per search
- **AI Model**: Uses `all-MiniLM-L6-v2` for semantic search
- **Place Types**: Comprehensive mapping of custom types to Google Places API types
- **Caching**: Optional result caching for performance
- **Rate Limiting**: Configurable API rate limiting

## 📊 Supported Place Types

The system supports a wide range of place categories:

- **Food & Dining**: restaurants, cafes, bars
- **Accommodation**: hotels, lodgings
- **Attractions**: museums, parks, temples, forts
- **Natural Features**: beaches, mountains, lakes
- **Services**: shopping malls, hospitals, schools
- **And many more...**

## 🧠 AI Features

### Semantic Search
- Uses sentence transformers to understand place descriptions
- Finds places based on meaning, not just keywords
- Automatically categorizes places for optimal recommendations

### Smart Categorization
- **Rated Places**: Places with user ratings and reviews
- **Semantic Places**: Cultural sites, landmarks, and attractions

## 🛠️ Development

### Project Structure
```
WanderWise/
├── app.py                 # Main Flask application
├── config.py             # Configuration and settings
├── requirements.txt      # Python dependencies
├── run.py               # Startup script
├── templates/           # HTML templates
│   └── index.html      # Main web interface
├── run.bat             # Windows batch file
└── run.sh              # Unix shell script
```

### Key Components

- **`app.py`**: Core Flask application with recommendation logic
- **`config.py`**: Centralized configuration management
- **`templates/index.html`**: Modern, responsive web interface
- **`run.py`**: Intelligent startup script with dependency checking


*Discover amazing places with the power of AI!*

