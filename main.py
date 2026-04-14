from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import base64
import shutil
from typing import Optional
from database import get_db_collection
from matching import model
from nearloc import nnear
from models import UserCreate
import uvicorn

app = FastAPI(title="Roommate-Dekho Backend")

# UPLOAD_FOLDER settings
UPLOAD_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Mount static and images directories
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images_dir", StaticFiles(directory=UPLOAD_FOLDER), name="images_dir")

templates = Jinja2Templates(directory="templates")

def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/images/{filename}")
async def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Image not found")

@app.get("/predict", response_class=HTMLResponse)
async def predict_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict_datapoint(
    request: Request,
    Name: str = Form(...),
    latitude: str = Form(""),
    longitude: str = Form(""),
    Budget: str = Form(...),
    Hobbies: str = Form(""),
    Is_Vegetarian: str = Form(None),
    mobile: str = Form(...),
    image: Optional[UploadFile] = File(None),
    collection = Depends(get_db_collection)
):
    try:
        # Handle default coordinates
        lat = latitude.strip()
        lon = longitude.strip()
        if not lat or not lon:
            lat, lon = "23.2599", "77.4126"
        
        location = (float(lat), float(lon))

        # Validate Budget
        try:
            budget_val = float(Budget.strip())
        except ValueError:
            raise HTTPException(status_code=400, detail="Budget must be a number")

        # Validate Mobile
        if not mobile.strip().isdigit():
            raise HTTPException(status_code=400, detail="Invalid mobile number")
        mobile_val = int(mobile.strip())

        # Handle Image Upload
        image_data = ""
        if image and image.filename:
            if allowed_file(image.filename):
                # Save to disk as in original app
                file_path = os.path.join(UPLOAD_FOLDER, image.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                
                # Convert to base64 for DB storage as in original app
                image.file.seek(0)
                image_bytes = await image.read()
                image_data = base64.b64encode(image_bytes).decode('utf-8')

        # Store in MongoDB
        user_count = collection.count_documents({})
        user_number = f"user{user_count + 1}"

        user_data = {
            'user': user_number,
            'Name': Name,
            'location': location,
            'Budget': budget_val,
            'Hobbies': Hobbies,
            'Is_Vegetarian': Is_Vegetarian,
            'mobile': mobile_val,
            'image': image_data
        }
        collection.insert_one(user_data)

        # Find nearest roommates
        near = nnear()
        collection.drop_indexes() # Reset indexes for fresh distance check
        all_users = list(collection.find({}, {'_id': 0}))
        nearby_users = near.find_nearest_by_location(all_users, user_number)

        # ML Model Prediction
        ml = model()
        result = ml.fit_it(user_number, nearby=nearby_users)

        return templates.TemplateResponse("return.html", {"request": request, "results": result})

    except Exception as e:
        return f"🚨 An error occurred: {str(e)}"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
