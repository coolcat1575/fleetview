from flask import Flask, jsonify
import subprocess
import json
import re
import os
from time import time

app = Flask(__name__)

# Read servers from environment
servers_env = os.getenv("DOCKER_SERVERS", "")
SERVERS = [s.strip() for s in servers_env.split(",") if s.strip()]

CACHE = None
LAST_FETCH = 0
CACHE_DURATION = 300  # 5 minutes

def get_containers(host):
    ssh_user = os.getenv("SSH_USER", "root")
    ssh_key = os.getenv("SSH_KEY_PATH", "/root/.ssh/id_rsa")

    try:
        output = subprocess.check_output(
            [
                "ssh", "-i", ssh_key,
                "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=5",
                f"{ssh_user}@{host}",
                "docker ps -a --format '{{json .}}'"
            ],
            timeout=10
        ).decode()

        containers = [json.loads(line) for line in output.strip().splitlines()]
        for c in containers:
            c["Host"] = host
            if "Names" in c:
                match = re.search(r'_(.*?)\.', c["Names"])
                if match:
                    c["Names"] = match.group(1)
        return containers
    except Exception as e:
        return [{"Host": host, "Status": "unreachable", "Error": str(e)}]

@app.route("/status")
def status():
    global CACHE, LAST_FETCH
    now = time()
    if not CACHE or now - LAST_FETCH > CACHE_DURATION:
        result = []
        for host in SERVERS:
            result.extend(get_containers(host))
        CACHE = result
        LAST_FETCH = now
    return jsonify(CACHE)

@app.route("/")
def index():
    with open("index.html") as f:
        return f.read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
