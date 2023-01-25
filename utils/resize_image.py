from PIL import Image
from pickletools import optimize
import os, sys
sys.path.append('api')
from settings import MEDIA_ROOT


def resize_image(name: str, new_width: float, new_heigth: float) -> None:
    img_full_path = os.path.join(MEDIA_ROOT, name)
    img_pil = Image.open(img_full_path)
    original_width, original_height = img_pil.size

    if original_width <= new_width:
        img_pil.close()
        return
    
    new_img = img_pil.resize((new_width, new_heigth), Image.LANCZOS)
    new_img.save(
        img_full_path,
        optimize=True,
        quality=100
    )