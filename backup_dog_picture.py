from pprint import pprint
from shlex import split
from tqdm import tqdm
import time
import requests
import json

def get_dog_picture (breed):

    url = f'https://dog.ceo/api/breed/{breed}/list'
# Getting a list of sub_breed
    response = requests.get(url)
    list_sub_breeds = response.json()['message']
    list_dog_picture = []
    if len(list_sub_breeds) > 0:
# Getting pictures of sub_breed
        for sub_breed in list_sub_breeds:
            url = f'https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random'
            response = requests.get(url)
            list_dog_picture.append(response.json()["message"])
    else:
# Getting pictures of sub_breed
        url = f'https://dog.ceo/api/breed/{breed}/images'
        response = requests.get(url)
        list_dog_picture.extend(response.json()["message"])

    return list_dog_picture

def save_picture(breed, token):
    result = {}
    result.setdefault("breed", breed)
# Getting a list of pictures
    pictures = get_dog_picture(breed)
# We are forming a header for authorization
    headers = {'Authorization': token}
    url_base = "https://cloud-api.yandex.net"
    url_make_folder = "/v1/disk/resources"
    url_path_upload = "/v1/disk/resources/upload"
# create a folder
    params = {
        "path": breed
    }
    response = requests.put(url_base + url_make_folder, params=params, headers=headers)
# Let's upload files
    list_picture_name = []
    for picture in tqdm(pictures):
        filename = picture.split("/")[-1]
        params = {
            "path": f'{breed}/{breed}_{filename}',
            "url": picture
        }
        response = requests.post(url_base + url_path_upload, params=params, headers=headers)
        list_picture_name.append(f'{breed}/{breed}_{filename}')
        time.sleep(0.1)
    result.setdefault("pictures", list_picture_name)
# We write the results to a file
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(result))

    return


if __name__ == '__main__':
    token = ""

    save_picture("akita",  token)


