from django.conf import settings

def get_media_url(media_file):
    """Construct the full S3 object URL for a media file."""
    return f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/content_images/{media_file.name}'
