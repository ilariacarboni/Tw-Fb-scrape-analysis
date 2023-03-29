from PIL import Image
import io

def edit_image(image_path):
    input_image = Image.open(image_path)

    width, height = input_image.size
    min_dim = min(width, height)

    #crop the input image to a square 
    crop_left = (width - min_dim) // 2
    crop_upper = (height - min_dim) // 2
    crop_right = crop_left + min_dim
    crop_lower = crop_upper + min_dim
    input_image = input_image.crop((crop_left, crop_upper, crop_right, crop_lower))

    #resize
    output_size = (1024, 1024)
    output_image = input_image.resize(output_size)

    #convert to PNG
    png_image = io.BytesIO()
    output_image.save(png_image, format="PNG")
    png_bytes = png_image.getvalue()

    return png_bytes
