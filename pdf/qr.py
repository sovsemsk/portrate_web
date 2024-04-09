import io

import fitz
import qrcode
from django.conf import settings

fitz.TOOLS.set_aa_level(0)


def make_qrcode(company_id, theme):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=50, border=0)
    qr.add_data(f"https://geo.portrate.io/@{company_id}/")
    qr.make(fit=True)

    if theme == "light":
        img = qr.make_image(fill_color="black", back_color="transparent")
    else:
        img = qr.make_image(fill_color="white", back_color="transparent")

    stream = io.BytesIO()
    img.save(stream, "PNG")
    return stream


def generate_stick(company_id, theme):
    png_stream = make_qrcode(company_id, theme)
    template = fitz.open(f"{settings.BASE_DIR}/pdf/qr_pdf_stick_{theme}.pdf")

    for page in template:
        rect = fitz.Rect(79, 199, 219, 339)
        page.insert_image(rect, stream=png_stream)

    pdf_stream = io.BytesIO()
    template.save(pdf_stream, deflate=True, garbage=3)
    return pdf_stream


def generate_business_card(company_id):
    pass
