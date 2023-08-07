"""Creates objects representing records and interface attributes from NEXI's ALL907"""


# Import modules from the Standard Library
import datetime
import string
import helpers
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
            super().__init__(subfield_count=19)

            # Set the value of subclass objects
            self.subfield_len[1] = 9
            self.subfield_val[1] = "390013800"
            self.subfield_len[2] = 5
            self.subfield_val[2] = ""
            self.subfield_padding_type[2] = " "
            self.subfield_len[3] = 5
            self.subfield_val[3] = ""
            self.subfield_padding_type[3] = " "
            self.subfield_len[4] = 5
            self.subfield_val[4] = ""
            self.subfield_padding_type[4] = " "
            self.subfield_len[5] = 23
            self.subfield_val[5] = ""
            self.subfield_padding_type[5] = " "
            self.subfield_len[6] = 7
            self.subfield_val[6] = "DAILY"
            self.subfield_padding_type[6] = " "
            self.subfield_len[7] = 9
            self.subfield_val[7] = "1" + datetime.date.today().strftime("%Y%m%d")
            self.subfield_len[8] = 9
            self.subfield_val[8] = 0 # Will be updated with the number of accounts in the file
            self.subfield_len[9] = 9
            self.subfield_val[9] = 0 # Will be updated with the number of plastics in the file
            self.subfield_len[10] = 9
            self.subfield_val[10] = 0 # Will be updated with the number of records in the file
            self.subfield_len[11] = 15
            self.subfield_val[11] = 0 # Will be updated with the sum of fields 10 when field 13 == DB
            self.subfield_len[12] = 15
            self.subfield_val[12] = 0 # Will be updated with the sum of fields 10 when field 13 == CR
            self.subfield_len[13] = 5
            self.subfield_val[13] = "36003" #file transfer destination id
            self.subfield_len[14] = 1
            self.subfield_val[14] = "H" # header identification
            self.subfield_len[15] = 14
            self.subfield_val[15] = datetime.datetime.today().strftime("%Y%m%d%H%M%S")  #batch id
            self.subfield_len[16] = 5
            self.subfield_val[16] = "13800" # company identifier
            self.subfield_len[17] = 9
            self.subfield_val[17] = 0 # check of number of transactions in the file, will be updated later
            self.subfield_padding_type[17] = "0"
            self.subfield_len[18] = 9
            self.subfield_val[18] = 0
            self.subfield_padding_type[18] = "0"
            self.subfield_len[19] = 0
            self.subfield_val[19] = "" # Filler, not used yet

        def update(self, amount, sign, account):
            """Updates the values of the subfields based on the record fields data"""
            if account not in self.accounts:
                self.subfield_val[8] += 1
                self.subfield_val[9] += 1
                self.accounts.append(account)

            self.subfield_val[10] += 1
            if sign == "DB":
                self.subfield_val[17] += 1
                self.subfield_val[11] += int(amount)
            else:
                self.subfield_val[12] += int(amount)
                self.subfield_val[17] += 1


    class Fields(Standard_Fields):
        """Defines the attributes of detail record fields"""
        def __init__(self):
            super().__init__(count = 181)

        def start(self, scenario, user_preset):
            """Sets the value of subclass objects, except for dynamic objects, which are set in the dynaset or inherit methods"""
            super().start()

            # Define the default value and properties of each record field
            # Field 1 - Issuer Id
            self.len[1] = 9
            self.def_val[1] = "390013800"
            # Field 2 - Card type - Identifies the first-level owner of the Issuer
            self.len[2] = 5
            self.def_val[2] = "00100" # Since temenos doesn't read the debit cards transactions, we default to the prepaid code
            # Field 3 - Identifies the second-level owner of the Issuer
            self.len[3] = 5
            # Field 4 - Identifies the third-level owner of the Issuer
            self.len[4] = 5
            # Field 5 - SIA Prepaid Card Number
            self.len[5] = 23
            self.def_val[5] = "200000745"
            # Field 6 - Plastic Number
            self.len[6] = 23
            self.def_val[6] = "546492******9929"
            # Field 7 - Issuer Key
            self.len[7] = 23
            self.padding_type[7] = "*"
            # Field 8 - Transaction Original Amount
            self.len[8] = 15
            self.dynamic[8] = True
            self.padding_type[8] = "amount"
            # Field 9 - Currency Code
            self.len[9] = 3
            self.def_val[9] = "978" # importante
            # Field 10 - Transaction Convertion Amount
            self.len[10] = 15
            self.inheritance[10] = 8
            self.padding_type[10] = "amount" # transazione in euro
            # Field 11 - Transaction Country Code
            self.len[11] = 3
            self.def_val[11] = "ITA"
            # Field 12 - SIA Transaction Code
            self.len[12] = 5
            self.def_val[12] = "01035" # importante
            self.padding_type[12] = "0"
            # Field 13 - Transaction Sign
            self.len[13] = 2
            self.def_val[13] = "DR"
            # Field 14 - Transaction Date posted in CAMS
            self.len[14] = 7
            self.def_val[14] = "1" + datetime.date.today().strftime("%y%m%d") # Se tra 100 anni stai leggendo questo codice, sappi che sono stato pigro e cambia 1 in 2
            # Field 15 - Authorization Date 
            self.len[15] = 7
            self.def_val[15] = "1" + datetime.date.today().strftime("%y%m%d")
            # Field 16 - Trans. time stamp 
            # e.g. 2023-04-16-19.48.00.01793
            self.len[16] = 26
            self.def_val[16] = str(datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S.%f"))
            # Field 17 - Transaction Identifier ARN
            # e.g. 255204713105209812762240  
            self.len[17] = 25
            self.dynamic[17] = True
            # Field 18 - Merchant Category Code
            self.len[18] = 4
            self.def_val[18] = "5999" # importante
            # Field 19 - Merchant Name
            self.len[19] = 25
            if scenario:
                self.def_val[19] = scenario
            else:
                self.def_val[19] = "Untitled"
            # Field 20 - Merchant City
            self.len[20] = 15
            self.def_val[20] = "Vegas"
            # Field 21 - Aggregato Merchant Name and City
            self.len[21] = 0
            # Field 22 - Merchant State Code
            self.len[22] = 3
            self.def_val[22] = "ITA"
            # Field 23 - Merchant Country Code
            self.len[23] = 3
            self.def_val[23] = "ITA"
            # Field 24 - Merchant Zip Code
            self.len[24] = 10
            self.def_val[24] = "00100"
            # Field 25 - Operator ID
            self.len[25] = 10
            self.def_val[25] = "CAN4DC7I"
            # Field 26 - Acquirer Code
            self.len[26] = 8
            # Field 27 - Terminal ID
            self.len[27] = 8
            self.dynamic[27] = True
            # Field 28 - Transaction Source
            self.len[28] = 2
            self.def_val[28] = "0" # Unknown
            # Field 29 - Current Available Balance
            self.len[29] = 15
            self.padding_type[29] = "0+" 
            # Field 30 - Merchant ID
            self.len[30] = 15
            self.def_val[30] = "000100000179533" # Copiato da 912
            # Field 31 - Message Type Code 
            self.len[31] = 4
            self.def_val[31] = "1240"
            # Field 32 - Function Code
            self.len[32] = 3 
            self.def_val[32] = "200"  # First presentment, VISA N/A
            # Field 33 - Format Code
            self.len[33] = 2
            self.def_val[33] = "00"
            # Field 34 - Card Acceptor Name and Location
            self.len[34] = 54
            self.dynamic[34] = True
            # Field 35 - Adjustment Reason Code
            self.len[35] = 3
            self.def_val[35] = ""
            # Field 36 - BIN/ICA
            self.len[36] = 6
            self.def_val[36] = "021630"
            # Field 37 - Extended Credit Reference Number
            self.len[37] = 5
            self.def_val[37] = "00000"
            # Field 38 - Extended Credit Plan Code
            self.len[38] = 2
            # Field 39 - Original Repayment Count
            self.len[39] = 3
            self.def_val[39] = "000"
            # Field 40 - Current Balance
            self.len[40] = 15
            self.padding_type[40] = "0-"
            # Field 41 - Transaction Mode
            self.len[41] = 1
            self.def_val[41] = "M"  # PAN Entry Mode Unknown
            # Field 42 - Account Type Code
            self.len[42] = 3
            self.def_val[42] = "AP1" # Profilo Friend 2: Account con carta prepagata AP1, con profilo Flex2 o Friend2
            # Field 43 - Transaction Source COde
            self.len[43] = 3
            self.def_val[43] = "MON" # Mastercard Interchange
            # Field 44 - Transaction Category Code
            self.len[44] = 3
            self.def_val[44] = "PU"  # Purchase
            # Field 45 - Transaction Level 3
            self.len[45] = 3
            self.def_val[45] = "DOM"  # Domestic
            # Field 46 - Transaction Level 4
            self.len[46] = 3
            self.def_val[46] = "NDS" # Non Disclosed Source
            # Field 47 - Transaction Level 5
            self.len[47] = 3
            self.def_val[47] = "VIR" 
            # Field 48 - Fee Type
            self.len[48] = 2
            self.def_val[48] = "00" # importante 
            # Field 49 - Fee Currency Code
            self.len[49] = 3
            self.inheritance[49] = 9
            self.def_val[49] = "" # importante 
            # Field 50 - Fee Sign
            self.len[50] = 1
            self.def_val[50] = "C" # importante 
            # Field 51 - Fee Amount
            self.len[51] = 8
            self.padding_type[51] = "amount" # importante 
            # Field 52 - Fee Exponent
            self.len[52] = 1
            self.def_val[52] = "2"
            # Field 53 - Microchip Transaction Indicator
            self.len[53] = 1
            self.def_val[53] = "N" # Per identificazione mettere Y
            # Field 54 - E-Commerce Security Level Indicator
            self.len[54] = 1
            self.inheritance[54] = 41
            # Field 55 - Primary Plastic Number
            self.len[55] = 23
            self.inheritance[55] = 6
            # Field 56 - Business Family Indicator
            self.len[56] = 1
            # Field 57 - Plastic Type
            self.len[57] = 3
            self.def_val[57] = "QF1"
            # Field 58 - Embossed Line 1
            self.len[58] = 26
            self.def_val[58] = "Piero Vella" # Cognome e nome del tizio
            # Field 59 - Credit Line
            self.len[59] = 15
            self.padding_type[59] = "0"
            # Field 60 - Temporary Credit Adjustment
            self.len[60] = 15
            self.padding_type[60] = "0"
            # Field 61 - Related Account Number
            self.len[61] = 23
            # Field 62 - Account Language Code
            self.len[62] = 3
            self.def_val[62] = "ITA"
            # Field 63 - Account Title 1
            self.len[63] = 40
            self.inheritance[63] = 58
            # Field 64 - Payment Method Code
            self.len[64] = 3
            self.def_val[64] = "MAN"
            # Field 65 - Auto Payment Indicator
            self.len[65] = 1
            self.def_val[65] = "N"
            # Field 66 - Auto Payment Method
            self.len[66] = 1
            # Field 67 - Pending Authorization Amount
            self.len[67] = 15
            self.padding_type[67] = "amount"
            # Field 68 - Total Payment Amount
            self.len[68] = 15
            self.padding_type[68] = "amount"
            # Field 69 - Last Statement Date
            self.len[69] = 7
            self.padding_type[69] = "0"
            # Field 70 - Account Billing Cycle Number
            self.len[70] = 3
            self.dynamic[70] = True
            # Field 71 - Exchange Rate
            self.len[71] = 15
            self.def_val[71] = "000000010000000"
            self.padding_type[71] = "exchange"
            # Field 72 - Code Transaction Fee
            self.len[72] = 4
            self.def_val[72] = "" # non capiamo il valore
            # Field 73 - Reimbursment Attribute
            self.len[73] = 1
            # Field 74 - Installment Eligibility Indicator
            self.len[74] = 1
            # Field 75 - Recurring Transaction Flag
            self.len[75] = 1
            # Field 76 - POS Entry Mode
            self.len[76] = 2
            # Field 77 - CardHolder ID Method
            self.len[77] = 1
            # Field 78 - POS terminal Capacibility
            self.len[78] = 1
            # Field 79 - Point of Service Data Code
            self.len[79] = 12
            # importante, controllare pagina 250 di ipm per i dati
            self.def_val[79] = "M10101M00346" # studiare
            # Field 80 - Approval Code
            self.len[80] = 6
            self.dynamic[80] = True
            self.padding_type[80] = "0"
            # Field 81 - Authorization Code
            self.len[81] = 6
            # Field 82 - Transaction Data End Time
            self.len[82] = 12
            self.def_val[82] = str(datetime.datetime.today().strftime("%y%m%d%H%M%S")) 
            # Field 83 - Message Reason Code
            self.len[83] = 4
            self.def_val[83] = "0000"
            # Field 84 - Cashback Amount
            self.len[84] = 15
            self.padding_type[84] = "amount"
            # Field 85 - Cashback Currency
            self.len[85] = 3
            self.def_val[85] = "000"
            # Field 86 - Cashback Sign
            self.len[86] = 2
            # Field 87 - Other Sender Informations
            self.len[87] = 54
            # Field 88 - Token Type
            self.len[88] = 2
            # Field 89 - Token Number
            self.len[89] = 19
            # Field 90 - Token Insurance Level
            self.len[90] = 2
            self.def_val[90] = "00"
            # Field 91 - Token Requestor ID
            self.len[91] = 11
            self.padding_type[91] = "0"
            # Popular Token Requestor IDs: 50110030273 (Apple Pay), 50120834693 (Google Pay)
            # Field 92 - Settlement Currency Code
            self.len[92] = 3
            self.def_val[92] = "978"
            # Field 93 - Settlement Flag
            self.len[93] = 1
            # Field 94 - Value Term
            self.len[94] = 3
            self.def_val[94] = "000"  # Auto Payment Transaction
            # Field 95 - Filler
            self.len[95] = 2
            # Field 96 - EMV Related Fields
            self.len[96] = 255
            # Field 97 - Card Sequence Number
            self.len[97] = 3
            self.def_val[97] = "000" # Number of time a card has been issued
            # Field 98 - Network Name
            self.len[98] = 6
            self.def_val[98] = "<IPM >"
            # Field 99 - Transaction Amount converted into the currency of the Cardholder with MasterCard’s currency conversion rates applying
            self.len[99] = 15
            self.dynamic[99] = True
            self.padding_type[99] = "amount"
            # Field 100 - Currency Conversion
            self.len[100] = 15
            self.def_val[100] = "000000010000000"
            self.padding_type[100] = "exchange"
            # Field 101 - Difference Between Transaction Converted Amount
            self.len[101] = 15
            self.padding_type[101] = "amount"
            # Field 102 - Related Account ID
            self.len[102] = 23
            # Field 103 - Primary Plastic Type
            self.len[103] = 3
            self.inheritance[103] = 57
            # Field 104 - Embossed Line 
            self.len[104] = 26
            self.inheritance[104] = 58
            # Field 105 - Minimum Payments Amount of the last Cycle Data
            self.len[105] = 15
            self.padding_type[105] = "amount"
            # Field 106 - Security Level Indicator
            self.len[106] = 1
            # Field 107 - Type of Cardholder Authentication
            self.len[107] = 1
            # Field 108 - Electronic Commerce Security Level Indicator
            self.len[108] = 1
            # Field 109 - Currency Conversion Assessment
            self.len[109] = 15
            self.padding_type[109] = "amount"
            # Field 110 - Settlement Date
            self.len[110] = 7
            self.inheritance[110] = 14
            # format CYYMMDD
            # Field 111 - Reconciliation Date
            self.len[111] = 7
            self.inheritance[111] = 14
            # format CYYMMDD
            # Field 112 - Interchange Fee
            self.len[112] = 12
            self.padding_type[112] = "amount" 
            # Field 113 - Reconciliation Amount
            self.len[113] = 12
            self.dynamic[113] = True
            self.inheritance[113] = 10
            self.padding_type[113] = "amount"
            # Field 114 - Cycle End Date
            self.len[114] = 10
            self.dynamic[114] = True
            # format 2023-04-30
            # Field 115 - Plastic Status
            self.len[115] = 3
            self.def_val[115] = "AA" # importante
            # Field 116 - Primary Bank Account Additional Info 1
            self.len[116] = 8
            # Field 117 - Primary Bank Account Additional Info 2
            self.len[117] = 8
            # Field 118 - Direct Credit Bank Account Additional Info 1
            self.len[118] = 8
            # Field 119 - Direct Credit Bank Account Additional Info 2
            self.len[119] = 8
            # Field 120 - Account Cost Center
            self.len[120] = 15
            self.def_val[120] = "000000000000100"
            # Field 121 - Transaction Id
            self.len[121] = 15
            self.dynamic[121] = True
            # e.g. "MRGO7M4ZF0415  "
            # Field 122 - Visa Multiple Clearing Sequence Number
            self.len[122] = 2
            self.def_val[122] = "00"
            # Field 123 - Visa Multiple Clearing Sequence Count
            self.len[123] = 2
            self.def_val[123] = "00"
            # Field 124 - Merchant Street Address Purchase Identifier
            self.len[124] = 45
            # e.g. "VIA TORRI BIANCHE                  16        "
            # Field 125 - Wallet Id
            self.len[125] = 3
            # 103 Apple Pay, 216 Android Pay, 217 Samsung Pay
            # Field 126 - Sender's Name
            self.len[126] = 30
            # Field 127 - Sender Address
            self.len[127] = 35
            # Field 128 - Sender City
            self.len[128] = 25
            # Field 129 - Sender Country
            self.len[129] = 3
            # Field 130 - Reserved For Internal Use
            self.len[130] = 14
            # Field 131 - Internal Sequence number
            self.len[131] = 1
            self.def_val[131] = "0"
            # Field 132 - Ancillary Fee Code 1
            self.len[132] = 2
            # Field 133 - Ancillary Fee Amount 1
            self.len[133] = 12
            self.padding_type[133] = "amount" 
            # Field 134 - Ancillary Fee Code 2
            self.len[134] = 2
            # Field 135 - Ancillary Fee Amount 2
            self.len[135] = 12
            self.padding_type[135] = "amount" 
            # Field 136 - Ancillary Fee Code 3
            self.len[136] = 2
            # Field 137 - Ancillary Fee Amount 3
            self.len[137] = 12
            self.padding_type[137] = "amount" 
            # Field 138 - Ancillary Fee Code 4
            self.len[138] = 2
            # Field 139 - Ancillary Fee Amount 4
            self.len[139] = 12
            self.padding_type[139] = "amount" 
            # Field 140 - Ancillary Fee Code 5
            self.len[140] = 2
            # Field 141 - Ancillary Fee Amount 5
            self.len[141] = 12
            self.padding_type[141] = "amount" 
            # Field 142 - Ancillary Fee Code 6
            self.len[142] = 2
            # Field 143 - Ancillary Fee Amount 6
            self.len[143] = 12
            self.padding_type[143] = "amount"
            # Field 144 - Balance info table
            self.len[144] = 420
            self.dynamic[144] = True
            # e.g. repeat "      00000000000000à" 20 times
            # Field 145 - Currency Conversion Rate Data
            self.len[145] = 6
            self.def_val[145] = str(datetime.date.today().strftime("%y%m%d")) # format YYMMDD
            # Field 146 - Card Payment Authorization Information
            self.len[146] = 3
            self.def_val[146] = "LN1" # Contactless (L) - Undefined (N) - Positive (1) from ALL949
            # Field 147 - Remote Payment Authorization Information
            self.len[147] = 10
            # Field 148 - Static AAV/CAVV
            self.len[148] = 32
            # Field 149 - 3DS Program Protocol
            self.len[149] = 1
            # Field 150 - Directory Server Transaction ID
            self.len[150] = 36
            # Universally Unique Transaction ID which can be provided by the Processors/acquirers as part of the authentication transaction
            # Field 151 - Low Risk Merchant Indicator
            self.len[151] = 2
            # importante
            # Field 152 - Electronic Data Extract
            self.len[152] = 6
            # Field 153 - Device Type
            self.len[153] = 2
            # Field 154 - Transaction Code Identifier
            self.len[154] = 3
            # Field 155 - Currency Conversion Data Indicator
            self.len[155] = 1
            self.def_val[155] = "1" # 0, 2 no auth data, 1 auth date
            # Field 156 - ECB Rate Deviation
            self.len[156] = 15
            # Field 157 - Fee Currency Code Reconciliator
            self.len[157] = 3
            self.def_val[157] = "978"
            # Field 158 - Fee Type Code (1st Occurrence)
            self.len[158] = 2
            self.def_val[158] = "00" 
            # Field 159 - Fee Sign (1st Occurrence)
            self.len[159] = 2
            self.def_val[159] = "C"
            # Field 160 - Fee Original Amount (1st Occurrence)
            self.len[160] = 18
            # Fee amount in original currency
            self.padding_type[160] = "amount" # Circa 2 per mille della trasanzione
            # Field 161 - Fee Converted Amount (1st Occurrence)
            self.len[161] = 18
            self.padding_type[161] = "amount" 
            # Field 162 - Fee Type Code (2nd Occurrence)
            self.len[162] = 2
            self.def_val[162] = "00" 
            # Field 163 - Fee Sign (2nd Occurrence)
            self.len[163] = 2
            self.def_val[163] = "C"
            # Field 164 - Fee Original Amount (2nd Occurrence)
            self.len[164] = 18
            # fee amount in original currency
            self.padding_type[164] = "amount"
            # Field 165 - Fee Converted Amount (2nd Occurrence)
            self.len[165] = 18
            self.padding_type[165] = "amount" 
            # Field 166 - Fee Type Code (3rd Occurrence)
            self.len[166] = 2
            self.def_val[166] = "00" 
            # Field 167 - Fee Sign (3rd Occurrence)
            self.len[167] = 2
            self.def_val[167] = "C" #guardare
            # Field 168 - Fee Original Amount (3rd Occurrence)
            self.len[168] = 18
            # Fee amount in original currency
            self.padding_type[168] = "amount"
            # Field 169 - Fee Converted Amount (3rd Occurrence)
            self.len[169] = 18
            self.padding_type[169] = "amount" 
            # Field 170 - Terminal ID Type 
            self.len[170] = 3
            self.def_val[170] = "NA" 
            # Field 171 - Country Code 
            self.len[171] = 3
            self.padding_type[171] = "0"
            self.def_val[171] = "380"
            # Field 172 - Original Trace ID 
            self.len[172] = 15
            # Field 173 - ACS SCA Management 
            self.len[173] = 1
            self.def_val[173] = ""  # Y, N, F
            # Field 174 - ACS SCA Authentication Method 
            self.len[174] = 6
            # Field 175 - ACS SCA PSD 2 Exception Reason 
            self.len[175] = 4
            # Field 176 - MIT CIT Category Code
            self.len[176] = 2
            # Field 177 - MIT CIT Sub Category Code 
            self.len[177] = 2
            # Field 178 - Statement Cycle Begin Data 
            self.len[178] = 10
            # format 2023-04-30
            # Field 179 - Effective Date 
            self.len[179] = 10
            # format 2023-04-30
            # Field 180 - Posting Sequence Number 
            self.len[180] = 6
            # Field 181 - FILLER 
            self.len[181] = 198

            self.preset(user_preset)
        
        def preset(self, preset):
            """Updates default values according to predefined presets"""
            match preset:   
                case "":
                    return 
                case "Purchase (Card Present)":
                    return          
                case "Purchase GBR":
                    self.dynamic[8] = False
                    self.def_val[8] = str(self.amount_counter * 1.1)
                    self.def_val[9] = "826"
                    self.dynamic[10] = True
                    self.def_val[20] = "London"
                    self.def_val[22] = "GBR"
                    self.def_val[45] = "RGN"
                    self.def_val[72] = "EB"
                    self.def_val[156] = "71343616C000001"
                case "3DS Purchase (Card Not Present)":
                    self.def_val[41] = "S"
                    self.def_val[54] = "S"
                    self.def_val[72] = "75"
                    self.def_val[106] = "2"
                    self.def_val[107] = "1"
                    self.def_val[108] = "2"
                    self.def_val[147] = "Y212KC00"
                    self.def_val[149] = "2"
                    self.def_val[170] = "CT6"
                case "Purchase (CP MDES)":
                    self.def_val[46] = "DIS"
                    self.def_val[53] = "Y"
                    self.def_val[72] = "P2"
                    self.def_val[88] = "C"
                    self.def_val[89] = "5306034" + self.val[5]
                    self.def_val[91] = "50110030273" # Trainline
                    self.def_val[146] = "LN1"
                    self.def_val[170] = "POI"            
                case "Purchase (CNP MDES)":
                    self.def_val[38] = "C"
                    self.def_val[41] = "S"
                    self.def_val[72] = "75"
                    self.def_val[106] = "2"
                    self.def_val[107] = "4"
                    self.def_val[108] = "2"
                    self.def_val[146] = ""
                    self.def_val[147] = "N242DX00"
                    self.def_val[170] = "CT6"
                case "Recurring Transaction":
                    self.def_val[41] = "7"
                    self.def_val[45] = "RGN"
                    self.def_val[54] = "7"
                    self.def_val[72] = "75"
                    self.def_val[88] = "H"
                    self.dynamic[89] = True
                    self.def_val[90] = "10"
                    self.def_val[91] = "50129930112" # Spotify
                    self.def_val[106] = "2"
                    self.def_val[107] = "4"
                    self.def_val[108] = "7"
                    self.def_val[147] = "MON247CX01"
                    self.def_val[151] = "03"
                    self.def_val[170] = "CT6"
                    self.dynamic[172] = True
                case "Withdrawal":
                    self.def_val[12] = "01025"
                    self.def_val[18] = "6011"
                    self.def_val[41] = "C"
                    self.def_val[44] = "CA"
                    self.def_val[47] = "ATM"
                    self.def_val[50] = "D"
                    self.def_val[53] = "Y"
                    self.def_val[54] = "C"
                case "Moneysend":
                    self.def_val[11] = "LUX"
                    self.def_val[12] = "01073" 
                    self.def_val[13] = "CR"
                    self.def_val[18] = "6537"
                    self.def_val[20] = "Luxembourg"
                    self.def_val[22] = "LUX"
                    self.def_val[23] = "LUX"
                    self.def_val[41] = "S"
                    self.def_val[44] = "PV"
                    self.def_val[45] = "RGN"
                    self.def_val[47] = "MAN"
                    self.def_val[54] = "S"
                    self.def_val[72] = "MS"
                    self.def_val[83] = "1401"
                    self.def_val[106] = "2"
                    self.def_val[107] = "1"
                    self.def_val[108] = "0"
                    self.def_val[126] = "Gino Paoli"
                    self.def_val[127] = "Via Palmanova"
                    self.def_val[128] = "Milano"
                    self.def_val[129] = "ITA"
                    self.def_val[146] = ""
                    self.def_val[154] = "C52"
                    self.def_val[170] = "CT6"
                case "Refund":
                    self.def_val[12] = "01071" 
                    self.def_val[13] = "CR"
                    self.def_val[41] = "S"
                    self.def_val[44] = "CV"
                    self.def_val[45] = "RGN"
                    self.def_val[47] = "MAN"
                    self.def_val[54] = "1"
                    self.def_val[72] = "75"
                    self.def_val[83] = "1400"
                    self.def_val[155] = "2"
                    self.def_val[159] = "D"
                    self.def_val[171] = ""
                    self.def_val[172] = ""
                case "Purchase With Cashback":
                    self.def_val[47] = "MAN"
                    self.def_val[72] = "51"
                    self.def_val[84] = "1"
                    self.def_val[86] = "D"
                    self.def_val[106] = "2"
                    self.def_val[107] = "1"
                    self.def_val[108] = "2"
                    self.def_val[146] = "MSI"
                    self.def_val[170] = "POI"
                case "Partial Clearing":
                    self.def_val[83] = "1403"
                case "Final Clearing":
                    self.def_val[83] = "1404"               
                case _:
                    print(f"\"{preset}\" is not a valid preset. Transaction will be treated as a Purchase (Card Present)")

        def dynaset(self, field):
            """Sets the value of dynamic fields"""
            match field:
                case 8:
                    return str(self.amount_counter)
                case 17:
                    return helpers.randgen(string.digits, 23)  
                case 27:
                    return helpers.randgen(string.digits, 8)   
                case 34:
                    return str(self.def_val[19] + " / " + self.def_val[20])          
                case 70:
                    result = datetime.datetime.today().strftime("%m")
                    if str(result) in ["01","03", "05", "07", "08", "10", "12"]:
                        return "031"
                    elif str(result) in ["04", "06", "09", "11"]:
                        return "030"
                    else :
                        return "028"           
                case 80:
                    return helpers.randgen(string.digits, 6)
                case 89:
                    return "5306034" + self.val[5].strip()
                case 99:
                    if self.val[13] == "DR":
                        return self.val[10]
                    else:
                        return ""
                case 113:
                    self.val[field] = self.inherit(field)
                    return self.val[field][3:]        
                case 114:
                    current_month = datetime.datetime.today().strftime("%m")
                    if current_month in ["01","03", "05", "07", "08", "10", "12"]:
                        return (datetime.datetime.today().strftime("%Y-%m") + "-31")
                    elif current_month in ["04", "06", "09", "11"]:
                        return (datetime.datetime.today().strftime("%Y-%m") + "-30")
                    else:
                        return (datetime.datetime.today().strftime("%Y-%m") + "-28")
                case 121:
                    return "MRG"+ helpers.randgen(string.ascii_uppercase + string.digits, 6) + datetime.datetime.today().strftime("%m%d")
                case 144:
                    return "      00000000000000à" * 19
                case 172:
                    return "MRG"+ helpers.randgen(string.ascii_uppercase + string.digits, 6) + datetime.datetime.today().strftime("%m%d")
        
        @property
        def header_info(self):
            """Returns a list of field that are necessary to update the file header"""
            return [self.val[10], self.val[13], self.val[5]]


    class Filename():
        """Defines the standard name for the batch file"""
        @classmethod
        def get(cls):
            return "PDD01.D" + datetime.date.today().strftime("%y%m%d") + ".T" + datetime.datetime.today().strftime("%H%M%S") + ".P001"