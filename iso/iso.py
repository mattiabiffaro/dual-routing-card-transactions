#!/usr/bin/env python3

"""This program gets a CSV file containing transactional data as ISO 8583 fields and transforms it into full raw ISO 8583 messages.
It sends such messages to a TCP/IP server and stores both the requests messages and the responses from the server in a new CSV file"""


# Import from the Standard Library
import sys
import csv
import re
import datetime
import time
import socket
import os

# Import from local directories
import interface_specifications


# Global variables
flags = {
    "transfer": False,
    "logs": True
}
field = all956.Fields()
in_filename = ""
out_filename = ""
log_filename = ""
logfile = None
message_count = 0
tcp_socket = None
timeout_message = "Timeout"


def main():

    argparse()

    # Initialize variables
    global flags
    global message_count
    global logfile
    global field

    # Open files
    infile = open(in_filename, encoding="utf-8-sig")
    outfile = open(out_filename, "w")
    if flags["logs"] is True:
        logfile = open(log_filename, "a")

    reader = csv.DictReader(infile)
    if len(reader.fieldnames) != 131:
        print(f"{in_filename} contains an incorrect template")
        sys.exit(1)
    fieldnames = ["Scenario", "ISO Request", "ISO Response", "Response Code"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:

        # Update/reset variables
        message_count += 1
        response_code = ""

        # Update Reversal Indicator
        if row["Message Type"] in ["1420", "1421"] or re.match("^.*Reversal.*$", row["Preset"], re.IGNORECASE):

            field.reversal_indicator = True
            if row["Message Type"] == "":
                row["Message Type"] = "1420"

        else:
            field.reversal_indicator = False

        field.start()
        message = ""

        # Assign preset
        field.preset(row["Preset"])

        # Set message type
        if row["Message Type"] != "":
            field.val[0] = row["Message Type"]
        else:
            field.val[0] = field.def_val["Message Type"]

        # Set default merchant name
        if row["DE043 - Acceptor Name Location"] == "" and row["Scenario"] != "" and field.reversal_indicator is False:
            row["DE043 - Acceptor Name Location"] = rf"{row['Scenario']}"

        # Assign values to fields
        for i in range(3, field.count + 1):

            field_n = i - 1

            if row[reader.fieldnames[i]] == "":
                field.set(field.val[0], field_n)

            else:

                if field.subfield_count[field_n] != 1:
                    field.val[field_n] = field.check_substructure(row[reader.fieldnames[i]], field_n)
                else:
                    field.val[field_n] = rf"{row[reader.fieldnames[i]]}"

            field.padding(field_n)

            # Update message and bitmap
            field.update_bitmap(field.val[field_n])
            message += field.val[field_n]

        # Set bitmap
        field.set(field.val[0], 1)

        # Finalize message
        message = field.val[0] + field.val[1] + message

        if flags["logs"] is True:
            format(message)

        # Send message to ISO Listener
        if flags["transfer"] is True:
            response = send(message)
            if flags["logs"] is True:
                response_code = format(response)
        else:
            response = ""

        # Update the outfile
        writer.writerow({"Scenario": row["Scenario"], "ISO Request": message, "ISO Response": response, "Response Code": response_code})

    # Close files and sockets
    infile.close()
    outfile.close()
    if flags["transfer"] is True:
        send(network.get("signoff"))
        print("Closing socket\n")
        tcp_socket.close()
    print(all956.esc("green") + out_filename + all956.esc("default") + " generated")
    if flags["logs"] is True:
        print(all956.esc("green") + log_filename + all956.esc("default") + " generated")
        logfile.close()

    print()
    sys.exit(0)


def argparse():
    """Parses arguments from the terminal"""

    # Initialize variables
    global flags
    global in_filename
    global out_filename
    global log_filename
    global tcp_socket
    global network
    docker = False
    iso_path = "/Cards/iso"
    out_path = ""
    logs_path = ""

    # Check correct usage
    if not 2 <= len(sys.argv) <= 5 or "--help" in sys.argv or "-h" in sys.argv:
        print("Correct usage: ./iso.py in/'input_file'.csv (out/'output_file'.csv) ([--send, -s]) (--nologs)")
        sys.exit(1)

    # Create out folder if it doesn't exist
    home = os.path.expanduser('~')
    if home == "/home/ubuntu":
        docker = True
        out_path = "/workspaces" + iso_path + "/out"
    else:
        out_path = home + iso_path + "/out"
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    # parse arguments
    for arg in sys.argv:

        if re.match("^.*iso.py$", arg):
            pass

        elif re.match("in/", arg):

            in_filename = arg
            if not re.match("^.*.csv$", in_filename):
                in_filename += ".csv"

        elif re.match("out/", arg):

            out_filename = arg
            if not re.match("^.*.csv$", out_filename):
                out_filename += ".csv"

        elif arg in ["--send", "-s"]:

            # Setup TCP/IP connection
            flags["transfer"] = True
            socket.setdefaulttimeout(3)
            network = all956.Network()
            print("Opening socket\n")
            try:
                tcp_socket = socket.create_connection(('XX.XXX.XX.XXX', XXX))
            except TimeoutError:
                raise TimeoutError("Not able to establish a connection with the ISO Listener")

        elif arg == "--nologs":

            flags["logs"] = False

        else:

            if flags["transfer"]:
                print("Closing socket")
                tcp_socket.close()
            print(f"{arg} is not a valid argument")
            sys.exit(1)

    if in_filename == "":

        print("Input file not specified. Type in/'filename'.csv to choose an input file")
        sys.exit(1)

    if out_filename == "":

        out_filename = "out/" + in_filename[3:]

    if flags["logs"]:
            
        # Create logs path if it doesn't exist
            if docker is True:
                logs_path = "/workspaces" + iso_path + "/logs"
            else:
                logs_path = home + iso_path + "/logs"
            if not os.path.exists(logs_path):
                os.mkdir(logs_path)

            # Generate log filename
            log_filename = "logs/" + in_filename[3:-4] + "_" + datetime.datetime.today().strftime("%y%m%d%H%M%S") + ".txt"


def maintain_connection():
    """Defines when ISO 8583 network management messages need to be sent"""

    global message_count
    global timeout_message

    if message_count == 1:

        response = send(network.get("signon"))
        if response == timeout_message:
            print("Can't establish a connection")
            print("Closing socket\n")
            tcp_socket.close()
            sys.exit(2)

    elif (message_count / 5.0).is_integer():

        response = send(network.get("echo"))
        if response == timeout_message:
            print("Echo timeout")


def send(message):
    """Sends messages to the ISO Listener via TCP/IP"""

    global message_count
    global timeout_message

    if message[0:4] != network.mti:
        maintain_connection()

    # Convert the message to binary
    request = {}
    request["value"] = message
    request["msg_type"] = request["value"][0:4]
    request["bitmap"] = request["value"][4:36]
    request["content"] = request["value"][36:]
    request["binary"] = request["msg_type"].encode("utf-8") + bytes.fromhex(request["bitmap"]) + request["content"].encode("utf-8")
    request["len"] = str(f"{len(request['binary']):04d}")
    request["binary"] = request["len"].encode("utf-8") + request["binary"]

    try:

        # Send message
        feedback = tcp_socket.sendall(request["binary"])
        if feedback == None:
            print(f"Request ({str(int(request['len']))} bytes long): {request['value']} ")
            response = {}
            response["binary"] = tcp_socket.recv(1024)

    except TimeoutError:
        if message[0:4] != network.mti:
            print(f"Message n. {message_count} timed out\n")
        return f"{timeout_message}"

    # Format response
    response["len"] = response["binary"][0:4].decode("utf-8")
    response["msg_type"] = response["binary"][4:8].decode("utf-8")
    response["bitmap"] = response["binary"][8:24].hex().upper()
    response["content"] = response["binary"][24:].decode("utf-8")
    response["value"] = response["msg_type"] + response["bitmap"] + response["content"]
    print(f"Response ({str(int(response['len']))} bytes long): {response['value']}\n")

    time.sleep(2)
    return response["value"]


def format(message):
    """Format raw messages to make them human-readable"""

    # Initialize variables
    global logfile
    global timeout_message
    global field
    cursor = temp_cursor = next = 0
    binbitmap_len = 128
    hexbitmap_len = 32
    values = ["" for i in range(field.count)]

    if message[0:4] not in field.present.keys():
        logfile.write(f"{message}\n\n")
        return

    # Print Message Type
    next += field.len[0]
    message_type = message[cursor:next]
    logfile.write(f"<MSG-{message_type}>\n")
    cursor = next
    field.present[message_type][0] = True

    # Get hexadecimal bitmap
    next += hexbitmap_len
    hexbitmap = message[cursor:next]
    # Print hexadecimal bitmap
    logfile.write(f"    001<{hexbitmap}>\n")
    field.present[message_type][1] = True
    cursor = next

    # Convert bitmap to binary
    binbitmap = bin(int(hexbitmap, 16))[2:]

    # Take note of present fields
    for i in range(1, binbitmap_len):
        if binbitmap[i] == "1":
            field.present[message_type][i + 1] = True
        else:
            field.present[message_type][i + 1] = False

    # Print each field
    for i in range(2, binbitmap_len):
        if field.present[message_type][i]:
            # Check field length
            if field.var_len[i] == 0:
                next += field.len[i]
            else:
                next += field.var_len[i]
                temp_cursor = next
                next += int(message[cursor:next])
                cursor = temp_cursor
            # Extract field from string and print it
            values[i] = message[cursor:next]
            logfile.write(f"    {i:03d}<{values[i]}>\n")
            # Update cursor position
            cursor = next

    logfile.write("\n")

    if message_type in ["1110", "1130", "1430"]:
        return values[39]
    else:
        return


if __name__ == "__main__":
    main()
