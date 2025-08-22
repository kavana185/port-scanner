import socket
from datetime import datetime
import threading

# Ask user for target & port range
target = input("Enter host to scan (e.g., scanme.nmap.org): ")
start_port = int(input("Enter start port (e.g., 1): "))
end_port = int(input("Enter end port (e.g., 1024): "))

print(f"\nStarting scan on {target} from port {start_port} to {end_port}")
print("Time started:", datetime.now())
print("-" * 50)

open_ports = []

# Thread worker function
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  
        result = sock.connect_ex((target, port))  
        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except:
                service = "Unknown"
            print(f"Port {port} OPEN ({service})")
            open_ports.append((port, service))
        sock.close()
    except Exception as e:
        pass

# Launch threads for faster scanning
threads = []
for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("-" * 50)
print("Scan finished at:", datetime.now())

# Save results to file
if open_ports:
    with open("scan_results.txt", "w") as f:
        f.write(f"Scan results for {target} ({datetime.now()}):\n")
        for port, service in open_ports:
            f.write(f"Port {port} OPEN ({service})\n")
    print(f"\n✅ Results saved to scan_results.txt")
else:
    print("\nNo open ports found.")
