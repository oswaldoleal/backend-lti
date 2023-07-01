import base64
import os

from imagekitio import ImageKit


class ImageKitHandler:
    PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
    PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
    URL_ENDPOINT = os.getenv("IMAGEKIT_URL")

    imagekit = ImageKit(
        private_key=PRIVATE_KEY,
        public_key=PUBLIC_KEY,
        url_endpoint=URL_ENDPOINT,
    )

    @classmethod
    def upload_image(cls, file, filename):
        upload_status = cls.imagekit.upload_file(
            file=base64.b64encode(open(file, "rb").read()),
            file_name=filename,
        )

        return upload_status

    @classmethod
    def delete_files(cls, file_ids):
        return cls.imagekit.bulk_file_delete(file_ids=file_ids)
