import base64
from io import BytesIO
from PIL import Image

# 2714 × 1720

from card_generator.utils import dummy_data

# Open an Image


def generate_nid_back(dvl=dummy_data["documents"]["DVL"]):
    dvl_back_blank_card = Image.open("card_generator/blank_cards/dvl_back_blank.png")
    buffered = BytesIO()
    dvl_back_blank_card.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str
