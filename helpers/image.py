import uuid
import base64
from PIL import Image
from datetime import datetime
from io import BytesIO
from django.core.files.base import ContentFile


def new_file_name(ext: str, storage_type: str='cart24'):
    storage_type = storage_type.lower()
    # return uuid.uuid4().hex + f".{storage_type}.{ext}"
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S%f")[:-3]
    return f"{uuid.uuid4().hex}_{formatted_datetime}.{storage_type}.{ext}"
def resize_image(img: Image.Image, size: tuple, _format='JPEG'):
    output = BytesIO()
    new_img = img.resize(size)
    new_img.save(output, format=_format)
    output.seek(0)
    return output.read()

def base64_to_image(base64_string, re_size=None):
    storage_type='s3'
    extentions = ['jpg', 'jpeg', 'png', 'gif']
    _format, imgstr=base64_string.split(";base64,")
    ext = _format.split("/")[-1]
    if ext in extentions:
        image_data = base64.b64decode(imgstr, validate=True)
        img = Image.open(BytesIO(image_data))
        _resize_image = resize_image(img,re_size,ext)
        return ContentFile(_resize_image, name=new_file_name(ext, storage_type))



