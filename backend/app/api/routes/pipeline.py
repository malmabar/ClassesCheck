from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps.rbac import require_mutation_access
from app.db.session import get_db
from app.services.run_lifecycle import RunLockBusyError
from app.services.run_service import build_codes_for_run


class RunPipelineRequest(BaseModel):
    run_id: str = Field(..., min_length=1)
    created_by: str = Field(default="api-user")


router = APIRouter(
    prefix="/api/v1/mc",
    tags=["mc-pipeline"],
    dependencies=[Depends(require_mutation_access)],
)


@router.post("/run")
def run_pipeline(request: RunPipelineRequest, db: Session = Depends(get_db)):
    try:
        result = build_codes_for_run(
            db=db,
            run_id=request.run_id,
            triggered_by=request.created_by,
        )
    except RunLockBusyError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "Pipeline run completed.",
        "result": result,
    }
