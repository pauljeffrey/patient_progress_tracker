import json
import random
import os
import matplotlib.pyplot as plt
import base64
# from typing import List
import io
from typing import List, Dict
from collections import defaultdict
from .structs import Metrics

theme = ['insight', 'impairment', 'sleep', 'nutrition', 'physical_activity', 'sexual_activity',
             'substance_use', 'sentiment','treatment_response']

def visualize_symptoms(symptoms_scores , use_symptoms=True , show_plot=False):
    """Generate a plot and return the image as bytes."""
    
    
    if not use_symptoms:
        # Filter items where the key is in the theme
        symptoms_scores = {key: value for key, value in symptoms_scores.items() if key in theme}
    else:
        # Filter items where the key is not in the theme
        symptoms_scores = {key: value for key, value in symptoms_scores.items() if key not in theme}

        
    # Find the maximum length of the score lists
    max_length = max(len(scores) for scores in symptoms_scores.values())
    
    # Shift shorter lists to the right
    aligned_scores = {}
    for symptom, scores in symptoms_scores.items():
        padding = [None] * (max_length - len(scores))
        aligned_scores[symptom] = padding + scores

    # Plot the symptoms
    plt.figure(figsize=(12, 8))
    for symptom, scores in aligned_scores.items():
        plt.plot(range(1, max_length + 1), scores, label=symptom, marker="o")
    
    plt.xlabel("Session Index")
    plt.ylabel("Symptom Score")
    plt.title("Symptom Progress Over Sessions")
    plt.legend()
    plt.grid(True)

    # Save plot to bytes
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    if show_plot:
        plt.show()
    # Encode image as base64
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return image_base64


def extract_relevant_fields(session_data):
    # Define the keys to extract
    keys_to_extract = [
        "Response to Treatment", "Symptoms", "Family Dynamics", "Sleep",
        "Nutrition", "Physical Activity", "Sexual Activity", "Substances",
        "Insight", "Relationships", "Impairments and Challenges", "Quote (Chief Complaint)", 'Diagnosis 1'
    ]
    
    # Initialize result dictionary
    extracted_fields = {}
    
    def find_key_recursively(data, key):
        """
        Recursively search for a key in a nested dictionary.
        Args:
            data (dict): The dictionary to search.
            key (str): The key to find.
        Returns:
            The value of the key if found, otherwise None.
        """
        if not isinstance(data, dict):
            return None
        if key in data:
            return data[key]
        for sub_key, sub_value in data.items():
            if isinstance(sub_value, dict):  # Only traverse dictionaries
                found_value = find_key_recursively(sub_value, key)
                if found_value is not None:
                    return found_value
        return None
    
    # Populate the dictionary with available data or "N/A"
    for key in keys_to_extract:
        extracted_fields[key] = find_key_recursively(session_data, key) or "N/A"
    
    return extracted_fields


async def track_metrics_over_time(scored_metrics: List[Metrics], unique_symptom_names: Dict[str, str]) -> Dict[str, List]:
    """
    Track all themes and symptoms over time, standardizing symptoms using unique_symptom_names.

    Args:
        scored_metrics (List[Metrics]): List of Metrics objects representing data over time steps.
        unique_symptom_names (Dict[str, str]): Mapping of similar symptom names to standardized names.

    Returns:
        Dict[str, List]: Dictionary tracking all themes and standardized symptoms over time.
    """
    # print("unique_symptom_names: ", unique_symptom_names)
    # Initialize a defaultdict to collect values over time
    tracked_data = defaultdict(list)

    for metric in scored_metrics:
        # Track non-symptom themes
        tracked_data['insight'].append(metric.insight)
        tracked_data['impairment'].append(metric.impairment)
        tracked_data['sleep'].append(metric.sleep)
        tracked_data['nutrition'].append(metric.nutrition)
        tracked_data['physical_activity'].append(metric.physical_activity)
        tracked_data['sexual_activity'].append(metric.sexual_activity)
        tracked_data['substance_use'].append(metric.substance_use)
        tracked_data['sentiment'].append(metric.sentiment)
        tracked_data['treatment_response'].append(metric.treatment_response)
        
        # Track symptoms, standardizing names
        for symptom in metric.symptoms:
            standardized_name = unique_symptom_names.get(symptom.symptom, symptom.symptom)
            tracked_data[standardized_name].append(symptom.score)
    
    # Convert defaultdict to a regular dictionary for the final result
    metrics_over_time = dict(tracked_data)
    metrics_over_time['sentiment'] = [score_sentiment(each_score) for each_score in metrics_over_time['sentiment']]
    
    return metrics_over_time


def score_sentiment(compound_score) -> int:
    """
    Score the sentiment on a 0–15 scale.
    Args:
        compound_score (int): sentiment compound score.
    Returns:
        int: The sentiment score on a 0–15 scale.
    """
    transformed_score = round(((compound_score + 1) / 2) * 15)

    return transformed_score

def split_scores(scores):
    symptom_scores = []
    other_metrics_scores = []
    sentiment_score = scores['sentiment']
    
    for key, value in scores.items():
        if key == 'sentiment':
            continue
        if  key in theme:
            other_metrics_scores.append(value)
        else:
            symptom_scores.append(value)
            
    return symptom_scores, other_metrics_scores, sentiment_score

def compute_cumulative_score(symptom_scores, theme_scores, sentiment_score, weights={'symptoms': 0.7, 'themes': 0.20, 'sentiment': 0.10}  ):
    """
    Compute the cumulative score from symptom, theme, and sentiment scores.
    Args:
        symptom_scores (list): List of normalized symptom scores.
        theme_scores (list): List of theme scores.
        sentiment_score (float): Sentiment score.
        weights (dict): Dictionary of weights for symptoms, themes, and sentiment.
    Returns:
        float: Cumulative score.
    """
    # Sum of scores
    total_symptom_score = sum(symptom_scores)
    total_theme_score = sum(theme_scores)

    # Weighted sum of all components
    weighted_sum = (
        weights['symptoms'] * total_symptom_score +
        weights['themes'] * total_theme_score +
        weights['sentiment'] * sentiment_score
    )

    # Total weight
    total_weight = weights['symptoms'] + weights['themes'] + weights['sentiment']

    # Compute cumulative score
    cumulative_score = weighted_sum / total_weight
    return cumulative_score


def calculate_progress(symptoms_scores_over_time, alpha=1.0):
    """
    Calculate progress scores considering intermediate steps, with weights for recent meetings
    and a scaled drop penalty.
    Args:
        symptoms_scores_over_time (dict): Dictionary of symptoms and their scores over time.
        alpha (float): Weighting factor for the drop penalty.
    Returns:
        dict: Symptom progress scores and overall progress percentage.
    """
    progress_scores = {}
    total_progress = 0
    # num_symptoms = len(symptoms_scores_over_time)

    for symptom, scores in symptoms_scores_over_time.items():
        n = len(scores)
        if n < 2:
            progress_scores[symptom] = 0  # No progress if there is only one score
            continue

        # Calculate weights for each time step
        weights = [(i + 1) / n for i in range(n)]

        # Calculate weighted average score
        weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
        weight_total = sum(weights)
        weighted_average = weighted_sum / weight_total

        # Initial score
        initial_score = scores[0]
        if initial_score == 0:
            initial_score = 1  # Avoid division by zero

        # Calculate progress percentage relative to the initial score
        progress_percentage = ((weighted_average - initial_score) / initial_score) * 100

        # Calculate drop penalty
        total_possible_drop = 15 * (n - 1)
        drop_penalty = (
            alpha
            * sum(max(0, scores[i] - scores[i + 1]) for i in range(n - 1))
            / total_possible_drop
            * 100
        )

        # Final progress score with penalty applied
        final_progress = progress_percentage - drop_penalty
        progress_scores[symptom] = final_progress
        total_progress += final_progress

    # Overall progress score
    # overall_progress = total_progress / num_symptoms

    return progress_scores         # "overall_progress": overall_progress


if __name__ == '__main__':
    file_name = random.choice(os.listdir("./data"))
    file_path = os.path.join(os.path.abspath('./data'), file_name)
    
    
    # Symptom scores over sessions
    symptom_scores = {
        "Anxiety": [-0.6, -0.4, -0.2],
        "Hopelessness": [-0.8, -0.7],
        "Sleep Issues": [-0.3, 0.0, 0.3, 0.5]
    }

    # Visualize the symptoms
    # visualize_symptoms(symptom_scores)
    
    # Sample session JSON data
    session_data = {
        "Progress and Response": {
            "Response to Treatment": "The client has shown minimal progress.",
        },
        "Psychological Factors": {
            "Symptoms": {
                "Symptom 1": {
                    "Description": "Increased stress and anxiety related to academic pressures.",
                    "Frequency": "Daily",
                    "Intensity": "High"
                }
            }
        },
        "Biological Factors": {
            "Sleep": "Difficulty sleeping due to stress.",
            "Nutrition": "NA",
            "Physical Activity": "NA",
            "Sexual Activity": "NA",
            "Substances": "NA"
        },
        "Mental Status Exam": {
            "Insight": "The client recognized worsening symptoms but felt unable to manage them."
        },
        "Social Factors": {
            "Relationships": "The client feels isolated."
        },
        "Presentation": {
            "Impairments and Challenges": "Difficulty maintaining personal relationships.",
            "Quote (Chief Complaint)": "\"I thought I was managing it better, but it just feels like everything is piling up again.\""
        }
    }

    # Call the function
    extracted_fields = extract_relevant_fields(session_data)
    print(extracted_fields)

