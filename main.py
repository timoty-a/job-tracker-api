from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

app =FastAPI()

ApplicationStatus = Literal[
    "applied",
    "interview",
    "offer",
    "rejected",
    "withdrawn"
]

@app.get("/")
def read_root():
    return{"message": "Job Tracker API is running"}


class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: ApplicationStatus

applications = [
    {
        "id": 1,
        "company": "Paystack",
        "role": "Backend Engineering Intern",
        "status": "applied"
    },
    {
        "id": 2,
        "company": "Flutterwave",
        "role": "Junior Backend Engineer",
        "status": "interview"
    }
]

@app.get("/applications")
def get_applications():
    return applications

@app.get("/applications/{application_id}")


def get_application(application_id: int):
    for application in applications:
        if application["id"] == application_id:
            return application

    raise HTTPException(
        status_code=404,
        detail="Application not found"
    )

@app.post("/applications", status_code=201)

def create_application(new_application: ApplicationCreate):
    new_id = max(
        [application["id"] for application in applications],
        default=0
    ) + 1

    application = {
        "id": new_id,
        "company": new_application.company,
        "role": new_application.role,
        "status": new_application.status
    }

    applications.append(application)
    return application


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus


@app.patch("/applications/{application_id}")
def update_application(
    application_id: int,
    update: ApplicationUpdate
):
    for application in applications:
        if application["id"] == application_id:
            application["status"] = update.status
            return application

    raise HTTPException(
        status_code=404,
        detail="Application not found"
    )


@app.delete("/applications/{application_id}", status_code=204)
def delete_application(application_id: int):
    for application in applications:
        if application["id"] == application_id:
            applications.remove(application)
            return
        
    raise HTTPException(
            status_code=404,
            detail="Application not found"
        )