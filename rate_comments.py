import json 
from openai import OpenAI
import ast

from dotenv import load_dotenv
import os
import re

class CommentRater:
    def __init__(self, comment, prompt, apikey):
        self.comment = comment
        self.prompt = prompt
        self.apikey = apikey
    
    def create_score(self):
        client = OpenAI(api_key=self.apikey)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": self.prompt.replace("{USER_COMMENT}", self.comment)}
                ]
                )
        result = completion.choices[0].message.content
        score_dict = json.loads(result)
        score_list = list(score_dict.values())
        mean_score = round(sum(score_list)/len(score_list))
        return mean_score