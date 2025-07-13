from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from jose import jwt, JWTError
import pandas as pd
import io

from app.models.predictor import predict_from_csv
from app.database import SessionLocal, Prediction, User
from app import auth

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

app = FastAPI(title="Web Prediksi Kelulusan Siswa")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter_by(username=username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
async def root():
    return {"message": "Selamat datang di API Prediksi Kelulusan!"}

@app.post("/predict")
async def predict(
    school: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        result = predict_from_csv(df)
        for item in result:
            db_pred = Prediction(
                school=school,
                nama=item["nama"],
                nilai_akhir=item["nilai_akhir"],
                absensi=item["absensi"],
                sikap=item["sikap"],
                predicted_status=item["predicted_status"],
                probability=item["probability"],
                timestamp=datetime.utcnow()
            )
            db.add(db_pred)
        db.commit()
        return {"status": "success", "school": school, "data": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history(school: str = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Prediction).order_by(Prediction.id.desc())
    if school:
        query = query.filter(Prediction.school == school)
    predictions = query.all()
    return [
        {
            "id": p.id,
            "school": p.school,
            "nama": p.nama,
            "nilai_akhir": p.nilai_akhir,
            "absensi": p.absensi,
            "sikap": p.sikap,
            "predicted_status": p.predicted_status,
            "probability": p.probability,
            "timestamp": p.timestamp.isoformat()
        }
        for p in predictions
    ]

@app.get("/stats")
def get_stats(school: str = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Prediction)
    if school:
        query = query.filter(Prediction.school == school)
    total = query.count()
    total_lulus = query.filter(Prediction.predicted_status == "lulus").count()
    total_tidak_lulus = query.filter(Prediction.predicted_status == "tidak lulus").count()
    return {
        "total": total,
        "lulus": total_lulus,
        "tidak_lulus": total_tidak_lulus
    }
