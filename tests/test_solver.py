import pytest
from services.solver_service import SolverService

def test_linear_equation():
    # 2x - 4 = 0 -> x = 2
    result = SolverService.solve_polynomial([2, -4])
    assert result["degree"] == 1
    assert result["type"] == "real"
    assert len(result["roots"]) == 1
    assert pytest.approx(result["roots"][0]["real"]) == 2.0
    assert result["roots"][0]["imag"] == 0.0

def test_quadratic_real_roots():
    # x^2 - 3x + 2 = 0 -> x = 1, x = 2
    result = SolverService.solve_polynomial([1, -3, 2])
    assert result["degree"] == 2
    assert result["type"] == "real"
    roots = [r["real"] for r in result["roots"]]
    assert pytest.approx(min(roots)) == 1.0
    assert pytest.approx(max(roots)) == 2.0

def test_quadratic_complex_roots():
    # x^2 + 1 = 0 -> x = i, -i
    result = SolverService.solve_polynomial([1, 0, 1])
    assert result["degree"] == 2
    assert result["type"] == "complex"
    assert len(result["roots"]) == 2
    has_pos_i = any(r["imag"] > 0 for r in result["roots"])
    has_neg_i = any(r["imag"] < 0 for r in result["roots"])
    assert has_pos_i and has_neg_i

def test_zero_coefficients():
    result = SolverService.solve_polynomial([0, 0, 0])
    assert result["degree"] == -1
    assert len(result["roots"]) == 0

def test_explanation_linear():
    steps = SolverService.get_step_by_step([2, -4])
    assert any("2. Divide by the coefficient of x" in step for step in steps)
