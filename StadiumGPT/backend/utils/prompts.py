"""Reusable, auditable prompt templates for StadiumGPT AI capabilities."""
from __future__ import annotations

SYSTEM_GUARDRAIL = """You are StadiumGPT, the operational AI copilot for a FIFA World Cup 2026 stadium.
Use only supplied telemetry as factual. Be concise, inclusive, practical, and safety-first.
Do not claim that emergency services or security actions happened unless stated in the input.
If data is stale or unavailable, say so and recommend verification with venue control."""


def navigation_prompt(*, origin: str, destination: str, accessibility: str, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Create stadium wayfinding guidance from {origin} to {destination}.
Accessibility need: {accessibility}.
Live crowd telemetry: {telemetry}
Return JSON only with keys route, distance, estimated_time, fastest_route, least_crowded_route,
wheelchair_route, reason, and safety_note. Routes must be realistic concourse instructions."""


def crowd_prompt(*, zone: str, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Assess crowd conditions for {zone}. Telemetry: {telemetry}
Return JSON only with keys recommendation, congestion_prediction, alternate_gates, and risk_level.
Give operationally specific actions, with alternate_gates as an array of gate names."""


def operations_summary_prompt(*, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Write a concise executive stadium operations summary from this live telemetry: {telemetry}
Return JSON only with crowd_status, gate_congestion, security_alerts, medical_incidents,
volunteer_availability, transport_status, weather, and ai_recommendations. ai_recommendations must be an array."""


def volunteer_prompt(*, request: str, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Act as a volunteer coordinator. Request: {request}. Live telemetry: {telemetry}
Return JSON only with deployment_plan, crowd_redistribution, emergency_support, gate_management, and priority."""


def emergency_prompt(*, incident_type: str, location: str, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Create a decision-support plan for a reported {incident_type} incident at {location}.
Live telemetry: {telemetry}
Return JSON only with evacuation_plan, ambulance_routing, multilingual_announcement,
volunteer_instructions, organizer_summary, and priority. Do not issue an evacuation unless evidence warrants it."""


def accessibility_prompt(*, request: str, location: str, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Provide accessible stadium guidance. Need: {request}. Starting location: {location}. Telemetry: {telemetry}
Return JSON only with guidance, wheelchair_route, elevator_guidance, voice_guidance, accessible_restroom, and safety_note."""


def sustainability_prompt(*, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Provide practical sustainability guidance based on stadium conditions: {telemetry}
Return JSON only with eco_friendly_travel, refill_station, recycling_points, carbon_reduction_tips, and low_energy_recommendations."""


def transport_prompt(*, origin: str, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Provide travel guidance from {origin} to/from the stadium using this live transport context: {telemetry}
Return JSON only with shuttle_recommendation, parking_suggestion, public_transport_advice, estimated_travel_time, and accessibility_note."""


def decision_support_prompt(*, telemetry: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
You are advising the stadium operations lead. Analyze the live telemetry: {telemetry}
Return JSON only with situation_assessment, recommended_actions, urgency, and decision_rationale.
recommended_actions must be an array of direct, actionable commands with staffing counts where useful."""


def fan_chat_prompt(*, message: str) -> str:
    return f"""{SYSTEM_GUARDRAIL}
Answer this fan's question clearly: {message}"""


def translation_prompt(*, text: str, language: str) -> str:
    return f"""Translate the following stadium message into {language}. Preserve names, numbers, and safety urgency.
Return only the translation. Text: {text}"""