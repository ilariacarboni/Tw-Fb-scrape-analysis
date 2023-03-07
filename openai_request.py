import openai
import configparser
import requests
import os
from edited_image import edit_image

def authenticate():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['chatgpt']['api_key']
    openai.api_key = api_key

def get_openai_response(prompt,max_tokens):
    
    authenticate()
    completion = openai.Completion.create(
        engine= "text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5
    )
    return completion.choices[0].text

def get_dalle_response(image_path):

    authenticate()
    png_data = edit_image(image_path)

    response = openai.Image.create_variation(
    image=png_data,
    n=3,
    size="512x512"
    )
    if not os.path.exists("dalle_images"):
        os.mkdir("dalle_images")

    for i, image in enumerate(response['data']):
        image_url = image['url']
        image_data = requests.get(image_url).content

        with open(f"dalle_images/image_{i+1}.png", "wb") as f:
            f.write(image_data)


