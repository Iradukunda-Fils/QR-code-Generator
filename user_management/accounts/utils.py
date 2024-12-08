import qrcode
from PIL import  Image, ImageDraw, ImageOps
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
import os
from django.conf import settings
import logging
from django.core.files import File

# Set up logging
logger = logging.getLogger(__name__)

#GENERATE THE QR CODE PATH

def qr_code_path(data, email, logo=None, qr_size=10):
    qr = qrcode.QRCode(
        version=qr_size,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill='black', back_color='white').convert('RGBA')

    if logo:
         # Open the logo image
        logo_image = Image.open(logo).convert('RGBA')
    
        # Resize the logo to a medium size (e.g., 20% of the QR code's width)
        logo_size = int(qr_image.size[0] * 0.20)  # Adjusted for medium size
        logo_image = logo_image.resize((logo_size, logo_size), Image.ANTIALIAS)
    
        # Create a circular mask for the logo
        mask = Image.new('L', (logo_size, logo_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, logo_size, logo_size), fill=255)
    
        # Apply the mask to create a circular logo
        logo_image = Image.composite(logo_image, Image.new('RGBA', logo_image.size, (0, 0, 0, 0)), mask)
    
        # Position the logo in the center of the QR code
        position = ((qr_image.size[0] - logo_size) // 2, (qr_image.size[1] - logo_size) // 2)
        qr_image.paste(logo_image, position, logo_image)
    

    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    buffer.seek(0)

    file_name = f"{email.split('@')[0]}_qr.png"
    path = default_storage.save(file_name, ContentFile(buffer.read()))

    return path

#QR CODE IMAGE ONLY

import os
import logging
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageOps
import qrcode
from django.conf import settings

logger = logging.getLogger(__name__)

def qr_code_image(instance, qr_size=10):
    # Create the QR code data using the instance's attributes
    role = "Admin" if instance.is_admin else ("Active" if instance.is_active else instance.role)
    formatted_date = instance.created_at.strftime('%Y-%m-%d')
    qr_data = f"""
    ---- User Information ----
    
    User_Id:          {instance.id}
    First Name:       {instance.first_name}
    Last Name:        {instance.last_name}
    Email:            {instance.email}
    Country:          {instance.country.name} 
    Country_Code:     {instance.country.code}
    Phone Number:     {instance.phone_number}
    Status:           {role}
    Registed_at:      {formatted_date}
    
    -------- End ------
    """
    
    # Determine the logo path
    logo_path = instance.profile_picture.path if instance.profile_picture else os.path.join(settings.MEDIA_ROOT, 'logo.png')
    
    # Ensure the logo exists before proceeding
    if not os.path.exists(logo_path):
        logger.warning(f"Logo file not found: {logo_path}")

    # Generate the QR code
    qr = qrcode.QRCode(
        version=qr_size,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create the QR code image
    qr_image = qr.make_image(fill='black', back_color='white').convert('RGBA')

    # Add the logo if it exists
    try:
        if os.path.exists(logo_path):
            # Open the logo image
            logo_image = Image.open(logo_path).convert('RGBA')

            # Resize the logo to be smaller to avoid interference with QR code
            logo_size = int(qr_image.size[0] * 0.20)  # Adjusted for a smaller size
            logo_image = logo_image.resize((logo_size, logo_size), Image.LANCZOS)
            
            # Create a circular mask for the logo
            mask = Image.new('L', (logo_size, logo_size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, logo_size, logo_size), fill=255)

            # Apply the mask to create a circular logo
            logo_image = Image.composite(logo_image, Image.new('RGBA', logo_image.size, (0, 0, 0, 0)), mask)

            # Position the logo in the center of the QR code
            position = ((qr_image.size[0] - logo_size) // 2, (qr_image.size[1] - logo_size) // 2)
            qr_image.paste(logo_image, position, logo_image)
    except Exception as e:
        logger.error(f"Error while adding logo to QR code: {e}")

    # Save the image to a BytesIO buffer instead of a file
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    buffer.seek(0)  # Reset the buffer's cursor to the beginning

    # Create a Django File object and set a name
    file_name = instance.email.split('@')[0]
    qr_code_file = File(buffer, name=f"user_{file_name}_qr_code.png")
    
    # Return the file object containing the QR code image
    return qr_code_file
