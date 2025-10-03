import sys
sys.set_int_max_str_digits(0)

encode_tree = {
    " ": "000",
    "e": "001",
    "m": "01000",
    "f": "01001",
    "y": "01010",
    "v": "010110",
    "k": "0101110",
    "j": "010111100",
    "z": "010111101",
    "x": "010111110",
    "q": "010111111",
    "h": "0110",
    "c": "01110",
    "b": "011110",
    "p": "011111",
    "t": "1000",
    "d": "10010",
    "g": "100110",
    "w": "100111",
    "a": "1010",
    "i": "10110",
    "n": "10111",
    "l": "11000",
    "u": "11001",
    "o": "1101",
    "s": "1110",
    "r": "1111"
}

decode_tree = [None,None]



for letter, code in encode_tree.items():
    spot = decode_tree
    for index in range(len(code)):
        one_or_zero = code[index]
        offset = int(one_or_zero)
        if index == len(code) - 1:
            spot[offset] = letter
        else:
            if spot[offset] is None:
                spot[offset] = [None,None]
            elif isinstance(spot[offset], list):
                pass
            else:
                assert False, "bad tree"
            spot = spot[offset]
def check_tree( decode_tree, ones_and_zeros ):
    if decode_tree is None:
        print( f"problem at {ones_and_zeros}" )
    #check if it is a list
    elif isinstance( decode_tree, list ):
        check_tree( decode_tree[0], ones_and_zeros + "0" )
        check_tree( decode_tree[1], ones_and_zeros + "1" )
    else:
        return
check_tree( decode_tree, "" )


def encode( text ):
    text = text.lower()
    result = "".join( encode_tree[letter] for letter in text if letter in encode_tree )
    return result

def decode( code ):
    result = ""
    spot = decode_tree
    for one_or_zero in code:
        offset = int(one_or_zero)
        if isinstance(spot[offset], list):
            spot = spot[offset]
        else:
            result += spot[offset]
            spot = decode_tree
    return result


def to_number( string ):
    return int( "1" + encode( string ), 2 )

def from_number( number ):
    return decode( bin( number )[3:] )


if __name__ == '__main__':
    # as_string = "I am a little piece of tin nobody knows what I might have been"
    # as_ones_and_zeros = encode( as_string )
    # padded_with_1 = "1" + as_ones_and_zeros
    # as_int = int( padded_with_1, 2 )
    # print( f"Number is {as_int}" )
    # back_to_padded_with_1 = bin( as_int )[2:]
    # back_to_ones_and_zeros = back_to_padded_with_1[1:]
    # back_to_string = decode( back_to_ones_and_zeros )
    # print( back_to_string )

    #print( from_number( to_number( "This little light of mine, I'm going to let it shine." )))

    string = ""
    while string != "exit":
        string = input( "> " )
        try:
            as_number = int( string )
            print( from_number( as_number ) )
        except ValueError:
            as_number = to_number( string )
            print( as_number )
            print( as_number < 43252003274489856000 )
            print( f"string length {len(string)} number length {len(str(as_number))}")
            print( from_number( as_number ) )