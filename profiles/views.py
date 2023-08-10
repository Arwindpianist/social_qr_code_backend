from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import JsonResponse
import qrcode
import io
from PIL import Image
from .models import UserProfile

def generate_qr_code(data):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to a BytesIO object
    qr_img = io.BytesIO()
    img.save(qr_img, "PNG")
    return qr_img.getvalue()

def profile_list(request):
    profiles = get_list_or_404(UserProfile)
    data = []
    for profile in profiles:
        qr_code_data = f"https://example.com/profile/{profile.id}/"  # Replace with the actual URL for the profile
        qr_code_image = generate_qr_code(qr_code_data)
        data.append({
            "name": profile.name,
            "qr_code": qr_code_image,
        })
    return JsonResponse(data, safe=False)
