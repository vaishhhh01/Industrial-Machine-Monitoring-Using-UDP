"""Control-room server: receives UDP telemetry from industrial machines."""

import argparse
import json
import socket
import time
from collections import defaultdict
from datetime import datetime

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024

MAX_TEMPERATURE = 80.0
MAX_VIBRATION = 7.0

parser = argparse.ArgumentParser(description="Industrial machine monitoring server (UDP)")
parser.add_argument("--host", default=SERVER_IP,
                    help="IP to bind to; use 0.0.0.0 to accept clients on other machines")
parser.add_argument("--port", type=int, default=SERVER_PORT)
args = parser.parse_args()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((args.host, args.port))
# Wake up every second so Ctrl+C is handled on Windows even when no packets arrive
server_socket.settimeout(1.0)

machines = defaultdict(lambda: {
    "last_sequence": 0,
    "received": 0,
    "missing": 0,
    "alerts": 0,
    "latency_ms": 0.0
})

total_packets = 0
total_bytes = 0
start_time = time.perf_counter()

print("=" * 60)
print("       INDUSTRIAL MACHINE MONITORING SERVER")
print("=" * 60)
print(f"Listening on UDP {args.host}:{args.port}")
print("Waiting for machine telemetry...\n")

try:
    while True:
        try:
            data, address = server_socket.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            continue

        arrival_time = datetime.now()
        total_packets += 1
        total_bytes += len(data)

        try:
            payload = json.loads(data.decode("utf-8"))

            machine_id = str(payload["machine_id"])
            sequence = int(payload["sequence"])
            timestamp = payload["timestamp"]
            temperature = float(payload["temperature"])
            vibration = float(payload["vibration"])

            if not (0 <= temperature <= 200 and 0 <= vibration <= 100):
                raise ValueError("Sensor reading outside valid range")

            # One-way latency: arrival time minus the time the client stamped
            # into the packet (same clock when client and server share a host)
            latency_ms = (arrival_time - datetime.fromisoformat(timestamp)).total_seconds() * 1000

            stats = machines[machine_id]
            stats["received"] += 1
            stats["latency_ms"] += latency_ms

            if sequence > stats["last_sequence"] + 1:
                missing = sequence - stats["last_sequence"] - 1
                stats["missing"] += missing
                print(f"WARNING: {missing} sequence gap(s) for {machine_id}")

            stats["last_sequence"] = max(stats["last_sequence"], sequence)

            print("-" * 60)
            print(f"Machine      : {machine_id}")
            print(f"Sequence No. : {sequence}")
            print(f"Timestamp    : {timestamp}")
            print(f"Temperature  : {temperature:.2f} °C")
            print(f"Vibration    : {vibration:.2f} g")

            alert = False

            if temperature > MAX_TEMPERATURE:
                print("ALERT: HIGH TEMPERATURE")
                alert = True

            if vibration > MAX_VIBRATION:
                print("ALERT: HIGH VIBRATION")
                alert = True

            if alert:
                stats["alerts"] += 1
            else:
                print("Status       : NORMAL")

        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as error:
            print("Invalid telemetry packet:", error)

except KeyboardInterrupt:
    elapsed = time.perf_counter() - start_time
    total_received = sum(stats["received"] for stats in machines.values())
    total_latency = sum(stats["latency_ms"] for stats in machines.values())

    print("\n\n========== PERFORMANCE SUMMARY ==========")
    print(f"Duration              : {elapsed:.2f} seconds")
    print(f"Total packets received: {total_packets}")
    print(f"Packet rate           : {total_packets / elapsed:.2f} packets/s")
    print(f"Payload throughput    : {total_bytes * 8 / elapsed:.2f} bits/s")
    if total_received:
        print(f"Average latency       : {total_latency / total_received:.3f} ms")

    for machine_id, stats in sorted(machines.items()):
        expected = stats["received"] + stats["missing"]
        print(f"\nMachine: {machine_id}")
        print(f"  Packets received : {stats['received']}")
        print(f"  Sequence gaps    : {stats['missing']}")
        print(f"  Packet loss      : {stats['missing'] / expected * 100:.2f} %")
        print(f"  Alert readings   : {stats['alerts']}")
        print(f"  Average latency  : {stats['latency_ms'] / stats['received']:.3f} ms")

finally:
    server_socket.close()
    print("Server stopped.")
