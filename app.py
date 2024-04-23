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


def get_completion(prompt, model="gpt-3.5-turbo-0125"):
    messages = [{"role": "user", "content": prompt}]
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return completion.choices[0].message


# Read JSON data from file
with open('output43.json', 'r') as json_file:
    data43 = json.load(json_file)

# print(data45)


details = f"""
You will be provided with invoice details.
Extract only below information fully

- details of purchaser / customer/ client/ shopper/consumer
- details of seller / vendor / dealer / supplier / retailer / distributor / wholesaler
- complete invoice details

'''{data43}'''

"""

image_details = get_completion(details)
print(image_details.content)

