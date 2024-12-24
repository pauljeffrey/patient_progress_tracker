from pydantic import BaseModel, Field
from typing import List, Dict

class Symptom(BaseModel):
    symptom: str = Field("symptom name from description")
    score: int = Field("score [int]")
    
    def to_dict(self):
        return self.dict()

class ClinicalSign(BaseModel):
    sign_name: str = Field("clinical sign detected")
    score: int = Field('score [int]')
    
    
class Metrics(BaseModel):
    symptoms: List[Symptom] = Field('List of all symptom names with their respective scores')
    treatment_response: int = Field('score for response to treatment [int]')
    insight: int = Field('insight score [int]')
    impairment: int = Field('impairment and challenge score [int]')
    sleep: int = Field('sleep score [int]')
    nutrition: int = Field('nutrition score [int]')
    physical_activity: int = Field('physical activity score [int]')
    sexual_activity: int = Field('sexual activity score [int]')
    substance_use: int = Field('substance score [int]')
    sentiment: float = Field('sentiment score [int]')
    clinical_signs: List[ClinicalSign] = Field('List of clinical signs with their respective scores')
    
class s(BaseModel):
    old_symptom_name: str = Field('original symptom name')
    standard_symptom_name: str = Field('new symptom name')
    
class StandardSymptoms(BaseModel):
    symptom_dict : List[s] = Field("list of symptoms and their corresponding new names as key-value pairs")
    
class SummaryAndRecommendations(BaseModel):
    summary : str = Field('summary of patients progress based on tracked metrics/symptoms scores')
    recommendation: str = Field('Recommendation based on patient\'s progress status (cummulative progress score)')