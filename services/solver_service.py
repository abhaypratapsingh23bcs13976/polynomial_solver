import numpy as np
import cmath

class SolverService:
    @staticmethod
    def solve_polynomial(coefficients):
        """
        Finds all roots of a polynomial with given coefficients.
        Coefficients should be in descending order: [a_n, a_{n-1}, ..., a_0]
        """
        # Remove leading zeros
        coeffs = np.trim_zeros(coefficients, 'f')
        
        if len(coeffs) == 0:
            return {
                "roots": [],
                "degree": -1,
                "type": "none"
            }
            
        degree = len(coeffs) - 1
        
        if degree == 0:
            return {
                "roots": [],
                "degree": 0,
                "type": "constant"
            }

        roots = np.roots(coeffs)
        
        # Convert complex numbers to serializable format
        root_list = []
        is_complex = False
        for r in roots:
            if np.iscomplex(r):
                is_complex = True
                root_list.append({"real": float(r.real), "imag": float(r.imag)})
            else:
                root_list.append({"real": float(r.real), "imag": 0.0})

        return {
            "roots": root_list,
            "degree": int(degree),
            "type": "complex" if is_complex else "real"
        }

    @staticmethod
    def get_step_by_step(coefficients):
        """
        Provides a step-by-step explanation for solving the polynomial.
        Currently supports linear (degree 1) and quadratic (degree 2).
        """
        coeffs = np.trim_zeros(coefficients, 'f')
        degree = len(coeffs) - 1
        
        steps = []
        
        if degree == 1:
            # ax + b = 0
            a, b = coeffs
            steps.append(f"Equation: {a}x {'+' if b >= 0 else '-'} {abs(b)} = 0")
            steps.append(f"1. Move the constant term to the other side: {a}x = {-b}")
            steps.append(f"2. Divide by the coefficient of x: x = {-b}/{a}")
            steps.append(f"Result: x = {-b/a}")
            
        elif degree == 2:
            # ax^2 + bx + c = 0
            a, b, c = coeffs
            steps.append(f"Equation: {a}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0")
            steps.append(f"Using the quadratic formula: x = [-b ± sqrt(b² - 4ac)] / 2a")
            
            discriminant = b**2 - 4*a*c
            steps.append(f"1. Identify coefficients: a = {a}, b = {b}, c = {c}")
            steps.append(f"2. Calculate discriminant (D = b² - 4ac): {b}² - 4({a})({c}) = {discriminant}")
            
            if discriminant > 0:
                sqrt_d = np.sqrt(discriminant)
                steps.append(f"3. D > 0, so there are two distinct real roots.")
                steps.append(f"4. x = [-({b}) ± {sqrt_d}] / {2*a}")
                r1 = (-b + sqrt_d) / (2*a)
                r2 = (-b - sqrt_d) / (2*a)
                steps.append(f"Result: x1 = {r1}, x2 = {r2}")
            elif discriminant == 0:
                steps.append(f"3. D = 0, so there is one repeated real root.")
                steps.append(f"4. x = -({b}) / (2 * {a})")
                r = -b / (2*a)
                steps.append(f"Result: x = {r}")
            else:
                sqrt_d = cmath.sqrt(discriminant)
                steps.append(f"3. D < 0, so there are two complex roots.")
                steps.append(f"4. x = [-({b}) ± {sqrt_d}] / {2*a}")
                r1 = (-b + sqrt_d) / (2*a)
                r2 = (-b - sqrt_d) / (2*a)
                steps.append(f"Result: x1 = {r1}, x2 = {r2}")
        else:
            steps.append(f"Step-by-step explanation is only available for polynomial degrees 1 and 2.")
            steps.append(f"For degree {degree}, numerical methods (numpy.roots) are used to find all roots.")

        return steps
