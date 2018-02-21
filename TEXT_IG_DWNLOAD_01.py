#TWIL IG

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
from InstagramAPI import InstagramAPI
from PIL import Image
from resizeimage import resizeimage
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

InstagramAPI = InstagramAPI("public.gallery.01", "icanCode69")
InstagramAPI.login()  # login

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    number = request.values.get('From', None)
    message_body = request.values.get('Body', None)
    num_media = int(request.values.get('NumMedia', 0))
    medias = request.values.get('MediaUrl0', None)
    media_type = request.values.get('MediaContentType0', None)
    resp = MessagingResponse()

    if num_media == 0:
        resp.message('Hello {}. Thank you for your message. We will certainly try to keep it in mind.' .format(number))
        print('Message received from {}. Message says: {}' .format(number, message_body))

    elif num_media == 1:
        resp.message('Hello {}, thank you for your anonymous submission. Please check out @public.gallery.01 to confirm upload.' .format(number))
        print('Message received from {}. Message says: {}' .format(number, medias))
        print('Media type = {}' .format(media_type))


        # Copy a network object to a local file

        # downloading with requests
        # download the url contents in binary format
        r = requests.get(medias, allow_redirects=True, verify=False)
        # open method to open a file on your system and write the contents
        with open("python1.jpg", "wb") as code:
            code.write(r.content)



    #>>Resizing to upload
        fd_img = open('python1.jpg', 'r')
        im = Image.open(fd_img)
        width, height = im.size

        aspectH = float(width) / float(height)
        aspectV = float(height) / float(width)

        print(width)
        print(height)
        print(aspectH)
        print(aspectV)
    #>>Proper dimensions and aspect ratio
        if (aspectH == 1 and width <= 2048 and height <= 2048):
            im.save('python2.jpg', im.format)
            fd_img.close()

        elif width < 865:
            im = resizeimage.resize_cover(im, [width,(width*1.25)])
            im.save('python2.jpg', im.format)
            fd_img.close()

        elif height < 566:
            im = resizeimage.resize_cover(im, [(height*1.91),height])
            im.save('python2.jpg', im.format)
            fd_img.close()

        elif aspectH > 1.25:

            im = resizeimage.resize_cover(im, [1080,566])
            im.save('python2.jpg', im.format)
            fd_img.close()

        elif aspectV < 1.91:

            im = resizeimage.resize_cover(im, [864,1080])
            im.save('python2.jpg', im.format)
            fd_img.close()

        else:
            im.save('python2.jpg', im.format)
            fd_img.close()



    #>>Upload photo to IG
        photo_path = 'python2.jpg'
        caption = message_body
        InstagramAPI.uploadPhoto(photo_path, caption=caption)


        #else:
         #   print('Message received from {}. Message says: {}' .format(number, message_body))
          #  resp.message('Hello {}, says: {}'.format(number, message_body))

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
