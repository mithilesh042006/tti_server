import json
import uuid
import logging
import base64
import os
from io import BytesIO
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from huggingface_hub import InferenceClient
from .models import GeneratedImage
import requests


# Setup logging
logger = logging.getLogger(__name__)

@csrf_exempt
def text_to_image(request):
    print("Received request for text-to-image generation")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            text = data.get("text")
            logger.info(f"Received text: {text}")

            if not text:
                return JsonResponse({"error": "Text is required"}, status=400)

            logger.info("Making request to Pollinations API")

            # Generate image
            url = f"https://pollinations.ai/p/{text}"
            response = requests.get(url)

            if response.ok:
                # Save the image locally
                image_bytes = response.content
                image = Image.open(BytesIO(image_bytes))

                # Save to model
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_bytes = buffered.getvalue()
                image_file = ContentFile(image_bytes, name=f"{uuid.uuid4()}.png")
                generated = GeneratedImage.objects.create(
                    prompt=text,
                    image=image_file
                )

                # Base64 for response (optional)
                img_str = base64.b64encode(image_bytes).decode("utf-8")
                logger.info("Successfully saved and returned generated image")

                return JsonResponse({
                    "image_data": img_str,
                    "image_url": generated.image.url,
                    "prompt": generated.prompt,
                    "created_at": generated.created_at.isoformat()
                })
            else:
                logger.error(f"Image generation failed: {response.status_code} - {response.text}")
                return JsonResponse({
                    "error": "Image generation failed",
                    "details": response.text
                }, status=response.status_code)

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            print(f"Exception during processing: {str(e)}")
            logger.error(f"Exception during processing: {str(e)}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)

# views.py
from django.http import JsonResponse
from .models import GeneratedImage

def image_history(request):
    images = GeneratedImage.objects.order_by('-created_at')[:20]
    image_list = [
        {
            "id": str(image.id),
            "prompt": image.prompt,
            "url": image.image.url,
            "created_at": image.created_at.isoformat()
        }
        for image in images
    ]
    return JsonResponse({"images": image_list})

