import requests
import json
import time

deviceID = '{IoT Device ID}'
apiURL = 'https://iot.cht.com.tw/iot/v1/device/' + deviceID + '/snapshot'

headers = { 
    "CK":"{IoT Project Key or Device Key}"
    
    }   

files = { "meta":(None,json.dumps({"id":"{IoT Sesnor ID}","value":["Raspberry pi camera"]}), "application/json"), "file": ('test-image', open("test-image.jpg", "rb"),"image/jpeg")}

response = requests.post(apiURL, files=files, headers=headers)
print(response.text.encode("ascii"))
