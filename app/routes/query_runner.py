from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from app.db import get_db_connection

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def run_query(payload : QueryRequest):
    try:
        db = get_db_connection()
        cur = db.cursor()
        cur.execute(payload.query)
        try:
            result = cur.fetchall()
        except:
            result = []
        db.commit()
        db.close()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code= 400,detail = str(e))