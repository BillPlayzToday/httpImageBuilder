import os
import json
from flask import Flask, request
from PIL import Image
from pathlib import Path

currentImage = None
senderIp = None
imagesizeX = 0
imagesizeY = 0

app = Flask(__name__)
@app.route("/",methods=["POST"])

def processRequest():
    global senderIp
    global currentImage
    global imageSizeX
    global imageSizeY
    if senderIp == None or senderIp == request.sender_addr:
        senderIp = request.sender_addr
        dataForm = request.json

        if dataForm.PostReason == "SendPictureResolution":
            if currentImage == None:
                currentImage = Image.new("RGB",(int(dataForm.X),int(dataForm.Y)),0)
                return "OK"
            else:
                return "ResolutionAlreadySet"
        elif dataForm.PostReason == "SendLine":
            if currentImage:
                imageSizeX,imageSizeY = currentImage.size
                for i in range(1,imageSizeX + 1):
                    currentImage.putpixel((i,dataForm.Line),(dataForm[str(i)].R,dataForm[str(i)].G,dataForm[str(i)].B))
                return "OK"
            else:
                return "NoImage"
        elif dataForm.PostReason == "SaveImage":
            if currentImage:
                if dataForm.Success == True:
                    currentImage.save("output/" + str(dataForm.FileName) + ".png",format="png")
                    print("Conversion done! Image saved as output/" + str(dataForm.FileName) + ".png")
                senderIp = None
                currentImage = None
                imagesizeX = 0
                imagesizeY = 0
                return "OK"
            else:
                return "NoImage"
    else:
        return "ServerInUse"

if __name__ == "__main__":
    app.run(host="0.0.0.0")