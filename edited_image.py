from PIL import Image
import io

def edit_image(image_path):
    # Open the input image
    input_image = Image.open(image_path)

    width, height = input_image.size
    min_dim = min(width, height)

    # Crop the input image to a square with size equal to the minimum dimension
    crop_left = (width - min_dim) // 2
    crop_upper = (height - min_dim) // 2
    crop_right = crop_left + min_dim
    crop_lower = crop_upper + min_dim
    input_image = input_image.crop((crop_left, crop_upper, crop_right, crop_lower))

    # Resize the input image to the desired size
    output_size = (1024, 1024)
    output_image = input_image.resize(output_size)

    # Convert to PNG format
    png_image = io.BytesIO()
    output_image.save(png_image, format="PNG")
    png_bytes = png_image.getvalue()

    return png_bytes
