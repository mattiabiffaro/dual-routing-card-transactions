"""Creates objects representing records and interface attributes from NEXI's ALL912"""


# Import modules from the Standard Library
import datetime
import helpers
import string
import csv

# Import from local directories
from intrf_specs import Standard_Header, Standard_Fields


class Interface():
    """Instantiates all elements of an interface"""
    def __init__(self):
        self.header = self.Header()
        self.field = self.Fields()
        self.filename = self.Filename.get()

    @property
    def records(self):
        return self._records
    
    @records.setter
    def records(self, reader):
        if not isinstance(reader, csv.DictReader):
            raise ValueError(f"Invalid records.setter type: {type(reader)}")
        
        self._records = []
        
        for row in reader:
            message = ""
            self.field.start(row["Scenario"], row["Preset"])

            # Assign values to fields
            for i in range(2, self.field.count + 2):
                field_n = i - 1
                field_id = reader.fieldnames[i]
                self.field.set(field_n, row[field_id])

            # Generate message and store it in the records list
            for i in range(2, self.field.count + 2):
                field_n = i - 1
                message += self.field.val[field_n]
            self.records.append(message)

            # Update header
            self.header.update(*self.field.header_info)  
            
        return self._records


    class Header(Standard_Header):
        """Defines the attribute of the header record and its subfields"""
        def __init__(self):
            super().__init__(subfield_count=9)

            # Set the value of subclass objects
            self.subfield_len[1] = 4
            self.subfield_val[1] = "1386"
            self.subfield_len[2] = 6
            self.subfield_val[2] = datetime.date.today().strftime("%y%m%d")
            self.subfield_len[3] = 9
            self.subfield_val[3] = 0 # Will be updated with the number of records
            self.subfield_len[4] = 9
            self.subfield_val[4] = 0 # Will be updated with the number of records with field 32 == DB
            self.subfield_len[5] = 15
            self.subfield_val[5] = 0 # Will be updated with the sum of fields 31 when field 32 == DB
            self.subfield_len[6] = 9
            self.subfield_val[6] = 0 # Will be updated with the number of records with field 32 == CR
            self.subfield_len[7] = 15
            self.subfield_val[7] = 0 # Will be updated with the sum of fields 31 when field 32 == CR
            self.subfield_len[8] = 3
            self.subfield_val[8] = datetime.date.today().strftime("%j")
            self.subfield_len[9] = 0
            self.subfield_val[9] = "" # Filler, not used yet

        def update(self, amount, sign):
            """Updates the values of the subfields based on the record fields data"""
            self.subfield_val[3] += 1
            if sign == "DB":
                self.subfield_val[4] += 1
                self.subfield_val[5] += int(amount)
            else:
                self.subfield_val[6] += 1
                self.subfield_val[7] += int(amount)


    class Fields(Standard_Fields):
        """Defines the attributes of detail record fields"""
        def __init__(self):
            super().__init__(count = 99)

        def start(self, scenario, user_preset):
            """Sets the value of subclass objects, except for dynamic objects, which are set in the dynaset or inherit methods"""
            super().start()

            # Define the default value and properties of each record field

            # Field 1 - Group
            self.len[1] = 4
            self.def_val[1] = "INTR"
            # Field 2 - Acquirer ID
            self.len[2] = 6
            self.def_val[2] = "513086"
            self.padding_type[2] = "0"
            # Field 3 - Transaction Type
            self.len[3] = 2
            self.def_val[3] = "05"
            # Field 4 - Reversal Indicator
            self.len[4] = 1
            self.def_val[4] = ""
            # Field 5 - Transaction Mode
            self.len[5] = 2
            self.def_val[5] = "M"
            # Field 6 - Transaction Source
            self.len[6] = 2
            self.def_val[6] = "PO"
            # Field 7 - Transaction Date
            self.len[7] = 6
            self.def_val[7] = datetime.date.today().strftime("%y%m%d")
            # Field 8 - Card No.
            self.len[8] = 19
            self.def_val[8] = "5573********9999"
            # Field 9 - Authorization Code
            self.len[9] = 6
            self.dynamic[9] = True
            self.def_val[9] = ""
            self.padding_type[9] = "0"
            # Field 10 - Card Scheme ID
            self.len[10] = 1
            self.def_val[10] = "M"
            # Field 11 - Additional Info
            self.len[11] = 21
            self.def_val[11] = ""
            # Field 12 - Visa Settlement Flag
            self.len[12] = 1
            self.def_val[12] = ""
            # Field 13 - Fraud Indicator
            self.len[13] = 1
            self.def_val[13] = ""
            # Field 14 - Source Amount In Trans. Cur.
            self.len[14] = 13
            self.dynamic[14] = True
            self.padding_type[14] = "amount"
            self.def_val[14] = ""
            # Field 15 - Transaction Sign
            self.len[15] = 2
            self.def_val[15] = "DB" # CR for credit transactions
            # Field 16 - Trans. Currency Code
            self.len[16] = 3
            self.def_val[16] = "EUR"
            # Field 17 - Amount In Settlement Currency
            self.len[17] = 13
            self.inheritance[17] = 14
            self.padding_type[17] = "amount"
            self.def_val[17] = ""
            # Field 18 - Amount Sign
            self.len[18] = 2
            self.inheritance[18] = 15
            self.def_val[18] = ""
            # Field 19 - Settlement Currency Code
            self.len[19] = 3
            self.def_val[19] = "EUR"
            # Field 20 - Merchant Name
            self.len[20] = 25
            if scenario:
                self.def_val[20] = scenario
            else:
                self.def_val[20] = "Untitled"
            # Field 21 - MCC
            self.len[21] = 4
            self.def_val[21] = "5999"
            self.padding_type[21] = "0"
            # Field 22 - Town
            self.len[22] = 13
            self.def_val[22] = "Vegas"
            # Field 23 - State
            self.len[23] = 3
            self.def_val[23] = "ITA"
            # Field 24 - Agency Of Current Acc.
            self.len[24] = 4
            self.padding_type[24] = "0"
            self.def_val[24] = ""
            # Field 25 - Current Account No.
            self.len[25] = 20
            self.def_val[25] = "600501992609"
            # Field 26 - Current Account Currency
            self.len[26] = 3
            self.inheritance[26] = 19
            self.def_val[26] = ""
            # Field 27 - Amount In Acct. Currency
            self.len[27] = 13
            self.inheritance[27] = 17
            self.padding_type[27] = "amount"
            self.def_val[27] = ""
            # Field 28 - Amount Sign
            self.len[28] = 2
            self.inheritance[28] = 15
            self.def_val[28] = ""
            # Field 29 - Transaction Fee In Current Acct. Currency
            self.len[29] = 9
            self.def_val[29] = "0"
            self.padding_type[29] = "amount"
            # Field 30 - Trans. Fee Sign
            self.len[30] = 2
            self.inheritance[30] = 15
            self.def_val[30] = ""
            # Field 31 - Trans. Amount In CAMS Account Currency
            self.len[31] = 13
            self.padding_type[31] = "amount"
            self.inheritance[31] = 17
            self.def_val[31] = ""
            # Field 32 - Amount Sign
            self.len[32] = 2
            self.inheritance[32] = 15
            self.def_val[32] = ""
            # Field 33 - Trans. Fee In CAMS Account Currency
            self.len[33] = 9
            self.inheritance[33] = 29
            self.padding_type[33] = "amount"
            self.def_val[33] = ""
            # Field 34 - Trans. Fee Sign
            self.len[34] = 2
            self.inheritance[34] = 15
            self.def_val[34] = ""
            # Field 35 - Exchange Rate
            self.len[35] = 11
            self.dynamic[35] = True
            self.padding_type[35] = "0"
            self.def_val[35] = ""
            # Field 36 - Exchange Rate Exponent
            self.len[36] = 2
            self.def_val[36] = "00" # This value is recalculated for eaach message whenever field 35 (exchange rate) is set via dynaset
            self.padding_type[36] = "0"
            # Field 37 - Cash Back Amount
            self.len[37] = 9
            self.padding_type[37] = "amount"
            self.def_val[37] = ""
            # Field 38 - Token Type
            self.len[38] = 2
            self.def_val[38] = ""
            # Field 39 - Token Assurance Level
            self.len[39] = 3
            self.def_val[39] = ""
            # Field 40 - Interchange Indicator
            self.len[40] = 1
            self.def_val[40] = "C"
            # Field 41 - CAMSII Transaction Type
            self.len[41] = 5
            self.def_val[41] = "01635"
            self.padding_type[41] = "0"
            # Field 42 - Terminal ID
            self.len[42] = 10
            self.def_val[42] = ""
            # Field 43 - Current Account No. Extension
            self.len[43] = 3
            self.def_val[43] = ""
            # Field 44 - Destination Amount
            self.len[44] = 13
            self.inheritance[44] = 17
            self.padding_type[44] = "amount"
            self.def_val[44] = ""
            # Field 45 - Destination Amount Sign
            self.len[45] = 2
            self.inheritance[45] = 15
            self.def_val[45] = ""
            # Field 46 - Destination Amount Currency
            self.len[46] = 3
            self.inheritance[46] = 19
            self.def_val[46] = ""
            # Field 47 - Regular Points Amount
            self.len[47] = 13
            self.padding_type[47] = "amount"
            self.def_val[47] = ""
            # Field 48 - File ID
            self.len[48] = 15
            self.padding_type[48] = "0"
            self.def_val[48] = ""
            # Field 49 - Uplift Amount
            self.len[49] = 15
            self.padding_type[49] = "amount"
            self.def_val[49] = ""
            # Field 50 - Exchange Rate Applied
            self.len[50] = 15
            self.def_val[50] = "000000010000000"
            # Field 51 - ARN
            self.len[51] = 23
            self.dynamic[51] = True
            self.padding_type[51] = "0"
            self.def_val[51] = ""
            # Field 52 - Bank Account Exchange Rate Applied
            self.len[52] = 11
            self.inheritance[52] = 35
            self.def_val[52] = ""
            # Field 53 - Bank Account Exchange Rate Exponent
            self.len[53] = 4
            self.inheritance[53] = 36
            self.padding_type[53] = "0"
            self.def_val[53] = ""
            # Field 54 - Mastercard Reconciliation Date/Visa Central Processing Date
            self.len[54] = 6
            self.inheritance[54] = 7
            self.def_val[54] = ""
            # Field 55 - Visa ISA Fee Flag
            self.len[55] = 1
            self.def_val[55] = ""
            # Field 56 - Interchange Fee
            self.len[56] = 9
            self.def_val[56] = "5"
            self.padding_type[56] = "0"
            # Field 57 - Transaction ID
            self.len[57] = 15
            self.dynamic[57] = True
            self.def_val[57] = ""
            # Field 58 - Visa Multiple Clearing Sequence Number
            self.len[58] = 2
            self.def_val[58] = ""
            # Field 59 - Visa Multiple Clearing Sequence Count
            self.len[59] = 2
            self.def_val[59] = ""
            # Field 60 - Sender Name
            self.len[60] = 30
            self.def_val[60] = ""
            # Field 61 - Sender Address
            self.len[61] = 35
            self.def_val[61] = ""
            # Field 62 - Sender City
            self.len[62] = 25
            self.def_val[62] = ""
            # Field 63 - Sender State\Province CD
            self.len[63] = 3
            self.def_val[63] = ""
            # Field 64 - Sender Country
            self.len[64] = 3
            self.def_val[64] = ""
            # Field 65 - Message Reason Code
            self.len[65] = 4
            self.padding_type[65] = "0"
            self.def_val[65] = ""
            # Field 66 - Transaction Level 5
            self.len[66] = 3
            self.def_val[66] = ""
            # Field 67 - Token
            self.len[67] = 19
            self.def_val[67] = ""
            # Field 68 - Token Requestor ID
            self.len[68] = 11
            self.padding_type[68] = "0"
            self.def_val[68] = ""
            # Field 69 - Settlement Date
            self.len[69] = 6
            self.inheritance[69] = 7
            self.def_val[69] = ""
            # Field 70 - Operator ID
            self.len[70] = 8
            self.def_val[70] = "CAN4DC71"
            # Field 71 - Receiving Time Stamp
            self.len[71] = 20
            self.def_val[71] = datetime.datetime.today().strftime("%Y%m%d%H%M%S%f")
            # Field 72 - External Bank Code
            self.len[72] = 6
            self.def_val[72] = "000600"
            # Field 73 - Released Outstanding Authorization Amount
            self.len[73] = 15
            self.padding_type[73] = "amount"
            self.def_val[73] = ""
            # Field 74 - Ancillary Fee Code 1
            self.len[74] = 2
            self.def_val[74] = ""
            # Field 75 - Ancillary Fee Amount 1
            self.len[75] = 12
            self.padding_type[75] = "amount"
            self.def_val[75] = ""
            # Field 76 - Ancillary Fee Code 2
            self.len[76] = 2
            self.def_val[76] = ""
            # Field 77 - Ancillary Fee Amount 2
            self.len[77] = 12
            self.padding_type[77] = "amount"
            self.def_val[77] = ""
            # Field 78 - Ancillary Fee Code 3
            self.len[78] = 2
            self.def_val[78] = ""
            # Field 79 - Ancillary Fee Amount 3
            self.len[79] = 12
            self.padding_type[79] = "amount"
            self.def_val[79] = ""
            # Field 80 - Ancillary Fee Code 4
            self.len[80] = 2
            self.def_val[80] = ""
            # Field 81 - Ancillary Fee Amount 4
            self.len[81] = 12
            self.padding_type[81] = "amount"
            self.def_val[81] = ""
            # Field 82 - Ancillary Fee Code 5
            self.len[82] = 2
            self.def_val[82] = ""
            # Field 83 - Ancillary Fee Amount 5
            self.len[83] = 12
            self.padding_type[83] = "amount"
            self.def_val[83] = ""
            # Field 84 - Ancillary Fee Code 6
            self.len[84] = 2
            self.def_val[84] = ""
            # Field 85 - Ancillary Fee Amount 6
            self.len[85] = 12
            self.padding_type[85] = "amount"
            self.def_val[85] = ""
            # Field 86 - Payment Additional Information
            self.len[86] = 3
            self.def_val[86] = ""
            # Field 87 - Currency Conversion Date
            self.len[87] = 6
            self.inheritance[87] = 7
            self.def_val[87] = ""
            # Field 88 - Initiated Via Remote Payment Channel
            self.len[88] = 2
            self.def_val[88] = ""
            # Field 89 - Customer Authentication
            self.len[89] = 3
            self.def_val[89] = ""
            # Field 90 - Card Payment Information
            self.len[90] = 3
            self.def_val[90] = ""
            # Field 91 - Remote Payment Information
            self.len[91] = 10
            self.def_val[91] = ""
            # Field 92 - Merchant ID
            self.len[92] = 15
            self.def_val[92] = "000100000179533"
            # Field 93 - Device Type
            self.len[93] = 2
            self.def_val[93] = ""
            # Field 94 - Low-risk Merchant Indicator
            self.len[94] = 2
            self.def_val[94] = ""
            # Field 95 - Original Trace ID
            self.len[95] = 15
            self.def_val[95] = ""
            # Field 96 - Currency Conversion Date Indicator
            self.len[96] = 1
            self.def_val[96] = "1"
            # Field 97 - ECB Rate Deviation
            self.len[97] = 15
            self.def_val[97] = ""
            # Field 98 - Terminal Type ID
            self.len[98] = 3
            self.def_val[98] = "NA"
            # Field 99 - Filler
            self.len[99] = 221
            self.def_val[99] = ""

            self.preset(user_preset)

        def preset(self, preset):
            """Updates default values according to predefined presets"""
            match preset:
                case "":
                    return 
                case "Purchase (Card Present)":
                    return          
                case "Purchase DKK":
                    self.dynamic[14] = False
                    self.def_val[14] = str(self.amount_counter * 7)
                    self.def_val[16] = "DKK"
                    self.dynamic[17] = True
                    self.def_val[22] = "Copenhagen"
                    self.def_val[23] = "DNK"
                    self.def_val[97] = "71343616C000001"
                case "3DS Purchase (Card Not Present)":
                    self.def_val[5] = "S"
                    self.def_val[6] = "MT"
                    self.def_val[89] = "212"
                    self.def_val[91] = "  Y212KB00" # Y is the 3DS Indicator
                    self.def_val[98] = "CT6"
                case "Purchase (CP MDES)":
                    self.def_val[38] = "C"
                    self.def_val[67] = "516764" + self.val[25].replace(" ", "")
                    self.def_val[68] = "50110030273" # Trainline
                    self.def_val[90] = "LN1"
                    self.def_val[98] = "POI"
                case "Purchase (CNP MDES)":
                    self.def_val[5] = "S"
                    self.def_val[6] = "MT"
                    self.def_val[38] = "C"
                    self.def_val[67] = "516764" + self.val[25].replace(" ", "")
                    self.def_val[68] = "50110030273" # Trainline
                    self.def_val[89] = "242"
                    self.def_val[91] = "M8Y212KB00"
                    self.def_val[98] = "CT6"
                case "Recurring Transaction":
                    self.def_val[5] = "7"
                    self.def_val[6] = "MT"
                    self.def_val[38] = "H"
                    self.def_val[39] = "10"
                    self.def_val[67] = "516764" + self.val[25].replace(" ", "")
                    self.def_val[68] = "50109483721" # Spotify
                    self.def_val[89] = "247"
                    self.def_val[94] = "03"
                    self.dynamic[95] = True
                case "Withdrawal":
                    self.def_val[3] = "05"
                    self.def_val[5] = "C"
                    self.def_val[6] = "AT"
                    self.def_val[21] = "6011"
                    self.def_val[41] = "01625"
                    self.def_val[98] = "ATM"
                case "Moneysend":
                    self.def_val[3] = "06"
                    self.def_val[5] = "S"
                    self.def_val[6] = "MT"
                    self.def_val[15] = "CR"
                    self.def_val[21] = "6537"
                    self.def_val[22] = "Luxembourg"
                    self.def_val[23] = "LUX"
                    self.def_val[41] = "01609"
                    self.def_val[60] = "Gino Paoli"
                    self.def_val[61] = "Via Palmanova"
                    self.def_val[62] = "Milano"
                    self.def_val[63] = "039"
                    self.def_val[64] = "ITA"
                    self.def_val[65] = "1401"
                    self.def_val[86] = "C52"
                    self.def_val[89] = "210"
                    self.def_val[98] = "CT6"
                case "Refund":
                    self.def_val[5] = "S"
                    self.def_val[6] = "MT"
                    self.def_val[15] = "CR"
                    self.def_val[41] = "01671"
                    self.def_val[65] = "1400"
                    self.def_val[96] = "2"
                    self.def_val[98] = "CT6"
                case "Purchase With Cashback":
                    self.def_val[37] = "1"
                    self.def_val[98] = "POI"
                case "Partial Clearing":
                    self.def_val[65] = "1403"
                case "Final Clearing":
                    self.def_val[65] = "1404"               
                case _:
                    print(f"\"{preset}\" is not a valid preset. Transaction will be treated as a Purchase (Card Present)")

        def dynaset(self, field):
            """Sets the value of dynamic fields"""
            match field:
                case 9:
                    return helpers.randgen(string.digits, 6)            
                case 14:
                    return str(self.amount_counter)           
                case 17:
                    return str(self.amount_counter)           
                case 35:
                    result = float(self.val[14]) / float(self.val[31])
                    if result.is_integer():
                        return str(int(result))
                    else:
                        result = round(result, 10)
                        result = str(result)
                        self.def_val[36] = str(len(result) - (result.find(".") + 1))
                        return result.replace(".", "")               
                case 51:
                    return helpers.randgen(string.digits, 23)       
                case 57:
                    return "MCC" + helpers.randgen(string.ascii_uppercase + string.digits, 6) + self.val[54]
                case 95:
                    return "MCC" + helpers.randgen(string.ascii_uppercase + string.digits, 6) + self.val[54]       
                case _:
                    return ""
        
        @property
        def header_info(self):
            """Returns a list of field that are necessary to update the file header"""
            return [self.val[31], self.val[32]]


    class Filename():
        """Defines the standard name for the batch file"""
        @classmethod
        def get(cls):
            return "INK01.D" + datetime.date.today().strftime("%y%m%d") + ".T" + datetime.datetime.today().strftime("%H%M%S") + ".P001"