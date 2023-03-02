import openai
import configparser

def get_openai_response(prompt,max_tokens):
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['chatgpt']['api_key']

    openai.api_key = api_key

    completion = openai.Completion.create(
        engine= "text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5
    )
    return completion.choices[0].text