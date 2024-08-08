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
        rect = pymupdf.Rect(30, 150, 150, 270)
        page.insert_image(rect, stream=png_stream)

        text_rect = pymupdf.Rect(30, 300, 270, 290)
        red = pymupdf.pdfcolor["red"]

        rc = page.insertTextbox(
            rect,
            "text",
            fontsize=16,  # choose fontsize (float)
            fontname="SF Pro",  # a PDF standard font
            fontfile=None,  # could be a file on your system
            align=1
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
