class Resume:
    id: str
    title: str
    start_date: str
    end_date: str
    body: str

class ResumeEducation(Resume):
    school: str
    formation_type: str
    status: str

class ResumeExperience(Resume):
    company: str
    company_url: str
    contract_type: str
