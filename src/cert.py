import subprocess
import ssl
import socket
import datetime


def check_and_update_cert(
    hostname: str, port: int, cert_path: str, days_before_expiry: int = 7
):
    # Connection to retrieve current certificate
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

    # Certificate expiry date
    expire_date = datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    remaining_days = (expire_date - datetime.datetime.utcnow()).days

    # Update if about to expire
    if remaining_days < days_before_expiry:
        print(f"Updating certificate, as it expires in {remaining_days} days")
        subprocess.run(
            [
                "openssl",
                "s_client",
                "-showcerts",
                "-servername",
                hostname,
                "-connect",
                f"{hostname}:{port}",
            ],
            input=b"\n",
            stdout=open(cert_path, "wb"),
            shell=True,
        )
    else:
        print(f"Certificate is valid for another {remaining_days} days")
