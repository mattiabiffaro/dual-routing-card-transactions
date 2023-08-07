# Import from the Standard Library
import random


# Global variables
codes = {} 
# Each dict item is a set of codes which were already used, hence not to be re-used. 
# The indices represent the number of characters of the items (e.g. codes[6] is a set of six character strings)


def esc(color):
    """Easily apply ANSI text color formatting"""
    match color:
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


def randgen(population, limit):
    """Generates single use strings pseudo-randomly"""
    global codes
    random.seed()
    result = ""

    if limit not in codes:
        codes[limit] = {""}
    
    while result in codes[limit]:
        result = "".join(random.choices(population, k=limit))

    codes[limit].add(result)
    return result