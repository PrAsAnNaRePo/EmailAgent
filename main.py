
from fastapi import FastAPI
import requests

app = FastAPI()

def run(uri, prompt, force_model=False):
    if force_model:
        prompt += "\nTo:"
    request = {
        'prompt': prompt,
        'max_new_tokens': 500,
        'auto_max_new_tokens': False,
        'max_tokens_second': 0,
        'do_sample': True,
        'temperature': 0.4,
        'repetition_penalty': 1.24,
        'temperature': 0.1,
        'skip_special_tokens': True,
        'stopping_strings': ['<|end_of_turn|>', '<|im_end|>', 'Observation']
    }

    response = requests.post(uri, json=request)
    print(response.status_code)
    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        return '\nTo:'+result if force_model else result

template = """You are a Email reply agent. You are working for a User. Here is the details of the User:
- name: prasanna
- age: 20
- work: Machine Learning Engineer.
- company: nnpy
- contact: +919361044845

You can use the user's info while writing reply for clients.
Make sure that you are sending reply as user (Prasanna). Act like a professional.
You will recieve email from clients, you have to send reply for each email
Only for reply only if you have information to send mail such as email.
Make sure that reply contains only the relevent and true information. assistant should not use false information. If you don't know the info, just don't put any random and place holders.
Please don't spam and write only correct and relevent contents in the body.
Here is the format to respond:
To: client_email@gmail.com
Subject: subject
body
"""

from pydantic import BaseModel

class EmailRequest(BaseModel):
    email: str
    url: str

@app.post("/")
def get_replay(req: EmailRequest):
    prompt = template + f'GPT4 User: {req.email}<|end_of_turn|>GPT4 Assistant:'
    response = run(req.url, prompt, force_model=True).strip()
    body = ''
    for idx, st in enumerate(response.split('\n')):
        if idx>1:
            body+='\n' if st == '' else st
        
    return {
        'email': response.split('\n')[0].replace("To:", '').strip(),
        'subject': response.split('\n')[1].replace("Subject:", '').strip(),
        'body': body.strip(),
    }
    
