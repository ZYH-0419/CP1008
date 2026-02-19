from fastapi import FastAPI, HTTPException, Body

app = FastAPI(title="Baseline API")

# In-memory store
items = {1: {"name": "apple", "price": 1.2}}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    # Inconsistent error format (plain string in detail)
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items")
def create_item(payload: dict = Body(...)):
    # Manual validation (inconsistent + incomplete)
    if "name" not in payload:
        # Inconsistent: different message style
        raise HTTPException(status_code=400, detail="Missing field: name")

    if "price" not in payload:
        raise HTTPException(status_code=400, detail={"error": "price is required"})  # detail is a dict here

    # Another inconsistency: price type not checked properly
    try:
        price = float(payload["price"])
    except Exception:
        # Inconsistent: returns a different structure
        raise HTTPException(status_code=422, detail={"msg": "price must be numeric"})

    new_id = max(items.keys(), default=0) + 1
    items[new_id] = {"name": payload["name"], "price": price}
    return {"id": new_id, **items[new_id]}
