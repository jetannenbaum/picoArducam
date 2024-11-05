from PIL import Image

def color565(red, green=0, blue=0):
    """
    Convert red, green and blue values (0-255) into a 16-bit 565 encoding.
    """
    if isinstance(red, (tuple, list)):
        red, green, blue = red[:3]
    return (red & 0xF8) << 8 | (green & 0xFC) << 3 | blue >> 3

def convert_jpeg_to_pixels(image_path):
    """Converts a JPEG image to a list of pixel values."""

    # Open the image
    image = Image.open(image_path)

    # Get the pixel values
    pixels = list(image.getdata())

    return pixels

# Example usage
pixels = convert_jpeg_to_pixels("C:/Esperanza/esperanzaSTEM/image.jpg")

print(len(pixels))

myFormat = "{:>5}"
f = open("C:/Esperanza/esperanzaSTEM/image.txt", "w")
for color in pixels:
    f.write(myFormat.format(color565(color[0], color[1], color[2])))
f.close()
