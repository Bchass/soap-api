#TODO: Figure out how to calculate resp correctly

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

    print(f"resp: {resp}\n")

    #fake stack canary
    stack_check_val = 0x313373
    print(f"[+] stack check start: 0x{stack_check_val:04x}") 

    #null buffers
    method_buf[:] = [0] * len(method_buf)
    action_buf[:] = [0] * len(action_buf)
    combined_action_buf[:] = [0] * len(combined_action_buf)

    #call find -1: print the method portion from the xml blob in resp
    #and save it to the method buf. Format: '<m:METHODResponse*')
    print(f"[+] sscanf call 1: parse method portion from resp")
    method_buf[0] = f"<m:{resp}*>"
    ss = method_buf[0]
    var2 = method_buf[0].find("Response") + len("Response") - 1
    if var2 != 0x0:
        print(f"[+] found 'Response' in method_buf, NULLED")
        method_buf[var2] = 0

   # ========= Second call to find() and NULL check fail ===========
   # search for service string in resp, no NULL check
   # a long enough METHOD would result in this truncated, causing find() to
   # return a NULL pointer

    print(f"[+] find call 1: check 'service:' in resp\n")
    var3 = method_buf[0].find("service:")
    if var3 == 0x0:
       print(f"\033[0;31m[!] didn't find 'service:', expect a NULL ptr deref\n\033[0m")
       print(f"resp: {resp}")

    print(f"[+] sscanf call 2: check for '<ResponseCode>' in resp")
    action_buf[0] = method_buf[0][max(0, var3 + len("service:")):]
    if action_buf[0].startswith("<"):
        action_buf[0] = action_buf[0][1:]
    else:
        print(f"Warning: action portion is not formatted correctly")
       
    # check for <Responsecode> in resp)
    print(f"[+] find call 2: check for '<ResponseCode>' in resp")
    var4 = method_buf[0].find("<ResponseCode>")

    var4 = method_buf[0].find("<ResponseCode>")
    if var4 != 0x0:
        # if its there, parse some stuff from it (not important right now)
        print("[+] found <ResponseCode>, passed check")
        undef2 = 0

    print(f"[+] stack check end: 0x{stack_check_val:04x}")
    return 0

def main():
    streams = 0
    # this will hold the payload (i.e. the Method portion we would submit)
    # read from env to make testing easier
    payload = input("Enter PAYLOAD value: ")
    print(f"[+] payload length: {(payload)}")
    # construct the response content the same way the server does in SendSoapRespCode()
    resp_b = [""] * 512
    # this is the fmt string the calling function uses to construct resp
    resp_fmt = "<m:%sResponse xmlns:m=\"urn:NETGEAR-ROUTER:service:%s:1\"></m:%sResponse>\r\n<ResponseCode>%03d</ResponseCode>\r\n"
    #print(f"{resp_fmt} {payload} 404")
    #for i in range(len(payload)):
      #  resp_b[i] = payload[i]
    # call the target function with the payload
    print("[+] calling target function...\n")
    replica(streams, "".join(resp_b))
    return 0

if __name__ == "__main__":
    main()
