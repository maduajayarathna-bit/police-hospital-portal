from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List, Dict, Any

app = FastAPI(
    title="Police Hospital Backend Engine",
    description="Developer & Super Admin: B.P.G. Anil Madusanka Jayarathna (PC 84489)",
    version="5.0.0"
)

# 1. CORS Middleware (මොබයිල් ඇප් එකට සහ HTML පිටුවලට Backend එක සමඟ සන්නිවේදනය කිරීමට මෙය අනිවාර්ය වේ)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # පරීක්ෂණ මට්ටමේදී සියලුම බාහිර ලින්ක්ස් වලට ඉඩ දෙයි
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. DATA MODELS
class PatientRegistration(BaseModel):
    full_name: str
    dob: date
    nic_no: str
    police_id_no: str
    contact_no: str

# DATA STORAGE (In-Memory)
temporary_patient_db: Dict[str, Dict[str, Any]] = {}
system_audit_logs: List[Dict[str, Any]] = []

def log_audit_trail(actor_id: str, action_type: str, target_table: str, record_id: str, changes: dict):
    log_entry = {
        "log_id": len(system_audit_logs) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor_id": actor_id,
        "action_type": action_type,
        "target_table": target_table,
        "record_id": record_id,
        "mutated_data_snapshot": changes
    }
    system_audit_logs.append(log_entry)

# 3. API ENDPOINTS
@app.get("/")
def root():
    return {"status": "Online", "owner": "B.P.G. Anil Madusanka Jayarathna (PC 84489)"}

@app.post("/api/patient/register", status_code=status.HTTP_201_CREATED)
def register_patient(patient: PatientRegistration):
    generated_reg_no = f"PH-{1000 + len(temporary_patient_db)}"
    temporary_patient_db[generated_reg_no] = {
        "profile": patient.dict(),
        "medical_history": {},
        "medical_reports": {}
    }
    log_audit_trail("OPD_Staff", "INSERT", "user_profiles", generated_reg_no, {"name": patient.full_name})
    return {"message": "Success", "police_hospital_reg_no": generated_reg_no}