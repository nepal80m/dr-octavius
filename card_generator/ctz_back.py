import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import datetime
import nepali_datetime
import re

from card_generator.utils import dummy_data

# 2107 × 1388
# x3.45
ctz_back_blank_card = Image.open("card_generator/blank_cards/ctz_back_blank.png")

times_new_roman_regular_50 = ImageFont.truetype(
    "card_generator/fonts/TimesNewRoman-Regular.ttf", 50
)
times_new_roman_font_bold_50 = ImageFont.truetype(
    "card_generator/fonts/TimesNewRoman-Bold.ttf", 50
)
devanagari_regular_65 = ImageFont.truetype(
    "card_generator/fonts/AdobeDevanagari-Regular.otf", 65
)
devanagari_bold_65 = ImageFont.truetype(
    "card_generator/fonts/AdobeDevanagari-Bold.otf", 65
)


def generate_ctz_back(ctz=dummy_data["documents"]["CTZ"]):
    pass

    # ctz = dummy_data["documents"]["CTZ"]

    I1 = ImageDraw.Draw(ctz_back_blank_card)

    # CCN
    CCN = ctz["CTZ_CCN"]

    I1.text(
        (785, 175),
        CCN,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )

    # gender
    gender = ctz["gender"]
    I1.text(
        (1725, 175),
        gender,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )

    # name
    nam_thar = ctz["first_name"]
    if ctz["middle_name"]:
        nam_thar += " " + ctz["middle_name"]
    nam_thar += " " + ctz["last_name"]
    I1.text(
        (785, 242),
        nam_thar,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )

    dob = datetime.datetime.strptime(ctz["dob"], "%Y-%m-%dT%H:%M:%S.%f%z")

    # dob_year
    dob_year = dob.strftime("%Y")
    I1.text(
        (920, 338),
        dob_year,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )
    # dob_month
    dob_month = dob.strftime("%b").upper()
    I1.text(
        (1320, 338),
        dob_month,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )
    # dob_day
    dob_day = dob.strftime("%d")
    I1.text(
        (1730, 338),
        dob_day,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )

    # birth_district
    birth_district = ctz["birth_district"]
    I1.text(
        (980, 412),
        birth_district,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )
    # birth_municipality
    birth_municipality = ctz["birth_municipality"]
    I1.text(
        (1095, 488),
        birth_municipality,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )
    # birth_ward
    birth_ward = ctz["birth_ward"]

    I1.text(
        (1840, 495),
        birth_ward,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )

    # permanent_district
    permanent_district = ctz["permanent_district"]
    I1.text(
        (980, 575),
        permanent_district,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )
    # permanent_municipality
    permanent_municipality = ctz["permanent_municipality"]
    I1.text(
        (1095, 650),
        permanent_municipality,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )
    # permanent_ward
    permanent_ward = ctz["permanent_ward"]

    I1.text(
        (1840, 650),
        permanent_ward,
        fill=(0, 0, 0),
        font=times_new_roman_regular_50,
    )

    # citizenship type
    ctz_type = ctz["CTZ_citizenship_type_devanagari"]
    I1.text(
        (435, 893),
        ctz_type,
        fill=(0, 0, 0),
        font=devanagari_regular_65,
    )

    # issuer name
    issuer_designation = ctz["CTZ_issuer_name_devanagari"]
    I1.text(
        (1505, 992),
        issuer_designation,
        fill=(0, 0, 0),
        font=devanagari_regular_65,
    )

    # issuer designation
    issuer_designation = ctz["CTZ_issuer_designation_devanagari"]
    I1.text(
        (1450, 1055),
        issuer_designation,
        fill=(0, 0, 0),
        font=devanagari_regular_65,
    )

    # date of issue
    date_of_issue = datetime.datetime.strptime(ctz["dob"], "%Y-%m-%dT%H:%M:%S.%f%z")
    date_of_issue_bs = nepali_datetime.datetime.from_datetime_datetime(date_of_issue)

    I1.text(
        (1545, 1120),
        date_of_issue_bs.strftime("%K-%n-%D"),
        fill=(0, 0, 0),
        font=devanagari_regular_65,
    )

    from io import BytesIO

    buffered = BytesIO()
    ctz_back_blank_card.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str
    # Display edited image
    # ctz_back_blank_card.show()

    # Save the edited image
    # ctz_card_back.save("dummy_ctz.png")

    # return ctz_back_blank_card


# generate_ctz_back()