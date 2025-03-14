from django.conf import settings
import os, datetime, uuid
from django.core.exceptions import ValidationError
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    ip = ip.split(":")[0]
    return ip


def get_path_file(path):
    path_to_media = str(settings.MEDIA_ROOT)
    relative_path = path.replace('media/', '')
    return path_to_media + relative_path


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    result = os.path.join(instance._meta.app_label, instance.__class__.__name__, datetime.datetime.today().strftime("%Y/%m/%d"), f'{str(uuid.uuid4())}.{ext}')
    return result


def summernote_upload_to():
    result = os.path.join("summernote", datetime.datetime.today().strftime("%Y/%m/%d"))
    return result


def validate_audio_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.wav']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Không hỗ trợ định dạng này')


def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.mov', '.wmv', '.avi']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Không hỗ trợ định dạng này')


def validate_document_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.doc', '.docx', '.pdf', '.xls', '.xlsx', '.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Không hỗ trợ định dạng này')
    

def create_slug(text):
    if text is None:
        return ''
    regex = {
        'a' : ['à', 'á', 'ả', 'ã', 'ạ', 'â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ'],
        'd' : ['đ'],
        'e' : ['è', 'é', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ề', 'ế', 'ể', 'ễ', 'ệ'],
        'i' : ['ì', 'í', 'ỉ', 'ĩ', 'ị'],
        'o' : ['ò', 'ó', 'ỏ', 'õ', 'ọ', 'ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ'],
        'u' : ['ù', 'ú', 'ủ', 'ũ', 'ụ', 'ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự'],
        'y' : ['ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ'],
        '-' : ['(', ')', '-', '_', ':', ';', '"', "'", '!', '.', ',', '[', ']', '{', '}', '+', '=', '@', '#', '$', '%',
               '^', '&', '*', '|', '?', '~', '/', '`']
    }
    mapping = {char: key for key, chars in regex.items() for char in chars}
    text_after_regex = ''.join(mapping.get(char, char) for char in text.lower())
    return text_after_regex.replace(' ', '-')


def send_socket(type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'signals', {
            "type": type,
            "data": data
        }
    )