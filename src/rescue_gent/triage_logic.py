from pydantic import BaseModel, Field
from typing import List, Optional

# This TriageData model is consistent with your llm_parser.py
class TriageData(BaseModel):
    urgency: int = Field(..., description="On a scale of 1-10, how immediate is the threat to life? 10 means people are in active, mortal danger right now (e.g., trapped in a fire, major bleeding).")
    vulnerable_individuals: List[str] = Field(default_factory=list, description="List of vulnerable groups explicitly mentioned (e.g., 'children', 'elderly', 'disabled', 'pregnant').")
    injury_severity: str = Field("None", description="The single WORST injury level described. Options: 'None', 'Minor', 'Serious' (e.g., broken bones), or 'Critical' (life-threatening injuries, death mentioned).")
    people_affected: int = Field(1, description="Best estimate of the number of people directly at risk.")
    latitude: Optional[float] = Field(None, description="The estimated latitude of the incident. Null if not identifiable.")
    longitude: Optional[float] = Field(None, description="The estimated longitude of the incident. Null if not identifiable.")
    summary: str = Field(..., description="A very brief, one-sentence summary of the core incident, like 'Building collapse with trapped children.'")
    resource_needs: List[str] = Field(default_factory=list, description="List of critical resources needed (e.g., 'ambulance', 'firefighters', 'boat', 'heavy machinery').")


def calculate_rescue_score(data: TriageData, original_message: str) -> dict:
    """
    Calculates a professional-grade priority score.
    A 'Critical' injury_severity is paramount.
    """
    score = 0
    reasoning = []

    # --- Stage 1: Assess Direct Threat to Life ---
    base_threat_score = 0
    if data.injury_severity == "Critical":
        base_threat_score = 80  # A death or critical injury sets a very high baseline
        reasoning.append("Critical Injury / Fatality Reported")
    elif data.injury_severity == "Serious":
        base_threat_score = 60
        reasoning.append("Serious Injuries Reported")
    elif data.injury_severity == "Minor":
        base_threat_score = 20
        reasoning.append("Minor Injuries Reported")
    
    urgency_contribution = data.urgency * 5
    score = max(base_threat_score, urgency_contribution)
    if data.urgency >= 8 and base_threat_score < 50:
        reasoning.append(f"High Urgency (Level {data.urgency})")

    # --- Stage 2: Contextual Modifiers ---
    if data.vulnerable_individuals:
        vulnerability_bonus = 15 * len(data.vulnerable_individuals)
        score += vulnerability_bonus
        reasoning.append(f"+{vulnerability_bonus} for Vulnerable Groups: {', '.join(data.vulnerable_individuals)}")

    if data.people_affected > 1:
        scale_bonus = min(data.people_affected * 2, 20) 
        score += scale_bonus
        reasoning.append(f"+{scale_bonus} for Scale ({data.people_affected} people)")
    
    critical_needs_list = {'firefighters', 'ambulance', 'heavy machinery'}
    if any(need.lower() in critical_needs_list for need in data.resource_needs):
        score += 5
        reasoning.append("+5 for Critical Resource Needs")

    # --- Stage 3: Quality Check and Finalization ---
    if data.urgency <= 2 and data.injury_severity == "None" and len(original_message) < 20:
        score = max(0, score - 30)
        reasoning.append("Penalty for low quality/spam report")

    final_score = min(int(score), 100)
    
    if data.injury_severity == "Critical" and final_score < 85:
        final_score = 85
        reasoning.append("Score elevated to minimum for Critical Injury")

    reasoning_summary = " | ".join(reasoning) if reasoning else "Standard assessment based on urgency."

    return {
        "priority_score": final_score,
        "details": data.model_dump(),
        "reasoning": reasoning_summary
    }