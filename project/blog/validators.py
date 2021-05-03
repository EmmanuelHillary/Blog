import os
import magic
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


def validate_file_type(upload):
    # Make uploaded file accessible for analysis by saving in tmp
    tmp_path = f'tmp/{upload.name[2:]}'
    # print(tmp_path)
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
    # Get MIME type of file using python-magic and then delete
    file_type = magic.from_file(full_tmp_path, mime=True)
    default_storage.delete(tmp_path)
    # print(file_type)
    # Raise validation error if uploaded file is not an acceptable form of media
    if file_type not in settings.IMAGE_TYPES and file_type not in settings.VIDEO_TYPES:
        raise ValidationError('File type not supported. JPEG, PNG, or MP4 recommended.')


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.mp4', '.mpg', '.mov', '.ogg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


"""
['.jpg', '.jpeg', '.png', '.gif']
['.mp4', '.mpeg', '.webm', '.mpg', '.ogg']
"""