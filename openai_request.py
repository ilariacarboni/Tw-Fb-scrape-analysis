import openai
import configparser

def get_openai_response(prompt):
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['chatgpt']['api_key']

    openai.api_key = api_key
    model_engine = "text-davinci-003"

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt +"\n give me some insights for this data?",
        max_tokens=1412,
        n=1,
        stop=None,
        temperature=0.3
    )
    return completion.choices[0].text