from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from typing import List, Dict, Any
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import base64
import uuid
from pathlib import Path

load_dotenv()

class ImageGeneratorTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="image_generator",
            description="Generates images using Google's Imagen model"
        )
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        # Create images directory if it doesn't exist
        self.images_dir = Path(__file__).parent.parent.parent / "images"
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="prompt",
                param_type=ParameterType.STRING,
                description="Text description of the image to generate",
                required=True
            ),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            prompt = kwargs["prompt"]

            response = self.client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                )
            )

            # Generate unique filename and save image
            filename = f"{uuid.uuid4()}.png"
            image_path = self.images_dir / filename
            
            # Save the generated image
            generated_image = response.generated_images[0]
            image = Image.open(BytesIO(generated_image.image.image_bytes))
            image.save(image_path)

            # Get relative path from project root
            relative_path = f"images/{filename}"

            return {
                "result": "Generated 1 image",
                "image_path": relative_path
            }

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    # Create an instance of the ImageGeneratorTool
    img_tool = ImageGeneratorTool()

    # Test parameters
    params = {
        "prompt": "Fuzzy bunnies in my kitchen"
    }

    # Call the execute method with the parameters
    result = img_tool.execute(**params)
    print(result)

    # Print the result (excluding the base64 data for brevity)

