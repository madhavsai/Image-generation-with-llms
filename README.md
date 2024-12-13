# LLM Prompt Expansion Application

This repository contains an application that leverages Ollama and the LLaMA 3.1 8 billion model to expand user-given prompts with additional details such as camera settings, scene settings, lighting, and other aspects. The backend API services are implemented using Flask.

## Features
- **Ollama and LLaMA 3.1 Model**: Utilizes Ollama and the LLaMA 3.1 8 billion model for prompt expansion.
- **Backend API**: Built using Flask for handling prompt expansion requests.

## Getting Started

### Prerequisites
- Python 3.7 or higher.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/LLM-prompt-expansion.git
   cd LLM-prompt-expansion
Install the required packages:

bash
pip install -r requirements.txt
Run the Flask application:

bash
python app.py
Usage
Start the Flask API: The application runs on http://localhost:5000. You can send POST requests to the /expand-prompt endpoint with the necessary parameters to expand prompts.

Example Requests:

Expand Prompt:

bash
curl -X POST http://localhost:5000/expand-prompt -d '{"prompt": "A sunset on the beach"}' -H "Content-Type: application/json"

Converse with LLM:

bash
curl -X POST http://localhost:5000/converse -d '{"prompt": "Can you help with graphic design?", "history": []}' -H "Content-Type: application/json"
Generate Prompt:

bash
curl -X POST http://localhost:5000/generate_image -d '{"promptType": "guided", "category": "product", "aspectRatio": "(16:9)", "promptGuided": {"description": "A sunset on the beach", "explaination": "vivid colors", "additionalInfo": "high resolution"}}' -H "Content-Type: application/json"
API Endpoints
GET /:

Description: Serves the index page.

Response: Renders the index.html template.

POST /pull_model:

Description: Pulls the latest model version from Ollama.

Request Parameters: None.

Response: JSON containing the output and any errors from the pull operation.

POST /expand-prompt:

Description: Expands a user-given prompt with additional details.

Request Parameters:

prompt (string, required): The initial user-given prompt.

Response: JSON containing the expanded prompt with additional details.

POST /generate_image:

Description: Generates an image prompt based on the category and preferences.

Request Parameters:

promptType (string, required): The type of prompt (e.g., guided or freeform).

category (string, required): The category of the image (e.g., product, people, scene, background).

aspectRatio (string, required): The aspect ratio of the image.

promptGuided (dict, optional): Guided prompt details including description, explanation, and additionalInfo.

Response: JSON containing the generated image URL.

POST /converse:

Description: Handles conversation with the LLM.

Request Parameters:

prompt (string, required): The user input.

history (list, optional): The conversation history.

Response: JSON containing the LLM response and updated conversation history.

POST /generate_image_2:

Description: Generates an image prompt based on the category.

Request Parameters:

category (string, required): The category of the image (e.g., product, people, scene, background).

prompt (string, required): The initial user-given prompt.

Response: JSON containing the generated image URL.

Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
