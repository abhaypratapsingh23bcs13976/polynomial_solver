from flask import Blueprint, request, jsonify
from services.solver_service import SolverService
from services.plot_service import PlotService
from utils.validators import PolynomialRequest
from pydantic import ValidationError
from utils.logger import logger

solver_bp = Blueprint('solver', __name__)

@solver_bp.route('/solve', methods=['POST'])
def solve_polynomial():
    """
    Solve a polynomial and return roots.
    ---
    tags:
      - Solver
    parameters:
      - in: body
        name: body
        schema:
          id: PolynomialCoefficients
          required:
            - coefficients
          properties:
            coefficients:
              type: array
              items:
                type: number
              example: [1, -5, 6]
              description: Coefficients in descending order (e.g., ax^2 + bx + c -> [a, b, c])
    responses:
      200:
        description: Successful solution
      400:
        description: Invalid input
    """
    try:
        data = request.get_json()
        validated_data = PolynomialRequest(**data)
        coefficients = validated_data.coefficients

        result = SolverService.solve_polynomial(coefficients)
        logger.info(f"Solved polynomial with coefficients: {coefficients}")
        
        return jsonify(result), 200

    except ValidationError as e:
        logger.warning(f"Validation error: {e.json()}")
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        logger.error(f"Unexpected error in /solve: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

@solver_bp.route('/explain', methods=['POST'])
def explain_polynomial():
    """
    Get step-by-step explanation for low-degree polynomials.
    ---
    tags:
      - Solver
    parameters:
      - in: body
        name: body
        schema:
          $ref: '#/definitions/PolynomialCoefficients'
    responses:
      200:
        description: Step-by-step explanation
    """
    try:
        data = request.get_json()
        validated_data = PolynomialRequest(**data)
        coefficients = validated_data.coefficients

        steps = SolverService.get_step_by_step(coefficients)
        logger.info(f"Generated explanation for coefficients: {coefficients}")
        
        return jsonify({"steps": steps}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        logger.error(f"Unexpected error in /explain: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

@solver_bp.route('/plot', methods=['POST'])
def plot_polynomial():
    """
    Generate a graph of the polynomial.
    ---
    tags:
      - Visualizer
    parameters:
      - in: body
        name: body
        schema:
          $ref: '#/definitions/PolynomialCoefficients'
    responses:
      200:
        description: Base64 encoded PNG plot
    """
    try:
        data = request.get_json()
        validated_data = PolynomialRequest(**data)
        coefficients = validated_data.coefficients

        image_base64 = PlotService.generate_plot(coefficients)
        logger.info(f"Generated plot for coefficients: {coefficients}")
        
        if not image_base64:
            return jsonify({"error": "Could not generate plot"}), 400
            
        return jsonify({"plot": image_base64}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        logger.error(f"Unexpected error in /plot: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500
