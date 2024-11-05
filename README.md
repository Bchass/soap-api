# SOAP-API
## Netgear
A collection of information I have gathered so far on the SOAP-API uses for their netgear routers.
This is a good read: https://blog.coffinsec.com/research/2022/06/19/orbi-hunting-1-soap-api-crashes.html.
I've decided to take the local test written in C and convert it to python for a better understanding.
I'm working with a `C6230` which uses the NightHawk app, from my research this app doesn't use the SOAP-API like the prior app did, but you can still interact with it using a package like pynetgear.
Thankfully Netgear supplies an open-source to the firmware: https://kb.netgear.com/2649/NETGEAR-Open-Source-Code-for-Programmers-GPL

- `Stack canary check` secrert value placed on the stack which changes everytime the program starts.

## Headers:

- `urn:NETGEAR-ROUTER:service:`
- `<urn:VENDOR:service:ACTION_str:1#METHOD_str`

## Functions

- `main()` will retrieve the SOAPAction header from some env var
- `SendSoapResponse()`  is responsible for handling HTTP response
- `SoapExecute()` the main function that handles SOAP request
- `SendSoapRespCode()` constructs a part of the HTTP response depending if the SOAP method was authenticated.
- `SendSoapResponse()` will send final response to the client. Aka making a change to your router in the webgui. Not sure about the NightHawk app. There has been some discussion that this app doesn't utilize SOAP.