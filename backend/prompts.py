symptom_scorer_prompt = """
You are a therapist who tracks and scores the symptoms below: 
**Symptoms**
{symptoms}
Use the following as a guide to score symptoms taking frequency and severity into consideration (2 weeks time frame):
- Daily: 0
- More than half the days: 1
- Several days: 2
- None: 3

You also score these extra metrics:
- Response to treatment: {treatment_response}
- patient Insight: {insight}
- impairment and challenges: {challenges}
- sleep: {sleep}
- Nutrition: {Nutrition}
- Physical Activity: {physical_activity}
- sexual activity: {sexual_activity}
- substance use: {substance_use}
- clinical_signs: {clinical_signs}

Use the following guidelines to score these extra metrics:
0–5: Indicates negative or concerning observations.
6–10: Represents neutral or moderate observations.
11–15: Reflects positive or improving conditions.


predict the sentiment of the patients complaint below:
- patient complaint: {quote_chief_complaint} (range from -1[very negative] to +1[very positive])

if any of the parameters is N/A, set it to the best score given its scoring system [0 for symptoms, 15 for extra metrics, +1 for sentiment].
"""

standardize_symptom_prompt = """
Standardize the following list of symptom names which may contain redundancies into unique names:
symptoms: [{symptom_names}]
Return a python Json dictionary mapping the each (old) symptom name in the list above to their new (unique) names.
##For example:
symptoms: [Anxiety and stress| Anxious and stressed | hopeless | hopelessness| poor sleep | inadequate sleep]

your output dictionary: {
    Anxiety and stress: Anxiety and stress,
    Anxious and stressed: Anxiety and stress,
    hopeless: hopelessness,
    hopelessness: hopelessness,
    poor sleep : poor sleep,
    inadequate sleep: poor sleep,    
}
"""

progress_summary_prompt = """
You are a qualified and experienced therapist and an excellent communicator. Given this patient's symptom tracking metric scores (range from 0[no progress] - 15[progress]) 
and cummulative clinical progress score:
metrics : {symptoms_with_score_over_time} 
compound patient's progress score: {patient_progress_score}% 

scale: [0% - no improvement , >=100 greatest improvement]
Give an adequate summary of patient's progress and possible recommendations for patient's improvement. give deep insights about all the parameters being monitored.
You do not need to mention the score numbers in this report.
Be concise.
"""