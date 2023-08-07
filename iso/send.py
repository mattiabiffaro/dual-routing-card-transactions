#!/usr/bin/env python3


# Import from Standard Library
import sys
import socket
socket.setdefaulttimeout(3)


def main():
    """Send ISO messages to Temenos UAT ISO Listener"""

    if len(sys.argv) != 2:
        print("Correct usage: ./send.py '[ISO message]'")
        sys.exit(1)

    # Convert the message to binary
    request = {}
    request["value"] = sys.argv[1]
    request["msg_type"] = request["value"][0:4]
    request["bitmap"] = request["value"][4:36]
    request["content"] = request["value"][36:]
    request["binary"] = request["msg_type"].encode("utf-8") + bytes.fromhex(request["bitmap"]) + request["content"].encode("utf-8")
    request["len"] = str(f"{len(request['binary']):04d}")
    request["binary"] = request["len"].encode("utf-8") + request["binary"]

    # Create a connection to the server application
    print("Opening socket")
    tcp_socket = socket.create_connection(('10.110.50.147', 462))

    # Send message
    try:

        feedback = tcp_socket.sendall(request["binary"])
        if feedback == None:
            print(f"Request ({str(int(request['len']))} bytes long): {request['value']} ")
            response = {}
            response["binary"] = tcp_socket.recv(1024)
            response["len"] = response["binary"][0:4].decode("utf-8")
            response["msg_type"] = response["binary"][4:8].decode("utf-8")
            response["bitmap"] = response["binary"][8:24].hex().upper()
            response["content"] = response["binary"][24:].decode("utf-8")
            response["value"] = response["msg_type"] + response["bitmap"] + response["content"]
            print(f"Response ({str(int(response['len']))} bytes long): {response['value']}")

    finally:
        print("Closing socket")
        tcp_socket.close()


if __name__ == "__main__":
    main()