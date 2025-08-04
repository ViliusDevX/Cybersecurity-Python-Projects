import ssl
import socket
from datetime import datetime, timezone
import sys

def get_cert_info(hostname, port=443):
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )

    try:
        conn.settimeout(5.0)
        conn.connect((hostname, port))
        cert = conn.getpeercert()
    except Exception as e:
        print(f"[!] Failed to connect or retrieve cert: {e}")
        return
    finally:
        conn.close()

    subject = dict(x[0] for x in cert['subject'])
    issued_to = subject.get('commonName', 'N/A')
    issuer = dict(x[0] for x in cert['issuer']).get('commonName', 'N/A')
    not_before = cert.get('notBefore')
    not_after = cert.get('notAfter')

    expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
    now = datetime.now(timezone.utc)
    days_left = (expiry_date.replace(tzinfo=timezone.utc) - now).days

    print(f"\n🔍 TLS Certificate Info for: {hostname}")
    print(f" - Issued To       : {issued_to}")
    print(f" - Issued By       : {issuer}")
    print(f" - Valid From      : {not_before}")
    print(f" - Expires On      : {not_after}")
    print(f" - Days Until Expiry: {days_left} days")
    print(f" - Status          : {'✅ Valid' if days_left > 0 else '❌ Expired'}")

if __name__ == "__main__":
    print("🔐 TLS Certificate Analyzer")
    user_host = input("Enter a domain (e.g., github.com): ").strip()

    if user_host:
        get_cert_info(user_host)
    else:
        print("[!] No domain entered.")
