# Progressive Web Application

Teacher: David Steedman

This repository contains the Progressive Web Application (PWA) project for the MHS Software Engineering class. This project focuses on building a collection management application using Flask, SQLite, and modern web development techniques.

## Project Tasks

### Task 1: Project Setup and Planning
- Set up Flask project with proper folder structure
- Initialize Git repository
- Design database schema for chosen collection type (Books, Movies, Music, Video Games, or Recipes)
- Create wireframes for desktop and mobile layouts

### Task 2: Backend Development with Flask
- File: `app.py`, `models.py`, `views.py`
- Description: Set up the Flask application with database integration and routing
- This task covers:
  - Database model implementation
  - CRUD operation routes
  - Query implementation with filters and sorting
  - Request handling with proper HTTP methods

### Task 3: User Interface and Design
- Files: `templates/*.html`, `static/css/`
- Description: Create responsive templates and styling
- This task covers:
  - Base template with inheritance
  - Bootstrap integration
  - Responsive layout
  - Custom CSS styling

### Task 4: Core Features
- Description: Implement all required application functionality
- This task covers:
  - Item creation with validation
  - Display with pagination
  - Update functionality
  - Delete with confirmation
  - Search and filter features

### Task 5: PWA Implementation
- Files: `manifest.json`, `service-worker.js`
- Description: Add Progressive Web App features
- This task covers:
  - Manifest file setup
  - Service worker implementation
  - Offline functionality
  - Installation capability

## Project Structure

```
project/
├── static/
│   ├── css/
│   ├── images/
│   └── manifest.json
├── templates/
│   ├── base.html
│   └── *.html
├── app.py
├── models.py
├── views.py
└── service-worker.js
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [MDN Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)