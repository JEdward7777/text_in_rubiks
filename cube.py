
import copy
import random


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
                print( self )
        return self

    def do_command( self, command ):
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
        elif command == "exit":
            done = True
        elif command == "reset":
            self = Cube( self.size )
        elif command == "scramble":
            self.scramble()
        else:
            raise ValueError( "I don't understand that command." )


def main( size=3 ):
    cube = Cube( size )

    done = False
    while not done:
        print( cube )

        #get the command.
        command = input( '> ' )

        #run the command
        try:
            cube.run_command( command )
        except ValueError as e:
            print( e )



if __name__ == "__main__":
    main()
