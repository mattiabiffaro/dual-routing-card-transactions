"""Defines common attributes and methods for NEXI interfaces' records"""


class Standard_Header():
    def __init__(self, subfield_count=0):
        self.val = "" # Value of the entire header
        self.subfield_count = subfield_count # Number of subfields
        self.subfield_val = [] # Subfield value
        self.subfield_len = [] # Subfield length
        self.subfield_padding_type = [] # Defines what character to use when applying padding
        self.accounts = [] # Count of distinct accounts

        # Reserve subfield 0. Subfields are 1 indexed in ALL interfaces
        self.subfield_val.append("Reserved")
        self.subfield_len.append(0)
        self.subfield_padding_type.append(" ")

        # Initialize subfields from 1 to self.subfield_count
        for i in range(self.subfield_count):
            self.subfield_val.append("")
            self.subfield_len.append(0)
            self.subfield_padding_type.append("0")
    
    def __str__(self):
        """Concatenates the header record subfields to get the final header record value"""
        # Normalize subfield values
        for i in range(1, self.subfield_count):
            if isinstance(self.subfield_val[i], int):
                self.subfield_val[i] = str(self.subfield_val[i])
            while len(self.subfield_val[i]) != self.subfield_len[i]:
                self.subfield_val[i] = self.subfield_padding_type[i] + self.subfield_val[i]
            self.val += self.subfield_val[i]

        return self.val


class Standard_Fields():
    def __init__(self, count=0):
        self.count = count # Number of fields
        self.val = [] # Field value
        self.len = [] # Field length
        self.dynamic = [] # Defines whether the field's default value is set dynamically
        self.def_val = [] # Defines static default values for non-dynamic fields
        self.inheritance = {} # Defines values for fields inheriting them from other fields
        self.padding_type = [] # Defines what character to use when applying padding
        self.amount_counter = 0 # Counter for default values of fields containing amounts of some kind

        # Reserve field 0. Fields are 1 indexed in ALL912
        self.val.append("Reserved")
        self.len.append(0)
        self.dynamic.append(False)
        self.def_val.append("")
        self.padding_type.append(" ")

        # Initialize fields from 1 to self.count
        for i in range(self.count):
            self.val.append("")
            self.len.append(0)
            self.dynamic.append(False)
            self.def_val.append("")
            self.padding_type.append(" ")

    def start(self):
        """Sets the value of subclass objects, except for dynamic objects, which are set in the dynaset or inherit methods"""
        # Update counters
        self.amount_counter += 1

        # Reset dynamic flags
        for i in range(self.count + 1):
            self.dynamic[i] = False
        
    def inherit(self, n):
        """Sets values for fields inheriting them from other fields"""
        return self.val[self.inheritance[n]]

    def set(self, n, user_val):
        """Checks the attributes of a field and sets the value accordingly"""
        if user_val == "":
            if self.dynamic[n] is True:
                self.val[n] = self.dynaset(n)
            elif n in self.inheritance:
                self.val[n] = self.inherit(n)
            else:
                self.val[n] = self.def_val[n]
        else:
            self.val[n] = user_val

        self.padding(n)

    def dynaset(self, field):
        """Sets the value of dynamic fields"""
        # Defined in child classes
        ...

    def padding(self, n):
        """Applies padding to get to the required field length"""
        if len(self.val[n]) > self.len[n]:
            raise ValueError(f"Value of field {n} exceeds maximum length {self.len[n]}")

        match self.padding_type[n]:
            case " ":
                while len(self.val[n]) != self.len[n]:
                    self.val[n] += self.padding_type[n]
            case "0":
                while len(self.val[n]) != self.len[n]:
                    self.val[n] = self.padding_type[n] + self.val[n]
            case "0+":
                while len(self.val[n]) != self.len[n]:
                    if len(self.val[n]) == 0:
                        self.val[n] = "+"
                    else:
                        self.val[n] = self.val[n] + "0" 
            case "0-":
                while len(self.val[n]) != self.len[n]:
                    if len(self.val[n]) == 0:
                        self.val[n] = "-"
                    else :
                        self.val[n] =  self.val[n] + "0" 
            case "amount":
                if len(self.val[n]) != self.len[n] and self.val[n] != "":
                    self.val[n] = str(round(float(self.val[n]) * 100))
                while len(self.val[n]) != self.len[n]:
                    self.val[n] = "0" + self.val[n]
            case "*":
                while len(self.val[n]) != self.len[n]:
                    self.val[n] += self.padding_type[n]            
            case "exchange":
                while len(self.val[n]) != self.len[n]:
                    self.val[n] += "0"

    def preset(self, preset):
        """Updates default values according to predefined presets"""
        # Defined in child classes
        ...

    def header_info(self):
        """Returns a list of field that are necessary to update the file header"""
        # Defined in child classes
        ...