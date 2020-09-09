from grid_captcha import CaptchaBuilder
import os

builder = CaptchaBuilder()

if not os.listdir("../images/test") and not os.listdir("../images/train"):
    for i in range(1, 101):
        builder.build()
        word = builder.word
        builder.save('rawdata\\test%d.jpeg' % i)

        image_jpeg = builder.base64()
        image_png = builder.base64(image_format='PNG')

    for i in range(1, 501):
        builder.build()
        word = builder.word
        builder.save('rawdata\\train%d.jpeg' % i)

        image_jpeg = builder.base64()
        image_png = builder.base64(image_format='PNG')
