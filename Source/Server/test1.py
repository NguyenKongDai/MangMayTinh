import json
filename = 'member.json'
entry = {"005": {
        "fullname": "Dũ Quốc Huy",
        "phone": "0123456789",
        "email": "huy2k2@gmail.com",
        "imageDir_small": "Image/small001.jpg",
        "imageDir_big": "Image/big001.jpg"
        }  }
# 1. Read file contents
with open(filename,encoding='utf-8') as file:
    data = json.load(file)
# 2. Update json object
data.append(entry)
# 3. Write json file
with open(filename,encoding='utf-8') as file:
    json.dump(data, file)