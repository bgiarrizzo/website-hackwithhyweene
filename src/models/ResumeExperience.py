from pydantic import BaseModel

class ResumeExperience(BaseModel):
    id: str
    title: str
    company: str
    company_url: str
    start_date: str
    end_date: str
    contract_type: str
    body: str
