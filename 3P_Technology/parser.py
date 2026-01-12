import re
from typing import Dict, Any

IO_REGEX = re.compile(r'(\d+)\s*(?:I/O|io points|io points|IO points)', re.I)
PROTOCOLS = ['Profinet', 'Modbus', 'OPC UA', 'EtherNet/IP', 'BACnet', 'IEC 61850']

def parse_tender_text(text: str) -> Dict[str, Any]:
    result = {}
    # IO points
    io_match = IO_REGEX.search(text)
    result['io_points'] = int(io_match.group(1)) if io_match else None

    # Protocols
    found = [p for p in PROTOCOLS if re.search(r'\b' + re.escape(p) + r'\b', text, re.I)]
    result['protocols'] = found

    # Redundancy
    if re.search(r'\bredundant\b|\bredundancy\b|N\-1\b|hot standby', text, re.I):
        result['redundancy'] = True
    else:
        result['redundancy'] = False

    # Response time requirements
    rt = re.search(r'response time[^\d]*(\d+)\s*ms', text, re.I)
    result['response_time_ms'] = int(rt.group(1)) if rt else None

    return result

# minimal test
if __name__ == "__main__":
    sample = "We require 128 I/O points, Profinet and OPC UA. Response time 50 ms. N-1 redundancy."
    print(parse_tender_text(sample))
