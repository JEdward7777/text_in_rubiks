
import copy
import random
import kociemba


NUM_ROTATIONS = 4


class Cube:
    X_AXIS = 0
    Y_AXIS = 1
    Z_AXIS = 2

    lines = None

    def clone( self ):
        return copy.deepcopy( self )

    #overload equality
    def __eq__( self, other ):
        self_str = str( self )
        other_str = str( other )
        return self_str.strip() == other_str.strip()
    
    #hash function for set.
    def __hash__(self) -> int:
        return hash( str( self ) )
    
    def is_solved( self ):
        return self == Cube( self.size )

    def __init__( self, size ):
        self.size = size

        lines = ""
        for y in range( size*3 ):
            for x in range( size*4 ):
                if y < size:
                    if x < size:
                        lines += " "
                    elif x < size*2:
                        lines += "y"
                    else:
                        lines += " "
                elif y < size * 2:
                    if x < size:
                        lines += "b"
                    elif x < size*2:
                        lines += 'r'
                    elif x < size*3:
                        lines += 'g'
                    else:
                        lines += 'o'
                else:
                    if x < size:
                        lines += " "
                    elif x < size*2:
                        lines += 'w'
                    else:
                        lines += ' '
            lines += "\n"

        self.lines = lines

    def __str__( self ):
        return self.lines
    
    def __repr__(self) -> str:
        return str(self)
    

    def rotate_area( self, from_array, to_array, offset_row, offset_column, clockwise ):
        for x in range( self.size ):
            for y in range( self.size ):
                if clockwise:
                    new_x = y
                    new_y = self.size - 1 - x
                else:
                    new_x = self.size - 1 - y
                    new_y = x
            
                to_array[offset_row + self.size-1 - new_y][offset_column + new_x] = from_array[offset_row + self.size-1 - y][offset_column + x]
        
    def rotate( self, axis, slice, distance ):
        if distance == 0: return

        while distance < 0: distance += NUM_ROTATIONS

        lines_from = [list( line ) for line in self.lines.splitlines()]
        lines_to = copy.deepcopy( lines_from )

        if slice < 0: slice += self.size

        for to_face in range( NUM_ROTATIONS ):
            from_face = (to_face+1) % NUM_ROTATIONS
            for i in range( self.size ):

                def location( face ):
                    if axis == Cube.X_AXIS:
                        if face < 3:
                            col = self.size + slice
                            row = i + face*self.size
                        else:
                            col = self.size*4 - 1 - slice
                            row = self.size*2 - 1 - i
                    elif axis == Cube.Y_AXIS:
                        row = self.size*2 - 1 - slice
                        col = i + face*self.size
                    else:
                        if face == 0:
                            row = self.size + i
                            col = slice
                        elif face == 1:
                            row = self.size*3-1-slice
                            col = self.size + i
                        elif face == 2:
                            row = self.size*2 - 1 - i
                            col = self.size*3 - 1 - slice
                        else:
                            row = slice
                            col = self.size*2 - 1 - i
                    return row, col 
                
                from_row, from_column = location( from_face )
                to_row, to_column = location( to_face )

                lines_to[to_row][to_column] = lines_from[from_row][from_column]

        do_rotation = False
        if slice == 0 or slice == self.size-1:
            do_rotation = True

    
        if axis == Cube.X_AXIS:
            if slice == 0:
                rot_row, rot_col = self.size, 0
            elif slice == self.size-1:
                rot_row, rot_col = self.size, self.size*2
        elif axis == Cube.Y_AXIS:
            if slice == 0:
                rot_row, rot_col = self.size*2, self.size
            elif slice == self.size-1:
                rot_row, rot_col = 0          , self.size
        else:
            if slice == 0:
                rot_row, rot_col = self.size, self.size*3
            elif slice == self.size-1:
                rot_row, rot_col = self.size, self.size

        if do_rotation:
            self.rotate_area( lines_from, lines_to, rot_row, rot_col, slice != 0 )

        self.lines = "\n".join( "".join( line ) for line in lines_to )

        self.rotate( axis, slice, distance-1 )

    def scramble( self, steps=20, talk=False ):
        for i in range( steps ):
            axis = random.choice( [Cube.X_AXIS, Cube.Y_AXIS, Cube.Z_AXIS] )
            slice = random.randint( 0, self.size-1 )
            distance = random.randint( 1, 3 )
            self.rotate( axis, slice, distance )
            
            if talk:
                print( f"axis {axis} slice {slice} distance {distance}" )
                if self.size == 3: print( self.get_solution() )
                print( self )


        return self

    def get_solution( self ):
        assert self.size == 3, "Solve only for 3x3x3 cube"

        location_names = [x.strip() for x in "U1, U2, U3, U4, U5, U6, U7, U8, U9, R1, R2, R3, R4, R5, R6, R7, R8, R9, F1, F2, F3, F4, F5, F6, F7, F8, F9, D1, D2, D3, D4, D5, D6, D7, D8, D9, L1, L2, L3, L4, L5, L6, L7, L8, L9, B1, B2, B3, B4, B5, B6, B7, B8, B9".split( "," )]
        location_spots = {
                                               "U1": (3,0), "U2": (4,0), "U3": (5,0),
                                               "U4": (3,1), "U5": (4,1), "U6": (5,1),
                                               "U7": (3,2), "U8": (4,2), "U9": (5,2),
        "L1": (0,3), "L2": (1,3), "L3": (2,3), "F1": (3,3), "F2": (4,3), "F3": (5,3), "R1": (6,3), "R2": (7,3), "R3": (8,3), "B1": (9,3), "B2": (10,3), "B3": (11,3),
        "L4": (0,4), "L5": (1,4), "L6": (2,4), "F4": (3,4), "F5": (4,4), "F6": (5,4), "R4": (6,4), "R5": (7,4), "R6": (8,4), "B4": (9,4), "B5": (10,4), "B6": (11,4),
        "L7": (0,5), "L8": (1,5), "L9": (2,5), "F7": (3,5), "F8": (4,5), "F9": (5,5), "R7": (6,5), "R8": (7,5), "R9": (8,5), "B7": (9,5), "B8": (10,5), "B9": (11,5),
                                               "D1": (3,6), "D2": (4,6), "D3": (5,6),
                                               "D4": (3,7), "D5": (4,7), "D6": (5,7),
                                               "D7": (3,8), "D8": (4,8), "D9": (5,8),
        }
        color_map = {
                      "y": "U",
            "b": "L", "r": "F", "g": "R", "o": "B",
                      "w": "D",
        }

        #before we can use kociemba, we need to rotate the cube with yellow face up and red in the front.

        cube_copy = self.clone()

        #get the y face on top
        lines_split = cube_copy.lines.split( "\n" )
        presolution = ""
        if lines_split[4][1] == 'y':
            presolution += 'z '
            for i in range( 3 ):
                cube_copy.rotate( Cube.Z_AXIS, slice=i, distance=1 )
        elif lines_split[4][4] == 'y':
            presolution += 'x '
            for i in range( 3 ):
                cube_copy.rotate( Cube.X_AXIS, slice=i, distance=1 )
        elif lines_split[4][7] == 'y':
            presolution += "z' "
            for i in range( 3 ):
                cube_copy.rotate( Cube.Z_AXIS, slice=i, distance=-1 )
        elif lines_split[4][10] == 'y':
            presolution += "x' "
            for i in range( cube_copy.size ):
                cube_copy.rotate( Cube.X_AXIS, slice=i, distance=-1 )
        elif lines_split[7][4] == 'y':
            presolution += 'x2 '
            for i in range( 3 ):
                cube_copy.rotate( Cube.X_AXIS, slice=i, distance=1 )
                cube_copy.rotate( Cube.X_AXIS, slice=i, distance=1 )
        
        lines_split = cube_copy.lines.split( "\n" )

        #now get r frace in front.
        if lines_split[4][1] == 'r':
            presolution += "y' "
            for i in range( cube_copy.size ):
                cube_copy.rotate( Cube.Y_AXIS, slice=i, distance=-1 )
        elif lines_split[4][7] == 'r':
            presolution += "y "
            for i in range( cube_copy.size ):
                cube_copy.rotate( Cube.Y_AXIS, slice=i, distance=1 )
        elif lines_split[4][10] == 'r':
            presolution += 'y2 '
            for i in range( cube_copy.size ):
                cube_copy.rotate( Cube.Y_AXIS, slice=i, distance=1 )
                cube_copy.rotate( Cube.Y_AXIS, slice=i, distance=1 )
        
        lines_split = cube_copy.lines.split( "\n" )

        current_string = ""
        for location_name in location_names:
            location = location_spots[location_name]
            current_color = lines_split[location[1]][location[0]]
            current_name = color_map[current_color]
            current_string += current_name

        return presolution + kociemba.solve( current_string )


    def do_command( self, command ):
        done = False
        if command == "L":
            #reverse direction because clockwise is backwards on left.
            self.rotate( Cube.X_AXIS, slice=0, distance=-1 )
        elif command == "L'":
            self.rotate( Cube.X_AXIS, slice=0, distance=1 )
        elif command == "L2":
            self.rotate( Cube.X_AXIS, slice=0, distance=2 )
        elif command == "R":
            self.rotate( Cube.X_AXIS, slice=-1, distance=1 )
        elif command == "R'":
            self.rotate( Cube.X_AXIS, slice=-1, distance=-1 )
        elif command == "R2":
            self.rotate( Cube.X_AXIS, slice=-1, distance=2 )
        elif command == "U":
            self.rotate( Cube.Y_AXIS, slice=-1, distance=1 )
        elif command == "U'":
            self.rotate( Cube.Y_AXIS, slice=-1, distance=-1 )
        elif command == "U2":
            self.rotate( Cube.Y_AXIS, slice=-1, distance=2 )
        elif command == "D":
            self.rotate( Cube.Y_AXIS, slice=0, distance=-1 )
        elif command == "D'":
            self.rotate( Cube.Y_AXIS, slice=0, distance=1 )
        elif command == "D2":
            self.rotate( Cube.Y_AXIS, slice=0, distance=2 )
        elif command == "F":
            self.rotate( Cube.Z_AXIS, slice=-1, distance=1 )
        elif command == "F'":
            self.rotate( Cube.Z_AXIS, slice=-1, distance=-1 )
        elif command == "F2":
            self.rotate( Cube.Z_AXIS, slice=-1, distance=2 )
        elif command == "B":
            self.rotate( Cube.Z_AXIS, slice=0, distance=-1 )
        elif command == "B'":
            self.rotate( Cube.Z_AXIS, slice=0, distance=1 )
        elif command == "B2":
            self.rotate( Cube.Z_AXIS, slice=0, distance=2 )
        elif command == "x":
            for i in range( self.size ):
                self.rotate( Cube.X_AXIS, slice=i, distance=1 )
        elif command == "x'":
            for i in range( self.size ):
                self.rotate( Cube.X_AXIS, slice=i, distance=-1 )
        elif command == "x2":
            for i in range( self.size ):
                self.rotate( Cube.X_AXIS, slice=i, distance=2 )
        elif command == "y":
            for i in range( self.size ):
                self.rotate( Cube.Y_AXIS, slice=i, distance=1 )
        elif command == "y'":
            for i in range( self.size ):
                self.rotate( Cube.Y_AXIS, slice=i, distance=-1 )
        elif command == "y2":
            for i in range( self.size ):
                self.rotate( Cube.Y_AXIS, slice=i, distance=2 )
        elif command == "z":
            for i in range( self.size ):
                self.rotate( Cube.Z_AXIS, slice=i, distance=1 )
        elif command == "z'":
            for i in range( self.size ):
                self.rotate( Cube.Z_AXIS, slice=i, distance=-1 )
        elif command == "z2":
            for i in range( self.size ):
                self.rotate( Cube.Z_AXIS, slice=i, distance=2 )
        elif command == "exit" or command == "exit()":
            done = True
        elif command == "reset":
            self.__init__( self.size )
        elif command == "scramble":
            self.scramble()
        elif command == "talk scramble":
            self.scramble( talk=True )
        elif command == "solve":
            print( self.get_solution() )
        elif command == "set":
            lines = []
            read_line = input( "" )
            while read_line != "":
                lines.append( read_line )
                read_line = input( "" )
            size = int(len( lines ) / 3)
            self.size = size
            self.lines = "\n".join( lines )
        else:
            raise ValueError( "I don't understand that command." )
        
        return done


def main( size=3 ):
    cube = Cube( size )

    done = False
    while not done:
        print( cube )

        #get the command.
        command = input( '> ' )

        #run the command
        try:
            done = cube.do_command( command )
        except ValueError as e:
            print( e )



if __name__ == "__main__":
    main()
