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
- **🏨 Integrated Booking System**: Direct links to major booking platforms
- **🚀 RESTful API**: Easy integration with other applications
- **⚡ Fast & Efficient**: Optimized search algorithms with intelligent caching
- **📊 Real-time Statistics**: Live counts of places found and categorized

## 🏗️ Architecture

The system uses a hybrid approach combining:
- **Rating-based recommendations** for places with user ratings
- **Semantic search** using sentence transformers for places without ratings
- **Google Places API** for comprehensive place data
- **Flask backend** with modern web technologies
- **Advanced booking integration** with multiple travel platforms

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Places API key
- Modern web browser

### Installation

1. **Clone or download the project**
   ```bash
   # Navigate to your project directory
   cd WanderWise
   ```

2. **Create a virtual environment**
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
   - **Rating**: Get top-rated places based on user reviews
   - **Semantic**: AI-powered recommendations based on descriptions and meaning
4. **Click Search** to get personalized recommendations
5. **Book directly** through integrated booking platforms for hotels

### Enhanced Booking Features

- **Multi-platform Integration**: Direct links to Booking.com, Agoda, Goibibo, Trivago, Expedia, and more
- **Smart Hotel Detection**: Automatically identifies hotels and shows booking options
- **Quick Booking Modal**: Access all booking platforms in one place
- **City-specific Search**: Optimized search queries for each booking platform

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
- Provides similarity scores for semantic matches

### Smart Categorization
- **Rated Places**: Places with user ratings and reviews, sorted by popularity
- **Semantic Places**: Cultural sites, landmarks, and attractions with AI-powered relevance scoring

## 🏨 Booking Integration

### Supported Platforms
- **Booking.com** - Global hotel booking
### Features
- **Automatic Hotel Detection**: Identifies hotels based on place types and descriptions
- **Smart URL Generation**: Creates optimized search queries for each platform
- **Responsive Design**: Works seamlessly on all devices
- **External Links**: Opens booking platforms in new tabs for convenience

## 🛠️ Development

### Project Structure
```
WanderWise/
├── app.py                 # Main Flask application with recommendation logic
├── config.py             # Configuration and settings management
├── requirements.txt      # Python dependencies
├── run.py               # Intelligent startup script
├── templates/           # HTML templates
│   └── index.html      # Modern, responsive web interface with booking features
├── run.bat             # Windows batch file for easy startup
├── run.sh              # Unix shell script for easy startup
├── Finalmodel.ipynb    # Jupyter notebook for model development and testing
└── flask_place_recommender.py  # Alternative implementation
```

### Key Components

- **`app.py`**: Core Flask application with advanced recommendation logic
- **`config.py`**: Centralized configuration management with environment variable support
- **`templates/index.html`**: Modern, responsive web interface with integrated booking system
- **`run.py`**: Intelligent startup script with dependency checking and configuration validation
- **`Finalmodel.ipynb`**: Development notebook for testing and refining the AI model

### Technical Features

- **Hybrid Recommendation Engine**: Combines rating-based and semantic search approaches
- **Real-time API Integration**: Live data from Google Places API
- **Responsive Web Design**: Mobile-first approach with modern CSS Grid and Flexbox
- **JavaScript ES6+**: Modern JavaScript with async/await for smooth user experience
- **Font Awesome Icons**: Rich visual elements throughout the interface

## 🚀 Performance & Optimization

- **Efficient Data Processing**: Pandas-based data manipulation for large datasets
- **Smart Caching**: Optional result caching to reduce API calls
- **Rate Limiting**: Configurable API rate limiting to prevent abuse
- **Compression**: Optional response compression for faster loading
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 🔒 Security & Best Practices

- **Environment Variables**: Secure API key management
- **Input Validation**: Comprehensive input sanitization
- **CORS Support**: Configurable cross-origin resource sharing
- **Logging**: Detailed logging for debugging and monitoring
- **Error Handling**: Graceful error handling without exposing sensitive information

## 📱 Browser Compatibility

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile Responsive**: Optimized for all screen sizes
- **Progressive Enhancement**: Core functionality works without JavaScript
- **Accessibility**: Semantic HTML and ARIA labels for screen readers

---

*Discover amazing places with the power of AI and book your next adventure seamlessly!* 🌍✨

