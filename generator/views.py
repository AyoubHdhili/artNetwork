from django.shortcuts import render
import requests
import base64
from PIL import Image
import io# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image"
headers = {"Authorization": "Bearer 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 "}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status Code:", response.status_code)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    return response.content  # Return the binary content directly

def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        style = request.POST.get('style')  # Get the selected style from the form
        if prompt and style:
            try:
                # Send the prompt and style to the API
                image_bytes = query({"inputs": prompt, "style": style})  # Adjust this line as per API requirements
                # Open the image
                image = Image.open(io.BytesIO(image_bytes))
                # Convert the image to a format that can be rendered in the template
                img_io = io.BytesIO()
                image.save(img_io, 'PNG')
                img_io.seek(0)
                image_data = base64.b64encode(img_io.read()).decode('utf-8')
                
                # Render the result template with the image
                return render(request, 'generate/result.html', {
                    'prompt': prompt,
                    'style': style,
                    'image_data': image_data,
                })
            except Exception as e:
                return render(request, 'generate/generate_image.html', {
                    'error': str(e),
                })
    return render(request, 'generate/generate_image.html')
