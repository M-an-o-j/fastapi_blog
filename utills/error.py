from fastapi import HTTPException

def error(status_code, message):
    raise HTTPException(status_code=status_code, detail=message)