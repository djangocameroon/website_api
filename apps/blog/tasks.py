from celery import shared_task
from apps.blog.models.image import Image

@shared_task
def handle_image_upload(image_id):
    image = Image.objects.get(id=image_id)
    
