from PIL import Image
from socket import gethostname, gethostbyname

def get_image_extenstion(image):    
    image = Image.open(image)
    return image.format.lower()


def get_local_ip_address():
    """
    Returns the local IP address of the machine, not the global IP address.
    
    The local IP address is the address assigned to the machine within a local network
    (typically something like 192.168.x.x or 10.x.x.x), as opposed to the global IP 
    address used for internet communication. This method uses the `socket` library to 
    obtain the local IP address of the machine running the code.
    """
    return gethostbyname(gethostname())
