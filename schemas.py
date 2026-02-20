from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any, Annotated
from datetime import datetime
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate_object_id(value: Any) -> ObjectId:
            if isinstance(value, ObjectId):
                return value
            if isinstance(value, str):
                if not ObjectId.is_valid(value):
                    raise ValueError("Invalid ObjectId")
                return ObjectId(value)
            raise ValueError("Invalid ObjectId")

        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.no_info_plain_validator_function(validate_object_id),
        ], serialization=core_schema.plain_serializer_function_ser_schema(str))



# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    age: Optional[int] = None
    gender: Optional[str] = None  # male, female, other
    height: Optional[float] = None  # in cm
    weight: Optional[float] = None  # in kg
    activity_level: Optional[str] = "moderate"  # sedentary, light, moderate, active, very_active
    goal: Optional[str] = "maintenance"  # weight_loss, weight_gain, maintenance, muscle_gain
    is_admin: bool = False


class UserCreate(BaseModel):
    """User creation model"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[str] = "moderate"
    goal: Optional[str] = "maintenance"
    is_admin: bool = False


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class User(UserBase):
    id: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# Health Metrics Schema
class HealthMetrics(BaseModel):
    # Blood Sugar
    fasting_glucose: Optional[float] = None
    random_glucose: Optional[float] = None
    hba1c: Optional[float] = None
    
    # Cholesterol
    total_cholesterol: Optional[float] = None
    hdl_cholesterol: Optional[float] = None
    ldl_cholesterol: Optional[float] = None
    triglycerides: Optional[float] = None
    
    # Blood Pressure
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    
    # Thyroid
    tsh: Optional[float] = None
    t3: Optional[float] = None
    t4: Optional[float] = None
    
    # Vitamins
    vitamin_d: Optional[float] = None
    vitamin_b12: Optional[float] = None
    
    # Other
    bmi: Optional[float] = None
    hemoglobin: Optional[float] = None


# Medical Report Schema
class MedicalReport(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    filename: str
    file_path: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    extracted_text: Optional[str] = None
    health_metrics: Optional[HealthMetrics] = None
    abnormal_flags: Optional[Dict[str, bool]] = None
    risk_level: Optional[str] = None  # low, medium, high
    analysis_summary: Optional[str] = None
    deficiencies: Optional[List[str]] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Diet Plan Schema
class MealPlan(BaseModel):
    meal_type: str  # breakfast, lunch, dinner, snack
    time: str
    food_items: List[str]
    calories: int
    protein: float
    carbs: float
    fat: float
    instructions: Optional[str] = None


class DayPlan(BaseModel):
    day: int
    total_calories: int
    meals: List[MealPlan]


class DietPlan(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    report_id: Optional[str] = None
    plan_type: str = "diet"
    created_date: datetime = Field(default_factory=datetime.utcnow)
    days: List[DayPlan]
    notes: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Workout Plan Schema
class Exercise(BaseModel):
    name: str
    sets: int
    reps: str
    duration: Optional[str] = None
    calories_burned: Optional[int] = None
    instructions: Optional[str] = None


class WorkoutDay(BaseModel):
    day: int
    focus: str  # cardio, strength, flexibility, rest
    exercises: List[Exercise]
    total_duration: int  # in minutes
    total_calories: int


class WorkoutPlan(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    report_id: Optional[str] = None
    plan_type: str = "workout"
    created_date: datetime = Field(default_factory=datetime.utcnow)
    days: List[WorkoutDay]
    notes: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Food Log Schema
class FoodLog(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    date: datetime = Field(default_factory=datetime.utcnow)
    meal_type: str
    food_name: str
    food_image_path: Optional[str] = None
    calories: int
    protein: float
    carbs: float
    fat: float
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Chatbot Schema
class ChatMessage(BaseModel):
    message: str
    user_context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str


    
    
class TokenData(BaseModel):
    email: Optional[str] = None


# Disease Outbreak Schemas
class DiseaseReport(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    location: str
    latitude: float
    longitude: float
    disease_type: str  # e.g., "Dengue", "Malaria", "Covid-19", "Flu"
    symptoms: List[str]
    reported_at: datetime = Field(default_factory=datetime.utcnow)
    severity: str = "moderate" # mild, moderate, severe, critical
    status: str = "verified" # verified, suspected

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class OutbreakAlert(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    location: str
    disease_type: str
    risk_level: str # low, medium, high, critical
    case_count: int
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    message: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Emergency Card Schemas
class EmergencyContact(BaseModel):
    name: str
    relation: str
    phone: str

class EmergencyProfile(BaseModel):
    blood_group: Optional[str] = None
    allergies: List[str] = []
    medical_conditions: List[str] = []
    current_medications: List[str] = []
    organ_donor: bool = False
    emergency_contacts: List[EmergencyContact] = []
    insurance_provider: Optional[str] = None
    insurance_policy_no: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
