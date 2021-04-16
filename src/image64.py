# ----------------------------------------------------------------------------------------------------
# Example program which encode file into base64 representation and decode as file again
# before used as foundation of transfer file through CoAP
# 
# Created by Fandi Adinata @2021 <https://githun.com/SuryaAssistant/coapfiletransfer>
# ----------------------------------------------------------------------------------------------------

import base64
import os
import datetime

# file location
transferred_file = "./sample_image/sample_image_1.jpg"
# get file extension information
file_name, file_extension = os.path.splitext(transferred_file)

# encode to base64 representation
with open("{}".format(transferred_file), "rb") as source_file:
    str_encode = base64.b64encode(source_file.read())
    #print (str_encode)

str_to_send = str(str_encode.decode('ascii', 'ignore'))

# get length of string
str_total_length = len(str_to_send)
print(str_total_length)

# ------------------------------------------------------------------------------------------------------------------------------------------------
# COAP TRANSMISSION
# ------------------------------------------------------------------------------------------------------------------------------------------------

# get file that transmitted
str_get = str_to_send

# get timestamp as name of file
timestamp = datetime.datetime.now()
file_timestamp = timestamp.strftime("%y") + timestamp.strftime("%m") + timestamp.strftime("%d") + timestamp.strftime("%H") + timestamp.strftime("%M") + timestamp.strftime("%S")
save_name = file_timestamp + file_extension
print (save_name)


# decode to image file
save_file = open("{}".format(save_name), "wb")
save_file.write(base64.b64decode(str_get))
save_file.close()
