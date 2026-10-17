# Wireshark captures

Raw captures from the three performance tests. Open them in Wireshark to check the
packet counts in the main README.

| File             | Test                         | Clients running                     | Packets |
|------------------|------------------------------|-------------------------------------|---------|
| `test_A.pcapng`  | A: baseline                  | `client1.py`                        | 60      |
| `test_B.pcapng`  | B: increased load            | `client1.py`, `client2.py`          | 180     |
| `test_C.pcapng`  | C: multi-client monitoring   | `client1.py`, `client2.py`, `client3.py` | 477 |

Capture settings:

- Interface: **Adapter for loopback traffic capture** (Npcap)
- Display filter: `udp.port == 8080`
- Duration: 60 seconds per test

Useful views once a file is open:

- **Statistics → Capture File Properties** for packet count, duration and average rate
- **Statistics → Conversations → UDP** to see one stream per machine (one source port each)
- **Statistics → I/O Graphs** to compare packet rate across the three tests
