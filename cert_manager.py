"""Create ssl certificates for all1input."""
# based on: https://github.com/titeuf87/python3-tls-example
import random
import sys
import argparse
from os.path import isfile
from OpenSSL import crypto

from config import CONFIG as c

class FileExists(Exception):

    """File exists, we don't want overwrite it."""

def create_root_ca(root_cert_name):
    """
    Generate root ca certificate in `root_cert_name`.pem and `root_cert_name`.key.

    Raises FileExists if above mentioned files exist.
    """
    if isfile("{}.pem".format(root_cert_name)) or isfile("{}.key".format(root_cert_name)):
        raise FileExists()
    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 4096)

    cert = crypto.X509()
    cert.set_version(3)
    cert.set_serial_number(int(random.random() * sys.maxsize))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(60 * 60 * 24 * 365)

    subject = cert.get_subject()
    subject.CN = "example.com"
    subject.O = "all1input"

    issuer = cert.get_issuer()
    issuer.CN = "example.com"
    issuer.O = "all1input"

    cert.set_pubkey(pkey)
    cert.add_extensions([
        crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE"),
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=cert)])
    cert.add_extensions([crypto.X509Extension(
        b"authorityKeyIdentifier", False, b"keyid:always", issuer=cert)])
    cert.sign(pkey, "sha1")

    with open("{}.pem".format(root_cert_name), "wb") as certfile:
        certfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        certfile.close()

    with open("{}.key".format(root_cert_name), "wb") as pkeyfile:
        pkeyfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        pkeyfile.close()

def create_certificate(cert_name, serverside, root_cert_name, ip=None):
    """
    Create signed certificate.

    cert_name: name - `cert_name`.crt and `cert_name`.key are created
    serverside: bool - is this a server certificate
    root_cert_name: name of root ca cert to use
    ip: ip address of the server

    Raises FileExists if cert files exist.
    """
    cert_filename = "{}.crt".format(cert_name)
    pkey_filename = "{}.key".format(cert_name)
    if isfile(cert_filename) or isfile(pkey_filename):
        raise FileExists()
    rootpem = open("{}.pem".format(root_cert_name), "rb").read()
    rootkey = open("{}.key".format(root_cert_name), "rb").read()
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, rootpem)
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, rootkey)

    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.set_serial_number(int(random.random() * sys.maxsize))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(60 * 60 * 24 * 365)
    cert.set_version(3)

    subject = cert.get_subject()
    subject.CN = cert_name
    subject.O = "all1input"

    if serverside:
        cert.add_extensions([crypto.X509Extension(
            b"subjectAltName",
            False,
            b"IP:{}".format(ip))])

    cert.set_issuer(ca_cert.get_subject())

    cert.set_pubkey(pkey)
    cert.sign(ca_key, "sha1")


    with open(cert_filename, "wb") as certfile:
        certfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        certfile.close()

    with open(pkey_filename, "wb") as pkeyfile:
        pkeyfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        pkeyfile.close()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        prog="cert_manager",
        description='Create certificates for all1input.')
    PARSER.add_argument(
        'action',
        choices=["all", "client"],
        help=("all: create root, server and client cert from config |"
              "client: creates client certificate with NAME"))
    PARSER.add_argument(
        "--name",
        default="client",
        help="certificate name to use for client certificate")

    ARGS = PARSER.parse_args()

    if ARGS.action == "all":
        try:
            print("Making root CA")
            create_root_ca(c.root_cert_name)
        except FileExists:
            print("Root CA already exists")
        try:
            print("Making server certificate")
            create_certificate(c.server_cert_name, True, c.root_cert_name, c.ip)
        except FileExists:
            print("Server cert already exists")
        try:
            print("Making client certificate")
            create_certificate(c.cert_name, False, c.root_cert_name)
        except FileExists:
            print("Client cert already exists")
    elif ARGS.action == "client":
        print("Making client certificate")
        create_certificate(ARGS.name, False, c.root_cert_name)
