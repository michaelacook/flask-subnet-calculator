from flask import Flask, request, jsonify, render_template
import ipaddress

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    cidr = data.get("cidr", "").strip()
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    hosts = list(network.hosts())
    total_hosts = len(hosts)

    result = {
        "network_address":   str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "subnet_mask":       str(network.netmask),
        "wildcard_mask":     str(network.hostmask),
        "cidr_notation":     str(network),
        "prefix_length":     network.prefixlen,
        "total_addresses":   network.num_addresses,
        "usable_hosts":      total_hosts,
        "first_host":        str(hosts[0]) if hosts else "N/A",
        "last_host":         str(hosts[-1]) if hosts else "N/A",
        "ip_class":          get_ip_class(str(network.network_address)),
        "is_private":        network.is_private,
        "supernet":          str(network.supernet()) if network.prefixlen > 0 else "N/A",
    }
    return jsonify(result)


@app.route("/subnets", methods=["POST"])
def subnets():
    data = request.get_json()
    cidr = data.get("cidr", "").strip()
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Determine classful parent boundary
    first_octet = int(str(network.network_address).split(".")[0])
    if first_octet < 128:
        classful_prefix = 8
    elif first_octet < 192:
        classful_prefix = 16
    else:
        classful_prefix = 24

    # Use the input network if it's already at or larger than classful boundary,
    # otherwise climb up to the classful parent
    if network.prefixlen <= classful_prefix:
        parent = network
    else:
        parent = network.supernet(new_prefix=classful_prefix)

    # Enumerate every individual subnet at the input prefix size within the parent
    target_prefix = max(network.prefixlen, classful_prefix + 1)
    # Floor target at /30 minimum meaningful size
    target_prefix = min(target_prefix, 30)

    subnet_list = list(parent.subnets(new_prefix=target_prefix))

    rows = []
    for subnet in subnet_list:
        hosts = list(subnet.hosts())
        rows.append({
            "network":         str(subnet.network_address),
            "first_host":      str(hosts[0]) if hosts else "N/A",
            "last_host":       str(hosts[-1]) if hosts else "N/A",
            "broadcast":       str(subnet.broadcast_address),
            "prefix":          f"/{subnet.prefixlen}",
            "usable_hosts":    len(hosts),
        })

    return jsonify({
        "base":   str(network),
        "parent": str(parent),
        "prefix": f"/{target_prefix}",
        "rows":   rows,
    })


def get_ip_class(ip):
    first_octet = int(ip.split(".")[0])
    if first_octet < 128:
        return "A"
    elif first_octet < 192:
        return "B"
    elif first_octet < 224:
        return "C"
    elif first_octet < 240:
        return "D (Multicast)"
    else:
        return "E (Reserved)"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)