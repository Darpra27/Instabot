# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 13:26:05 2020

@author: David
"""
import glob
import os
import sys
import time
from io import open
try:
    import Image
except ImportError:
    from PIL import Image

sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

posted_pic_list = []
try:
    with open("pics.txt", "r", encoding="utf8") as f:
        posted_pic_list = f.read().splitlines()
except Exception:
    posted_pic_list = []

timeout = 5*60*60  # pics will be posted every 24 hours

bot = Bot()
bot.login(username='username', password='password')
# medias = bot.get_total_user_medias(bot.user_id)
# bot.delete_medias(medias)
while True:
    folder_path = "*/pics"
    pics = glob.glob(folder_path + "/*.jpeg")
    pics = sorted(pics)
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue

            pic_name = pic[:-4].split("-")
            pic_name = "-".join(pic_name[1:])

            print("upload: " + pic_name)

            description_file = folder_path + "/" + pic_name + ".txt"

            image_file = pic

            image = Image.open(image_file)
            # image.show()
            xcenter = image.width/2
            ycenter = image.height/2
            cropped = image.crop((0, ycenter-xcenter-100, image.width, image.width+100))
            cropped.save(image_file)

            if os.path.isfile(description_file):
                with open(description_file, "r") as file:
                    caption = file.read()
            else:
                caption = pic_name.replace("-", " ")
                caption = pic_name.replace(".", "")

            bot.upload_photo(pic, caption=caption)
            if bot.api.last_response.status_code != 200:
                print(bot.api.last_response)
                # snd msg
                break

            if pic not in posted_pic_list:
                posted_pic_list.append(pic)
                with open("pics.txt", "a", encoding="utf8") as f:
                    f.write(pic + "\n")

            time.sleep(timeout)

    except Exception as e:
        print(str(e))
    time.sleep(60)
