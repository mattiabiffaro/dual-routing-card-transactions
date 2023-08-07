#!/usr/bin/env python3


# Import from the Standard Library
import sys
import re

# Import from local directories
import all912
import all907


def main():

    # Check correct usage
    if len(sys.argv) != 3:
        print("Correct usage: ../parser.py --gdf \'[message]\'")
        sys.exit(1)

    # Check filetype option
    if sys.argv[1] == "--gdf":
        field = all912.Fields()
    elif sys.argv[1] == "--pdd":
        field = all907.Fields()
    else:
        print("Usage: the second argument must be --gdf or --pdd")
        sys.exit(1)

    msg = sys.argv[2]
    field.start()

    # Iterate over the message
    cursor = 0
    next = 0
    for i in range (1, field.count + 1):
        next = cursor + field.len[i]
        # Get the current field value
        field.val[i] = msg[cursor:next]
        # Check if it's empty (that is, only composed of blanks)
        if re.search("^ *$", field.val[i]) == None:
            # Remove whitespace at the beginning and at the end of the string. Then print to screen
            field.val[i] = re.sub('^\s+|\s+$', '', field.val[i])
            print(f"{i:03d}<{field.val[i]}>")
        cursor = next

    sys.exit(0)


if __name__ == "__main__":
    main()