# Standard Library
import sys

# Octoxlabs
from octoxlabs import OctoxLabs

fields = ["Hostname", "Domain", "OS.Type", "IpAddresses"]
query = "Adapters = active-directory"

octox = OctoxLabs(ip="test.octoxlabs.local", token="34AaBbCc")
if not octox.ping():
    sys.exit(1)

count, scroll_id, devices = octox.search_scroll_devices(query=query, fields=fields)
print(f"Total device count: {count}")


def prepare_device_instance(data):
    line = []
    for f in fields:
        value = device.get(f, "")
        if value:
            value = "|".join(value) if len(value) > 1 else value[0]
        line.append(str(value))
    return ";".join(line)


while devices:
    for device in devices:
        print(prepare_device_instance(device))

    _, __, devices = octox.search_scroll_devices(query=query, fields=fields, scroll_id=scroll_id)
