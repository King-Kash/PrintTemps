# import requests
# import time

# DUET_IP = '169.254.1.2'
# DUET_POLL_INTERVAL = 0.1

# while True:
#     response = requests.get(f"http://{DUET_IP}/rr_reply", timeout=1)
#     message = response.text.strip()
#     if message:
#         print(message)
#     time.sleep(0.5)


import requests
import time

base = "http://169.254.1.2"

# Connect
session_info = requests.get(f"{base}/rr_connect?password=")
print("Connect:", session_info.json())
session_key = session_info.json()["sessionKey"]

#monitor key=seqs
intial_comm_count = requests.get(f"{base}/rr_model?key=seqs&sessionKey={session_key}").json()["result"]["reply"]
print("intial comm count", intial_comm_count)
# Send G-code
gcode = "M115"
r = requests.get(f"{base}/rr_gcode?gcode={gcode}&sessionKey={session_key}")
print("G-code Sent:", r.json())


# Poll for reply
while True:
    current_comm_count = requests.get(f"{base}/rr_model?key=seqs").json()["result"]["reply"]
    if (current_comm_count != intial_comm_count):
        print("new comm count", current_comm_count)
        r = requests.get(f"{base}/rr_reply?sessionKey={session_key}", timeout=1)
        if r.text.strip():
            print("Reply:", r.text)
            break
    else:
        print("No reply received.")
        time.sleep(0.1)
