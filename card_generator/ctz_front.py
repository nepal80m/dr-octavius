import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import datetime
import nepali_datetime
from card_generator.utils import dummy_data, replace_with_nepali_numbers

# 3075 × 2006
# x5


# Call draw Method to add 2D graphics in an image
def generate_ctz_front(ctz=dummy_data["documents"]["CTZ"]):
    # Open an Image
    ctz_front_blank_card = Image.open("card_generator/blank_cards/ctz_front_blank.png")

    devanagari_regular_90 = ImageFont.truetype(
        "card_generator/fonts/AdobeDevanagari-Regular.otf", 90
    )
    devanagari_bold_90 = ImageFont.truetype(
        "card_generator/fonts/AdobeDevanagari-Bold.otf", 90
    )

    # ctz = dummy_data["documents"]["CTZ"]

    # im = Image.open(BytesIO(base64.b64decode(ctz["face_image"])))

    # face_image_data = re.sub("^data:image/.+;base64,", "", ctz["face_image"])
    face_image = Image.open(BytesIO(base64.b64decode(ctz["face_image"])))
    face_image = face_image.resize((500, 500))
    # I1.paste(face_image, (50, 50))
    ctz_front_blank_card.paste(face_image, (215, 725))
    I1 = ImageDraw.Draw(ctz_front_blank_card)

    # Issued District
    issued_district = ctz["CTZ_issued_district_devanagari"]

    I1.text(
        (1750, 305),
        issued_district,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # CCN
    CCN_dev = replace_with_nepali_numbers(ctz["CTZ_CCN"])
    I1.text(
        (495, 585),
        CCN_dev,
        fill=(0, 0, 0),
        font=devanagari_bold_90,
    )

    # name
    nam_thar = ctz["first_name_devanagari"]
    if ctz["middle_name_devanagari"]:
        nam_thar += " " + ctz["middle_name_devanagari"]
    nam_thar += " " + ctz["last_name_devanagari"]
    I1.text(
        (1355, 680),
        nam_thar,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # linga
    gender = ctz["gender"]
    if gender.lower() == "male":
        linga = "पुरुष"
    elif gender.lower() == "female":
        linga = "महिला"
    else:
        linga = "अन्य"
    I1.text(
        (2365, 680),
        linga,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # birth_district
    birth_district_dev = ctz["birth_district_devanagari"]
    I1.text(
        (1565, 775),
        birth_district_dev,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )
    # birth_municipality
    birth_municipality_dev = ctz["birth_municipality_devanagari"]
    I1.text(
        (1605, 875),
        birth_municipality_dev,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )
    # birth_ward
    birth_ward_dev = replace_with_nepali_numbers(str(ctz["birth_ward_number"]))
    I1.text(
        (2405, 880),
        birth_ward_dev,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # permanent_district
    permanent_district_dev = ctz["permanent_district_devanagari"]
    I1.text(
        (1570, 980),
        permanent_district_dev,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )
    # permanent_municipality
    permanent_municipality_dev = ctz["permanent_municipality_devanagari"]
    I1.text(
        (1615, 1078),
        permanent_municipality_dev,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )
    # permanent_ward
    permanent_ward_dev = replace_with_nepali_numbers(str(ctz["permanent_ward_number"]))
    I1.text(
        (2405, 1070),
        permanent_ward_dev,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    dob = datetime.date.fromisoformat(ctz["date_of_birth"])
    dob_bs = nepali_datetime.date.from_datetime_date(dob)
    print(dob_bs)

    # dob_year
    dob_year = dob_bs.strftime("%K")
    I1.text(
        (1515, 1185),
        dob_year,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )
    # dob_month
    dob_month = dob_bs.strftime("%n")
    I1.text(
        (2025, 1185),
        dob_month,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )
    # dob_day
    dob_day = dob_bs.strftime("%D")
    I1.text(
        (2370, 1190),
        dob_day,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # father name
    father_name = ctz["father_first_name_devanagari"]
    if ctz["father_middle_name_devanagari"]:
        father_name += " " + ctz["father_middle_name_devanagari"]
    father_name += " " + ctz["father_last_name_devanagari"]
    I1.text(
        (1365, 1340),
        father_name,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # father CCN

    father_CCN = replace_with_nepali_numbers(ctz["CTZ_father_CCN"])
    I1.text(
        (2525, 1345),
        father_CCN,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )
    # father address

    father_address = ctz["CTZ_father_address_devanagari"]
    I1.text(
        (1365, 1445),
        father_address,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # father citizenship type
    father_ctz_type = ctz["CTZ_father_citizenship_type_devanagari"]
    I1.text(
        (2780, 1450),
        father_ctz_type,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # mother name
    mother_name = ctz["mother_first_name_devanagari"]
    if ctz["mother_middle_name_devanagari"]:
        mother_name += " " + ctz["mother_middle_name_devanagari"]
    mother_name += " " + ctz["mother_last_name_devanagari"]
    I1.text(
        (1365, 1550),
        mother_name,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # mother CCN

    mother_CCN = replace_with_nepali_numbers(ctz["CTZ_mother_CCN"])
    I1.text(
        (2525, 1555),
        mother_CCN,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )
    # mother address

    mother_address = ctz["CTZ_mother_address_devanagari"]
    I1.text(
        (1365, 1655),
        mother_address,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # mother citizenship type
    mother_ctz_type = ctz["CTZ_mother_citizenship_type_devanagari"]
    I1.text(
        (2780, 1655),
        mother_ctz_type,
        fill=(0, 0, 0),
        font=devanagari_regular_90,
    )

    # Display edited image
    # ctz_front_blank_card.show()

    # Save the edited image
    # ctz_front_blank_card.save("dummy_ctz.png")

    # return ctz_front_blank_card

    buffered = BytesIO()
    ctz_front_blank_card.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str
