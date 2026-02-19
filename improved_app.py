from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict

app = FastAPI(title="Improved API (Centralised Validation + Standardised Errors)")

# In-memory store
items: Dict[int, Dict] = {1: {"name": "apple", "price": 1.2}}

# --- Standard error response helper ---
def error_response(status_code: int, error_code: str, message: str, details=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "error_code": error_code,
            "message": message,
            "details": details or [],
        },
    )

# --- Centralised validation schema ---
class ItemIn(BaseModel):
    model_config = ConfigDict(extra="forbid")  # reject unknown fields
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)

# --- Centralised exception handler for validation errors ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for e in exc.errors():
        loc = e.get("loc", [])
        # loc looks like ("body", "price") or ("path", "item_id")
        field = ".".join(str(x) for x in loc if x not in ("body", "query", "path"))

        details.append({
            "field": field or "request",
            "reason": e.get("msg", "Invalid value")
        })

    return error_response(
        status_code=422,
        error_code="VALIDATION_ERROR",
        message="Fix the highlighted fields and try again.",
        details=details
    )

# --- Centralised exception handler for app errors ---
class AppError(Exception):
    def __init__(self, status_code: int, error_code: str, message: str, details=None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or []

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return error_response(exc.status_code, exc.error_code, exc.message, exc.details)

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise AppError(
            status_code=404,
            error_code="ITEM_NOT_FOUND",
            message="Item not found.",
            details=[{"field": "item_id", "reason": f"{item_id} does not exist"}]
        )
    return items[item_id]

@app.post("/items")
def create_item(item: ItemIn):
    new_id = max(items.keys(), default=0) + 1
    items[new_id] = {"name": item.name, "price": item.price}
    return {"id": new_id, **items[new_id]}
