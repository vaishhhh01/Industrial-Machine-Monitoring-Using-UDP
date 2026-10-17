# Problem Statement and Network Design (Assessment 8)

**Course:** Computer Network & Data Communication, VIT Vellore
**Team:** Sruthika Sivagami R (25BIT0438), Kritika P (25BIT0321), Vaishnavi Thiruvengadam (25BIT0431)

## Industrial Machine Monitoring using UDP

### Problem statement

Modern smart manufacturing environments rely heavily on continuous, real-time oversight
of heavy industrial machinery (such as CNC mills, conveyor motors, turbines, and robotic
arms) to prevent equipment failures, costly downtime, and safety hazards. Industrial
machines operating under high thermal and mechanical stress continuously generate
time-sensitive sensor data, specifically temperature and vibration metrics, that must be
transmitted to a centralized monitoring system with minimal delay to catch anomalies
before a breakdown occurs.

### Limitations of traditional protocols

Traditional enterprise architectures often default to TCP or HTTP. However, in a
high-frequency telemetry environment, TCP's built-in connection handshakes, strict
sequencing, and automatic packet retransmission cause head-of-line blocking and latency.
If a packet is delayed by network congestion, the retransmitted data is obsolete because
a newer sensor reading has already replaced it.

### Proposed solution

To overcome the limitations of reliable protocols, the project implements a lightweight,
connectionless UDP (User Datagram Protocol) architecture:

- **Low-latency architecture:** UDP is chosen because it bypasses connection
  establishment overhead, enabling continuous, instantaneous data broadcasting with
  minimal protocol framing.
- **Data freshness over delivery guarantees:** The solution prioritizes real-time
  operational tracking where data freshness overrides absolute delivery guarantees,
  ensuring the central server instantly processes metrics and flags threshold warnings
  even if an occasional packet is dropped.
- **Performance evaluation framework:** The system models multi-client telemetry
  streaming to evaluate network dynamics such as packet loss, latency, throughput, and
  the practical impact of unreliable transport on industrial monitoring accuracy.

## Network design

![Network design](network-design.png)

> **Note:** The diagram was drawn at the design stage. It shows port 5000 and a
> conveyor motor and robotic arm as example machines. The final implementation uses
> **port 8080** and three simulated machines: CNC-Machine-01, Motor-Machine-02 and
> Turbine-Machine-03.

### Protocol stack

| Layer                      | Protocol / technology |
|----------------------------|-----------------------|
| Application                | JSON                  |
| Transport                  | UDP / Python sockets  |
| Network                    | IPv4                  |
| Data link / physical       | Ethernet              |

### Configuration

| Setting               | Value                                                   |
|-----------------------|---------------------------------------------------------|
| Binding host / IP     | localhost (`127.0.0.1`)                                 |
| Communication port    | `8080`                                                  |
| Socket address family | `socket.AF_INET` (IPv4)                                 |
| Socket type           | `socket.SOCK_DGRAM` (connectionless UDP datagram socket)|
| Receive buffer size   | 1024 bytes                                              |
