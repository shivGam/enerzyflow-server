from fastapi import APIRouter
from app.db import get_db_connection

router = APIRouter()

@router.get('/healthcheck')
def health_check():
    try:
        db = get_db_connection()
        cur = db.cursor()
        cur.execute("SELECT 1;")
        db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error","message": str(e) }