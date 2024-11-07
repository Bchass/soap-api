import re

def replica(streams, resp):
    #order of variables in memory
    content_len = ""
    jwt = ""
    var2 = ""
    var3 = ""
    var4 = ""
    method_buf = ""
    action_buf = ""
    combined_action_buf = ""
    undef1 = ""
    undef2 = ""


    #fake stack canary
    stack_check_val = 0x313373
    print(f"resp: {resp}")
    print(f"[+] stack check start: 0x{stack_check_val:x}") 

    #null buffers
    method_buf = ""
    action_buf = ""
    combined_action_buf = ""

    #call find -1: print the method portion from the xml blob in resp
    #and save it to the method buf. Format: '<m:METHODResponse*')
    print(f"[+] search call 1: parse method portion from resp")
    match = re.search(r"<m:(\w+)Response", resp)
    if match:
        method_buf = match.group(1)
        print(f"[+] method_buf parsed as {method_buf}")
    else:
        print(f"[!] Error: \033[0;31mMethod\033[0m not found in resp.")

    if "Response" in method_buf:
        print("[+] found \033[0;31m'Response'\033[0m in method_buff, NULLED")
        method_buf = method_buf.replace("Response", "")

   # ========= Second call to find() and NULL check fail ===========
   # search for service string in resp, no NULL check
   # a long enough METHOD would result in this truncated, causing find() to
   # return a NULL pointer

    print(f"[+] search call 1: check \033[0;31m'service:'\033[0m in resp")
    service_match = re.search(r"service:(\w+)", resp)
    if service_match:
        var3 = service_match.group

    if "Response" in method_buf:
        print("[+] found \033[0;31m'Response'\033[0m in method_bufm NULLED")
        method_buf = method_buf.replace("Response", "")

    service_match = re.search(r"service:([^:]+)", resp)
    if service_match:
        action_buf = service_match.group(1)
        print("[!] didn't find \033[0;31m'service:'\033[0m, expect a NULL ptr deref")

    print("[+] search call 2: check for \033[0;31m'<ResponseCode>'\033[0m in resp")
    response_code_match = re.search(r"<ResponseCode>(\d{3})</ResponseCode>", resp)
    if response_code_match:
        print("[+] found  \033[0;31m<ResponseCode>\033[0m, passed check")
        undef1 = 0
    else:
        print("[!] <ResponseCode> not found, fail check")

    print(f"[+] stack check end: 0x{stack_check_val:x}")
    return 0

def main():
    streams = 0
    # this will hold the payload (i.e. the Method portion we would submit)
    # read from env to make testing easier
    payload = input("PAYLOAD: ")
    print(f"[+] payload length: {payload}")
    # construct the response content the same way the server does in SendSoapRespCode()
    resp_fmt = "<m:{}Response xmlns:m=\"urn:NETGEAR-ROUTER:service:{}:1\"></m:{}Response>\r\n<ResponseCode>404</ResponseCode>\r\n"
    resp = resp_fmt.format(payload, "ConfigSync", payload)

    print("[+] calling target function...\n")
    replica(streams, resp)
    return 0


if __name__ == "__main__":
    main()
