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
