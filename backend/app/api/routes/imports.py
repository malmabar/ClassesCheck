from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps.rbac import require_mutation_access
from app.db.session import get_db
from app.services.import_service import import_ss01_csv


router = APIRouter(
    prefix="/api/v1/mc/import",
    tags=["mc-import"],
    dependencies=[Depends(require_mutation_access)],
)


@router.post("/ss01")
async def import_ss01(
    file: UploadFile = File(...),
    semester: str = Form(...),
    period: str = Form(...),
    created_by: str = Form(default="api-user"),
    db: Session = Depends(get_db),
):
    file_content = await file.read()
    if not file_content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        result = import_ss01_csv(
            db=db,
            file_bytes=file_content,
            file_name=file.filename or "ss01.csv",
            semester=semester,
            period=period,
            created_by=created_by,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "SS01 import completed.",
        "result": result,
    }
