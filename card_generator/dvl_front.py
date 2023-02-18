import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import datetime
import nepali_datetime

# 2714 × 1720

from card_generator.utils import dummy_data

# Open an Image
dvl_front_blank_card = Image.open("card_generator/blank_cards/dvl_front_blank.png")

times_new_roman_regular_50 = ImageFont.truetype(
    "card_generator/fonts/TimesNewRoman-Regular.ttf", 50
)
times_new_roman_bold_50 = ImageFont.truetype(
    "card_generator/fonts/TimesNewRoman-Bold.ttf", 50
)
calibre_regular_70 = ImageFont.truetype("card_generator/fonts/Calibre-Regular.otf", 70)

devanagari_regular_65 = ImageFont.truetype(
    "card_generator/fonts/AdobeDevanagari-Regular.otf", 65
)
devanagari_bold_65 = ImageFont.truetype(
    "card_generator/fonts/AdobeDevanagari-Bold.otf", 65
)


def generate_dvl_front(dvl=dummy_data["documents"]["DVL"]):

    # im = Image.open(BytesIO(base64.b64decode(ctz["face_image"])))

    # face_image_data = re.sub("^data:image/.+;base64,", "", dvl["face_image"])
    face_image = Image.open(BytesIO(base64.b64decode(dvl["face_image"])))
    face_image = face_image.resize((500, 500))
    # I1.paste(face_image, (50, 50))
    # dvl_card_front.paste(face_image, (2070, 100))
    dvl_front_blank_card.paste(face_image, (2070, 415))
    I1 = ImageDraw.Draw(dvl_front_blank_card)

    # dvl_dln
    dln = dvl["DVL_DLN"]

    I1.text(
        (155, 390),
        f"D.L.No: {dln}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )
    # blood group
    blood_group = dvl["DVL_blood_group"]

    I1.text(
        (155, 470),
        f"B.G.: {blood_group}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # doi
    doi = datetime.datetime.strptime(dvl["DVL_date_of_issue"], "%Y-%m-%dT%H:%M:%S.%f%z")

    I1.text(
        (155, 1115),
        f"D.O.I.: {doi.strftime('%d-%m-%Y')}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )
    # doe
    doe = datetime.datetime.strptime(
        dvl["DVL_date_of_expiry"], "%Y-%m-%dT%H:%M:%S.%f%z"
    )

    I1.text(
        (155, 1195),
        f"D.O.E.: {doe.strftime('%d-%m-%Y')}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # name
    name = dvl["first_name"]
    if dvl["middle_name"]:
        name += " " + dvl["middle_name"]
    name += " " + dvl["last_name"]
    I1.text(
        (995, 550),
        f"Name: {name}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # permanent_municipality - ward
    permanent_municipality = dvl["permanent_municipality"]
    permanent_ward = dvl["permanent_ward"]
    I1.text(
        (995, 635),
        f"Address: {permanent_municipality} - {permanent_ward}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # permanent_district,state
    permanent_district = dvl["permanent_district"]
    permanent_state = dvl["permanent_state"]
    I1.text(
        (1245, 695),
        f"{permanent_district}, {permanent_state}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )
    # Nepal
    I1.text(
        (1245, 755),
        "Nepal",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # dob
    dob = datetime.datetime.strptime(dvl["dob"], "%Y-%m-%dT%H:%M:%S.%f%z")

    I1.text(
        (995, 835),
        f"D.O.B.: {dob.strftime('%d-%m-%Y')}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # f/h name
    father_name = dvl["father_first_name"]
    if dvl["father_middle_name"]:
        father_name += " " + dvl["father_middle_name"]
    father_name += " " + dvl["father_last_name"]
    I1.text(
        (995, 915),
        f"F/H Name: {father_name}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # f/h name
    nin = dvl["NIN"]
    I1.text(
        (995, 995),
        f"National Identity No.: {nin}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # contact number
    mobile_number = dvl["mobile_number"]
    I1.text(
        (995, 1075),
        f"Contact No.: {mobile_number[4:]}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # categories
    categories = dvl["DVL_categories"]
    I1.text(
        (2090, 1100),
        f"Category: {', '.join(categories)}",
        fill=(0, 0, 0),
        font=calibre_regular_70,
    )

    # Display edited image
    # img.show()
    # dvl_front_blank_card.show()

    # Save the edited image
    # dvl_front_blank_card.save("dummy_ctz.png")

    # return dvl_front_blank_card
    buffered = BytesIO()
    dvl_front_blank_card.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str
