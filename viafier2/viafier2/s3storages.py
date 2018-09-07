from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    bucket_name = settings.STATICSTORAGE_BUCKET
    location = settings.STATIC_URL.lstrip('/')


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.MEDIASTORAGE_BUCKET
    location = settings.MEDIA_URL.lstrip('/')
