from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class CrowdSensorIn(BaseModel):
    zone: str = Field(min_length=2, max_length=100)
    count: int = Field(ge=0, le=250000)
    capacity: int = Field(gt=0, le=250000)
    flow_per_minute: float = Field(ge=0, le=50000)
    source: str = Field(default="sensor_api", min_length=2, max_length=80)
    observed_at: datetime | None = None

    @field_validator("zone", "source")
    @classmethod
    def normalized(cls, value: str) -> str:
        return value.strip()

class CrowdLiveOut(BaseModel):
    zone: str
    density: str
    percentage: int = Field(ge=0, le=100)
    predicted_percentage_15m: int = Field(ge=0, le=100)
    flow_per_minute: float
    source: str
    updated_at: datetime
    alternate_gates: list[str]
    recommendation: str
    congestion_prediction: str
    risk_level: str

class NavigationEnhancedOut(BaseModel):
    route: str
    distance: str
    estimated_time: str
    fastest_route: str
    least_crowded_route: str
    wheelchair_route: str
    reason: str
    safety_note: str

class OperationsSummaryOut(BaseModel):
    crowd_status: str
    gate_congestion: str
    security_alerts: str
    medical_incidents: str
    volunteer_availability: str
    transport_status: str
    weather: str
    ai_recommendations: list[str]
    data_context: str

class VolunteerRequest(BaseModel):
    request: str = Field(min_length=3, max_length=2000)
class VolunteerOut(BaseModel):
    deployment_plan: str
    crowd_redistribution: str
    emergency_support: str
    gate_management: str
    priority: str

class EmergencyEnhancedOut(BaseModel):
    status: str
    incident_id: str
    reported_at: datetime
    evacuation_plan: str
    ambulance_routing: str
    multilingual_announcement: str
    volunteer_instructions: str
    organizer_summary: str
    priority: str

class AccessibilityRequest(BaseModel):
    request: str = Field(min_length=3, max_length=2000)
    location: str = Field(default="current location", min_length=2, max_length=160)
class AccessibilityOut(BaseModel):
    guidance: str
    wheelchair_route: str
    elevator_guidance: str
    voice_guidance: str
    accessible_restroom: str
    safety_note: str

class SustainabilityOut(BaseModel):
    eco_friendly_travel: str
    refill_station: str
    recycling_points: str
    carbon_reduction_tips: str
    low_energy_recommendations: str

class TransportOut(BaseModel):
    shuttle_recommendation: str
    parking_suggestion: str
    public_transport_advice: str
    estimated_travel_time: str
    accessibility_note: str

class DecisionSupportOut(BaseModel):
    situation_assessment: str
    recommended_actions: list[str]
    urgency: str
    decision_rationale: str
    data_context: str