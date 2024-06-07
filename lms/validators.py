from rest_framework.serializers import ValidationError

url_youtube = "http://youtube.com"


def validate_youtube_url(value):
    if url_youtube not in value.lover():
        raise ValidationError("Необходимо присутствие ссылки на youtube.")
