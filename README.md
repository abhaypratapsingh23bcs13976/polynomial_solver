# Polynomial Equation Solver API

A production-ready REST API built with Flask to solve polynomial equations of any degree. It uses powerful numerical computing libraries (NumPy) to compute both real and complex roots, provides interactive graphical visualizations, and a beautiful UI.

## Features

- **High Precision Solver**: Find roots for ANY degree polynomial (real and complex).
- **Explanations**: Step-by-step logic for 1st (linear) and 2nd (quadratic) degree polynomials.
- **Visualization**: Generates equation curves and plotted roots.
- **Modern UI**: Comes with a sleek glassmorphic dashboard out-of-the-box.
- **Swagger Documentation**: Interactive API testing available at `/apidocs`.

## Tech Stack

- **Backend**: Python 3, Flask
- **Math/Graphs**: NumPy, Matplotlib
- **Validation**: Pydantic
- **Frontend**: HTML5, Vanilla CSS, Vanilla JS
- **Documentation**: Flasgger
- **Testing**: PyTest

## Local Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Visit the dashboard at `http://localhost:5000`
4. Access API docs at `http://localhost:5000/apidocs`

## API Endpoints

### `POST /api/solve`
Request body: `{"coefficients": [1, -5, 6]}`

### `POST /api/plot`
Request body: `{"coefficients": [1, -5, 6]}`

### `POST /api/explain`
Request body: `{"coefficients": [1, -5, 6]}`

## Docker Deployment

Build and run using Docker:
```bash
docker build -t polynomial-solver .
docker run -p 5000:5000 polynomial-solver
```
