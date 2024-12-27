# MoodLens

**MoodLens** is a Flask-based application that combines text sentiment analysis and facial emotion detection using multiple AI models. It features both text analysis using Hugging Face's Transformers library and real-time emotion detection through webcam integration.

## Features

### Text Sentiment Analysis
- Analyze text sentiment using either DistilBERT or OpenAI models
- Classify text as Positive, Negative, or Neutral
- Toggle between AI models to compare results
- Historical tracking of all analyses

### Facial Emotion Detection
- Real-time webcam emotion detection
- Multiple detection backends (RetinaFace, MTCNN, OpenCV, SSD)
- Confidence scores for each detected emotion
- Timer option for perfect captures

### Dashboard & Analytics
- Interactive dashboard showing sentiment trends
- Word clouds for positive, negative, and neutral sentiments
- Data filtering by date range
- CSV export functionality

### User Management
- Role-based access control
- Admin interface for user management
- Secure authentication system

## Technologies Used
- **Backend**: Python, Flask
- **Database**: SQLite
- **AI Models**: 
  - Text Analysis: DistilBERT, OpenAI
  - Facial Detection: DeepFace
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Visualization**: Matplotlib, Word Clouds

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MoodLens.git

## Design Patterns

1. **Active Record Pattern**:
  - SQLAlchemy models (User, Role, UserRole, SentimentLog) map directly to database tables
  - Models encapsulate database operations and business logic
  - Each class represents both data and behavior

2. **Singleton Pattern**: 
  - Single database connection instance managed through SQLAlchemy
  - Ensures consistent database access across the application
  - Implemented via Flask-SQLAlchemy's db object

3. **Factory Pattern**:
  - Flask application factory for flexible app instance creation
  - Allows different configurations for development/production
  - Supports modular application setup

4. **Dependency Injection**:
  - Database instance injected into models and Flask app
  - Promotes loose coupling between components
  - Enables easier testing and configuration changes

5. **Repository Pattern**:
  - Data access abstracted through SQLAlchemy ORM
  - Separates database queries from business logic
  - Provides consistent interface for data operations

6. **Data Mapper Pattern**: 
  - SQLAlchemy ORM maps objects to database tables
  - Separates domain logic from data persistence
  - Maintains clean separation of concerns

7. **Service Layer Pattern**:
  - Business logic isolated in service modules
  - Clear separation from data access and presentation layers
  - Promotes code reuse and maintainability

## Screenshots

![MoodLens Dashboard](/screenshots/dashboard.png)
*Dashboard showing sentiment analysis trends and word clouds*

![Webcam Emotion Detection](/screenshots/webcam.png)
*Real-time emotion detection with confidence scores*

![User Management](/screenshots/users.png)
*Admin interface for user role management*

![Sentiment Analysis](/screenshots/sentiment.png)
*Text sentiment analysis with model selection*

## Learning Outcomes

- Implemented multiple AI models for text and facial analysis
- Integrated real-time webcam capture and processing
- Built a complete Flask web application with user authentication
- Created interactive data visualizations and dashboard
- Applied various software design patterns in practice
- Developed a role-based access control system
- Gained experience with:
 - Python web development
 - AI/ML model integration
 - Database design and ORM usage
 - Frontend development with Bootstrap
 - User authentication and authorization
 - RESTful API design
 - Version control with Git

## Future Improvements

1. **Technical Enhancements**:
  - Migrate to PostgreSQL for better scalability
  - Add comprehensive error handling
  - Implement input validation
  - Add loading states for better UX

2. **Feature Additions**:
  - Dark/light theme toggle
  - Side-by-side model comparison
  - Favorites system for analyses
  - Additional export formats

3. **User Experience**:
  - Enhanced mobile responsiveness
  - Interactive graphs
  - Improved navigation
  - Better feedback messages

4. **Development**:
  - Add basic unit tests
  - Improve documentation
  - Optimize performance
  - Enhance security measures

## License

MIT License

Copyright (c) 2024 Gordy Frank

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


