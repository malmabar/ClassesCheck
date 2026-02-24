from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.check_service import run_checks_for_run


class RunChecksRequest(BaseModel):
    run_id: str = Field(..., min_length=1)
    created_by: str = Field(default="api-user")


router = APIRouter(prefix="/api/v1/mc/checks", tags=["mc-checks"])


@router.post("/run")
def run_checks(request: RunChecksRequest, db: Session = Depends(get_db)):
    try:
        result = run_checks_for_run(
            db=db,
            run_id=request.run_id,
            triggered_by=request.created_by,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "Checks run completed.",
        "result": result,
    }
