# httpImageBuilder
Build a png image line by line, via http post requests

## Requirements
- You will need a working version of **flask**
- Confirmed working on Ubuntu 20.04 Focal Fossa with Python3.7 installed

## How it works
This diagram might help you understand.
![Diagram](https://user-images.githubusercontent.com/95703244/169982325-e3667233-ee69-42d4-a618-e98175596fbd.png)

## How to use
You gotta send the following requests (examples in the demo file):
1. Handshake (Image Size)
2. Line by line (JSON table including RGB-255 format)
3. Render Request (Image Name)
