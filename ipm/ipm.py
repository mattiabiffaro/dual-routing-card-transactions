#!/usr/bin/env python3


"""Creates batch flat files based on NEXI's ALL interfaces related to clearing messages"""


# Import from Standard Library
import sys
import csv
import re
import os

# Import from local directories
import all912
import all907
import w_ftp
from helpers import esc


def main():
    args, interface = argparse()

    # Open files
    infile = open(args["in_filename"], encoding="utf-8-sig")
    outfile = open(args["out_filename"], "w")
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    # Generate records
    interface.records = reader  

    # Write header to the outfile
    writer.writerow([interface.header])

    # Write all records to the outfile
    for record in interface.records:
        writer.writerow([record])

    print(esc("green") + args["out_filename"] + esc("default") + " generated\n")

    # Close files
    infile.close()
    outfile.close()

    # Send files to Temenos FTP
    if args["transfer"] is True:
        send(args["out_filename"], args["t24_env"], args["filetype"].upper())

    sys.exit(0)

def argparse():
    """Parse arguments and check usage"""
    # Initialize variables
    args = {
        "filetype": "",
        "in_filename": "",
        "out_filename": "",
        "t24_env": "",
        "transfer": ""
    }
    ipm_path = "/Cards/ipm"
    out_path = ""

    # Check correct usage
    if not 2 <= len(sys.argv) <= 6 or "--help" in sys.argv or "-h" in sys.argv:
        sys.exit("Correct usage: ./ipm.py --gdf in/'input_file'.csv (out/'output_file'.csv) ([--send, -s]) ([--uat, --upg])")

    # Create out folder if it doesn't exist
    home = os.path.expanduser('~')
    if home == "/home/ubuntu":
        out_path = "/workspaces" + ipm_path + "/out"
    else:
        out_path = home + ipm_path + "/out"
    if not os.path.exists(out_path):
        os.mkdir(out_path) 

    # Parse arguments
    for arg in sys.argv:
        if re.match("^.*ipm.py", arg):
            pass
        elif arg in ["--gdf","--pdd"]:
            args["filetype"] = arg[2:]
        elif re.match("in/", arg):
            args["in_filename"] = arg
            if not re.match("^.*.csv$", args["in_filename"]):
                args["in_filename"] += ".csv"
        elif re.match("out/", arg):
            args["out_filename"] = arg
            if not re.match("^.*.csv$", args["out_filename"]):
                args["out_filename"] += ".csv"
        elif arg in ["--send", "-s"]:
            args["transfer"] = True
        elif arg in ["--upg", "--uat"]:
            args["t24_env"] = arg[2:].upper()
        else:
            sys.exit(f"{arg} is not a valid argument")

    if not args["filetype"]:
        sys.exit("Select a filetype like '--gdf' or '--pdd'")
    elif args["filetype"] == "gdf":
        interface = all912.Interface()
    elif args["filetype"] == "pdd":
        interface = all907.Interface()

    if not args["in_filename"]:
        sys.exit("Input file not specified. Type in/'filename'.csv to choose an input file")
    if not args["out_filename"]:
        args["out_filename"] = "out/" + interface.filename

    if args["transfer"] and not args["t24_env"]:
        args["t24_env"] = "UAT"

    return args, interface


def send(file, env, file_type):
    """Send files to T24 FTP server"""
    # Formal checks
    if file_type == "GDF" and not re.fullmatch(r"(out|pyt)/INK01\.D[0-9]{6}\.T[0-9]{6}\.P001", file):
        print("Output file must be named with the INK01.DYYMMDD.THHMMSS.P001 format in order to be sent via FTP")
        print(f"Try: ./ipm.py --{file_type.lower()} --{env.lower()} in/'filename'.csv -s")
        sys.exit(1)
    elif file_type == "PDD" and not re.fullmatch(r"(out|pyt)/PDD01\.D[0-9]{6}\.T[0-9]{6}\.P001", file):
        print("Output file must be named with the PDD01.DYYMMDD.THHMMSS.P001 format in order to be sent via FTP")
        print(f"Try: ./ipm.py --{file_type.lower()} --{env.lower()} in/'filename'.csv -s")
        sys.exit(1)

    # Assign credentials
    if env == "UAT" :
        address = "10.110.50.150"
        user = "ftpMedlabRead-UAT"
        password = "LO_12DVGTH2HT"
        if file_type == "GDF":
            directory = "/bnk.interface/FTPSIA-UAT/SiaCardsGDFT24In"
        elif file_type == "PDD":
             directory = "/bnk.interface/FTPSIA-UAT/SiaCardsPrePT24In"
    elif env == "UPG":
        address = "10.110.59.150"
        user = "ftpFlowe-Live"
        password = "LO_98RDV8CVH2AZ"
        if file_type == "GDF":
             directory = "/bnk.interface/FTPSIA-LIVE/SiaCardsGDFT24In"
        elif file_type == "PDD":
             directory = "/bnk.interface/FTPSIA-LIVE/SiaCardsPrePT24In"

    # Send file
    print(f"Sending {file} to Temenos {env}...")
    with w_ftp.FTP_TLS(host=address) as ftp:
            responses = {}
            responses["login"] = ftp.login(user=user, passwd=password)
            print(f"Temenos: {responses['login']}")
            ftp.prot_p()
            print(f"Changing directory to {directory}")
            responses["change_directory"] = ftp.cwd(directory)
            print(f"Temenos: {responses['change_directory']}")
            with open(file, "rb") as reader:
                cmd = "STOR " + file[4:]
                responses["transfer"] = ftp.storbinary(cmd, reader)
                print(f"Temenos: {responses['transfer']}")
                return responses


if __name__ == "__main__":
    main()