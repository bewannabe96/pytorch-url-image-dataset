import os
import uuid

import requests


def download_image(image_url: str, folder_path: str) -> str:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        unique_id = str(uuid.uuid4())
        file_path = os.path.join(folder_path, unique_id)

        with open(file_path, 'wb') as out_file:
            out_file.write(response.content)

        return unique_id
    except Exception:
        print(f"An error occurred while downloading image: {image_url}")
