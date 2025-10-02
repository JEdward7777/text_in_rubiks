# I want to know if you rotate the face near you on the cube and then
# rotate the cube around with you, how many times you can repeat that until
# you get back to the original position.

from cube import Cube


size = 4
def main():
    solved_cube = Cube(size)

    c = Cube(size)

    count = 0
    found_it = False
    while not found_it:
        c.do_command( 'F' )
        #now rotate the cube so that the F becomes the L.
        c.do_command( "y" )

        count += 1

        if c == solved_cube:
            found_it = True
            print( f"found it in {count} moves." )
            print( c )
        else:
            if count % 1000 == 0:
                print( f"count {count}." )


if __name__ == "__main__":
    main()