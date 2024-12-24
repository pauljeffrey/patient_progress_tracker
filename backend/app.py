from .backend import *
from .utils import *
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import json
from typing import List

app = FastAPI()

# Helper functions
def load_file(file: UploadFile):
    """Load file content into a dictionary."""
    content = file.file.read().decode("utf-8")
    try:
        if file.filename.endswith(".json"):
            return json.loads(content)
        elif file.filename.endswith(".txt"):
            return json.loads(content)
    except Exception as e:
        raise ValueError(f"Failed to parse file: {e}")
 

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}   
    

@app.post("/track_symptoms/")
async def track_symptoms(files: List[UploadFile]= File(...), debug=True):
    """Placeholder function for tracking symptoms."""
    try:
        extracted_data = []
        # Process uploaded files
        for file in files:
            all_data = load_file(file)
            
            # Extract relevant fields (example from first file)
            extracted_data.append(extract_relevant_fields(all_data))

        #Score symptoms (metrics)
        scored_metrics = await score_symptoms(extracted_data)
     
        symptoms = []
        
        for each in scored_metrics:
            for symptom in each.symptoms:
                symptoms.append(symptom.symptom)
                
        standardized_symptom_names= await standardize_symptom_names(symptoms)
     
        # Track metrics over time
        metrics_over_time = await track_metrics_over_time(scored_metrics, standardized_symptom_names)
            
        
        ## calculate progress
        progress_scores = calculate_progress(metrics_over_time)
        symptoms_scores, other_metrics_scores, sentiment_score = split_scores(progress_scores)
        patient_cummulative_score = min(100, max(0, compute_cumulative_score(symptoms_scores, other_metrics_scores, sentiment_score)))
        
        if debug:
            print("extracted_data: ", extracted_data)
            print("scored metrics: ", scored_metrics[-1])
            print("unique symptoms: ", standardized_symptom_names)
            print("metrics over time: ", metrics_over_time)
            print("symptom scores: ", symptoms_scores)
            print("metrics scores: ", other_metrics_scores, sentiment_score)
            print('patient_cummulative_score: ', patient_cummulative_score)
            print('metrics over time (stringified): ', json.dumps(metrics_over_time))
            
        # summarize and recommend
        assistant_notes = await summarize_recommend(metrics_over_time, patient_cummulative_score)
        
        # plot symptoms
        symptoms_plot_image = visualize_symptoms(metrics_over_time)
        
        # print(symptoms_plot_image)
        #plot other metrics
        theme_plot_image = visualize_symptoms(metrics_over_time, use_symptoms= False)
        
        # Build response object
        response = {
            "diagnosis": extracted_data[-1]["Diagnosis 1"]['Description'],
            "summary": assistant_notes.summary,
            'recommendation': assistant_notes.recommendation,
            "progress_score": f'{round(patient_cummulative_score, 2)}%',
            "symptoms_plot_image": symptoms_plot_image,
            "theme_plot_image": theme_plot_image,
            "other_info": extracted_data,
        }
        
        return JSONResponse(content=response)

    except Exception as e:
        print(f"Error : {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)