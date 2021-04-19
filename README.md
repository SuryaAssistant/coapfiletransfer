<span align = "center">

# CoAP File Transfer

</span>

<br>

## What is CoAP File Transfer

CoAP file transfer is an example method of transferring any file from client computer to server through constrained application protocol (CoAP) which used in IoT communication technology.

<br>

## How it works?

Transferred file will be encoded first into base64 before sent to server through CoAP and you can call it as "transferred string". After The "transferred string" reach the server, it will be decoded into file again from base64 string and saved as a file on server. 

<br>

## Library

Before using this example, you need to install `aiocoap` first.

```
$ pip install aiocoap
```

<br>

## Server

Clone this repository on your server

```
$ git clone https://github.com/SuryaAssistant/coapfiletransfer
```

Run `server.py`

<br>

## Client

Clone this repository on your client

```
$ git clone https://github.com/SuryaAssistant/coapfiletransfer
```

Open `client_put_image.py` and change the `ip_server` with your server ip address. Save and run `client_put_image.py`
