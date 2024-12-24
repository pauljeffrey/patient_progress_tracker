# from prompts import *
from .utils import *
from .prompts import *
from .structs import *
from typing import List, Union, Dict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

# Load the .env file
load_dotenv()

# Access the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key, temperature=0, seed=42)


symptom_scorer = llm.with_structured_output(Metrics)
symptom_standardizer = llm.with_structured_output(StandardSymptoms)
assistant = llm.with_structured_output(SummaryAndRecommendations)

# Functions to fill prompts dynamically and invoke models/services
async def score_symptoms(session_notes: List[Dict]):
    """Fill the symptom scoring prompt and invoke the symptom scorer."""

    filled_prompt = [symptom_scorer_prompt.format(
        symptoms=str(each_note.get("Symptoms", "N/A")),
        treatment_response=each_note.get("Response to Treatment", "N/A"),
        insight=each_note.get("Insight", "N/A"),
        challenges=each_note.get("Impairments and Challenges", "N/A"),
        sleep=each_note.get("Sleep", "N/A"),
        Nutrition=each_note.get("Nutrition", "N/A"),
        physical_activity=each_note.get("Physical Activity", "15"),
        sexual_activity=each_note.get("Sexual Activity", "15"),
        substance_use=each_note.get("Substances", "15"),
        clinical_signs=each_note.get("clinical_signs", "15"),
        quote_chief_complaint=each_note.get("Quote (Chief Complaint)", "N/A"),
    ) 
    for each_note in session_notes]
    # print("note sample: ", filled_prompt[-1])
    return await symptom_scorer.abatch(filled_prompt)


# async def standardize_symptom_names(symptoms: List[str]):
#     """Fill the standardization prompt and invoke the standardizer."""
#     symptoms = "| ".join([symptom.strip() for symptom in symptoms])
#     print("symptoms noted: ", ", ".join(symptoms))
#     filled_prompt = standardize_symptom_prompt.format(
#         symptom_names= symptoms
#     )
#     return symptom_standardizer.invoke(filled_prompt)

async def standardize_symptom_names(symptoms: List[str]):
    """Fill the standardization prompt and invoke the standardizer."""
    # Prepare symptoms as a clean, formatted list
    symptom_names = "| ".join(symptoms)
    
    # Use f-string to safely fill the prompt
    filled_prompt = f"""
    Standardize the following list of '|' separated symptom names which may contain redundancies into unique names:
    symptoms: [{symptom_names}]
    
    Return a python dictionary mapping the each (old) symptom name in the list above to their new (unique) names.
    ##Example:
    symptoms: [Anxiety and stress| Anxious and stressed | hopeless | hopelessness| poor sleep | inadequate sleep]

    your output dictionary: {{
        Anxiety and stress: Anxiety and stress,
        Anxious and stressed: Anxiety and stress,
        hopeless: hopelessness,
        hopelessness: hopelessness,
        poor sleep : poor sleep,
        inadequate sleep: poor sleep,    
    }}
   
    """
    standardize_symptom_names = await symptom_standardizer.ainvoke(filled_prompt)
    
    return {symptom.old_symptom_name: symptom.standard_symptom_name for symptom in standardize_symptom_names.symptom_dict}



async def summarize_recommend(symptoms_with_score_over_time: dict, patient_progress_score: float):
    """Fill the progress summary prompt and invoke the assistant."""
    filled_prompt = progress_summary_prompt.format(
        symptoms_with_score_over_time=json.dumps(symptoms_with_score_over_time),
        patient_progress_score=patient_progress_score,
    )
    return await assistant.ainvoke(filled_prompt)
