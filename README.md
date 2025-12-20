# 0x05. AirBnB Clone - RESTful API

## 🏠 Project Overview

**AirBnB_clone_v3** is the third iteration of the AirBnB clone project, focusing on building a comprehensive **RESTful API** using Flask. This API serves as the backend interface for the AirBnB clone application, providing endpoints to manage users, places, cities, states, amenities, and reviews.

This project transforms the command-line console from previous versions into a fully-functional web service, allowing client applications to interact with the AirBnB database through standard HTTP methods.

---

## 🎯 Learning Objectives

By completing this project, you will master:

- **RESTful API Design Principles** - Understanding resource-based architecture
- **HTTP Methods** - Implementing GET, POST, PUT, DELETE operations
- **Flask Framework** - Building web services with Flask and Flask-RESTful
- **API Routing** - Creating logical and intuitive endpoint structures
- **JSON Serialization** - Converting Python objects to JSON responses
- **Error Handling** - Implementing proper HTTP status codes and error messages
- **CORS** - Handling Cross-Origin Resource Sharing for web clients
- **Database Integration** - Connecting API endpoints to database models
- **API Documentation** - Writing clear documentation for API consumers

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3 |
| **Web Framework** | Flask |
| **API Extension** | Flask-RESTful |
| **CORS Handling** | Flask-CORS |
| **Database ORM** | SQLAlchemy |
| **Database** | MySQL / File Storage |
| **Testing** | unittest, curl |
| **Documentation** | Swagger/OpenAPI (optional) |

---

## 📁 Project Structure

```
AirBnB_clone_v3/
├── api/
│   ├── v1/
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── index.py          # API status and stats
│   │   │   ├── states.py         # State endpoints
│   │   │   ├── cities.py         # City endpoints
│   │   │   ├── amenities.py      # Amenity endpoints
│   │   │   ├── users.py          # User endpoints
│   │   │   ├── places.py         # Place endpoints
│   │   │   ├── places_reviews.py # Review endpoints
│   │   │   └── places_amenities.py # Place-Amenity relationship
│   │   ├── __init__.py
│   │   └── app.py                # Flask application setup
│   └── __init__.py
├── models/
│   ├── engine/
│   │   ├── db_storage.py         # Database storage engine
│   │   └── file_storage.py       # File storage engine
│   ├── __init__.py
│   ├── base_model.py             # Base class for all models
│   ├── state.py                  # State model
│   ├── city.py                   # City model
│   ├── amenity.py                # Amenity model
│   ├── user.py                   # User model
│   ├── place.py                  # Place model
│   └── review.py                 # Review model
├── tests/                        # Unit tests
├── setup_mysql_dev.sql           # Database setup script
├── setup_mysql_test.sql          # Test database setup
└── README.md                     # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher (for database storage)
- pip package manager
- virtualenv (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/AirBnB_clone_v3.git
cd AirBnB_clone_v3
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages**:
```
Flask==2.0.1
Flask-CORS==3.0.10
SQLAlchemy==1.4.22
mysqlclient==2.0.3
flasgger==0.9.5
```

### Step 4: Set Up the Database

```bash
# Create the development database
cat setup_mysql_dev.sql | mysql -uroot -p

# Create the test database (optional)
cat setup_mysql_test.sql | mysql -uroot -p
```

### Step 5: Configure Environment Variables

```bash
# Set storage type (db or file)
export HBNB_TYPE_STORAGE=db

# Database configuration
export HBNB_MYSQL_USER=hbnb_dev
export HBNB_MYSQL_PWD=hbnb_dev_pwd
export HBNB_MYSQL_HOST=localhost
export HBNB_MYSQL_DB=hbnb_dev_db

# API configuration
export HBNB_API_HOST=0.0.0.0
export HBNB_API_PORT=5000
```

---

## 🎮 Running the API

### Start the Development Server

```bash
python3 -m api.v1.app
```

The API will be available at: `http://0.0.0.0:5000/api/v1/`

### Using Different Storage Types

**File Storage**:
```bash
HBNB_TYPE_STORAGE=file python3 -m api.v1.app
```

**Database Storage**:
```bash
HBNB_TYPE_STORAGE=db python3 -m api.v1.app
```

---

## 📡 API Endpoints

### Status & Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/status` | Returns API status |
| GET | `/api/v1/stats` | Returns object count statistics |

### States

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/states` | Retrieve all states |
| GET | `/api/v1/states/<state_id>` | Retrieve a specific state |
| POST | `/api/v1/states` | Create a new state |
| PUT | `/api/v1/states/<state_id>` | Update a state |
| DELETE | `/api/v1/states/<state_id>` | Delete a state |

### Cities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/states/<state_id>/cities` | Retrieve all cities in a state |
| GET | `/api/v1/cities/<city_id>` | Retrieve a specific city |
| POST | `/api/v1/states/<state_id>/cities` | Create a new city |
| PUT | `/api/v1/cities/<city_id>` | Update a city |
| DELETE | `/api/v1/cities/<city_id>` | Delete a city |

### Amenities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/amenities` | Retrieve all amenities |
| GET | `/api/v1/amenities/<amenity_id>` | Retrieve a specific amenity |
| POST | `/api/v1/amenities` | Create a new amenity |
| PUT | `/api/v1/amenities/<amenity_id>` | Update an amenity |
| DELETE | `/api/v1/amenities/<amenity_id>` | Delete an amenity |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users` | Retrieve all users |
| GET | `/api/v1/users/<user_id>` | Retrieve a specific user |
| POST | `/api/v1/users` | Create a new user |
| PUT | `/api/v1/users/<user_id>` | Update a user |
| DELETE | `/api/v1/users/<user_id>` | Delete a user |

### Places

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cities/<city_id>/places` | Retrieve all places in a city |
| GET | `/api/v1/places/<place_id>` | Retrieve a specific place |
| POST | `/api/v1/cities/<city_id>/places` | Create a new place |
| PUT | `/api/v1/places/<place_id>` | Update a place |
| DELETE | `/api/v1/places/<place_id>` | Delete a place |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/places/<place_id>/reviews` | Retrieve all reviews for a place |
| GET | `/api/v1/reviews/<review_id>` | Retrieve a specific review |
| POST | `/api/v1/places/<place_id>/reviews` | Create a new review |
| PUT | `/api/v1/reviews/<review_id>` | Update a review |
| DELETE | `/api/v1/reviews/<review_id>` | Delete a review |

### Place-Amenity Relationships

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/places/<place_id>/amenities` | Retrieve all amenities for a place |
| POST | `/api/v1/places/<place_id>/amenities/<amenity_id>` | Link an amenity to a place |
| DELETE | `/api/v1/places/<place_id>/amenities/<amenity_id>` | Unlink an amenity from a place |

---

## 💡 Usage Examples

### Get API Status

```bash
curl -X GET http://0.0.0.0:5000/api/v1/status
```

**Response**:
```json
{
  "status": "OK"
}
```

### Get Statistics

```bash
curl -X GET http://0.0.0.0:5000/api/v1/stats
```

**Response**:
```json
{
  "amenities": 10,
  "cities": 25,
  "places": 100,
  "reviews": 50,
  "states": 5,
  "users": 30
}
```

### Retrieve All States

```bash
curl -X GET http://0.0.0.0:5000/api/v1/states
```

**Response**:
```json
[
  {
    "id": "421a55f4-7d82-47d9-b54c-a76916479545",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "name": "California"
  },
  {
    "id": "421a55f4-7d82-47d9-b54c-a76916479546",
    "created_at": "2024-01-15T10:31:00",
    "updated_at": "2024-01-15T10:31:00",
    "name": "Arizona"
  }
]
```

### Create a New State

```bash
curl -X POST http://0.0.0.0:5000/api/v1/states \
  -H "Content-Type: application/json" \
  -d '{"name": "Texas"}'
```

**Response**:
```json
{
  "id": "421a55f4-7d82-47d9-b54c-a76916479547",
  "created_at": "2024-01-15T10:32:00",
  "updated_at": "2024-01-15T10:32:00",
  "name": "Texas"
}
```

### Update a State

```bash
curl -X PUT http://0.0.0.0:5000/api/v1/states/421a55f4-7d82-47d9-b54c-a76916479547 \
  -H "Content-Type: application/json" \
  -d '{"name": "New Texas"}'
```

### Delete a State

```bash
curl -X DELETE http://0.0.0.0:5000/api/v1/states/421a55f4-7d82-47d9-b54c-a76916479547
```

**Response**:
```json
{}
```

---

## 🔒 HTTP Status Codes

The API uses standard HTTP status codes:

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Missing or invalid data |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server error |

---

## 🧪 Testing

### Run All Tests

```bash
python3 -m unittest discover tests
```

### Run Specific Test File

```bash
python3 -m unittest tests/test_models/test_state.py
```

### Test API Endpoints with curl

```bash
# Test status endpoint
curl -X GET http://0.0.0.0:5000/api/v1/status

# Test creating a state
curl -X POST http://0.0.0.0:5000/api/v1/states \
  -H "Content-Type: application/json" \
  -d '{"name": "California"}'

# Test retrieving states
curl -X GET http://0.0.0.0:5000/api/v1/states
```

---

## 🌐 CORS Configuration

Cross-Origin Resource Sharing (CORS) is enabled for all routes with origin `0.0.0.0`:

```python
from flask_cors import CORS

CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
```

This allows web applications hosted on different domains to interact with the API.

---

## 📝 Error Handling

The API returns JSON-formatted error messages:

**404 Not Found**:
```json
{
  "error": "Not found"
}
```

**400 Bad Request**:
```json
{
  "error": "Missing name"
}
```

All error handlers are defined in the blueprint initialization to ensure consistent error responses across all endpoints.

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HBNB_TYPE_STORAGE` | Storage type (db/file) | file |
| `HBNB_MYSQL_USER` | MySQL username | hbnb_dev |
| `HBNB_MYSQL_PWD` | MySQL password | hbnb_dev_pwd |
| `HBNB_MYSQL_HOST` | MySQL host | localhost |
| `HBNB_MYSQL_DB` | MySQL database name | hbnb_dev_db |
| `HBNB_API_HOST` | API host | 0.0.0.0 |
| `HBNB_API_PORT` | API port | 5000 |

---

## 🚧 Common Issues & Troubleshooting

### Issue: "No module named 'MySQLdb'"

**Solution**: Install MySQL client
```bash
sudo apt-get install python3-dev libmysqlclient-dev
pip install mysqlclient
```

### Issue: "Can't connect to MySQL server"

**Solution**: Check MySQL service and credentials
```bash
sudo service mysql status
mysql -u hbnb_dev -p
```

### Issue: "Address already in use"

**Solution**: Kill the process using port 5000
```bash
sudo lsof -t -i:5000 | xargs kill -9
```

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [RESTful API Design Guide](https://restfulapi.net/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is part of the ALX Software Engineering program and is intended for educational purposes.

---

## ✨ Authors

- **Z-ajamy** - [GitHub Profile](https://github.com/Z-ajamy?tab=overview&from=2025-10-01&to=2025-10-22)

---

## 🎓 Acknowledgments

- ALX Software Engineering Program
- Holberton School
- Flask and Python communities

---

**Previous Versions**:
- [AirBnB Clone v1](../AirBnB_clone_v1) - Console
- [AirBnB Clone v2](../AirBnB_clone_v2) - Web Static

**Next Version**:
- [AirBnB Clone v4](../AirBnB_clone_v4) - Web Dynamic

---

*Built with 🐍 Python and ❤️*
