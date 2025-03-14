# Technical Context: Russian Noun Cases Drill

## Technologies Used

### Core Technologies
1. **Python**: The primary programming language used for the backend implementation.
2. **Flask**: A lightweight Python web framework that provides the foundation for the application.
3. **PyMorphy3**: A morphological analyzer for Russian language that handles noun declensions.
4. **Jinja2**: A template engine integrated with Flask for generating HTML pages.
5. **HTML/CSS**: Frontend technologies for structure and styling.

### Libraries and Dependencies
- **Flask**: Web framework (version not specified in config)
- **PyMorphy3**: Russian morphological analyzer
- No JavaScript frameworks appear to be in use; the application relies on server-side rendering and form submissions

### Data Storage
- **JSON Files**: Static data is stored in JSON format
  - `data/nouns.json`: Contains the list of Russian nouns used in drills
  - `data/sentences.json`: Contains sentences organized by grammatical case for the insert drill

### Frontend
- **CSS**: Custom styles defined in `static/styles.css`
- **Responsive Design**: Media queries for different screen sizes
- **No External CSS Frameworks**: The application uses custom CSS rather than Bootstrap or other frameworks

## Development Setup

### Local Development Environment
The application is configured to run in debug mode by default, as specified in `config.py`:
```python
DEBUG = True
```

The application runs on port 5001 as specified in `app.py`:
```python
app.run(debug=app.config['DEBUG'], port=5001)
```

### Running the Application
To run the application locally:
1. Ensure Python and required dependencies are installed
2. Run `python app.py` from the project root directory
3. Access the application at `http://localhost:5001`

### Project Structure
```
/
├── app.py                 # Application entry point
├── config.py              # Configuration settings
├── models.py              # Data models
├── routes.py              # Route handlers
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── data/                  # Data files
│   ├── nouns.json         # Russian nouns for drills
│   └── sentences.json     # Sentences for insert drill
├── static/                # Static assets
│   └── styles.css         # CSS styles
└── templates/             # Jinja2 templates
    ├── base.html          # Base template
    ├── home.html          # Home page
    ├── forward_drill.html # Forward drill page
    ├── backward_drill.html# Backward drill page
    └── insert_drill.html  # Insert drill page
```

## Technical Constraints

### Language Support
- The application supports two languages: English (`en`) and Russian (`ru`)
- Language preference is stored in the Flask session
- Default language is English if no preference is set

### Browser Compatibility
- The application uses standard HTML5 and CSS3 features
- Responsive design supports various screen sizes
- No JavaScript dependencies means broad browser compatibility

### Performance Considerations
- PyMorphy3 analyzer is initialized once at application startup
- JSON data is loaded when the DrillData class is instantiated
- No database queries or external API calls that might impact performance

### Security Considerations
- Flask's `SECRET_KEY` is used for session security
- In production, the secret key should be set via environment variables:
  ```python
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
  ```
- No user authentication or data storage beyond session data

## Dependencies

### Python Package Dependencies
The application requires the following Python packages (from requirements.txt):
- Flask: Web framework
- PyMorphy3: Russian morphological analyzer

### External Dependencies
- No external APIs or services are used
- No database requirements
- No JavaScript libraries or CDN dependencies

## Deployment Considerations

### Environment Variables
- `SECRET_KEY`: For Flask session security (optional, defaults to hardcoded value)

### Serving in Production
- The development server (`app.run()`) should not be used in production
- A production WSGI server like Gunicorn or uWSGI would be appropriate
- Static files should be served by a web server like Nginx in production

### Scaling Considerations
- The application has minimal resource requirements
- No database or external service dependencies simplifies scaling
- Stateless design (except for language preference in session) allows for horizontal scaling
