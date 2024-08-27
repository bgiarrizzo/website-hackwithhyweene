from pydantic import BaseModel

class ResumeEducation(BaseModel):
    id: str
    title: str
    school: str
    start_date: str
    end_date: str
    formation_type: str
    status: str
    body: str
