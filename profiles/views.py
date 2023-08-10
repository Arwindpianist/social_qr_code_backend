# views.py

import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
import qrcode
import io
from PIL import Image
from .models import UserProfile

class CreateProfileView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            instagram = data.get('instagram')
            twitter = data.get('twitter')
            email = data.get('email')
            phone_number = data.get('phone_number')

            # Create the user profile
            profile = UserProfile.objects.create(
                username=username,
                instagram=instagram,
                twitter=twitter,
                email=email,
                phone_number=phone_number
            )

            # Return a success response
            return JsonResponse({'message': 'Profile created successfully'}, status=201)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while creating the profile'}, status=500)

class GenerateQRCodeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')

            # Get the user's profile
            profile = get_object_or_404(UserProfile, username=username)

            # Generate the QR code data
            qr_code_data = f"https://social-qr-code-backend.onrender.com/api/profiles/{profile.id}/"

            # Create a QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_code_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Convert the image to a BytesIO object
            qr_img = io.BytesIO()
            img.save(qr_img, "PNG")

            # Return the URL of the generated QR code
            return JsonResponse({'qr_code_url': qr_img.getvalue()}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while generating the QR code'}, status=500)

class DisplayProfileView(View):
    def get(self, request, username):
        profile = get_object_or_404(UserProfile, username=username)
        context = {
            'user': profile.user,
            'profile': profile,
        }
        return render(request, 'profile.html', context)
