'''
Note: This script can not be run in this plaformIO project. Creat a clean directory and a vertual environment in order to run this code.

Strtup Steps:
1. Run .\duet-env\Scripts\Activate.ps1 on VSCode bootup
2. Run the lor_reader/data_logger/py (data_logger.py is file I wrote this code in)
3. Run GCode Script (Message will pop up on Duet GUI reminding you to run this script first)
'''
import serial
import time
from datetime import datetime
import requests
import threading
from queue import Queue

DUET_IP = '169.254.1.2'
DUET_POLL_INTERVAL = 0.3

ARDUINO_PORT = 'COM8'
ARDUINO_BAUD = 9600

TARGET_TEMP = 30

#TRACKING VARIABLES
currentLayer = 0
currentBead = 0
reset_timer = True
last_log_time = 0.0
temp = None
message_queue = Queue()
    
#ESTABLISH CONNECTIONS
ser_arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD, timeout=1)
time.sleep(1)
print("Connectd to Arduino on", ARDUINO_PORT)

session_info = requests.get(f"http://{DUET_IP}/rr_connect?password=", timeout=0.5)
session_key = session_info.json()["sessionKey"]
if len(session_info.json()) > 1:
    print("Connected to Duet Board. Session Key:", session_key)

#INTILIZE TRACKING OF AVAILABLE MESSAGES FOR HTTP READ
initial_comm_count = requests.get(f"http://{DUET_IP}/rr_model?key=seqs&sessionKey={session_key}", timeout=0.5).json()["result"]["reply"]
#SHUTDOWN EVENT
stop_event = threading.Event()

def duet_reader():
    global currentLayer, currentBead, reset_timer, initial_comm_count
    while not stop_event.is_set():
        current_comm_count = requests.get(f"http://{DUET_IP}/rr_model?key=seqs&sessionKey={session_key}", timeout=0.5).json()["result"]["reply"]
        if current_comm_count != initial_comm_count:
            # print("new comm count", current_comm_count)
            initial_comm_count = current_comm_count
            r = requests.get(f"http://{DUET_IP}/rr_reply?sessionKey={session_key}", timeout=0.5)
            message = r.text.strip()
            if message == "NEXT_LAYER" or message == "PRINT_COMPLETE":
                message_queue.put(message)
        else:
            time.sleep(0.1)

duet_thread = threading.Thread(target=duet_reader, daemon=True)
duet_thread.start()


#LOG DATA TO CSV AND KILL WHEN PRINT COMPLETE
with open('log.csv', 'w') as f:
    f.write("Timestamp,LayerNumber,BeadNumber,ElapsedTime(s),Temperature(C)\n")
    try:
        while not stop_event.is_set():
            while not message_queue.empty():
                message = message_queue.get()
                if message == "NEXT_LAYER":
                    print(f"Layer {currentLayer} complete.")
                    currentLayer += 1
                    currentBead = 0
                    reset_timer = True
                    last_log_time = 0.0
                if message == "PRINT_COMPLETE":
                    print("Logging Complete. Data stored in log.csv.")
                    stop_event.set()
                    break
            line = ser_arduino.readline().decode('utf-8', errors='replace').strip()
            if line:
                parts = line.strip().split(',')
                action = parts[0]
                temp = float(parts[1]) if len(parts) > 1 else None
                if action == "log":
                    if reset_timer:
                        start = time.perf_counter()
                        reset_timer = False
                    now = time.perf_counter()
                    should_log = (
                        now - last_log_time >= 0.7
                        or last_log_time == 0.0
                        or temp >= TARGET_TEMP
                    )
                    if should_log:
                        elapsed = now - start
                        date_time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        f.write(f"{date_time_stamp},{currentLayer},{currentBead},{elapsed:.3f},{temp:.2f}\n")
                        f.flush()
                        print(f"{date_time_stamp},{currentLayer},{currentBead},{elapsed:.3f},{temp:.2f}")
                        last_log_time = now
                if action == "done":
                    currentBead += 1
                    reset_timer=True
                    print(f"Bead {currentBead} done.")
    except KeyboardInterrupt:
        print('\nExiting.')
        duet_thread.join()
        ser_arduino.close()
    finally:
        duet_thread.join()
        ser_arduino.close()
        requests.get(f"http://{DUET_IP}/rr_disconnect?sessionKey={session_key}", timeout=0.5)


