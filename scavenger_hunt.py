import re

def solve_scavenger_hunt(packets):
    num_to_payload = {}

    for packet in packets:
        if not isinstance(packet, str):
            continue

        m = re.match(r"^\s*(\d+)", packet)   # number at the start
        if not m:
            continue

        num = int(m.group(1))
        payload = packet[m.end():]           # everything after the leading number

        if num not in num_to_payload:
            num_to_payload[num] = payload

    message = []
    target = 1

    # 1,2,4,8,... as long as it exists
    while target in num_to_payload:
        payload = num_to_payload[target]
        message.append("".join(c for c in payload if c.isalpha()))
        target *= 2

    return "".join(message)


# Test Case
data = ["1the@", "5ignore!", "2secret#", "99lost*", "4path!"]
print(f"Decoded Message: {solve_scavenger_hunt(data)}")
# -> thesecretpath
