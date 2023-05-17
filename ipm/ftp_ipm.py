"""Send files to FTP server"""


# Import from local directories
import w_ftp


def send(file, env, file_type):

    # Assign credentials
    if env == "UAT":
        address = "XX.XXX.XX.XXX"
        user = "XXX-UAT"
        password = "XXX"
        if file_type == "GDF":
            directory = "XXX"
    elif env == "UPG":
        user = "XXX-UPG"
        address = "XX.XXX.XX.XXX"
        password = "XXX"
        if file_type == "GDF":
             directory = "XXX"

    # Send file
    with w_ftp.FTP_TLS(host=address) as ftp:
            responses = {}
            responses["login"] = ftp.login(user=user, passwd=password)
            print(f"FTP Server: {responses['login']}")
            ftp.prot_p()
            print(f"Changing directory to {directory}")
            responses["change_directory"] = ftp.cwd(directory)
            print(f"FTP Server: {responses['change_directory']}")
            with open(file, "rb") as reader:
                cmd = "STOR " + file[4:]
                responses["transfer"] = ftp.storbinary(cmd, reader)
                print(f"FTP Server: {responses['transfer']}")
