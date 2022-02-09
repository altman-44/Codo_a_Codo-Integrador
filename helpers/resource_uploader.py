import os
import cloudinary.uploader as cloudinaryUploader
from global_variables import PROFILE_IMAGE_TITLE

def uploadProfileImage(profileImageFile, userId):
    profileImageTitle = PROFILE_IMAGE_TITLE.format(userId)
    result = cloudinaryUploader.upload(
        profileImageFile,
        folder=(os.getenv('CLOUDINARY_FOLDER')) + '/',
        public_id=profileImageTitle
    )
    return result