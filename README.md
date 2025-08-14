# 🌍 WanderWise - AI-Powered Place Recommender

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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

1. **Clone the repository**
   ```bash
   git clone <repository-url>
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
- **Hybrid Approach**: Combines both methods for comprehensive results

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

### Adding New Features

1. **New Place Types**: Add to `CUSTOM_TO_GOOGLE_TYPE` in `config.py`
2. **AI Models**: Modify `SENTENCE_TRANSFORMER_MODEL` in `config.py`
3. **API Endpoints**: Add new routes in `app.py`
4. **UI Enhancements**: Modify `templates/index.html`

## 📈 Performance

- **Search Speed**: Optimized algorithms for fast results
- **Memory Usage**: Efficient data processing with pandas
- **API Efficiency**: Smart pagination and result limiting
- **Caching**: Optional result caching for repeated searches

## 🔒 Security

- **API Key Protection**: Environment variable configuration
- **Input Validation**: Comprehensive request validation
- **Rate Limiting**: Configurable API rate limiting
- **CORS Support**: Cross-origin resource sharing configuration

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**:
   ```bash
   export FLASK_DEBUG=False
   export DEVELOPMENT_MODE=False
   export FLASK_HOST=127.0.0.1
   ```

2. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up reverse proxy** (nginx recommended)

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (when available)
python -m pytest

# Format code
black app.py config.py

# Lint code
flake8 app.py config.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Places API** for comprehensive place data
- **Sentence Transformers** for AI-powered semantic search
- **Flask** for the web framework
- **Open source community** for various dependencies

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the code comments for detailed explanations
- **Community**: Join discussions in the project repository

## 🔮 Roadmap

- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Advanced AI**: More sophisticated recommendation algorithms
- [ ] **Social Features**: User reviews and ratings
- [ ] **Offline Support**: Cached recommendations for offline use
- [ ] **Multi-language**: Internationalization support
- [ ] **Analytics**: Usage statistics and insights

---

**Made with ❤️ for travelers and explorers worldwide**

*Discover amazing places with the power of AI!*

