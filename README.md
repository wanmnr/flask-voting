# Flask Application

A Flask web application with asset management and other features.

## Requirements

- Python 3.8+
- pipenv

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

## Install pipenv if you haven't

```bash
pip install pipenv
```

## Install dependencies and create virtual environment

```bash
pipenv install
```

## Activate virtual environment

```bash
pipenv shell
```

## Edit .env file with your configurations

```bash
touch .env
```

## Run the Flask development server:

```bash
flask run
```

## Access the application at:

```bash
http://127.0.0.1:5000
```

## Asset Management

The application uses Flask-Assets for managing and minifying CSS/JavaScript files.

### Asset Commands

#### Build and minify assets:

```bash
flask assets build
```

#### Remove built assets:

```bash
flask assets clean

```

#### Watch assets for changes during development:

```bash
flask assets watch
```

## DB Related

### For first-time setup:

```bash
flask db create
flask db init
```

### For complete reset:

```bash
flask db recreate  # This now includes initialization
```

## Deployment

### For production deployment:

#### Set production environment:

```bash
export FLASK_ENV=production
```

#### Run using a production server:

```bash
gunicorn wsgi:app
```


## License