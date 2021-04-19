# ----------------------------------------------------------------------------------------------------
# Example program which support file transfer
# from client and server through CoAP using aiocoap
# Created by Fandi Adinata @2021 <https://github.com/SuryaAssistant/coapfiletransfer>
#
# Thanks to aiocoap  
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# ----------------------------------------------------------------------------------------------------

import logging
import asyncio

from aiocoap import *

import base64
import os
import datetime
import socket

logging.basicConfig(level=logging.INFO)

async def main():
    """The payload is bigger than 1kB, and thus sent as several blocks."""
    
    # get client IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_client = s.getsockname()[0]
    s.close()

    # server ip address as destination
    #ip_server = "127.0.0.1"
    ip_server = "192.168.43.115"

    # file location
    transferred_file = "./sample_image/sample_image_1.jpg"

    # get file information
    file_name, file_extension = os.path.splitext(transferred_file)

    # encode to base64 representation
    with open("{}".format(transferred_file), "rb") as source_file:
        str_encode = base64.b64encode(source_file.read())

    # set as "fully" string content
    str_to_send = str(str_encode.decode('ascii', 'ignore'))

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    # combine with file information and encode as ascii
    pre_payload = str(ip_client) + (",") + str(file_name) + (",") + str(file_extension) + (",") + str_to_send
    payload  = pre_payload.encode('ascii')

    # send PUT to server
    request = Message(code=PUT, payload=payload, uri="coap://{}/image".format(ip_server))

    response = await context.request(request).response

    #print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())