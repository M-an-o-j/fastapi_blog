from fastapi import HTTPException
from fastapi.responses import JSONResponse

def errorhandler(status_code, message):
    raise HTTPException(status_code=status_code, detail=message)

