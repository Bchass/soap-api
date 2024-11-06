#TODO: Figure out how to calculate resp correctly

import re

def replica(streams, resp):
    #order of variables in memory
    content_len = None
    jwt = None
    var2 = None
    var3 = None
    var4 = None
    method_buf = [""] * 64
    action_buf = [""] * 32
    combined_action_buf = [""] * 128
    undef1 = None
    undef2 = None
    stack_check_val = None

    #fake stack canary
    stack_check_val = 0x313373
    print(f"[+] stack check start: 0x{stack_check_val:04x}") 

    #null buffers
    method_buf[:] = [0] * len(method_buf)
    action_buf[:] = [0] * len(action_buf)
    combined_action_buf[:] = [0] * len(combined_action_buf)

    #call find -1: print the method portion from the xml blob in resp
    #and save it to the method buf. Format: '<m:METHODResponse*')
    print(f"[+] find call 1: parse method portion from resp")
    method_buf[0] = f"<m:%sResponse%*s"

    var2 = method_buf[0].find("Response") + len("Response") - 1
    if var2 != -1:
        print(f"[+] found \033[0;31m'Response'\033[0m in method_buf, NULLED")
        var2 == -1

   # ========= Second call to find() and NULL check fail ===========
   # search for service string in resp, no NULL check
   # a long enough METHOD would result in this truncated, causing find() to
   # return a NULL pointer

    print(f"[+] find call 1: check \033[0;31m'service:'\033[0m in resp")
    var3 = method_buf[0].find("service:")
    if var3 == -1:
        print(f"[!] didn't find \033[0;31m'service:'\033[0m,expect a NULL ptr deref")
        #print("resp: %s", resp)
       

    print(f"[+] find call 2: check for '<ResponseCode>' in resp")

    #TODO: Figure out service
    var3_fmt = 'service:%[^:]'
    pattern = r'service:(.*)'
    match = re.match(pattern, var3_fmt)
    if match:
        action_buf_1 = match.group(1).strip()
        print(action_buf_1)

    print(f"[+] str call 2: check for '<ResponseCode>' in resp")
    var3 = method_buf[0].find("<ResponseCode>")
    if var3 != -1:
        print(f"[+] found <ResponseCode>, passed check")
        undef1 = 0

    print(f"[+] stack check end: 0x{stack_check_val:04x}")
    return 0

def main():
    streams = 0
    # this will hold the payload (i.e. the Method portion we would submit)
    # read from env to make testing easier
    payload = input("PAYLOAD: ")
    print(f"[+] payload length: {payload}")
    # construct the response content the same way the server does in SendSoapRespCode()
    #resp_b = [""] * 512
    resp_b = str([0] * 512)
    print("[+] calling target function...\n")
    # this is the fmt string the calling function uses to construct resp
    resp_fmt = "<m:%sResponse xmlns:m=\"urn:NETGEAR-ROUTER:service:%s:1\"></m:%sResponse>\r\n<ResponseCode>%03d</ResponseCode>\r\n"
    #for i in range(len(payload)):
    #    resp_b[i] = payload[i]
    #print(resp_b, 512, resp_fmt, payload, "ConfigSync", payload, 404)
    # call the target function with the payload
    replica(streams, "".join(resp_b))
    return 0

if __name__ == "__main__":
    main()
