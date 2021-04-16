# ----------------------------------------------------------------------------------------------------
# Example program which support file transfer
# from client and server through CoAP using aiocoap
# Created by Fandi Adinata @2021 <https://githun.com/SuryaAssistant/coapfiletransfer>
#
# Thanks to aiocoap  
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# ----------------------------------------------------------------------------------------------------

import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

import base64
import os

class BlockResource(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()
        self.set_content(b"ISI PUT_ASLI.\n")

    def set_content(self, content):
        self.content = content

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)


class SeparateLargeResource(resource.Resource):
    """Example resource which supports the GET method. It uses asyncio.sleep to
    simulate a long-running operation, and thus forces the protocol to send
    empty ACK first. """

    def get_link_description(self):
        # Publish additional data in .well-known/core
        return dict(**super().get_link_description(), title="A large resource")

    async def render_get(self, request):
        await asyncio.sleep(3)

        payload = "Three rings for the elven kings under the sky, seven rings "\
                "for dwarven lords in their halls of stone, nine rings for "\
                "mortal men doomed to die, one ring for the dark lord on his "\
                "dark throne.".encode('ascii')
        return aiocoap.Message(payload=payload)

class WhoAmI(resource.Resource):
    async def render_get(self, request):
        text = ["Used protocol: %s." % request.remote.scheme]

        text.append("Request came from %s." % request.remote.hostinfo)
        text.append("The server address used %s." % request.remote.hostinfo_local)

        claims = list(request.remote.authenticated_claims)
        if claims:
            text.append("Authenticated claims of the client: %s." % ", ".join(repr(c) for c in claims))
        else:
            text.append("No claims authenticated.")

        return aiocoap.Message(content_format=0,
                payload="\n".join(text).encode('utf8'))
    
# class to save image
class save_image(resource.Resource):
    def __init__(self):
        super().__init__()
        self.set_content(b"None.\n")

    def set_content(self, content):
        self.content = content
        
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        
        # convert to string
        get_payload = request.payload.decode('ascii', 'ignore').split(',')
        
        file_name = get_payload[0]
        file_extension = get_payload[1]
        image_payload = get_payload[2]
                
        # get timestamp as name of file
        timestamp = datetime.datetime.now()
        file_timestamp = timestamp.strftime("%y") + timestamp.strftime("%m") + timestamp.strftime("%d") + timestamp.strftime("%H") + timestamp.strftime("%M") + timestamp.strftime("%S")
        save_name = file_timestamp + file_extension

        # decode to image file
        save_file = open("./image/{}".format(save_name), "wb")
        save_file.write(base64.b64decode(image_payload))
        save_file.close()
        
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['other', 'separate'], SeparateLargeResource())
    root.add_resource(['whoami'], WhoAmI())
    root.add_resource(['image'], save_image())
    
    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
