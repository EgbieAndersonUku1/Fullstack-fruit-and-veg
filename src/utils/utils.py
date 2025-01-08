from PIL import Image


def get_image_extenstion(image):    
    image = Image.open(image)
    return image.format.lower()
