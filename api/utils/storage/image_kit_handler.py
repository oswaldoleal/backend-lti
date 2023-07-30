import base64
import os

from imagekitio import ImageKit


class ImageKitHandler:
    PRIVATE_KEY = None
    PUBLIC_KEY = None
    URL_ENDPOINT = None
    imagekit = None

    @classmethod
    def initialize_image_kit(cls):
        if cls.imagekit is None:
            cls.PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
            cls.PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
            cls.URL_ENDPOINT = os.getenv("IMAGEKIT_URL")
            cls.imagekit = ImageKit(
                private_key=cls.PRIVATE_KEY,
                public_key=cls.PUBLIC_KEY,
                url_endpoint=cls.URL_ENDPOINT,
            )

    @classmethod
    def upload_image(cls, file, filename):
        cls.initialize_image_kit()
        upload_status = cls.imagekit.upload_file(
            file=base64.b64encode(open(file, "rb").read()),
            file_name=filename,
        )

        return upload_status

    @classmethod
    def delete_files(cls, file_ids):
        return cls.imagekit.bulk_file_delete(file_ids=file_ids)
