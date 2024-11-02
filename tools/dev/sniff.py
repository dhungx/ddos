"""Sniff the packets that are passing through the host."""

import sys
from scapy.all import sniff

def start_sniff(filter: str = "tcp", count: int = 50) -> None:
    """Start packet sniffing.

    Args:
        filter: A filter for the packets to capture (default: "tcp").
        count: The number of packets to capture (default: 50).
    """
    print(f"Starting to sniff {count} packets with filter '{filter}'...")
    capture = sniff(filter=filter, count=count)
    print("Sniffing complete.")
    capture.summary()

if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:
            start_sniff(sys.argv[1], int(sys.argv[2]))
        elif len(sys.argv) == 1:
            start_sniff()  # Use default parameters
        else:
            print("Usage: python script.py <filter> <count>")
            print("Example: python script.py 'tcp' 100")
    except ValueError:
        print("Error: Count must be an integer.")
    except Exception as e:
        print(f"An error occurred: {e}")
