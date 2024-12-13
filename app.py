from flask import Flask, request, jsonify
import ollama
import requests
import json
import re
import subprocess

from flask_cors import CORS



app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes


@app.route('/pull_model', methods=['POST'])
def pull_model():
    try:
        result = subprocess.run(["ollama", "pull", "llama3.1:latest"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return jsonify({
            "output": result.stdout,
            "error": result.stderr
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": f"An error occurred: {e}"
        }), 



def preprocess_text(text):
    # Remove leading and trailing whitespace
    cleaned_text = text.strip()
    
    # Remove leading \n if it exists
    cleaned_text = re.sub(r'^\n', '', cleaned_text)
    
    # Remove leading and trailing quotation marks
    if cleaned_text.startswith('"') and cleaned_text.endswith('"'):
        cleaned_text = cleaned_text[1:-1]
    
    return cleaned_text

def product_prompt(input_prompt):
    prompt_template="you are an expert in the graphic design and photography industry for 10 years. and you help me creating the good prompts based on the things I am providing to you. you can improve the prompts for text to image models. so from next I will give you information about the image I want, you prepare the prompt. you should not do other than that. just give me the single prompt. Consider elements like camera angle, lighting, shot type, and the overall atmosphere to bring scenes to life.And you are creating the prompts for the product category.and dont tell things like Here's a prompt that or something and this is the things you are taking and genarate the prompt   "
    prompt = input_prompt
    response = ollama.generate(model='llama3.1:latest', prompt=prompt_template+prompt)
    print(response)
    return response['response']


def people_prompt(input_prompt):
    prompt_template="you are an expert in the graphic design industry for 10 years. and you help me creating the good prompts based on the things I am providing to you. you can improve the prompts for text to image models. so from next I will give you information about the image I want, you prepare the prompt. you should not do other than that. just give me the single prompt. Consider elements like camera angle, lighting, shot type, and the overall atmosphere to bring scenes to life.And you are creating the prompts for the e commerce, social media posts, graphic design. These can range from a closeup shot of a female mode to a group of people working in factory .and dont tell things like Here's a prompt that or something and this is the things you are taking and generate the prompt "
    prompt = input_prompt
    response = ollama.generate(model='llama3.1:latest', prompt=prompt_template+prompt)
    print(response)
    return response['response']


def scene_prompt(input_prompt):
    prompt_template="you are an expert in the graphic design industry for 10 years. and you help me creating the good prompts based on the things I am providing to you. you can improve the prompts for text to image models. so from next I will give you information about the image I want, you prepare the prompt. you should not do other than that. just give me the single prompt. Consider elements like camera angle, lighting, shot type, and the overall atmosphere to bring scenes to life.And you are creating the prompts for the e commerce, social media posts, graphic design. These can range from a simple coffee shop to a luxurious hotel balcony with beach view. and dont tell things like Here's a prompt that or something and this is the things you are taking and generate the prompt "
    prompt = input_prompt
    response = ollama.generate(model='llama3.1:latest', prompt=prompt_template+prompt)
    print(response)
    return response['response']


def background_prompt(input_prompt):
    prompt_template="you are an expert in the graphic design industry for 10 years. and you help me creating the good prompts based on the things I am providing to you. you can improve the prompts for text to image models. so from next I will give you information about the image I want, you prepare the prompt. you should not do other than that. just give me the single prompt. Consider elements like camera angle, lighting, shot type, and the overall atmosphere to bring scenes to life.And you are creating the prompts for the background images for e commerce, social media posts, graphic design.Do not include the subject or product the use mentions,you are createing backgrounds for those subjects or products.stick to creating seamless background images for different purposes defined by user. These can range from simple textures to complex scenes like a vintage-style café. and dont tell things like Here's a prompt that or something and this is the things you are taking and generate the prompt "
    prompt = input_prompt
    response = ollama.generate(model='llama3.1:latest', prompt=prompt_template+prompt)
    print(response)
    return response['response']

import requests
import json

def send_prompt(prompt, aspect_ratio):
    ip_address = request.host
    url = "http://stoic_shaw:5000/generate-image"  # Replace with the actual server URL
    headers = {"Content-Type": "application/json"}

    # Define a mapping of aspect ratios to width and height
    aspect_ratio_mapping = {
        "(4:3)": (1440, 1080),
        "(3:4)": (1080, 1440),
        "(1:1)": (1080, 1080),
        "(16:9)": (1920, 1080)
    }

    # Default to 4:3 (Landscape) if not found
    width, height = aspect_ratio_mapping.get(aspect_ratio, (1440, 1080))

    data = {
        "prompt": prompt,
        "width": width,
        "height": height
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json().get("image_urls")
    else:
        return None


# Function to handle LLM conversation
def converse_with_llm(conversation_history):
    prompt_template = ("You are an expert in the graphic design industry with 10 years of experience. "
                       "Help users generate images based on their requirements. Do not discuss anything outside "
                       "the context of design. If users ask about other topics, simply state that you cannot assist "
                       "with those and can only help with their design needs. Answer everything related to graphic "
                       "design, e-commerce advertisements, and any design-related topics.")
    conversation = "\n".join(conversation_history)
    full_prompt = f"{prompt_template}\n{conversation}\nYou:"
    response = ollama.generate(model='llama3.1:latest', prompt=full_prompt)
    return response['response']

# Endpoint to handle conversation
@app.route('/converse', methods=['POST'])
def converse():
    data = request.get_json()
    user_input = data.get('prompt', '')
    conversation_history = data.get('history', [])
    
    # Add user input to conversation history
    conversation_history.append(f"User: {user_input}")
    
    # Get response from LLM
    llm_response = converse_with_llm(conversation_history)
    
    # Add LLM response to conversation history
    conversation_history.append(f"LLM: {llm_response}")
    
    return jsonify({'response': llm_response, 'history': conversation_history})

@app.route('/generate_image_2', methods=['POST'])
def generate_promt_2():
    data = request.get_json()
    print(data)

    image_category = data.get('category')
    prompt = data.get('prompt', '')
    image_category = data.get('category')
    prompt = data.get('prompt', '')
    if image_category=="product":
        result_promt=product_prompt(prompt)
    elif image_category=="people":
        result_promt=people_prompt(prompt)
    elif image_category=="scene":
        result_promt=scene_prompt(prompt)
    elif image_category=="background":
        result_promt=background_prompt(prompt)
    result_promt=preprocess_text(result_promt)

    image_url=result_promt


    return jsonify({'image_url': image_url})

def update_urls(urls, host_ip):
    print(host_ip)
    print(urls)
    updated_urls = []
    host_ip=host_ip.split(":")[0]
    for url in urls:

        # Replace only the IP address, keep the port number and path intact
        url_parts = url.split("stoic_shaw")
        new_url = "http://"+f"{host_ip}{url_parts[1]}"
        updated_urls.append(new_url)
    return updated_urls

@app.route('/generate_image', methods=['POST'])
def generate_prompt():
    data = request.get_json()
    print(data)
    promptType = data.get('promptType', '')
    image_category = data.get('category', '')
    aspect_ratio = data.get('aspectRatio', '')

    if promptType == "guided":
        description = data['promptGuided'].get('description', '').strip()
        explanation = data['promptGuided'].get('explaination', '').strip()
        additional_info = data['promptGuided'].get('additionalInfo', '').strip()
        prompt = f"{description} with {explanation} background setting and {additional_info}".strip()
    else:
        prompt = data.get('prompt', '').strip()

    def create_complete_prompt(prompt, attributes):
        non_empty_attributes = {k: v for k, v in attributes.items() if v.strip()}
        complete_prompt = f"{prompt} with these preferences: " + ", ".join(
            [f"{k} is {v}" for k, v in non_empty_attributes.items()]
        )
        return complete_prompt if non_empty_attributes else prompt

    if image_category == "product":
        attributes = {
            'background': data['product'].get('background', ''),
            'cameraAngle': data['product'].get('cameraAngle', ''),
            'composition': data['product'].get('composition', ''),
            'lighting': data['product'].get('lighting', ''),
            'shotType': data['product'].get('shotType', ''),
            'style': data['product'].get('style', ''),
            'tone': data['product'].get('tone', '')
        }
        result_prompt = product_prompt(create_complete_prompt(prompt, attributes))
    elif image_category == "people":
        attributes = {
            'background': data['people'].get('background', ''),
            'cameraAngle': data['people'].get('cameraAngle', ''),
            'lighting': data['people'].get('lighting', ''),
            'mood': data['people'].get('mood', ''),
            'shotType': data['people'].get('shotType', ''),
            'style': data['people'].get('style', ''),
            'tone': data['people'].get('tone', '')
        }
        result_prompt = people_prompt(create_complete_prompt(prompt, attributes))
    elif image_category == "scene":
        attributes = {
            'atmosphere': data['scene'].get('atmosphere', ''),
            'cameraAngle': data['scene'].get('cameraAngle', ''),
            'composition': data['scene'].get('composition', ''),
            'lighting': data['scene'].get('lighting', ''),
            'location': data['scene'].get('location', ''),
            'shotType': data['scene'].get('shotType', ''),
            'style': data['scene'].get('style', ''),
            'tone': data['scene'].get('tone', '')
        }
        result_prompt = scene_prompt(create_complete_prompt(prompt, attributes))
    elif image_category == "background":
        attributes = {
            'style': data['background'].get('style', ''),
            'tone': data['background'].get('tone', ''),
            'type': data['background'].get('type', '')
        }
        result_prompt = background_prompt(create_complete_prompt(prompt, attributes))

    result_prompt = preprocess_text(result_prompt)
    print(result_prompt)

    ip_address = request.host
    result_images_urls=send_prompt(result_prompt,aspect_ratio)
    print(result_images_urls)
    result_images_urls= update_urls(result_images_urls, ip_address)
    return jsonify({'image_url': result_images_urls})


    #return jsonify({'image_url':  ["http://127.0.0.1:5001/static/image/20241025172108.png","http://127.0.0.1:5001/static/image/20241025172211.png","http://127.0.0.1:5001/static/image/20241025172451.png","http://127.0.0.1:5001/static/image/20241024130502.png"]})

    # for main_key, details in data.items():
    #     if main_key == 'product':
    #         background = details.get('background', '')
    #         camera_angle = details.get('cameraAngle', '')
    #         composition = details.get('composition', '')
    #         lighting = details.get('lighting', '')
    #         shot_type = details.get('shotType', '')
    #         style = details.get('style', '')
    #         tone = details.get('tone', '')
    #         prompt = details.get('prompt', '')

    #         #prompt = f"Create a product image with {background} background, {camera_angle} camera angle, {composition} composition, {lighting} lighting, {shot_type} shot type, {style} style, and {tone} tone."
    #         result_promt = preprocess_text(prompt)

    #     elif main_key == 'scene':
    #         atmosphere = details.get('atmosphere', '')
    #         camera_angle = details.get('cameraAngle', '')
    #         composition = details.get('composition', '')
    #         lighting = details.get('lighting', '')
    #         location = details.get('location', '')
    #         shot_type = details.get('shotType', '')
    #         style = details.get('style', '')
    #         tone = details.get('tone', '')
    #         prompt = details.get('prompt', '')

    #         #prompt = f"Create a scene image with {atmosphere} atmosphere, {camera_angle} camera angle, {composition} composition, {lighting} lighting, {location} location, {shot_type} shot type, {style} style, and {tone} tone."
    #         result_promt = preprocess_text(prompt)

    #     elif main_key == 'background':
    #         style = details.get('style', '')
    #         tone = details.get('tone', '')
    #         type_ = details.get('type', '')
    #         prompt = details.get('prompt', '')

    #         #prompt = f"Create a background image with {style} style, {tone} tone, and {type_} type."
    #         result_promt = preprocess_text(prompt)

    #     elif main_key == 'people':
    #         background = details.get('background', '')
    #         camera_angle = details.get('cameraAngle', '')
    #         lighting = details.get('lighting', '')
    #         mood = details.get('mood', '')
    #         shot_type = details.get('shotType', '')
    #         style = details.get('style', '')
    #         tone = details.get('tone', '')
    #         prompt = details.get('prompt', '')

    #         #prompt = f"Create a people image with {background} background, {camera_angle} camera angle, {lighting} lighting, {mood} mood, {shot_type} shot type, {style} style, and {tone} tone."
    #         result_promt = preprocess_text(prompt)
        

    #     image_url = send_prompt(result_promt)
    #     return jsonify({'image_url': ["http://127.0.0.1:5001/static/image/20241025172108.png","http://127.0.0.1:5001/static/image/20241025172211.png","http://127.0.0.1:5001/static/image/20241025172451.png","http://127.0.0.1:5001/static/image/20241024130502.png"]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
