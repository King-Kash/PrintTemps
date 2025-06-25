'''
1. Get the time from the server
2. Read a lineby line from the Serial Port
3. Format lines from Serial monitor into CSV format
4. Write to a running csv file.
    - when opening on first layer use 'w' on the rest of the layers use 'a'
'''
import csv
import serial
import time
from datetime import datetime

PORT = 'COM8'
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(1)
print("Connectd to", PORT)

currentLayer = 0
reset_timer = True
last_write = 0.0

writemode = None
if currentLayer == 0:
    writemode = 'w'
else:
    writemode = 'a'

with open('log.csv', writemode) as f:
    f.write("Timestamp,Layer,ElapsedTime(s),Temperature(C)\n")

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='replace').strip()
                parts = line.strip().split(',')
                action = parts[0]
                temp = float(parts[1]) if len(parts) > 1 else None
                if action == "log":
                    if reset_timer:
                        start = time.perf_counter()
                        reset_timer = False
                    elapsed = time.perf_counter() - start
                    if (elapsed - last_write) > 1:
                        last_write = elapsed
                        date_time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        f.write(f"{date_time_stamp},{currentLayer},{elapsed:.3f},{temp:.2f}\n")
                        f.flush()
                        print(f"{date_time_stamp},{currentLayer},{elapsed:.3f},{temp:.2f}")
                if action == "done":
                    currentLayer += 1
                    reset_timer=True
                    print(f"Layer {currentLayer} done. Awaiting new data...")

    except KeyboardInterrupt:
        print('\nExiting.')
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
        print("Serial connection closed.")

