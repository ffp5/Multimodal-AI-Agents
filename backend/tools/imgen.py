from backend.tools.base_tool import BaseTool, ToolParameter, ParameterType
from typing import List, Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ImageGeneratorTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="image_generator",
            description="Generates images using DALL-E 3 based on text descriptions"
        )
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def _define_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="prompt",
                param_type=ParameterType.STRING,
                description="Text description of the image to generate",
                required=True
            ),
            ToolParameter(
                name="size",
                param_type=ParameterType.STRING,
                description="Image size (1024x1024, 256x256, or 512x512)",
                required=False,
                default="256x256"
            ),
            ToolParameter(
                name="quality",
                param_type=ParameterType.STRING,
                description="Image quality (standard or hd)",
                required=False,
                default="standard"
            ),
            ToolParameter(
                name="n",
                param_type=ParameterType.INTEGER,
                description="Number of images to generate (1-10)",
                required=False,
                default=1
            )
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            prompt = kwargs["prompt"]
            size = kwargs.get("size", "256x256")
            quality = kwargs.get("quality", "standard")
            n = min(max(1, kwargs.get("n", 1)), 10)  # Ensure n is between 1 and 10

            # Validate size parameter
            valid_sizes = ["1024x1024", "512x512", "256x256"]
            if size not in valid_sizes:
                return {"error": f"Invalid size. Must be one of: {', '.join(valid_sizes)}"}

            # Validate quality parameter
            if quality not in ["standard", "hd"]:
                return {"error": "Invalid quality. Must be 'standard' or 'hd'"}

            response = self.client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size=size,
                quality=quality,
                n=n,
            )

            # Format the response
            generated_images = [
                {
                    "url": image.url,
                    "revised_prompt": image.revised_prompt if hasattr(image, 'revised_prompt') else None
                }
                for image in response.data
            ]

            return {
                "result": f"Generated {len(generated_images)} image(s)",
                "images_url": generated_images.pop()["url"] if n == 1 else [img["url"] for img in generated_images]
            }

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    # Create an instance of the ImageGeneratorTool
    img_tool = ImageGeneratorTool()

    # Test parameters
    params = {
        "prompt": "a white siamese cat sitting in a garden with butterflies",
        "size": "256x256",
        "quality": "standard",
        "n": 1
    }

    # Call the execute method with the parameters
    result = img_tool.execute(**params)

    # Print the result
    print(result)


