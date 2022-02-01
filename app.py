import os
import json
from typing import no_type_check_decorator
from webbrowser import get
from flask import Flask, request
from PIL import Image

currentImage = None
senderIp = None
imageSizeX = 0
imageSizeY = 0

app = Flask(__name__)
@app.route("/",methods=["POST"])

def processRequest():
    global senderIp
    global currentImage
    global imageSizeX
    global imageSizeY
    if senderIp == None or senderIp == request.remote_addr:
        senderIp = request.remote_addr
        dataForm = request.json

        if dataForm["PostReason"] == "Handshake":
            print("[POST] Handshake")
            if currentImage == None:
                currentImage = Image.new("RGB",(int(dataForm["X"]),int(dataForm["Y"])),0)
                return "OK"
            else:
                return "ResolutionAlreadySet"
        elif dataForm["PostReason"] == "PostLine":
            print("[POST] Post Line " + str(dataForm["Line"]) + " of " + str(imageSizeY))
            if currentImage:
                imageSizeX,imageSizeY = currentImage.size
                for i in range(0,imageSizeX - 1):
                    currentImage.putpixel((i,dataForm["Line"]),(dataForm[str(i)]["R"],dataForm[str(i)]["G"],dataForm[str(i)]["B"],255))
                return "OK"
            else:
                return "NoImage"
        elif dataForm["PostReason"] == "SaveImage":
            print("[POST] Save image")
            if currentImage:
                if dataForm["Success"] == True:
                    # Enhance Image (Fix broken pixels)
                    print("[PROCESS] Enhancing Image")
                    for y in range(0,imageSizeY - 1):
                        if y / 10 == round(y / 10):
                            print("[PROCESS] " + str(y / (imageSizeY - 1)) + "%")
                        for x in range(0,imageSizeX - 1):
                            pixelsAround = {
                                "top": currentImage.getpixel((x,(y - 1))),
                                "left": currentImage.getpixel(((x - 1),y)),
                                "right": currentImage.getpixel(((x + 1),y)),
                                "bottom": currentImage.getpixel((x,(y + 1)))
                            }
                            pixelsAroundEqual = True
                            for side in pixelsAround:
                                if pixelsAround.get(side) != pixelsAround.get("top"):
                                    pixelsAroundEqual = False
                            if pixelsAroundEqual:
                                pixelsAroundEqual = pixelsAround.get("top")
                                if currentImage.getpixel((x,y)) != pixelsAroundEqual:
                                    #print(pixelsAroundEqual)
                                    currentImage.putpixel((x,y),(pixelsAroundEqual[0],pixelsAroundEqual[1],pixelsAroundEqual[2],255)) # TUPLE ERROR?!!? fixed?

                    # Save Image
                    currentImage.save("output/" + str(dataForm["FileName"]) + ".png",format="png")
                    print("[REPORT] DONE! Image saved: 'output/" + str(dataForm["FileName"]) + ".png'")
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