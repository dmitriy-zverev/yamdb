# YaMDb API

YaMDb API is a RESTful API for collecting user reviews about titles (films, books, music). The project allows users to leave reviews, rate titles, and comment on other users' reviews.

## Description

The YaMDb project collects user reviews on titles. Titles are divided into categories: "Books", "Films", "Music" and others. The list of categories can be expanded by administrators.

The titles themselves are not stored in YaMDb - you cannot watch a movie or listen to music here.

Each category contains titles: books, films or music. For example, the "Books" category may contain titles like "Winnie-the-Pooh" and "The Martian Chronicles", while the "Music" category may contain the song "Yesterday" by "The Beatles" and Bach's second suite.

A title can be assigned a genre from a preset list (for example, "Fairy Tale", "Rock" or "Arthouse"). Only administrators can create new genres.

Grateful or outraged users leave text reviews for titles and rate them on a scale from one to ten; user ratings form an average title rating. A user can leave only one review per title.

## Technologies

- Python 3.x
- Django 5.2.7
- Django REST Framework 3.16.1
- JWT Authentication (djangorestframework-simplejwt 5.5.1)
- Django Filter 25.2
- PostgreSQL/SQLite
- pytest for testing

## Installation

1. Clone the repository:
```bash
git clone yamdb
cd api_yamdb
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/Mac
venv\Scripts\activate     # for Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
cd api_yamdb
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Project Structure

```
api_yamdb/
├── api/                    # API endpoints and views
├── api_yamdb/             # Project settings
├── reviews/               # Reviews, titles, categories, and genres
├── users/                 # User management and authentication
├── static/                # Static files and test data
├── templates/             # HTML templates
└── manage.py              # Django management script
```

## Features

### User Roles

The project implements three user roles:

- **User** - can read everything, create reviews and ratings, comment on reviews
- **Moderator** - same as User, plus can edit and delete any reviews and comments
- **Admin** - full access to manage all project content, can create and delete titles, categories, and genres, assign user roles

### API Endpoints

#### Authentication
- `POST /api/v1/auth/signup/` - User registration
- `POST /api/v1/auth/signin/` - Renew login token
- `POST /api/v1/auth/token/` - Get JWT token

#### Users
- `GET /api/v1/users/` - Get list of users (Admin)
- `POST /api/v1/users/` - Create user (Admin)
- `GET /api/v1/users/{username}/` - Get user by username (Admin)
- `PATCH /api/v1/users/{username}/` - Update user (Admin)
- `DELETE /api/v1/users/{username}/` - Delete user (Admin)
- `GET /api/v1/users/me/` - Get current user profile
- `PATCH /api/v1/users/me/` - Update current user profile

#### Categories
- `GET /api/v1/categories/` - Get list of categories
- `POST /api/v1/categories/` - Create category (Admin)
- `DELETE /api/v1/categories/{slug}/` - Delete category (Admin)

#### Genres
- `GET /api/v1/genres/` - Get list of genres
- `POST /api/v1/genres/` - Create genre (Admin)
- `DELETE /api/v1/genres/{slug}/` - Delete genre (Admin)

#### Titles
- `GET /api/v1/titles/` - Get list of titles
- `POST /api/v1/titles/` - Create title (Admin)
- `GET /api/v1/titles/{title_id}/` - Get title details
- `PATCH /api/v1/titles/{title_id}/` - Update title (Admin)
- `DELETE /api/v1/titles/{title_id}/` - Delete title (Admin)

#### Reviews
- `GET /api/v1/titles/{title_id}/reviews/` - Get list of reviews
- `POST /api/v1/titles/{title_id}/reviews/` - Create review
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/` - Get review details
- `PATCH /api/v1/titles/{title_id}/reviews/{review_id}/` - Update review (Author/Moderator/Admin)
- `DELETE /api/v1/titles/{title_id}/reviews/{review_id}/` - Delete review (Author/Moderator/Admin)

#### Comments
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/` - Get list of comments
- `POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/` - Create comment
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - Get comment details
- `PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - Update comment (Author/Moderator/Admin)
- `DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` - Delete comment (Author/Moderator/Admin)

## API Documentation

After starting the server, full API documentation is available at:
- ReDoc: `http://127.0.0.1:8000/redoc/`

## Testing

Run tests using pytest:

```bash
pytest tests
```

## Data Import

The project includes test data in CSV format located in `static/data/`. You can import this data to populate the database with sample content.

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Register a new user via `/api/v1/auth/signup/` or log in via `/api/v1/auth/signin/`
2. Obtain a token via `/api/v1/auth/token/`
3. Include the token in the Authorization header: `Authorization: Bearer <your_token>`

## Examples

### Register a new user
```bash
POST /api/v1/auth/signup/
{
  "email": "user@example.com",
  "username": "username"
}
```

### Loggin in for a current user
```bash
POST /api/v1/auth/signin/
{
  "username": "username"
}
```

### Create a review
```bash
POST /api/v1/titles/{title_id}/reviews/
Authorization: Bearer <your_token>
{
  "text": "Great movie!",
  "score": 9
}
```

### Get list of titles with filters
```bash
GET /api/v1/titles/?category=movie&genre=comedy&year=2020
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
