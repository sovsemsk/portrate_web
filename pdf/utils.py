import io

import pymupdf
import qrcode
from django.conf import settings
from django.utils.text import Truncator

pymupdf.TOOLS.set_aa_level(0)


def make_qrcode(company_id, theme):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=50, border=0)
    qr.add_data(f"https://geo.portrate.io/@{company_id}?utm_source=QR")
    qr.make(fit=True)

    if theme == "light":
        img = qr.make_image(fill_color="black", back_color="transparent")
    else:
        img = qr.make_image(fill_color="white", back_color="transparent")

    stream = io.BytesIO()
    img.save(stream, "PNG")
    return stream


def make_stick(company, theme):
    png_stream = make_qrcode(company.id, theme)
    template = pymupdf.open(f"{settings.BASE_DIR}/pdf/stick-{theme}.pdf")

    for page in template:
        page.insert_image(pymupdf.Rect(30, 150, 150, 270), stream=png_stream)

        font = pymupdf.Font(fontfile=f"{settings.BASE_DIR}/pdf/Roboto-Regular.ttf")
        page.insert_font(fontname="roboto", fontbuffer=font.buffer)

        if theme == "light":
            color = pymupdf.pdfcolor["black"]
        else:
            color = pymupdf.pdfcolor["white"]

        page.insert_textbox(
            pymupdf.Rect(30, 300, 260, 315),
            Truncator(company.name).chars(50),
            color=color,
            encoding=pymupdf.TEXT_ENCODING_CYRILLIC,
            fontname="roboto",
            fontsize=10,
            stroke_opacity=0
        )

        if company.address:
            page.insert_textbox(
                pymupdf.Rect(30, 315, 260, 385),
                Truncator(company.address).chars(130),
                color=pymupdf.pdfcolor["gray50"],
                encoding=pymupdf.TEXT_ENCODING_CYRILLIC,
                fontname="roboto",
                fontsize=10,
                lineheight=1.6,
                stroke_opacity=0
            )

    pdf_stream = io.BytesIO()
    template.save(pdf_stream, deflate=True, garbage=3)
    return pdf_stream


def make_card(company, theme):
    png_stream = make_qrcode(company.id, theme)
    template = pymupdf.open(f"{settings.BASE_DIR}/pdf/card-{theme}.pdf")

    for page in template:
        page.insert_image(pymupdf.Rect(20, 20, 90, 90), stream=png_stream)

        font = pymupdf.Font(fontfile=f"{settings.BASE_DIR}/pdf/Roboto-Regular.ttf")
        page.insert_font(fontname="roboto", fontbuffer=font.buffer)

        if theme == "light":
            color = pymupdf.pdfcolor["black"]
        else:
            color = pymupdf.pdfcolor["white"]

        page.insert_textbox(
            pymupdf.Rect(100, 66, 240, 81),
            Truncator(company.name).chars(30),
            color=color,
            encoding=pymupdf.TEXT_ENCODING_CYRILLIC,
            fontname="roboto",
            fontsize=10,
            stroke_opacity=0,

        )

        if company.address:
            page.insert_textbox(
                pymupdf.Rect(100, 81, 240, 126),
                Truncator(company.address).chars(130),
                color=pymupdf.pdfcolor["gray50"],
                encoding=pymupdf.TEXT_ENCODING_CYRILLIC,
                fontname="roboto",
                fontsize=8,
                lineheight=1.5,
                stroke_opacity=0
            )

    pdf_stream = io.BytesIO()
    template.save(pdf_stream, deflate=True, garbage=3)
    return pdf_stream


def make_qr(company, theme):
    png_stream = make_qrcode(company.id, theme)
    template = pymupdf.open(f"{settings.BASE_DIR}/pdf/qr-light.pdf")

    for page in template:
        page.insert_image(pymupdf.Rect(15, 15, 126, 126), stream=png_stream)

    pdf_stream = io.BytesIO()
    template.save(pdf_stream, deflate=True, garbage=3)
    return pdf_stream
