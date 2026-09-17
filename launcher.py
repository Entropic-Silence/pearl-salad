"""Configure once, then replace PID 1 with WildRig for correct signal handling."""
import hashlib
import json
import os
import re
import secrets
import socket
import sys


def command(env):
    wallet = env.get("WALLET", "").strip()
    if not re.fullmatch(r"prl1[023456789acdefghjklmnpqrstuvwxyz]{20,100}", wallet):
        raise ValueError("Set WALLET to your Pearl address (prl1...), not the account URL")
    prefix = env.get("WORKER_PREFIX", "salad")
    if not re.fullmatch(r"[a-zA-Z0-9-]{1,10}", prefix):
        raise ValueError("WORKER_PREFIX must be 1-10 letters, digits or hyphens")
    machine = env.get("SALAD_MACHINE_ID") or env.get("HOSTNAME") or socket.gethostname()
    machine_hash = hashlib.sha256(machine.encode()).hexdigest()[:8]
    # 96 random bits also separate simultaneous groups on the same machine.
    worker = f"{prefix}-{machine_hash}-{secrets.token_hex(12)}"
    pool = env.get("POOL", "pool.pearlhash.xyz:9000")
    if not re.fullmatch(r"(?:stratum\+tcp://)?[A-Za-z0-9.-]+:[0-9]{1,5}", pool):
        raise ValueError("POOL must be host:port or stratum+tcp://host:port")
    return ["/opt/miner/wildrig-multi", "--algo", "pearlhash", "--url", pool,
            "--user", wallet, "--worker", worker, "--pass", "x", "--no-color",
            "--print-time", "30", "--retry-pause", "10", "--watchdog"]


if __name__ == "__main__":
    try:
        cmd = command(os.environ)
    except ValueError as exc:
        sys.exit(str(exc))
    print("Launch: " + json.dumps(cmd), flush=True)
    if os.environ.get("DRY_RUN") != "1":
        os.execv(cmd[0], cmd)
