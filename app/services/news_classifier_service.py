import os
import json

os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

import torch
from transformers import pipeline


def classify_text(input_data):
    try:

        classifier = pipeline("zero-shot-classification",
                              model="facebook/bart-large-mnli",
                              device=0)

        candidate_labels = ["terrorism related", "not terrorism related"]

        if isinstance(input_data, str):
            text_to_analyze = input_data
        elif isinstance(input_data, dict):
            text_to_analyze = input_data.get('text', '') or input_data.get('content', '')
        else:
            raise ValueError("Input must be either text string or JSON dictionary")

        if not text_to_analyze:
            raise ValueError("No text content found to analyze")

        result = classifier(text_to_analyze, candidate_labels)

        is_terrorism = result['labels'][0] == "terrorism related"
        score = result['scores'][0]

        response = {
            'is_terrorism': is_terrorism,
            'confidence': score,
            'classification': 'Yes' if is_terrorism else 'No',
            'analyzed_text': text_to_analyze[:100] + '...' if len(text_to_analyze) > 100 else text_to_analyze
        }
        print(
            'classify_text: \n',
            json.dumps(response, indent=4)
        )

        return response

    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
    news_text = "A bomb exploded in the city center, causing multiple casualties."
    result = classify_text(news_text)
    print("\nClassification Result (Plain Text):", json.dumps(result, indent=2))

    json_input = {
        "text": "A bomb exploded in the city center, causing multiple casualties.",
        "date": "2024-01-01",
        "source": "news_agency"
    }
    result = classify_text(json_input)
    print("\nClassification Result (JSON):", json.dumps(result, indent=2))
