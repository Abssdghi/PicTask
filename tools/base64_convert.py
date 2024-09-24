import base64

def path_to_base64(path):
    with open(path, "rb") as image_file:
        image_data = image_file.read()

    image_base64 = base64.b64encode(image_data).decode('utf-8')
    return image_base64


def base64_save(base64_code, path):
    data = base64.b64decode(base64_code)

    with open(path, "wb") as new:
        new.write(data)
