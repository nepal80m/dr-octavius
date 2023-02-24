import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import datetime
import nepali_datetime
import re

# 831 × 533
# x1.54
from card_generator.utils import dummy_data, replace_with_nepali_numbers

# Open an Image
nid_front_blank_card = Image.open("card_generator/blank_cards/nid_front_blank.png")

calibre_regular_20 = ImageFont.truetype("card_generator/fonts/Calibre-Regular.otf", 20)
calibre_medium_20 = ImageFont.truetype("card_generator/fonts/Calibre-Medium.otf", 20)

devanagari_regular_24 = ImageFont.truetype(
    "card_generator/fonts/AdobeDevanagari-Regular.otf", 24
)
devanagari_bold_24 = ImageFont.truetype(
    "card_generator/fonts/AdobeDevanagari-Bold.otf", 24
)


def generate_nid_front(nid=dummy_data["documents"]["NID"]):

    # nid = dummy_data["documents"]["NID"]

    # face_image_data = re.sub("^data:image/.+;base64,", "", nid["face_image"])
    face_image = Image.open(BytesIO(base64.b64decode(nid["face_image"])))
    face_image_200 = face_image.resize((225, 225))
    face_image_50 = face_image.resize((75, 75))
    # I1.paste(face_image, (50, 50))
    nid_front_blank_card.paste(face_image_200, (570, 125))
    nid_front_blank_card.paste(face_image_50, (110, 410))
    I1 = ImageDraw.Draw(nid_front_blank_card)

    # Nationality

    nationality = nid["nationality"]
    I1.text(
        (30, 115),
        nationality,
        fill=(0, 0, 0),
        font=calibre_medium_20,
    )

    # Gender
    gender = nid["gender"][0]
    I1.text(
        (157, 115),
        gender,
        fill=(0, 0, 0),
        font=calibre_medium_20,
    )

    # Surname devenagari
    last_name = nid["last_name_devanagari"]
    I1.text(
        (232, 115),
        last_name,
        fill=(0, 0, 0),
        font=devanagari_bold_24,
    )
    # Surname
    last_name = nid["last_name"]
    I1.text(
        (232, 145),
        last_name,
        fill=(0, 0, 0),
        font=calibre_medium_20,
    )

    # given name devangari
    name_devanagari = nid["first_name_devanagari"]
    if nid["middle_name_devanagari"]:
        name_devanagari += " " + nid["middle_name_devanagari"]
    I1.text(
        (232, 222),
        name_devanagari,
        fill=(0, 0, 0),
        font=devanagari_bold_24,
    )
    # given name
    name = nid["first_name"]
    if nid["middle_name"]:
        name += " " + nid["middle_name"]
    I1.text(
        (232, 252),
        name,
        fill=(0, 0, 0),
        font=calibre_medium_20,
    )

    dob = datetime.date.fromisoformat(nid["dob"])
    dob_bs = nepali_datetime.date.from_datetime_date(dob)

    # dob nepali
    I1.text(
        (232, 325),
        dob_bs.strftime("%K-%n-%D"),
        fill=(0, 0, 0),
        font=devanagari_bold_24,
    )
    # dob
    I1.text(
        (388, 330),
        dob.strftime("%Y-%m-%d"),
        fill=(0, 0, 0),
        font=calibre_medium_20,
    )

    # mother name
    mother_name = nid["mother_first_name_devanagari"]
    if nid["mother_middle_name_devanagari"]:
        mother_name += " " + nid["mother_middle_name_devanagari"]
    mother_name += " " + nid["mother_last_name_devanagari"]
    I1.text(
        (232, 388),
        mother_name,
        fill=(0, 0, 0),
        font=devanagari_bold_24,
    )

    # father name
    father_name = nid["father_first_name_devanagari"]
    if nid["father_middle_name_devanagari"]:
        father_name += " " + nid["father_middle_name_devanagari"]
    father_name += " " + nid["father_last_name_devanagari"]
    I1.text(
        (232, 432),
        father_name,
        fill=(0, 0, 0),
        font=devanagari_bold_24,
    )

    # Date of issue
    doi = datetime.date.fromisoformat(nid["NID_date_of_issue"])
    I1.text(
        (232, 480),
        doi.strftime("%d-%m-%Y"),
        fill=(0, 0, 0),
        font=calibre_medium_20,
    )

    # NIN devanagari
    nin_dev = replace_with_nepali_numbers(nid["NIN"])
    I1.text(
        (30, 325),
        nin_dev,
        fill=(0, 0, 0),
        font=devanagari_bold_24,
    )
    # NIN
    nin = nid["NIN"]
    I1.text(
        (30, 355),
        nin,
        fill=(0, 0, 0),
        font=calibre_medium_20,
    )

    # Display edited image
    # img.show()
    # nid_front_blank_card.show()

    # Save the edited image
    # nid_front_blank_card.save("dummy_ctz.png")

    # return nid_front_blank_card
    buffered = BytesIO()
    nid_front_blank_card.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str
