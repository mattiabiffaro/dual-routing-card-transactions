# Card Transactions Simulator

## Video Demo: [Watch on Youtube](https://youtu.be/f7GdWSJweIc)

## Introduction
This project is meant to help issuing banks to test card transactions. An issuing bank is a financial institution that issues payment cards to individuals and firms, hereby called cardholders. On many card networks, such transactions are performed via the exchange of messages following the [ISO 8583](https://en.wikipedia.org/wiki/ISO_8583) protocol.

### Authorization flow
A simple transaction is carried out as follows at the authorization level:
1. The cardholder presents a card for a purchase
2. The merchant, via its Point of Sale (POS) device, processes the card and transaction information and sends it to his bank (the acquiring bank)
3. The acquiring bank generates an authorization request that it submits to the card network
4. The network pre-processes the request and forwards it to the issuing bank
5. The issuing bank approves or declines the transaction and sends back an authorization response
6. The network forwards the response to the acquiring bank
7. The acquiring bank forwards the response to the merchant
8. The merchant receives the authorization response and completes the transaction accordingly

### What the tool does
The Card Transaction Simulator can be used to generate ISO 8583 compliant messages and send them to an issuing bank to test how the system responds.

### How to use
#### Filling in the template
The user is required to compile a template in Excel format. This template contains a cell for each ISO 8583 Data Element, plus a few additional fields for increased usability. Not all fields need to be populated, as later the system will fill in the missing information to the best of its predictive capabilities. Then, the template needs to be converted to a .csv file.

#### Running the script
With the template ready, it is time to run the tool, which takes the following arguments
>python iso.py in/'input_file' (out/'output_file') ([--send, -s]) ([--logs, -l])

Where
- *iso.py* is the program name
- *in/'input_file'* is the name of the template, including its relative path (*in/*)
- *out/'output_file'* is an optional argument that allows the user to choose the name of the output file that will be generated. It includes its relative path (*out/*)
- *--send* or *-s* is an optional argument that dictates whether the output messages need to be sent to the issuing bank or just saved locally
- *--logs* or *-l* is an optional argument that specifies whether the message exchange needs to be saved in a .txt file in human readable format (raw ISO 8583 messages are not easy to read otherwise)
- *--help* or *-h* is an optional argument that stops the program execution and prints to the screen instructions on how to use iso.py

#### What the tool does when running
##### Message generation
Once executed, iso.py generates an output csv file with the raw ISO messages generated on the basis of what the user provided in the template. Missing information is filled in dynamically based on what is explicitely provided, such that the tool always produces formally correct messages that will not be discarded by the issuing bank due to formal errors. This functionality is implemented via the [csv module](https://docs.python.org/3/library/csv.html) in the Python standard library.

##### Data Transfer
If the optional send flag is provided, the ISO messages are sent via TCP/IP to a server commonly called ISO Listener, which - as the name implies - listens to ISO messages, approves or declines the transaction and generates the appropriate responses, which are in turn sent back to the TCP/IP client (that is, the device from where iso.py is running). This is managed via the [socket module](https://docs.python.org/3/library/socket.html) in the Python standard library.

##### Logs
Since raw ISO 8583 messages are not easy to read, using the logs flag triggers the production of a text file containing a neater version of the messages, displaying each field value on a separate row, prefixed by its field number.

### Code structure
#### Imports
The tool imports a series of modules from the standard library plus a local module (hereby referred to as the helper module) that defines the attributes of the ISO 8583 messages and their subfields (i.e. default values to be used, number of fields, field length, inheritance from other fields, whether default values need to be dynamically generated and how) via a Python class object. These attributes are in part standardized in the protocol itself and in part dependent on the specific implementation of the card network, of the issuing bank and of the card processor (a third party provider) of the latter.

#### main()
In the main function, the following happens:
1. Command line arguments are parsed (more in the argparse)
2. Files are opened for reading (input file) and for writing (output file and, optionally, logs file)
3. Iterating over every row in the input file, each cell is checked and - if it's populated - the corresponding value is assigned to the respective field, otherwise, the value is generated following the instructions contained in the helper module
4. The fields are then concatenated in a single raw ISO message
5. If the logs flag is active, the message is formatted neatly and written to the logs file
6. If the send flag is active, a socket is opened and the message is sent to a TCP/IP server. The socket then listens for a response and stores it. If the logs flag is also active, the response is stored in a variable, formatted and written to the logs file
7. Scenario name (an optional field in the template), ISO request, ISO response (when applicable) and ISO response code (when applicable) are written to the output file
8. All files and the TCP/IP socket are closed

#### argparse()
The argument parsing function performs the following checks:
* Whether an input file was passed via command line, otherwise it exits the program
* Whether an output filename was specified, otherwise it creates one that is equal to the name of the input file
* Whether one of the optional flags was used: the help flag that prints the possible parameters that the program takes and exits the program; the send flag for sending messages via TCP/IP; the logs flag for storing logs in a text file

#### format(message)
Formats the messages neatly by printing the fields one by one on a different row in a text file when the command line argument *--logs*  (or *-l* for short) is used.

#### send(message)
Sends messages to the ISO Listener (a TCP/IP server that listens to ISO messages) when the command line argument *--send* (or *-s* for short) is used. The function calls maintain_connection when ISO 8583 networking messages need to be sent.

#### maintain_connection(message)
An ISO Listener needs to receive ISO 8583 networking messages to keep the connection alive. maintain_connection is used to send an ISO 8583 sign on message when first called, echo messages to keep the connection alive every 5 other messages sent and finally a sign off message before the socket is closed.
