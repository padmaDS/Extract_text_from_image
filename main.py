import csv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

import json
import ast
import pandas as pd
import numpy as np
import json
import csv


from dotenv import load_dotenv
load_dotenv()

endpoint = os.environ["endpoint"]
key = os.environ["key"]


import json
endpoint = "https://ds-formrecognition.cognitiveservices.azure.com/"
key = "754a604f96fe40f2b7d0e51a8e06dd03"
def analyze_read_from_image(image_path):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    with open(image_path, "rb") as image_file:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-read", image_file
        )
        result = poller.result()

        output = {}

        # Extract styles information
        styles_info = {}
        for idx, style in enumerate(result.styles):
            styles_info["Style {}".format(idx + 1)] = "handwritten" if style.is_handwritten else "no handwritten"
        output.update(styles_info)

        # Extract content information
        content = result.content
        output["Content"] = content
        
        return output

def write_to_json(output, json_file):
    with open(json_file, "w") as file:
        json.dump(output, file, indent=4)

if __name__ == "__main__":
    image_path = "image\MicrosoftTeams-image (43).png"  # Replace this with the path to your image file
    output = analyze_read_from_image(image_path)
    
    # Print out the output for verification
    print("Output:", output)
    
    json_file = "output43.json"
    write_to_json(output, json_file)
    print(f"Results have been written to {json_file}.")