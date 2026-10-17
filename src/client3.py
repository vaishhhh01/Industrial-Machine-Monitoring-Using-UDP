"""Turbine-Machine-03: sends temperature and vibration telemetry over UDP every 0.2 s."""

import argparse
import json
import random
import socket
import time
from datetime import datetime

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
MACHINE_ID = "Turbine-Machine-03"
SEND_INTERVAL = 0.2  # seconds

parser = argparse.ArgumentParser(description=f"{MACHINE_ID} telemetry client (UDP)")
parser.add_argument("--server", default=SERVER_IP, help="IP of the monitoring server")
parser.add_argument("--port", type=int, default=SERVER_PORT)
parser.add_argument("--loss", type=float, default=0.0,
                    help="percent of packets to skip, to test the server's gap detection")
args = parser.parse_args()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sequence_number = 0
packets_sent = 0

print(f"{MACHINE_ID} started...")

try:
    while True:
        sequence_number += 1

        payload = {
            "machine_id": MACHINE_ID,
            "sequence": sequence_number,
            "timestamp": datetime.now().isoformat(),
            "temperature": round(random.uniform(65, 100), 2),
            "vibration": round(random.uniform(2, 10), 2),
            "status": "RUNNING"
        }

        if random.uniform(0, 100) < args.loss:
            print(f"Dropped #{sequence_number} (simulated loss)")
        else:
            message = json.dumps(payload).encode("utf-8")
            client_socket.sendto(message, (args.server, args.port))
            packets_sent += 1

            print(f"Sent #{sequence_number} | "
                  f"Temp: {payload['temperature']}°C | "
                  f"Vibration: {payload['vibration']}g")

        time.sleep(SEND_INTERVAL)

except KeyboardInterrupt:
    print(f"\n{MACHINE_ID} stopped. Packets sent: {packets_sent}")

finally:
    client_socket.close()
