from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Application
from schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatus,
    ApplicationUpdate,
)


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Job Tracker API is running"}


@app.get(
    "/applications",
    response_model=list[ApplicationResponse]
)
def get_applications(
    db: Session = Depends(get_db),
    status: ApplicationStatus | None = None
):
    statement = select(Application)

    if status is not None:
        statement = statement.where(
            Application.status == status
        )

    return db.scalars(statement).all()


@app.get(
    "/applications/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.get(Application, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@app.post(
    "/applications",
    response_model=ApplicationResponse,
    status_code=201
)
def create_application(
    new_application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    application = Application(
        company=new_application.company,
        role=new_application.role,
        status=new_application.status
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@app.patch(
    "/applications/{application_id}",
    response_model=ApplicationResponse
)
def update_application(
    application_id: int,
    update: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    application = db.get(Application, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application.status = update.status
    db.commit()
    db.refresh(application)

    return application


@app.delete(
    "/applications/{application_id}",
    status_code=204
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.get(Application, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()