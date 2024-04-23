from flask import Flask, request, jsonify
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import json
from dotenv import load_dotenv
import openai
import requests
import os
import openai
import json
import ast
import pandas as pd
import numpy as np
import json
import csv

from openai import OpenAI
import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]
endpoint = os.environ["endpoint"]
key = os.environ["key"]

app = Flask(__name__)

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
    
def write_to_json(output, json_file_path):
    with open(json_file_path, "w") as file:
        json.dump(output, file, indent=4)

def get_completion(prompt, model="gpt-3.5-turbo-0125"):
    messages = [{"role": "user", "content": prompt}]
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return completion.choices[0].message

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

@app.route('/invoice_details', methods=['POST'])
def extract_and_complete():
    data = request.json
    image_url = data.get('image_url')
    
    if not image_url:
        return jsonify({'error': 'Image URL not provided'}), 400
    
    try:
        # Download the image
        image_path = "image.jpg"  # Specify the path where you want to save the image
        success = download_image(image_url, image_path)
        if not success:
            return jsonify({'error': f'Failed to download image from {image_url}'}), 500
        
        # Extract information from the image
        output = analyze_read_from_image(image_path)
        
        # Write output to JSON file
        json_file_path = "output.json"
        write_to_json(output, json_file_path)
        print(f"Results have been written to {json_file_path}.")

        # Construct completion prompt
        details = f"""
        You will be provided with invoice information in json format.
        Extract only the following information fully:
        - details of purchaser / customer/ client/ shopper/consumer
        - details of seller / vendor / dealer / supplier / retailer / distributor / wholesaler
        - complete invoice details

        '''{output}'''
        """

        # Get completion from OpenAI
        completion_result = get_completion(details)
        
        # Access the content of the completion result
        # completion_content = completion_result.content
        completion_content = json.loads(completion_result.content)
        
        return jsonify({'complete_details': completion_content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
