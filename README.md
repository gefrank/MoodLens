# MoodLens

**MoodLens** is a Flask-based sentiment analysis application using Hugging Face's Transformers library and Matplotlib for data visualization.

## Features:
- Analyze text sentiment (Positive, Negative, Neutral).
- View sentiment trends through a dynamic dashboard.
- Visualize data with bar and pie charts.

## Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/MoodLens.git

## Design Patterns
1. Active Record Pattern:
   SQLAlchemy models (User, Role, UserRole, SentimentLog) are examples of the Active Record pattern. Each model class directly maps to a database table, and instances of these classes represent rows in the table. The models include methods for interacting with the database, such as querying, inserting, updating, and deleting records.

2. Singleton Pattern:
   The db instance created by SQLAlchemy() in database.py is a singleton. It ensures that there is a single shared instance of the database connection throughout the application.

3. Factory Pattern:
   Flask itself uses the factory pattern for creating application instances. This is evident in how the app instance is created and configured in your main application file.
   
4. Dependency Injection:
   The db instance is injected into the models and the Flask application. This is done by initializing db in database.py and then calling db.init_app(app) in the main application file to bind it to the Flask app.

5. Repository Pattern:
   Although not explicitly shown, the use of SQLAlchemy's ORM can be seen as an implementation of the Repository pattern. The models act as repositories that encapsulate the logic needed to access data sources and perform CRUD operations.

6. Data Mapper Pattern:
   SQLAlchemy itself is an implementation of the Data Mapper pattern. It separates the in-memory objects from the database schema, allowing for more flexibility and decoupling of the database logic from the business logic.

7. Service Layer Pattern:
   If you have separate service classes or functions that handle business logic and interact with the models, this would be an example of the Service Layer pattern. This pattern helps to keep the business logic separate from the data access logic.
