def int_input(string, range = float("inf")):
    while True:
        x = input(string)
        if x.isdecimal() and 0<int(x)<=range:
            return int(x)
        else:
            while True:
                x = input("Invalid input!\n1. Try again\n2. Leave\n")
                if x.isdecimal() and int(x) == 1:
                    break
                elif x.isdecimal() and int(x) == 2:
                    return range
                
def is_float(string):
    """
    
    """
    try:
        if float(string)>=0:
            return True
        else:
            return False
    except:
        return False
    

def float_input(string):
    """
    
    """
    while True:
        x = input(string)
        if is_float(x):
            return float(x)
        else:
            while True:
                x = input("Invalid input!\n1. Try again\n2. Leave\n")
                if x.isdecimal() and int(x) == 1:
                    break
                elif x.isdecimal() and int(x) == 2:
                    return 0