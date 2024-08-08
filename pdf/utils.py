import io

import pymupdf
import qrcode
from django.conf import settings

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

        font = pymupdf.Font(fontfile=f"{settings.BASE_DIR}/pdf/sf_pro.ttf")
        page.insert_font(fontname="sf_pro", fontbuffer=font.buffer)

        if theme == "light":
            color_name = pymupdf.pdfcolor["black"]
        else:
            color_name = pymupdf.pdfcolor["white"]

        page.insert_textbox(
            pymupdf.Rect(30, 280, 270, 305),
            company.name,
            color=color_name,
            encoding=pymupdf.TEXT_ENCODING_CYRILLIC,
            fontname="sf_pro",
            fontsize=14,
            stroke_opacity=0,

        )

        if company.address:
            page.insert_textbox(
                pymupdf.Rect(30, 300, 270, 390),
                company.address,
                color=pymupdf.pdfcolor["gray50"],
                encoding=pymupdf.TEXT_ENCODING_CYRILLIC,
                fontname="sf_pro",
                fontsize=11,
                stroke_opacity=0
            )

    pdf_stream = io.BytesIO()
    template.save(pdf_stream, deflate=True, garbage=3)
    return pdf_stream


def make_card(company, theme):
    png_stream = make_qrcode(company.id, theme)
    template = pymupdf.open(f"{settings.BASE_DIR}/pdf/card-{theme}.pdf")

    for page in template:
        rect = pymupdf.Rect(20, 20, 90, 90)
        page.insert_image(rect, stream=png_stream)

    pdf_stream = io.BytesIO()
    template.save(pdf_stream, deflate=True, garbage=3)
    return pdf_stream
