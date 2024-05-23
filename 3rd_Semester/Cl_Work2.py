from fastapi import FastAPI, Path, Query

app = FastAPI()

# d_values = {}
d_values = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}


# http://127.0.0.1:8000/change_dict/
@app.get("/change_dict/")
def get_dict():
    return {"value": d_values}

# http://127.0.0.1:8000/change_dict/?key=key10&value=value10
@app.post("/change_dict/")
def add_to_dict(key: str = Query(...), value: str = Query(...)):
    d_values[key] = value
    return {"message": f"Added {key}: {value} to dictionary"}

# http://127.0.0.1:8000/change_dict/key111?value=value111
@app.put("/change_dict/{key}")
def update_dict(key: str, value: str):
    if key in d_values:
        d_values[key] = value
        return {"message": f"Updated {key} to {value}"}
    else:
        return {"message": "No key in our dictionary"}

# http://127.0.0.1:8000/change_dict/key11
@app.delete("/change_dict/{key}")
def delete_from_dict(key: str):
    if key in d_values:
        del d_values[key]
        return {"message": f"Deleted {key} from dictionary"}
    else:
        return {"message": "No key in our dictionary"}
