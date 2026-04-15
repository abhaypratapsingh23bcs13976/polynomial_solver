from pydantic import BaseModel, Field, validator
from typing import List

class PolynomialRequest(BaseModel):
    coefficients: List[float] = Field(..., description="List of polynomial coefficients in descending order of power.")

    @validator('coefficients')
    def check_coefficients_not_empty(cls, v):
        if not v:
            raise ValueError('Coefficients list cannot be empty')
        # Check if at least one coefficient is non-zero (to avoid 0=0 trivial case which isn't a polynomial equation)
        if all(c == 0 for c in v):
            raise ValueError('Polynomial cannot have all zero coefficients')
        return v

    @validator('coefficients')
    def check_degree_limit(cls, v):
        if len(v) > 100:
            raise ValueError('Polynomial degree is too large (max degree 99)')
        return v
