from rest_framework.serializers import ValidationError

url_youtube = "youtube"


def validate_youtube_url(value):
    """ Проверка того, что в url присутствует слово youtube"""
    if url_youtube not in value.lower():
        raise ValidationError("Необходимо присутствие ссылки на youtube.")
