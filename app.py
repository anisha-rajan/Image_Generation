import gradio as gr
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image

# Set up Google GenAI API Key (Replace with your actual API key)
genai.configure(api_key="AIzaSyD1zUY1srmMIYmE_6NfjmIzb6yYpbcIDCk")  

def image_to_tamil_poem(image):
    """Generates a Tamil poem about an upload image using Gemini 1.5 Pro"""

    try:
        # Convert image to bytes
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        
        # Convert image to Base64 for Gemini API
        image_b64 = base64.b64encode(img_bytes).decode('utf-8')
        prompt = "Describe this image in one sentence."

        # Use Gemini 1.5 Pro for image analysis
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([{"mime_type": "image/png", "data": image_b64}, prompt])
        description = response.text if response else "No description available."

        # Generate Tamil poem based on the description
        response_poem = model.generate_content(f"Based on this image description: {description}, write a short poem in Tamil.")
        tamil_poem = response_poem.text if response_poem else "கவிதை உருவாக்கப்படவில்லை."

        return tamil_poem

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Define Gradio Interface
interface = gr.Interface(
    fn=image_to_tamil_poem,
    inputs=gr.Image(type="pil"),
    outputs=gr.Textbox(label="Generated Tamil Poem"),
    title="AI-Powered Tamil Poem Generator (Using Gemini AI)",
    description="Upload an image, and AI will generate a short Tamil poem based on it."
)

if __name__ == "__main__":
    interface.launch()
