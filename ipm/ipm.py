#!/usr/bin/env python3


"""Generate clearing transactions according to IPM specifications"""


# Import from Standard Library
import sys
import csv
import re
import os

# Import from local directories
import interface_specifications
import ftp_ipm
from helpers import esc


# Global variables
transfer = False
in_filename = ""
out_filename = ""
ftp_env = ""


def main():

    argparse()

    # Initialize variables
    field = interface_specifications.Fields()
    header = interface_specifications.Header()
    records = []

    # Open files
    infile = open(in_filename, encoding="utf-8-sig")
    outfile = open(out_filename, "w")

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        field.start()
        message = ""

        # Set default merchant name
        if row["Field 20 - Merchant Name"] == "" and row["Scenario"] != "":
            field.def_val[20] = row["Scenario"]

        # Assign preset
        if row["Preset"] != "":
            field.preset(row["Preset"])

        # Assign values to fields
        for i in range(2, field.count + 2):
            field_n = i - 1
            if row[reader.fieldnames[i]] == "":
                field.val[field_n] = field.set(field_n)
            else:
                field.val[field_n] = row[reader.fieldnames[i]]
            field.padding(field_n)

        # Generate message and store it in the records list
        for i in range(2, field.count + 2):
            field_n = i - 1
            message += field.val[field_n]
        records.append(message)

        # Update header
        header.update(field.val[31], field.val[32])

    # Write header to the outfile
    writer.writerow([header.get()])

    # Write all records to the outfile
    for record in records:
        writer.writerow([record])
    print(esc("green") + out_filename + esc("default") + " generated\n")

    # Close files
    infile.close()
    outfile.close()

    # Send files to FTP Server
    if transfer is True:
        if re.search("^out/INK01\.D[0-9]{6}\.T[0-9]{6}\.P001$", out_filename):
            print(f"Sending {out_filename} to FTP {ftp_env}...")
            ftp_ipm.send(out_filename, ftp_env, "GDF")
        else:
            print("Output file must be named with the INK01.DYYMMDD.THHMMSS.P001 format in order to be sent via FTP")
            print("Try: ./gdf.py in/'filename'.csv -s")
            sys.exit(1)

    sys.exit(0)


def argparse():
    """Parse arguments and check usage"""

    # Initialize variables
    global transfer
    global in_filename
    global out_filename
    global ftp_env
    gdf_path = "/dual-routing-card-transactions/ipm"
    out_path = ""
    filetype = ""

    # Check correct usage
    if not 2 <= len(sys.argv) <= 6 or "--help" in sys.argv or "-h" in sys.argv:
        print("Correct usage: ./ipm.py --gdf in/'input_file'.csv (out/'output_file'.csv) ([--send, -s]) ([--uat, --upg])")
        sys.exit(1)

    # Create out folder if it doesn't exist
    home = os.path.expanduser('~')
    if home == "/home/ubuntu":
        out_path = "/workspaces" + gdf_path + "/out"
    else:
        out_path = home + gdf_path + "/out"
    if not os.path.exists(out_path):
        os.mkdir(out_path) 

    # Parse arguments
    for arg in sys.argv:
        if re.match("^.*ipm.py", arg):
            pass
        elif arg in ["--gdf"]:
            filetype = arg[2:]
        elif re.match("in/", arg):
            in_filename = arg
            if not re.match("^.*.csv$", in_filename):
                in_filename += ".csv"
        elif re.match("out/", arg):
            out_filename = arg
            if not re.match("^.*.csv$", out_filename):
                out_filename += ".csv"
        elif arg in ["--send", "-s"]:
            transfer = True
        elif arg in ["--upg", "--uat"]:
            ftp_env = arg[2:].upper()
        else:
            print(f"{arg} is not a valid argument")
            sys.exit(1)

    if filetype == "":
        print("Select a filetype like '--gdf'")
        sys.exit(1)

    if in_filename == "":
        print("Input file not specified. Type in/'filename'.csv to choose an input file")
        sys.exit(1)
    if out_filename == "":
        out_filename = "out/" + interface_specifications.file_name()

    if transfer and ftp_env == "":
        ftp_env = "UAT"


if __name__ == "__main__":
    main()
