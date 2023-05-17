"""Creates objects representing records and interface attributes from the ISO8583 interface specifications"""


# Import modules from the Standard Library
import datetime
import random


# Global variables
RAND_MAX6 = 0xF423F # Max value randgen can generate when limit is RAND_MAX6 (6 dgitis)
RAND_MAX12 = 0xE8D4A50FFF # Max value randgen can generate when limit is RAND_MAX12 (12 digits)
codes6 = {0} # Codes already used by randgen when limit is RAND_MAX6
codes12 = {0} # Codes already used by randgen when limit is RAND_MAX12


class Network:
    """Defines networking messages"""

    def __init__(self, mti = "1804", bitmap = "80300100000000200000000C00000000", destination = "0512928", originator = "0512928", signon = "", echo = "", signoff = ""):

        self.mti = mti
        self.bitmap = bitmap
        self.destination = destination
        self.originator = originator
        self.signon = signon
        self.echo = echo
        self.signoff = signoff

    def get(self, type):

        STAN = str(f"{randgen(RAND_MAX6):06d}")
        timestamp = datetime.datetime.today().strftime("%y%m%d%H%M%S")

        match type:

            case "signon":

                function = "801"
                transport_data = "0200316Stratus HalloMsg"

            case "echo":

                function = "831"
                transport_data = "0190316Stratus EchoMsg"

            case "signoff":

                function = "802"
                transport_data = "0220316Stratus HalloMsg"

        return (self.mti + self.bitmap + STAN + timestamp + function + transport_data + self.destination + self.originator)


class Fields:
    """Defines the attributes of message fields"""

    def __init__(self, count = 129, bitmap = "", val = [], present = {}, len = [], var_len = [], dynamic = [], def_val = {}, inheritance = {}, padding_type = [], amount_counter = 0, reversal_indicator = False, original_data = {}, subfield_count = [], subfield_val = [], subfield_type = [], subfield_present = {}, subfield_def_val = {}, subfield_dynamic = []):

        self.count = count # Number of fields. Note that DE000 is the message type
        self.bitmap = bitmap
        self.val = val # Field value
        self.present = present # Defines if a field is supposed to be present for a given message type
        self.present["1100"] = []
        self.present["1110"] = []
        self.present["1120"] = self.present["1121"] = []
        self.present["1130"] = []
        self.present["1420"] = self.present["1421"] = []
        self.present["1430"] = []
        self.len = len # Field length. Note that it indicates the max threshold for variable length fields
        self.var_len = var_len # Defines which fields have variable length and how many bytes must be used as a prefix to declare the actual length
        self.dynamic = dynamic # Defines whether the field's default value is set dynamically
        self.def_val = def_val # Defines static default values for non-dynamic fields
        self.def_val["Message Type"] = ""
        self.def_val["1100"] = []
        self.def_val["1110"] = []
        self.def_val["1120"] = self.def_val["1121"] = []
        self.def_val["1130"] = []
        self.def_val["1420"] = self.def_val["1421"] = []
        self.def_val["1430"] = []
        self.inheritance = inheritance # Defines values for fields inheriting them from other fields
        self.padding_type = padding_type # Defines what character to use when applying padding
        self.amount_counter = amount_counter # Counter for default values of fields containing amounts of some kind
        self.reversal_indicator = reversal_indicator # Defines whether the next transaction is a reversal
        self.original_data = original_data # Preserves previous transaction data for reversal requests
        self.original_data = {
            0: "",
            2: "",
            3: "",
            4: "",
            6: "",
            11: "",
            12: "",
            22: "",
            26: "",
            32: "",
            33: "",
            37: "",
            38: "",
            42: "",
            43: "",
            49: "",
            51: "",
            63: "",
            102: ""
        }
        self.subfield_count = subfield_count
        self.subfield_val = subfield_val
        self.subfield_type = subfield_type
        self.subfield_present = subfield_present
        self.subfield_present["1100"] = []
        self.subfield_present["1120"] = self.subfield_present["1121"] = []
        self.subfield_present["1420"] = self.subfield_present["1421"] = []
        self.subfield_def_val = subfield_def_val
        self.subfield_def_val["1100"] = []
        self.subfield_def_val["1120"] = self.subfield_def_val["1121"] = []
        self.subfield_def_val["1420"] = self.subfield_def_val["1421"] = []
        self.subfield_dynamic = subfield_dynamic

        # Initialize fields up to to self.count
        for i in range(self.count):
            self.val.append("")
            self.present["1100"].append(False)
            self.present["1110"].append(False)
            self.present["1120"].append(False)
            self.present["1121"].append(False)
            self.present["1130"].append(False)
            self.present["1420"].append(False)
            self.present["1421"].append(False)
            self.present["1430"].append(False)
            self.len.append(0)
            self.var_len.append(0)
            self.dynamic.append(False)
            self.def_val["1100"].append("")
            self.def_val["1110"].append("")
            self.def_val["1120"].append("")
            self.def_val["1121"].append("")
            self.def_val["1130"].append("")
            self.def_val["1420"].append("")
            self.def_val["1421"].append("")
            self.def_val["1430"].append("")
            self.padding_type.append("0")
            self.subfield_count.append(1)
            self.subfield_val.append([])
            self.subfield_type.append(None)
            self.subfield_val[i].append("")
            self.subfield_val[i].append("")
            self.subfield_present["1100"].append([])
            self.subfield_present["1100"][i].append(False)
            self.subfield_present["1100"][i].append(False)
            self.subfield_present["1120"].append([])
            self.subfield_present["1120"][i].append(False)
            self.subfield_present["1120"][i].append(False)
            self.subfield_present["1121"].append([])
            self.subfield_present["1121"][i].append(False)
            self.subfield_present["1121"][i].append(False)
            self.subfield_present["1420"].append([])
            self.subfield_present["1420"][i].append(False)
            self.subfield_present["1420"][i].append(False)
            self.subfield_present["1421"].append([])
            self.subfield_present["1421"][i].append(False)
            self.subfield_present["1421"][i].append(False)
            self.subfield_def_val["1100"].append([])
            self.subfield_def_val["1100"][i].append("")
            self.subfield_def_val["1100"][i].append("")
            self.subfield_def_val["1120"].append([])
            self.subfield_def_val["1120"][i].append("")
            self.subfield_def_val["1120"][i].append("")
            self.subfield_def_val["1121"].append([])
            self.subfield_def_val["1121"][i].append("")
            self.subfield_def_val["1121"][i].append("")
            self.subfield_def_val["1420"].append([])
            self.subfield_def_val["1420"][i].append("")
            self.subfield_def_val["1420"][i].append("")
            self.subfield_def_val["1421"].append([])
            self.subfield_def_val["1421"][i].append("")
            self.subfield_def_val["1421"][i].append("")
            self.subfield_dynamic.append([])
            self.subfield_dynamic[i].append(False)
            self.subfield_dynamic[i].append(False)

        # Set static attributes

        # Field 0 - Message Type
        self.len[0] = 4
        # Field 1 - Bitmap
        self.len[1] = 32
        self.dynamic[1] = True
        # Field 2 - PAN
        self.len[2] = 19
        self.var_len[2] = 2
        # Field 3 - Processing Code
        self.len[3] = 6
        # Field 4 - Amount, Transaction
        self.len[4] = 12
        self.padding_type[4] = "amount"
        # Field 6 - Amount, Cardholder Billing
        self.len[6] = 12
        self.padding_type[6] = "amount"
        # Field 11 - System Trace Audit Number
        self.len[11] = 6
        self.dynamic[11] = True
        # Field 12 - Date And Time - Local Transaction
        self.len[12] = 12
        # Field 14 - Date, Expiration
        self.len[14] = 4
        self.padding_type[14] = "*"
        # Field 22 - Point Of Service Data Code
        self.len[22] = 12
        self.subfield_count[22] = 12
        self.subfield_type[22] = ""
        for i in range(self.subfield_count[22] - 1):
            self.subfield_val[22].append("")
            self.subfield_present["1100"][22].append(False)
            self.subfield_def_val["1100"][22].append("")
            self.subfield_present["1120"][22].append(False)
            self.subfield_def_val["1120"][22].append("")
            self.subfield_present["1121"][22].append(False)
            self.subfield_def_val["1121"][22].append("")
            self.subfield_present["1420"][22].append(False)
            self.subfield_def_val["1420"][22].append("")
            self.subfield_present["1421"][22].append(False)
            self.subfield_def_val["1421"][22].append("")
            self.subfield_dynamic[22].append(False)
        # Field 23 - Card Sequence Number
        self.len[23] = 3
        # Field 24 - Function Code
        self.len[24] = 3
        # Field 25 - Reason Code
        self.len[25] = 4
        # Field 26 - Card Acceptor Business Code
        self.len[26] = 4
        # Field 32 - Acquiring Institution Identification Code
        self.len[32] = 11
        self.var_len[32] = 2
        # Field 33 - Forwarding Institution Identification Code
        self.len[33] = 11
        self.var_len[33] = 2
        # Field 37 - Retrieval Reference Number
        self.len[37] = 12
        self.dynamic[37] = True
        # Field 38 - Approval Code
        self.len[38] = 6
        self.dynamic[38] = True
        # Field 39 - Action Code
        self.len[39] = 3
        # Field 41 - Card Acceptor Terminal Identification
        self.len[41] = 8
        self.padding_type[41] = " "
        # Field 42 - Card Acceptor Identification Code
        self.len[42] = 15
        self.padding_type[42] = " "
        # Field 43 - Card Acceptor Name/Location
        self.len[43] = 99
        self.var_len[43] = 2
        self.padding_type[43] = " "
        self.subfield_count[43] = 4
        self.subfield_type[43] = "\\"
        for i in range(self.subfield_count[43] - 1):
            self.subfield_val[43].append("")
            self.subfield_present["1100"][43].append(False)
            self.subfield_def_val["1100"][43].append("")
            self.subfield_present["1120"][43].append(False)
            self.subfield_def_val["1120"][43].append("")
            self.subfield_present["1121"][43].append(False)
            self.subfield_def_val["1121"][43].append("")
            self.subfield_present["1420"][43].append(False)
            self.subfield_def_val["1420"][43].append("")
            self.subfield_present["1421"][43].append(False)
            self.subfield_def_val["1421"][43].append("")
            self.subfield_dynamic[43].append(False)
        # Field 46 - Amount Fee
        self.len[46] = 9
        self.var_len[46] = 3
        # Field 48 - Additional Data
        self.len[48] = 999
        self.var_len[48] = 3
        # Field 49 - Currency Code, Transaction
        self.len[49] = 3
        # Field 51 - Currency Code, Cardholder Billing
        self.len[51] = 3
        # Field 54 - Amounts, Additional
        self.len[54] = 120
        self.var_len[54] = 3
        # Field 56 - Original Data Elements
        self.len[56] = 35
        self.var_len[56] = 2
        self.dynamic[56] = True
        # Field 59 - Transport Data
        self.len[59] = 999
        self.var_len[59] = 3
        # Field 63 - Network Data
        self.len[63] = 999
        self.var_len[63] = 3
        self.dynamic[63] = True
        self.subfield_count[63] = 25
        self.subfield_type[63] = "tags"
        for i in range(self.subfield_count[63] - 1):
            self.subfield_val[63].append("")
            self.subfield_present["1100"][63].append(False)
            self.subfield_def_val["1100"][63].append("")
            self.subfield_present["1120"][63].append(False)
            self.subfield_def_val["1120"][63].append("")
            self.subfield_present["1121"][63].append(False)
            self.subfield_def_val["1121"][63].append("")
            self.subfield_present["1420"][63].append(False)
            self.subfield_def_val["1420"][63].append("")
            self.subfield_present["1421"][63].append(False)
            self.subfield_def_val["1421"][63].append("")
            self.subfield_dynamic[63].append(False)
        self.subfield_dynamic[63][1] = True
        self.subfield_dynamic[63][2] = True
        # Field 93 - Transaction Destination Institution Identification Code
        self.len[93] = 11
        self.var_len[93] = 2
        # Field 94 - Transaction Originator Institution Identification Code
        self.len[94] = 11
        self.var_len[94] = 2
        # Field 100 - Receiving Institution Identification Code
        self.len[100] = 11
        self.var_len[100] = 2
        # Field 102 - Account Identification 1
        self.len[102] = 23 # It is 28 in ALL956, but 23 is used in the actual messages
        self.var_len[102] = 2
        # Field 116 - POST Data
        self.len[116] = 255
        self.var_len[116] = 3
        self.subfield_count[116] = 14
        self.subfield_type[116] = ""
        for i in range(self.subfield_count[116] - 1):
            self.subfield_val[116].append("")
            self.subfield_present["1100"][116].append(False)
            self.subfield_def_val["1100"][116].append("")
            self.subfield_present["1120"][116].append(False)
            self.subfield_def_val["1120"][116].append("")
            self.subfield_present["1121"][116].append(False)
            self.subfield_def_val["1121"][116].append("")
            self.subfield_present["1420"][116].append(False)
            self.subfield_def_val["1420"][116].append("")
            self.subfield_present["1421"][116].append(False)
            self.subfield_def_val["1421"][116].append("")
            self.subfield_dynamic[116].append(False)

    def start(self):
        """Sets the value of subclass objects, except for dynamic objects, which are set in the dynaset or inherit methods"""

        # Preserve original data if needed
        if self.reversal_indicator is True:
            for key in self.original_data:
                if self.var_len[key] != 0:
                    self.original_data[key] = self.val[key][self.var_len[key]:]
                else:
                    self.original_data[key] = self.val[key]

        # Reset all attributes
        for i in range(self.count):
            self.val[i] = ""
            self.present["1100"][i] = self.present["1120"][i] = self.present["1420"][i] = False
            self.def_val["1100"][i] = self.def_val["1120"][i] = self.def_val["1420"][i] = ""
            if self.subfield_count[i] != 1:
                for j in range(self.subfield_count[i] + 1):
                    self.subfield_present["1100"][i][j] = self.subfield_present["1120"][i][j] = self.subfield_present["1420"][i][j] = False
                    self.subfield_def_val["1100"][i][j] = self.subfield_def_val["1120"][i][j] = self.subfield_def_val["1420"][i][j] = ""
                    self.subfield_val[i][j] = ""

        # Update counters
        self.amount_counter += 1

        # Define the default value and properties of each data element

        # Field 0 - Message Type
        self.def_val["Message Type"] = "1100"
        # Field 1 - Bitmap
        self.present["1100"][1] = self.present["1120"][1] = self.present["1420"][1] = True
        self.bitmap = "1"
        # Field 2 - PAN
        self.present["1100"][2] = self.present["1120"][2] = self.present["1420"][2] = True
        self.def_val["1100"][2] = self.def_val["1120"][2] = self.def_val["1420"][2] = "557383******9999"
        # Field 3 - Processing Code
        self.present["1100"][3] = self.present["1120"][3] = self.present["1420"][3] = True
        self.def_val["1100"][3] = self.def_val["1120"][3] = self.def_val["1420"][3] = "000000"
        # Field 4 - Amount, Transaction
        self.dynamic[4] = True
        self.present["1100"][4] = self.present["1120"][4] = self.present["1420"][4] = True
        # Field 6 - Amount, Cardholder Billing
        self.inheritance[6] = 4
        self.present["1100"][6] = self.present["1120"][6] = self.present["1420"][6] = True
        # Field 11 - System Trace Audit Number
        self.present["1100"][11] = self.present["1120"][11] = self.present["1420"][11] = True
        # Field 12 - Date And Time - Local Transaction
        self.present["1100"][12] = self.present["1120"][12] = self.present["1420"][12] = True
        self.def_val["1100"][12] = self.def_val["1120"][12] = self.def_val["1420"][12] = datetime.datetime.today().strftime("%y%m%d%H%M%S")
        # Field 14 - Date, Expiration
        self.present["1100"][14] = self.present["1120"][14] = True
        self.def_val["1100"][14] = self.def_val["1120"][14] = "****"
        # Field 22 - Point Of Service Data Code
        self.present["1100"][22] = self.present["1120"][22] = self.present["1420"][22] = True
        self.def_val["1100"][22] = self.def_val["1120"][22] = self.def_val["1420"][22] = "L10101L5500C"
        self.subfield_present["1100"][22][1] = self.subfield_present["1120"][22][1] = self.subfield_present["1420"][22][1] = True
        self.subfield_def_val["1100"][22][1] = self.subfield_def_val["1120"][22][1] = self.subfield_def_val["1420"][22][1] = "L"
        self.subfield_present["1100"][22][2] = self.subfield_present["1120"][22][2] = self.subfield_present["1420"][22][2] = True
        self.subfield_def_val["1100"][22][2] = self.subfield_def_val["1120"][22][2] = self.subfield_def_val["1420"][22][2] = "1"
        self.subfield_present["1100"][22][3] = self.subfield_present["1120"][22][3] = self.subfield_present["1420"][22][3] = True
        self.subfield_def_val["1100"][22][3] = self.subfield_def_val["1120"][22][3] = self.subfield_def_val["1420"][22][3] = "0"
        self.subfield_present["1100"][22][4] = self.subfield_present["1120"][22][4] = self.subfield_present["1420"][22][4] = True
        self.subfield_def_val["1100"][22][4] = self.subfield_def_val["1120"][22][4] = self.subfield_def_val["1420"][22][4] = "1"
        self.subfield_present["1100"][22][5] = self.subfield_present["1120"][22][5] = self.subfield_present["1420"][22][5] = True
        self.subfield_def_val["1100"][22][5] = self.subfield_def_val["1120"][22][5] = self.subfield_def_val["1420"][22][5] = "0"
        self.subfield_present["1100"][22][6] = self.subfield_present["1120"][22][6] = self.subfield_present["1420"][22][6] = True
        self.subfield_def_val["1100"][22][6] = self.subfield_def_val["1120"][22][6] = self.subfield_def_val["1420"][22][6] = "1"
        self.subfield_present["1100"][22][7] = self.subfield_present["1120"][22][7] = self.subfield_present["1420"][22][7] = True
        self.subfield_def_val["1100"][22][7] = self.subfield_def_val["1120"][22][7] = self.subfield_def_val["1420"][22][7] = "L"
        self.subfield_present["1100"][22][8] = self.subfield_present["1120"][22][8] = self.subfield_present["1420"][22][8] = True
        self.subfield_def_val["1100"][22][8] = self.subfield_def_val["1120"][22][8] = self.subfield_def_val["1420"][22][8] = "5"
        self.subfield_present["1100"][22][9] = self.subfield_present["1120"][22][9] = self.subfield_present["1420"][22][9] = True
        self.subfield_def_val["1100"][22][9] = self.subfield_def_val["1120"][22][9] = self.subfield_def_val["1420"][22][9] = "5"
        self.subfield_present["1100"][22][10] = self.subfield_present["1120"][22][10] = self.subfield_present["1420"][22][10] = True
        self.subfield_def_val["1100"][22][10] = self.subfield_def_val["1120"][22][10] = self.subfield_def_val["1420"][22][10] = "0"
        self.subfield_present["1100"][22][11] = self.subfield_present["1120"][22][11] = self.subfield_present["1420"][22][11] = True
        self.subfield_def_val["1100"][22][11] = self.subfield_def_val["1120"][22][11] = self.subfield_def_val["1420"][22][11] = "0"
        self.subfield_present["1100"][22][12] = self.subfield_present["1120"][22][12] = self.subfield_present["1420"][22][12] = True
        self.subfield_def_val["1100"][22][12] = self.subfield_def_val["1120"][22][12] = self.subfield_def_val["1420"][22][12] = "C"
        # Field 23 - Card Sequence Number
        self.present["1100"][23] = self.present["1120"][23] = self.present["1420"][23] = True
        self.def_val["1100"][23] = self.def_val["1120"][23] = self.def_val["1420"][23] = "000"
        # Field 24 - Function Code
        self.present["1100"][24] = self.present["1120"][24] = self.present["1420"][24] = True
        self.def_val["1100"][24] = self.def_val["1120"][24] = "100"
        self.def_val["1420"][24] = "400"
        # Field 25 - Reason Code
        self.present["1120"][25] = self.present["1420"][25] = True
        self.def_val["1120"][25] = self.def_val["1420"][25] = "1403"
        # Field 26 - Card Acceptor Business Code
        self.present["1100"][26] = self.present["1120"][26] = True
        self.def_val["1100"][26] = self.def_val["1120"][26] = "5999"
        # Field 32 - Acquiring Institution Identification Code
        self.present["1100"][32] = self.present["1120"][32] = self.present["1420"][32] = True
        self.def_val["1100"][32] = self.def_val["1120"][32] = self.def_val["1420"][32] = "999701"
        # Field 33 - Forwarding Institution Identification Code
        self.present["1100"][33] = self.present["1120"][33] = self.present["1420"][33] = True
        self.def_val["1100"][33] = self.def_val["1120"][33] = self.def_val["1420"][33] = "12928"
        # Field 37 - Retrieval Reference Number
        self.present["1100"][37] = self.present["1120"][37] = self.present["1420"][37] = True
        # Field 38 - Approval Code
        self.present["1100"][38] = self.present["1120"][38] = self.present["1420"][38] = True
        # Field 39 - Action Code
        self.present["1120"][39] = True
        self.def_val["1120"][39] = "000"
        # Field 41 - Card Acceptor Terminal Identification
        self.present["1100"][41] = self.present["1120"][41] = self.present["1420"][41] = True
        self.def_val["1100"][41] = self.def_val["1120"][41] = self.def_val["1420"][41] = "MTF TEST"
        # Field 42 - Card Acceptor Identification Code
        self.present["1100"][42] = self.present["1120"][42] = self.present["1420"][42] = True
        self.def_val["1100"][42] = self.def_val["1120"][42] = self.def_val["1420"][42] = "ABC123TESTMTF19"
        # Field 43 - Card Acceptor Name/Location
        self.present["1100"][43] = self.present["1120"][43] = True
        self.def_val["1100"][43] = self.def_val["1120"][43] = r"Untitled\\Milan\             ITA"
        self.subfield_present["1100"][43][1] = self.subfield_present["1120"][43][1] = True
        self.subfield_def_val["1100"][43][1] = self.subfield_def_val["1120"][43][1] = "Untitled"
        self.subfield_present["1100"][43][2] = self.subfield_present["1120"][43][2] = True
        self.subfield_def_val["1100"][43][2] = self.subfield_def_val["1120"][43][2] = ""
        self.subfield_present["1100"][43][3] = self.subfield_present["1120"][43][3] = True
        self.subfield_def_val["1100"][43][3] = self.subfield_def_val["1120"][43][3] = "Milan"
        self.subfield_present["1100"][43][4] = self.subfield_present["1120"][43][4] = True
        self.subfield_def_val["1100"][43][4] = self.subfield_def_val["1120"][43][4] = "             ITA"
        # Field 49 - Currency Code, Transaction
        self.present["1100"][49] = self.present["1120"][49] = self.present["1420"][49] = True
        self.def_val["1100"][49] = self.def_val["1120"][49] = self.def_val["1420"][49] = "978"
        # Field 51 - Currency Code, Cardholder Billing
        self.present["1100"][51] = self.present["1120"][51] = self.present["1420"][51] = True
        self.def_val["1100"][51] = self.def_val["1120"][51] = self.def_val["1420"][51] = "978"
        # Field 56 - Original Data Elements
        self.present["1420"][56] = True
        # Field 63 - Network Data
        self.present["1100"][63] = self.present["1120"][63] = self.present["1420"][63] = True
        self.subfield_present["1100"][63][1] = self.subfield_present["1120"][63][1] = True
        self.subfield_present["1420"][63][2] = True
        self.subfield_present["1100"][63][5] = True
        self.subfield_def_val["1100"][63][5] = "0"
        # Field 93 - Transaction Destination Institution Identification Code
        self.present["1100"][93] = self.present["1120"][93] = self.present["1420"][93] = True
        self.def_val["1100"][93] = self.def_val["1120"][93] = self.def_val["1420"][93] = "12928"
        # Field 94 - Transaction Originator Institution Identification Code
        self.present["1100"][94] = self.present["1120"][94] = self.present["1420"][94] = True
        self.def_val["1100"][94] = self.def_val["1120"][94] = self.def_val["1420"][94] = "999701"
        # Field 100 - Receiving Institution Identification Code
        self.present["1100"][100] = self.present["1120"][100] = self.present["1420"][100] = True
        self.def_val["1100"][100] = self.def_val["1120"][100] = self.def_val["1420"][100] = "00000000000"
        # Field 102 - Account Identification 1
        self.present["1100"][102] = self.present["1120"][102] = self.present["1420"][102] = True
        self.def_val["1100"][102] = self.def_val["1120"][102] = self.def_val["1420"][102] = "600501992609           "
        # Field 116 - POS Data
        self.present["1100"][116] = self.present["1120"][116] = self.present["1420"][116] = True
        self.def_val["1100"][116] = self.def_val["1120"][116] = self.def_val["1420"][116] = "102510000660038063301-1234"
        self.subfield_present["1100"][116][1] = self.subfield_present["1120"][116][1] = self.subfield_present["1420"][116][1] = True
        self.subfield_def_val["1100"][116][1] = self.subfield_def_val["1120"][116][1] = self.subfield_def_val["1420"][116][1] = "1"
        self.subfield_present["1100"][116][2] = self.subfield_present["1120"][116][2] = self.subfield_present["1420"][116][2] = True
        self.subfield_def_val["1100"][116][2] = self.subfield_def_val["1120"][116][2] = self.subfield_def_val["1420"][116][2] = "0"
        self.subfield_present["1100"][116][3] = self.subfield_present["1120"][116][3] = self.subfield_present["1420"][116][3] = True
        self.subfield_def_val["1100"][116][3] = self.subfield_def_val["1120"][116][3] = self.subfield_def_val["1420"][116][3] = "2"
        self.subfield_present["1100"][116][4] = self.subfield_present["1120"][116][4] = self.subfield_present["1420"][116][4] = True
        self.subfield_def_val["1100"][116][4] = self.subfield_def_val["1120"][116][4] = self.subfield_def_val["1420"][116][4] = "5"
        self.subfield_present["1100"][116][5] = self.subfield_present["1120"][116][5] = self.subfield_present["1420"][116][5] = True
        self.subfield_def_val["1100"][116][5] = self.subfield_def_val["1120"][116][5] = self.subfield_def_val["1420"][116][5] = "1"
        self.subfield_present["1100"][116][6] = self.subfield_present["1120"][116][6] = self.subfield_present["1420"][116][6] = True
        self.subfield_def_val["1100"][116][6] = self.subfield_def_val["1120"][116][6] = self.subfield_def_val["1420"][116][6] = "0"
        self.subfield_present["1100"][116][7] = self.subfield_present["1120"][116][7] = self.subfield_present["1420"][116][7] = True
        self.subfield_def_val["1100"][116][7] = self.subfield_def_val["1120"][116][7] = self.subfield_def_val["1420"][116][7] = "0"
        self.subfield_present["1100"][116][8] = self.subfield_present["1120"][116][8] = self.subfield_present["1420"][116][8] = True
        self.subfield_def_val["1100"][116][8] = self.subfield_def_val["1120"][116][8] = self.subfield_def_val["1420"][116][8] = "0"
        self.subfield_present["1100"][116][9] = self.subfield_present["1120"][116][9] = self.subfield_present["1420"][116][9] = True
        self.subfield_def_val["1100"][116][9] = self.subfield_def_val["1120"][116][9] = self.subfield_def_val["1420"][116][9] = "0"
        self.subfield_present["1100"][116][10] = self.subfield_present["1120"][116][10] = self.subfield_present["1420"][116][10] = True
        self.subfield_def_val["1100"][116][10] = self.subfield_def_val["1120"][116][10] = self.subfield_def_val["1420"][116][10] = "6"
        self.subfield_present["1100"][116][11] = self.subfield_present["1120"][116][11] = self.subfield_present["1420"][116][11] = True
        self.subfield_def_val["1100"][116][11] = self.subfield_def_val["1120"][116][11] = self.subfield_def_val["1420"][116][11] = "6"
        self.subfield_present["1100"][116][12] = self.subfield_present["1120"][116][12] = self.subfield_present["1420"][116][12] = True
        self.subfield_def_val["1100"][116][12] = self.subfield_def_val["1120"][116][12] = self.subfield_def_val["1420"][116][12] = "00"
        self.subfield_present["1100"][116][13] = self.subfield_present["1120"][116][13] = self.subfield_present["1420"][116][13] = True
        self.subfield_def_val["1100"][116][13] = self.subfield_def_val["1120"][116][13] = self.subfield_def_val["1420"][116][13] = "380"
        self.subfield_present["1100"][116][14] = self.subfield_present["1120"][116][14] = self.subfield_present["1420"][116][14] = True
        self.subfield_def_val["1100"][116][14] = self.subfield_def_val["1120"][116][14] = self.subfield_def_val["1420"][116][14] = "63301-1234"

    def preset(self, preset):
        """Updates default values according to predefined templates"""

        # Apply preset
        match preset:

            case "" | "Purchase Contactless":
                pass

            case "Moneysend":
                
                self.def_val["1100"][3] = self.def_val["1120"][3] = self.def_val["1420"][3] = "280000"
                self.def_val["1100"][22] = self.def_val["1120"][22] = self.def_val["1420"][22] = "100050J00011"
                self.def_val["1100"][26] = self.def_val["1120"][26] = "6537"
                self.def_val["1100"][43] = self.def_val["1120"][43] = r"Untitled\\Luxembourg\             LUX"
                self.def_val["1100"][116] = self.def_val["1120"][116] = self.def_val["1420"][116] = "1025100006000442"
                self.subfield_def_val["1100"][22][1] = self.subfield_def_val["1120"][22][1] = self.subfield_def_val["1420"][22][1] = "1"
                self.subfield_def_val["1100"][22][2] = self.subfield_def_val["1120"][22][2] = self.subfield_def_val["1420"][22][2] = "0"
                self.subfield_def_val["1100"][22][4] = self.subfield_def_val["1120"][22][4] = self.subfield_def_val["1420"][22][4] = "0"
                self.subfield_def_val["1100"][22][5] = self.subfield_def_val["1120"][22][5] = self.subfield_def_val["1420"][22][5] = "5"
                self.subfield_def_val["1100"][22][6] = self.subfield_def_val["1120"][22][6] = self.subfield_def_val["1420"][22][6] = "0"
                self.subfield_def_val["1100"][22][7] = self.subfield_def_val["1120"][22][7] = self.subfield_def_val["1420"][22][7] = "J"
                self.subfield_def_val["1100"][22][8] = self.subfield_def_val["1120"][22][8] = self.subfield_def_val["1420"][22][8] = "0"
                self.subfield_def_val["1100"][22][9] = self.subfield_def_val["1120"][22][9] = self.subfield_def_val["1420"][22][9] = "0"
                self.subfield_def_val["1100"][22][11] = self.subfield_def_val["1120"][22][11] = self.subfield_def_val["1420"][22][11] = "1"
                self.subfield_def_val["1100"][22][12] = self.subfield_def_val["1120"][22][12] = self.subfield_def_val["1420"][22][12] = "1"
                self.subfield_def_val["1100"][43][3] = self.subfield_def_val["1120"][43][3] = "Luxembourg"
                self.subfield_def_val["1100"][43][4] = self.subfield_def_val["1120"][43][4] = "             LUX"
                self.subfield_present["1100"][63][6] = self.subfield_present["1120"][63][6] = self.subfield_present["1420"][63][6] = True
                self.subfield_def_val["1100"][63][6] = self.subfield_def_val["1120"][63][6] = self.subfield_def_val["1420"][63][6] = "C04"
                self.subfield_present["1100"][63][7] = self.subfield_present["1120"][63][7] = self.subfield_present["1420"][63][7] = True
                self.subfield_def_val["1100"][63][7] = self.subfield_def_val["1120"][63][7] = self.subfield_def_val["1420"][63][7] = "02"
                self.subfield_present["1100"][63][25] = self.subfield_present["1120"][63][25] = self.subfield_present["1420"][63][25] = True
                self.subfield_def_val["1100"][63][25] = self.subfield_def_val["1120"][63][25] = "PY"
                self.subfield_def_val["1420"][63][25] = "PYR"
                self.subfield_def_val["1100"][116][11] = self.subfield_def_val["1120"][116][11] = self.subfield_def_val["1420"][116][11] = "0"
                self.subfield_def_val["1100"][116][13] = self.subfield_def_val["1120"][116][13] = self.subfield_def_val["1420"][116][13] = "442"
                self.subfield_def_val["1100"][116][14] = self.subfield_def_val["1120"][116][14] = self.subfield_def_val["1420"][116][14] = ""

            case "AFD PreAuth":
                
                self.def_val["1100"][22] = self.def_val["1420"][22] = "51010155500C"
                self.def_val["1100"][24] = "170"
                self.def_val["1100"][26] = "5542"
                self.def_val["1100"][116] = self.def_val["1420"][116] = "101000400130038081024     "
                self.subfield_def_val["1100"][22][1] = self.subfield_def_val["1120"][22][1] = self.subfield_def_val["1420"][22][1] = "5"
                self.subfield_def_val["1100"][22][7] = self.subfield_def_val["1120"][22][7] = self.subfield_def_val["1420"][22][7] = "5"
                self.subfield_def_val["1100"][63][5] = "1"
                self.subfield_def_val["1100"][116][3] = self.subfield_def_val["1120"][116][3] = self.subfield_def_val["1420"][116][3] = "1"
                self.subfield_def_val["1100"][116][4] = self.subfield_def_val["1120"][116][4] = self.subfield_def_val["1420"][116][4] = "0"
                self.subfield_def_val["1100"][116][5] = self.subfield_def_val["1120"][116][5] = self.subfield_def_val["1420"][116][5] = "0"
                self.subfield_def_val["1100"][116][7] = self.subfield_def_val["1120"][116][7] = self.subfield_def_val["1420"][116][7] = "4"
                self.subfield_def_val["1100"][116][10] = self.subfield_def_val["1120"][116][10] = self.subfield_def_val["1420"][116][10] = "1"
                self.subfield_def_val["1100"][116][11] = self.subfield_def_val["1120"][116][11] = self.subfield_def_val["1420"][116][11] = "3"
                self.subfield_def_val["1100"][116][14] = self.subfield_def_val["1120"][116][14] = self.subfield_def_val["1420"][116][14] = "81024     "

            case "AFD Advice":

                self.def_val["Message Type"] = "1120"
                self.def_val["1120"][22] = self.def_val["1420"][22] = "51010155500C"
                self.def_val["1120"][24] = "171"
                self.def_val["1120"][25] = "1404"
                self.def_val["1120"][26] = "5542"
                self.def_val["1120"][116] = self.def_val["1420"][116] = "101000400130038081024     "
                self.subfield_def_val["1100"][22][1] = self.subfield_def_val["1120"][22][1] = self.subfield_def_val["1420"][22][1] = "5"
                self.subfield_def_val["1100"][22][7] = self.subfield_def_val["1120"][22][7] = self.subfield_def_val["1420"][22][7] = "5"
                self.subfield_present["1100"][63][5] = False
                self.subfield_def_val["1120"][116][3] = self.subfield_def_val["1420"][116][3] = "1"
                self.subfield_def_val["1120"][116][4] = self.subfield_def_val["1420"][116][4] = "0"
                self.subfield_def_val["1120"][116][5] = self.subfield_def_val["1420"][116][5] = "0"
                self.subfield_def_val["1120"][116][7] = self.subfield_def_val["1420"][116][7] = "4"
                self.subfield_def_val["1120"][116][10] = self.subfield_def_val["1420"][116][10] = "1"
                self.subfield_def_val["1120"][116][11] = self.subfield_def_val["1420"][116][11] = "3"
                self.subfield_def_val["1120"][116][14] = self.subfield_def_val["1420"][116][14] = "81024     "

            case "Withdrawal":
                
                self.def_val["1100"][3] = self.def_val["1120"][3] = self.def_val["1420"][3] = "010000"
                self.def_val["1100"][22] = self.def_val["1120"][22] = self.def_val["1420"][22] = "511201515046"
                self.def_val["1100"][26] = self.def_val["1120"][26] = "6011"
                self.def_val["1100"][116] = self.def_val["1120"][116] = self.def_val["1420"][116] = "100001000050038080131     "
                self.subfield_def_val["1100"][22][1] = self.subfield_def_val["1120"][22][1] = self.subfield_def_val["1420"][22][1] = "5"
                self.subfield_def_val["1100"][22][3] = self.subfield_def_val["1120"][22][3] = self.subfield_def_val["1420"][22][3] = "1"
                self.subfield_def_val["1100"][22][4] = self.subfield_def_val["1120"][22][4] = self.subfield_def_val["1420"][22][4] = "2"
                self.subfield_def_val["1100"][22][7] = self.subfield_def_val["1120"][22][7] = self.subfield_def_val["1420"][22][7] = "5"
                self.subfield_def_val["1100"][22][8] = self.subfield_def_val["1120"][22][8] = self.subfield_def_val["1420"][22][8] = "1"
                self.subfield_def_val["1100"][22][11] = self.subfield_def_val["1120"][22][11] = self.subfield_def_val["1420"][22][11] = "4"
                self.subfield_def_val["1100"][22][12] = self.subfield_def_val["1120"][22][12] = self.subfield_def_val["1420"][22][12] = "6"   
                self.subfield_def_val["1100"][116][3] = self.subfield_def_val["1120"][116][3] = self.subfield_def_val["1420"][116][3] = "0"
                self.subfield_def_val["1100"][116][4] = self.subfield_def_val["1120"][116][4] = self.subfield_def_val["1420"][116][4] = "0"
                self.subfield_def_val["1100"][116][5] = self.subfield_def_val["1120"][116][5] = self.subfield_def_val["1420"][116][5] = "0"
                self.subfield_def_val["1100"][116][6] = self.subfield_def_val["1120"][116][6] = self.subfield_def_val["1420"][116][6] = "1"
                self.subfield_def_val["1100"][116][10] = self.subfield_def_val["1120"][116][10] = self.subfield_def_val["1420"][116][10] = "0"
                self.subfield_def_val["1100"][116][11] = self.subfield_def_val["1120"][116][11] = self.subfield_def_val["1420"][116][11] = "5"
                self.subfield_def_val["1100"][116][14] = self.subfield_def_val["1120"][116][14] = self.subfield_def_val["1420"][116][14] = "80131     "

            case "Refund":

                self.def_val["1100"][3] = self.def_val["1120"][3] = self.def_val["1420"][3] = "200000"
                self.def_val["1100"][22] = self.def_val["1120"][22] = self.def_val["1420"][22] = "Z00140Z00001"
                self.def_val["1100"][116] = self.def_val["1120"][116] = self.def_val["1420"][116] = "102410000600025075013     "
                self.subfield_def_val["1100"][22][1] = self.subfield_def_val["1120"][22][1] = self.subfield_def_val["1420"][22][1] = "Z"
                self.subfield_def_val["1100"][22][2] = self.subfield_def_val["1120"][22][2] = self.subfield_def_val["1420"][22][2] = "0"
                self.subfield_def_val["1100"][22][5] = self.subfield_def_val["1120"][22][5] = self.subfield_def_val["1420"][22][5] = "4"
                self.subfield_def_val["1100"][22][6] = self.subfield_def_val["1120"][22][6] = self.subfield_def_val["1420"][22][6] = "0"
                self.subfield_def_val["1100"][22][7] = self.subfield_def_val["1120"][22][7] = self.subfield_def_val["1420"][22][7] = "Z"
                self.subfield_def_val["1100"][22][8] = self.subfield_def_val["1120"][22][8] = self.subfield_def_val["1420"][22][8] = "0"
                self.subfield_def_val["1100"][22][9] = self.subfield_def_val["1120"][22][9] = self.subfield_def_val["1420"][22][9] = "0"
                self.subfield_def_val["1100"][22][12] = self.subfield_def_val["1120"][22][12] = self.subfield_def_val["1420"][22][12] = "1"
                self.subfield_def_val["1100"][116][4] = self.subfield_def_val["1120"][116][4] = self.subfield_def_val["1420"][116][4] = "4"
                self.subfield_def_val["1100"][116][11] = self.subfield_def_val["1120"][116][11] = self.subfield_def_val["1420"][116][11] = "0"
                self.subfield_def_val["1100"][116][13] = self.subfield_def_val["1120"][116][13] = self.subfield_def_val["1420"][116][13] = "250"
                self.subfield_def_val["1100"][116][14] = self.subfield_def_val["1120"][116][14] = self.subfield_def_val["1420"][116][14] = "75013     "

            case "Payment IQ":
                
                self.def_val["1100"][3] = self.def_val["1120"][3] = self.def_val["1420"][3] = "280000"
                self.def_val["1100"][22] = self.def_val["1120"][22] = self.def_val["1420"][22] = "100050J00011"
                self.def_val["1100"][26] = self.def_val["1120"][26] = "6537"
                self.def_val["1100"][43] = self.def_val["1120"][43] = r"Untitled\\Luxembourg\             LUX"
                self.def_val["1100"][116] = self.def_val["1120"][116] = self.def_val["1420"][116] = "1025100006000442"
                self.subfield_def_val["1100"][22][1] = self.subfield_def_val["1120"][22][1] = self.subfield_def_val["1420"][22][1] = "1"
                self.subfield_def_val["1100"][22][2] = self.subfield_def_val["1120"][22][2] = self.subfield_def_val["1420"][22][2] = "0"
                self.subfield_def_val["1100"][22][4] = self.subfield_def_val["1120"][22][4] = self.subfield_def_val["1420"][22][4] = "0"
                self.subfield_def_val["1100"][22][5] = self.subfield_def_val["1120"][22][5] = self.subfield_def_val["1420"][22][5] = "5"
                self.subfield_def_val["1100"][22][6] = self.subfield_def_val["1120"][22][6] = self.subfield_def_val["1420"][22][6] = "0"
                self.subfield_def_val["1100"][22][7] = self.subfield_def_val["1120"][22][7] = self.subfield_def_val["1420"][22][7] = "J"
                self.subfield_def_val["1100"][22][8] = self.subfield_def_val["1120"][22][8] = self.subfield_def_val["1420"][22][8] = "0"
                self.subfield_def_val["1100"][22][9] = self.subfield_def_val["1120"][22][9] = self.subfield_def_val["1420"][22][9] = "0"
                self.subfield_def_val["1100"][22][11] = self.subfield_def_val["1120"][22][11] = self.subfield_def_val["1420"][22][11] = "1"
                self.subfield_def_val["1100"][22][12] = self.subfield_def_val["1120"][22][12] = self.subfield_def_val["1420"][22][12] = "1"
                self.subfield_def_val["1100"][43][3] = self.subfield_def_val["1120"][43][3] = "Luxembourg"
                self.subfield_def_val["1100"][43][4] = self.subfield_def_val["1120"][43][4] = "             LUX"
                self.subfield_present["1100"][63][6] = self.subfield_present["1120"][63][6] = self.subfield_present["1420"][63][6] = True
                self.subfield_def_val["1100"][63][6] = self.subfield_def_val["1120"][63][6] = self.subfield_def_val["1420"][63][6] = "C68"
                self.subfield_present["1100"][63][7] = self.subfield_present["1120"][63][7] = self.subfield_present["1420"][63][7] = True
                self.subfield_def_val["1100"][63][7] = self.subfield_def_val["1120"][63][7] = self.subfield_def_val["1420"][63][7] = "02"
                self.subfield_present["1100"][63][25] = self.subfield_present["1120"][63][25] = self.subfield_present["1420"][63][25] = True
                self.subfield_def_val["1100"][63][25] = self.subfield_def_val["1120"][63][25] = "IQ"
                self.subfield_def_val["1420"][63][25] = "IQR"
                self.subfield_def_val["1100"][116][11] = self.subfield_def_val["1120"][116][11] = self.subfield_def_val["1420"][116][11] = "0"
                self.subfield_def_val["1100"][116][13] = self.subfield_def_val["1120"][116][13] = self.subfield_def_val["1420"][116][13] = "442"
                self.subfield_def_val["1100"][116][14] = self.subfield_def_val["1120"][116][14] = self.subfield_def_val["1420"][116][14] = ""

            case "Purchase With Cashback":

                self.def_val["1100"][3] = self.def_val["1120"][3] = self.def_val["1420"][3] = "090000"

            case "Purchase DKK":

                self.inheritance.pop(6)
                self.dynamic[4] = False
                self.def_val["1100"][4] = self.def_val["1120"][4] = str(self.amount_counter * 7)
                self.def_val["1100"][6] = self.def_val["1120"][6] = str(self.amount_counter)
                self.subfield_present["1100"][63][9] = self.subfield_present["1120"][63][9] = True
                self.subfield_dynamic[63][9] = True

            case "Purchase MDES":

                self.subfield_present["1100"][63][10] = self.subfield_present["1120"][63][10] = True
                self.subfield_def_val["1100"][63][10] = self.subfield_def_val["1120"][63][10] = "50110030273" # Apple Pay
                self.subfield_present["1100"][63][11] = self.subfield_present["1120"][63][11] = True
                self.subfield_def_val["1100"][63][11] = self.subfield_def_val["1120"][63][11] = "5167648699999999"
                self.subfield_present["1100"][63][12] = self.subfield_present["1120"][63][12] = True
                self.subfield_def_val["1100"][63][12] = self.subfield_def_val["1120"][63][12] = "C"

            case "Purchase 3DS":

                self.subfield_present["1100"][63][23] = self.subfield_present["1120"][63][23] = True
                self.subfield_def_val["1100"][63][23] = self.subfield_def_val["1120"][63][23] = "kBNYW3cMyr4uVCcQgenZtJeBqvxO"

            case "Advice Decline":

                self.def_val["Message Type"] = "1120"
                self.present["1120"][39] = True
                self.def_val["1120"][39] = "100"
                self.subfield_present["1120"][63][14] = True
                self.subfield_def_val["1120"][63][14] = "15492"

            case _:

                print(f"\"{preset}\" is not a valid preset. Transaction will be treated as \"Purchase Contactless\"\n")

        # Set attributes for repeat messages by copying what is set for original messages
        for i in range(self.count):
            self.present["1121"][i] = self.present["1120"][i]
            self.present["1421"][i] = self.present["1420"][i]
            self.def_val["1121"][i] = self.def_val["1120"][i]
            self.def_val["1421"][i] = self.def_val["1420"][i]
            if self.subfield_count[i] != 1:
                for j in range(self.subfield_count[i] + 1):
                    self.subfield_present["1121"][i][j] = self.subfield_present["1120"][i][j]
                    self.subfield_present["1421"][i][j] = self.subfield_present["1420"][i][j]
                    self.subfield_def_val["1121"][i][j] = self.subfield_def_val["1120"][i][j]
                    self.subfield_def_val["1421"][i][j] = self.subfield_def_val["1420"][i][j]

    def inherit(self, n):
        """Sets values for fields inheriting them from other fields"""

        self.val[n] = self.val[self.inheritance[n]]

    def padding(self, n):
        """Applies padding to get to the required field length"""

        if len(self.val[n]) > self.len[n]:
            raise ValueError(f"Value of field {n} exceeds maximum length {self.len[n]}")

        if self.val[n] == "":
            return
        
        match self.var_len[n]:

            case 0:
                if self.padding_type[n] == " ":
                    while len(self.val[n]) != self.len[n]:
                        self.val[n] += self.padding_type[n]
                elif self.padding_type[n] == "amount":
                    if len(self.val[n]) != self.len[n] and self.val[n] != "":
                        self.val[n] = str(round(float(self.val[n]) * 100))
                    while len(self.val[n]) != self.len[n]:
                        self.val[n] = "0" + self.val[n]
                else:
                    while len(self.val[n]) != self.len[n]:
                        self.val[n] = self.padding_type[n] + self.val[n]

            case 2:
                if n == 102:
                    while len(self.val[n]) != self.len[n]:
                        self.val[n] += " "  
                self.val[n] = str(f"{len(self.val[n]):02d}") + rf"{self.val[n]}"

            case 3:
                self.val[n] = str(f"{len(self.val[n]):03d}") + rf"{self.val[n]}"

    def dynaset(self, field):
        """Sets the value of dynamic fields"""

        match field:

            case 1:
                return self.iso_hex()

            case 4:
                if self.reversal_indicator is False:
                    return str(self.amount_counter)
                else:
                    return self.original_data[field]

            case 11:
                return str(f"{randgen(RAND_MAX6):06d}")

            case 37:
                return str(f"{randgen(RAND_MAX12):012d}")

            case 38:
                if self.reversal_indicator is False:
                    return str(f"{randgen(RAND_MAX6):06d}")
                else:
                    return self.original_data[field]

            case 56:
                if self.reversal_indicator is False:
                    return ("1100" + str(f"{randgen(RAND_MAX6):06d}") + datetime.datetime.today().strftime("%y%m%d%H%M%S") + str(f"{len(self.def_val['1100'][32]):02d}") + self.def_val["1100"][32])
                else:
                    return (self.original_data[0] + self.original_data[11] + self.original_data[12] + self.original_data[32])

            case 63:
                return self.check_substructure("", field)

    def check_substructure(self, value, n):
        """Checks the subfields inside a data element and fills in the missing ones when they are expected"""

        result = ""
        val_len = len(value)

        if self.subfield_type[n] == None:
            return

        elif self.subfield_type[n] == "tags":

            next = 0

            # Check which tags are present
            for i in range(self.subfield_count[n]):

                if next == val_len:
                    break

                # Store the tag number in subfield_elements
                cursor = next
                next += 2
                try:
                    tag_n = int(value[cursor:next])
                except ValueError:
                    raise ValueError(
                        f"\"{value}\" is not a valid subfields set. DE063 subfields must be prefixed with tag id and tag length (e.g."
                        + esc("red") + "01"
                        + esc("blue") + "09"
                        + esc("green") + "MDU999999"
                        + esc("red") + "05"
                        + esc("blue") + "01"
                        + esc("green") + "0"
                        + esc("default") + ")"
                        )
                self.subfield_present[self.val[0]][n][tag_n] = True

                # Get the tag length
                cursor = next
                next += 2
                tag_len = int(value[cursor:next])

                # Get the tag value
                cursor = next
                next += tag_len
                self.subfield_val[n][tag_n] = value[cursor:next]

            # Set subfield value
            for tag, present in enumerate(self.subfield_present[self.val[0]][n]):

                if present and self.subfield_val[n][tag] == "":

                    if self.reversal_indicator is True and n in self.original_data.keys():
                        self.subfield_val[n][tag] = self.extract_original_subfield(n, tag)

                    elif self.subfield_dynamic[n][tag]:
                        self.subfield_val[n][tag] = self.subfield_dynaset(n, tag)

                    else:
                        self.subfield_val[n][tag] = self.subfield_def_val[self.val[0]][n][tag]

            # Compose field value
            for tag, val in enumerate(self.subfield_val[n]):
                if val != "" and self.subfield_present[self.val[0]][n][tag]:
                    result += (str(f"{tag:02d}") + str(f"{len(val):02d}") + val)

        else:

            # Extract subfields
            if self.subfield_type[n] == "":

                if n == 116 and val_len > 12:

                    subfield_list = list(value[0:11])
                    subfield_list.append(value[11:13])

                    if val_len > 15:

                        subfield_list.append(value[13:16])

                        if val_len > 16:
                            subfield_list.append(value[16:])

                else:
                    subfield_list = list(value)

            else:
                subfield_list = value.split(f"{self.subfield_type[n]}")

            # Set subfield value
            if self.subfield_type[n] == "":

                for key, val in enumerate(subfield_list):
                    if val.strip() != "":
                        self.subfield_present[self.val[0]][n][key + 1] = True
                        self.subfield_val[n][key + 1] = val

            else:

                for key, val in enumerate(subfield_list):
                    self.subfield_present[self.val[0]][n][key + 1] = True
                    self.subfield_val[n][key + 1] = val

            for tag, present in enumerate(self.subfield_present[self.val[0]][n]):

                if present and (self.subfield_val[n][tag] == "" or (self.subfield_type[n] and self.subfield_val[n][tag] in ["", " "])):

                    if self.reversal_indicator is True and n in self.original_data.keys():
                        self.subfield_val[n][tag] = self.extract_original_subfield(n, tag)

                    elif self.subfield_dynamic[n][tag]:
                        self.subfield_val[n][tag] = self.subfield_dynaset(n, tag)

                    else:
                        self.subfield_val[n][tag] = self.subfield_def_val[self.val[0]][n][tag]

            # Compose field value
            for tag, val in enumerate(self.subfield_val[n]):
                if self.subfield_present[self.val[0]][n][tag]:
                    result += (rf"{val}" + rf"{self.subfield_type[n]}")

            if self.subfield_type[n] != "":
                result = result[0:-1]

        return result

    def extract_original_subfield(self, field, subfield):
        """Gets a specific subfield from self.original_data"""

        if self.subfield_type[field] == None:
            return

        elif self.subfield_type[field] == "tags":

            if field == 63 and subfield == 2:
                subfield = 1

            next = 0

            for i in range(self.subfield_count[field]):

                if next == len(self.original_data[field]):
                    break

                # Get the tag number
                cursor = next
                next += 2
                tag_n = int(self.original_data[field][cursor:next])

                # Get the tag length
                cursor = next
                next += 2
                tag_len = int(self.original_data[field][cursor:next])

                # Get the tag value
                cursor = next
                next += tag_len
                tag_value = self.original_data[field][cursor:next]

                # Extract value if it's the desired one
                if tag_n == subfield:
                    if field == 63 and tag_n == 25:
                        return (tag_value + "R")
                    else:
                        return tag_value

    def subfield_dynaset(self, field, subfield):
        """Sets the value of dynamic subfields"""

        if field == 63:
            if subfield == 1:
                return ("MDU" + str(f"{randgen(RAND_MAX6):06d}"))
            
            elif subfield == 2:
                return ("MDU" + str(f"{randgen(RAND_MAX6):06d}") + datetime.datetime.today().strftime("%m%d") + "  ")
            
            elif subfield == 9:

                result = float(self.val[4]) / float(self.val[6])
                s_result = str(result)
                decimal = str(len(s_result) - (s_result.find(".") + 1))
                return (decimal + s_result.replace(".", "") + "C" + "000000")          

    def set(self, type, n):
        """Checks the attributes of a field and sets the default value accordingly"""

        if self.present[type][n] is False:
            return ""

        if self.dynamic[n] is True:
            self.val[n] = self.dynaset(n)
        elif n in self.inheritance:
            self.inherit(n)
        elif self.reversal_indicator is True and n in self.original_data.keys():
            self.val[n] = self.original_data[n]
        else:
            self.val[n] = self.def_val[type][n]

    def update_bitmap(self, value):
        """Builds the bitmap (DE001) of the ISO message"""

        if value == "":
            self.bitmap += "0"
        else:
            self.bitmap += "1"

    def iso_hex(self):
        """Transforms the bitmap from binary to hexadecimal"""

        # Initialize variables
        cursor = 0
        bitmap_len = len(self.bitmap)
        hex_bitmap = ""

        # Build hexadecimal bitmap
        while cursor < bitmap_len:

            next = cursor + 4
            hex_bitmap += hex(int(self.bitmap[cursor:next], 2))[2:].upper()
            cursor = next

        return hex_bitmap


def randgen(limit):
    """Generates single use integers pseudo-randomly"""

    random.seed()
    x = 0

    if limit == RAND_MAX6:
        while x in codes6:
            x = random.randint(0, limit)
        codes6.add(x)
    elif limit == RAND_MAX12:
        while x in codes12:
            x = random.randint(0, limit)
        codes12.add(x)

    return x

def esc(code):
    """Easily apply ANSI text color formatting"""

    match code:
        case "default":
            code = 0
        case "red":
            code = 31
        case "green":
            code = 32
        case "blue":
            code = 34
        case _:
            code = 0

    return f"\033[{code}m"
