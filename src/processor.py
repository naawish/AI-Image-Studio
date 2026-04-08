import io
from PIL import Image
from rembg import remove

def process_image(input_path, remove_bg=False, target_format="PNG"):
    img = Image.open(input_path)
    if remove_bg:
        img = remove(img)
    
    if target_format in ["JPEG", "JPG"] and img.mode == "RGBA":
        img = img.convert("RGB")
        
    output_buffer = io.BytesIO()
    img.save(output_buffer, format=target_format)
    return img, output_buffer.getvalue()