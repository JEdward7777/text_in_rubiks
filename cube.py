
import copy
import random
import kociemba
import huffy_code


NUM_ROTATIONS = 4

BY_3_NUM_CORNERS = 8
BY_3_NUM_EDGES = 4*3
BY_3_NUM_CORNER_ROTATIONS = 3
BY_3_NUM_EDGE_ROTATIONS = 2


#now convert this into a cube.
BY_3_CORNER_LOCATIONS = [ 
    [ [ 3, 0 ], [  0, 3 ], [ 11, 3 ] ], #ULB
    [ [ 5, 0 ], [  9, 3 ], [  8, 3 ] ], #URB
    [ [ 3, 2 ], [  3, 3 ], [  2, 3 ] ], #ULF
    [ [ 5, 2 ], [  6, 3 ], [  5, 3 ] ], #URF
    [ [ 0, 5 ], [  3, 8 ], [ 11, 5 ] ], #DLB
    [ [ 2, 5 ], [  3, 5 ], [  3, 6 ] ], #DLF
    [ [ 5, 5 ], [  6, 5 ], [  5, 6 ] ], #DRF
    [ [ 8, 5 ], [  9, 5 ], [  5, 8 ] ], #DRB
]

BY_3_EDGE_LOCATIONS = [
    [ [ 4, 0 ], [ 10, 3 ] ], #UB
    [ [ 3, 1 ], [  1, 3 ] ], #UL
    [ [ 5, 1 ], [  7, 3 ] ], #UR
    [ [ 4, 2 ], [  4, 3 ] ], #UF
    [ [ 0, 4 ], [ 11, 4 ] ], #LB
    [ [ 2, 4 ], [  3, 4 ] ], #LF
    [ [ 5, 4 ], [  6, 4 ] ], #RF
    [ [ 8, 4 ], [  9, 4 ] ], #RB
    [ [ 1, 5 ], [  3, 7 ] ], #LD
    [ [ 4, 5 ], [  4, 6 ] ], #FD
    [ [ 7, 5 ], [  5, 7 ] ], #RD
    [ [ 10,5 ], [  4, 8 ] ], #BD
]


def numberToLocations( number ):
    number_left = number

    #peel off some values off front which helps
    #with solvablility distribution.
    last_corner_pos = number_left % 2
    number_left = number_left // 2
    last_corner_rotation = number_left % BY_3_NUM_CORNER_ROTATIONS
    number_left = number_left // BY_3_NUM_CORNER_ROTATIONS
    last_edge_rotation = number_left % BY_3_NUM_EDGE_ROTATIONS
    number_left = number_left // BY_3_NUM_EDGE_ROTATIONS

    #determine the locations of the corners.
    available_corners = list(range(BY_3_NUM_CORNERS))
    corner_selection = [-1 for i in range(BY_3_NUM_CORNERS)]
    for i in range(BY_3_NUM_CORNERS):
        spots_left = len( available_corners )

        if i != BY_3_NUM_CORNERS-2:
            #munus 2 because the last last location
            #is degenerate.
            picked_offset = number_left % spots_left
            number_left = number_left // spots_left
        else:
            #special case for last corner.
            picked_offset = last_corner_pos
        picked_location = available_corners.pop( picked_offset )
        corner_selection[picked_location] = i

    #assert no -1 in corner_selection
    assert -1 not in corner_selection, "no -1 in corner_selection"

    #determine the angle of the corners.
    corner_angle = [-1 for i in range(BY_3_NUM_CORNERS)]
    for i in range(BY_3_NUM_CORNERS):
        if i != 0:
            #All the rotations are the same count so testing for zero
            #is enough.
            corner_angle[i] = number_left % BY_3_NUM_CORNER_ROTATIONS
            number_left = number_left // BY_3_NUM_CORNER_ROTATIONS
        else:
            corner_angle[i] = last_corner_rotation

    #determine the location of the edges.
    available_edges = list(range(BY_3_NUM_EDGES))
    edge_selection = [-1 for i in range(BY_3_NUM_EDGES)]
    for i in range(BY_3_NUM_EDGES):
        spots_left = len( available_edges )
        picked_offset = number_left % spots_left
        number_left = number_left // spots_left
        picked_location = available_edges.pop( picked_offset )
        edge_selection[picked_location] = i

    #assert no -1 in edge_selection
    assert -1 not in edge_selection, "no -1 in edge_selection"

    #determine the angle of the edges.
    edge_angle = [-1 for i in range(BY_3_NUM_EDGES)]
    for i in range(BY_3_NUM_EDGES):
        if i != 0:
            edge_angle[i] = number_left % BY_3_NUM_EDGE_ROTATIONS
            number_left = number_left // BY_3_NUM_EDGE_ROTATIONS
        else:
            edge_angle[i] = last_edge_rotation

    return corner_selection, corner_angle, edge_selection, edge_angle

def locationsToNumber( corner_selection, corner_angle, edge_selection, edge_angle ):
    number = 0

    last_corner_pos = None
    last_corner_rotation = None
    last_edge_rotation = None

    #come from the angle of the edges.
    for i in range( BY_3_NUM_EDGES-1, -1, -1 ):
        if i != 0:
            number *= BY_3_NUM_EDGE_ROTATIONS
            number += edge_angle[i]
        else:
            last_edge_rotation = edge_angle[i]

    #now utilize the location of the edges.
    for i in range( BY_3_NUM_EDGES-1, -1, -1 ):
        spots_left = BY_3_NUM_EDGES - i
        #add up the indexes before it that would be blank during population.
        found_it = False
        would_be_blanks_found = 0
        search_index = 0
        while search_index < len( edge_selection ) and not found_it:
            if edge_selection[search_index] == i:
                found_it = True
            elif edge_selection[search_index] > i:
                would_be_blanks_found += 1
            search_index += 1
        assert found_it, "Didn't find edge in edge_selection"

        number *= spots_left
        number += would_be_blanks_found

    #now utilize the angle of the corners.
    for i in range( BY_3_NUM_CORNERS-1, -1, -1 ):
        if i != 0:
            number *= BY_3_NUM_CORNER_ROTATIONS
            number += corner_angle[i]
        else:
            last_corner_rotation = corner_angle[i]

    #now utilize the location of the corners.
    for i in range( BY_3_NUM_CORNERS-1, -1, -1 ):
        spots_left = BY_3_NUM_CORNERS - i
        #add up the indexes before it that would be blank during population.
        found_it = False
        would_be_blanks_found = 0
        search_index = 0
        while search_index < len( corner_selection ) and not found_it:
            if corner_selection[search_index] == i:
                found_it = True
            elif corner_selection[search_index] > i:
                would_be_blanks_found += 1
            search_index += 1
        assert found_it, "Didn't find corner in corner_selection"

        if i != BY_3_NUM_CORNERS-2:
            number *= spots_left
            number += would_be_blanks_found
        else:
            last_corner_pos = would_be_blanks_found

    number *= BY_3_NUM_EDGE_ROTATIONS
    number += last_edge_rotation

    number *= BY_3_NUM_CORNER_ROTATIONS
    number += last_corner_rotation

    number *= 2
    number += last_corner_pos

    return number


def locations_to_cube( corner_selection, corner_angle, edge_selection, edge_angle ):
    from_cube = Cube( 3 )
    to_cube = Cube( 3 )

    from_lines_split = from_cube.lines.split( "\n" )
    to_lines_split = [ list(line) for line in to_cube.lines.split( "\n" ) ]

    double_check_out = []
    for _ in range( 3*3 ):
        line = []
        double_check_out.append( line )
        for _ in range( 3*4 ):
            line.append( ' ' )

    for i_c in range( BY_3_NUM_CORNERS ):
        for i_angle in range( BY_3_NUM_CORNER_ROTATIONS ):
            from_x = BY_3_CORNER_LOCATIONS[i_c][i_angle][0]
            from_y = BY_3_CORNER_LOCATIONS[i_c][i_angle][1]

            i_angle_to = corner_angle[i_c] + i_angle
            if i_angle_to >= BY_3_NUM_CORNER_ROTATIONS:
                i_angle_to -= BY_3_NUM_CORNER_ROTATIONS

            to_x = BY_3_CORNER_LOCATIONS[corner_selection[i_c]][i_angle_to][0]
            to_y = BY_3_CORNER_LOCATIONS[corner_selection[i_c]][i_angle_to][1]

            color = from_lines_split[from_y][from_x]
            to_lines_split[to_y][to_x] = color
            double_check_out[to_y][to_x] = color

    for i_e in range( BY_3_NUM_EDGES ):
        for i_angle in range( BY_3_NUM_EDGE_ROTATIONS ):
            from_x = BY_3_EDGE_LOCATIONS[i_e][i_angle][0]
            from_y = BY_3_EDGE_LOCATIONS[i_e][i_angle][1]

            i_angle_to = edge_angle[i_e] + i_angle
            if i_angle_to >= BY_3_NUM_EDGE_ROTATIONS:
                i_angle_to -= BY_3_NUM_EDGE_ROTATIONS

            to_x = BY_3_EDGE_LOCATIONS[edge_selection[i_e]][i_angle_to][0]
            to_y = BY_3_EDGE_LOCATIONS[edge_selection[i_e]][i_angle_to][1]

            color = from_lines_split[from_y][from_x]
            to_lines_split[to_y][to_x] = color
            double_check_out[to_y][to_x] = color

    #print( double_check_out )

    to_cube.lines = "\n".join( "".join( color for color in line ) for line in to_lines_split )

    return to_cube

def cube_to_locations( cube ):
    #going to throw away the informatino of the cube being rotated without slices
    #because that information gets lost just handing the cube.
    _, cube = cube.get_presolution()

    #I am not reconstructing the number yet, so I don't have to do it in reverse,
    #I just have to find where each cube and edge ran off to.

    reference_cube = Cube( 3 )

    reference_lines_split = reference_cube.lines.split( "\n" )
    cube_lines_split = cube.lines.split( "\n" )


    corner_selection = []
    corner_angle = []
    edge_selection = []
    edge_angle = []

    for i_cube in range( BY_3_NUM_CORNERS ):
        #search through all the locations and angles to figure out
        #where i_cube is at.
        pos_search = 0
        found_it = False
        while pos_search < BY_3_NUM_CORNERS and not found_it:
            angle_search = 0
            while angle_search < BY_3_NUM_CORNER_ROTATIONS and not found_it:
                angle_index_search = 0
                is_this_one = True
                while angle_index_search < BY_3_NUM_CORNER_ROTATIONS and is_this_one:

                    effected_out_angle = angle_search + angle_index_search
                    if effected_out_angle >= BY_3_NUM_CORNER_ROTATIONS:
                        effected_out_angle -= BY_3_NUM_CORNER_ROTATIONS

                    from_x = BY_3_CORNER_LOCATIONS[i_cube][angle_index_search][0]
                    from_y = BY_3_CORNER_LOCATIONS[i_cube][angle_index_search][1]

                    to_x = BY_3_CORNER_LOCATIONS[pos_search][effected_out_angle][0]
                    to_y = BY_3_CORNER_LOCATIONS[pos_search][effected_out_angle][1]

                    if cube_lines_split[to_y][to_x] != reference_lines_split[from_y][from_x]:
                        is_this_one = False
                    else:
                        angle_index_search += 1
                if is_this_one:
                    found_it = True
                else:
                    angle_search += 1
            if not found_it:
                pos_search += 1

        assert found_it, f"Couldn't find corner {i_cube}"

        corner_selection.append( pos_search )
        corner_angle.append( angle_search )


    for i_edge in range( BY_3_NUM_EDGES ):
        #search through all the locations and angles to figure out
        #where i_edge is at.
        pos_search = 0
        found_it = False
        while pos_search < BY_3_NUM_EDGES and not found_it:
            angle_search = 0
            while angle_search < BY_3_NUM_EDGE_ROTATIONS and not found_it:
                angle_index_search = 0
                is_this_one = True
                while angle_index_search < BY_3_NUM_EDGE_ROTATIONS and is_this_one:

                    effected_out_angle = angle_search + angle_index_search
                    if effected_out_angle >= BY_3_NUM_EDGE_ROTATIONS:
                        effected_out_angle -= BY_3_NUM_EDGE_ROTATIONS

                    from_x = BY_3_EDGE_LOCATIONS[i_edge][angle_index_search][0]
                    from_y = BY_3_EDGE_LOCATIONS[i_edge][angle_index_search][1]

                    to_x = BY_3_EDGE_LOCATIONS[pos_search][effected_out_angle][0]
                    to_y = BY_3_EDGE_LOCATIONS[pos_search][effected_out_angle][1]

                    if cube_lines_split[to_y][to_x] != reference_lines_split[from_y][from_x]:
                        is_this_one = False
                    else:
                        angle_index_search += 1
                if is_this_one:
                    found_it = True
                else:
                    angle_search += 1
            if not found_it:
                pos_search += 1

        assert found_it, f"Couldn't find edge {i_edge}"

        edge_selection.append( pos_search )
        edge_angle.append( angle_search )

    return corner_selection, corner_angle, edge_selection, edge_angle

                



def numberToCube( number, talk_skipped=False ):

    found_it = None
    for extra_number in range( 12 ):
        number_with_extra = number*12 + extra_number
        corner_selection, corner_angle, edge_selection, edge_angle = numberToLocations( number_with_extra )
        to_cube = locations_to_cube( corner_selection, corner_angle, edge_selection, edge_angle )
        try:
            #print( to_cube )
            to_cube.get_solution()
            found_it = to_cube
            if talk_skipped: 
                print( f" {number}:{extra_number}" )
            else:
                return to_cube
        except:
            pass

    assert found_it is not None, "no solution found"
    return found_it


def test_cube_to_locations():
    #i = 1
    #if True:
    for _ in range( 10000 ):
        i = random.randint( 0, 43252003274489855999 )

        corner_selection, corner_angle, edge_selection, edge_angle = numberToLocations( i )
        cube = locations_to_cube( corner_selection, corner_angle, edge_selection, edge_angle )
        corner_selection2, corner_angle2, edge_selection2, edge_angle2 = cube_to_locations( cube )
        assert corner_selection == corner_selection2, f"{corner_selection} != {corner_selection2}"
        assert corner_angle == corner_angle2, f"{corner_angle} != {corner_angle2}"
        assert edge_selection == edge_selection2, f"{edge_selection} != {edge_selection2}"
        assert edge_angle == edge_angle2, f"{edge_angle} != {edge_angle2}"
        reconstructed_number = locationsToNumber( corner_selection2, corner_angle2, edge_selection2, edge_angle2 )

        assert i == reconstructed_number, f"{i} != {reconstructed_number}"

    print( "passed" )

def cubeToNumber( cube ):
    corner_selection, corner_angle, edge_selection, edge_angle = cube_to_locations( cube )
    number_with_extra = locationsToNumber( corner_selection, corner_angle, edge_selection, edge_angle )
    number_without_extra = number_with_extra // 12
    return number_without_extra

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
        
    def rotate( self, axis, slice_n, distance ):
        if distance == 0: return

        while distance < 0: distance += NUM_ROTATIONS

        lines_from = [list( line ) for line in self.lines.splitlines()]
        lines_to = copy.deepcopy( lines_from )

        if slice_n < 0: slice_n += self.size

        for to_face in range( NUM_ROTATIONS ):
            from_face = (to_face+1) % NUM_ROTATIONS
            for i in range( self.size ):

                def location( face ):
                    if axis == Cube.X_AXIS:
                        if face < 3:
                            col = self.size + slice_n
                            row = i + face*self.size
                        else:
                            col = self.size*4 - 1 - slice_n
                            row = self.size*2 - 1 - i
                    elif axis == Cube.Y_AXIS:
                        row = self.size*2 - 1 - slice_n
                        col = i + face*self.size
                    else:
                        if face == 0:
                            row = self.size + i
                            col = slice_n
                        elif face == 1:
                            row = self.size*3-1-slice_n
                            col = self.size + i
                        elif face == 2:
                            row = self.size*2 - 1 - i
                            col = self.size*3 - 1 - slice_n
                        else:
                            row = slice_n
                            col = self.size*2 - 1 - i
                    return row, col 
                
                from_row, from_column = location( from_face )
                to_row, to_column = location( to_face )

                lines_to[to_row][to_column] = lines_from[from_row][from_column]

        do_rotation = False
        if slice_n == 0 or slice_n == self.size-1:
            do_rotation = True

    
        if axis == Cube.X_AXIS:
            if slice_n == 0:
                rot_row, rot_col = self.size, 0
            elif slice_n == self.size-1:
                rot_row, rot_col = self.size, self.size*2
        elif axis == Cube.Y_AXIS:
            if slice_n == 0:
                rot_row, rot_col = self.size*2, self.size
            elif slice_n == self.size-1:
                rot_row, rot_col = 0          , self.size
        else:
            if slice_n == 0:
                rot_row, rot_col = self.size, self.size*3
            elif slice_n == self.size-1:
                rot_row, rot_col = self.size, self.size

        if do_rotation:
            self.rotate_area( lines_from, lines_to, rot_row, rot_col, slice_n != 0 )

        self.lines = "\n".join( "".join( line ) for line in lines_to )

        self.rotate( axis, slice_n, distance-1 )

    def scramble( self, steps=20, talk=False ):
        for i in range( steps ):
            axis = random.choice( [Cube.X_AXIS, Cube.Y_AXIS, Cube.Z_AXIS] )
            slice_n = random.randint( 0, self.size-1 )
            distance = random.randint( 1, 3 )
            self.rotate( axis, slice_n, distance )
            
            if talk:
                print( f"axis {axis} slice_n {slice_n} distance {distance}" )
                if self.size == 3: print( self.get_solution() )
                print( self )


        return self

    def get_presolution( self ):
        cube_copy = self.clone()

        #get the y face on top
        lines_split = cube_copy.lines.split( "\n" )
        presolution = ""
        if lines_split[4][1] == 'y':
            presolution += 'z '
            for i in range( 3 ):
                cube_copy.rotate( Cube.Z_AXIS, slice_n=i, distance=1 )
        elif lines_split[4][4] == 'y':
            presolution += 'x '
            for i in range( 3 ):
                cube_copy.rotate( Cube.X_AXIS, slice_n=i, distance=1 )
        elif lines_split[4][7] == 'y':
            presolution += "z' "
            for i in range( 3 ):
                cube_copy.rotate( Cube.Z_AXIS, slice_n=i, distance=-1 )
        elif lines_split[4][10] == 'y':
            presolution += "x' "
            for i in range( cube_copy.size ):
                cube_copy.rotate( Cube.X_AXIS, slice_n=i, distance=-1 )
        elif lines_split[7][4] == 'y':
            presolution += 'x2 '
            for i in range( 3 ):
                cube_copy.rotate( Cube.X_AXIS, slice_n=i, distance=1 )
                cube_copy.rotate( Cube.X_AXIS, slice_n=i, distance=1 )


        lines_split = cube_copy.lines.split( "\n" )
        #now get r frace in front.
        if lines_split[4][1] == 'r':
            presolution += "y' "
            for i in range( cube_copy.size ):
                cube_copy.rotate( Cube.Y_AXIS, slice_n=i, distance=-1 )
        elif lines_split[4][7] == 'r':
            presolution += "y "
            for i in range( cube_copy.size ):
                cube_copy.rotate( Cube.Y_AXIS, slice_n=i, distance=1 )
        elif lines_split[4][10] == 'r':
            presolution += 'y2 '
            for i in range( cube_copy.size ):
                cube_copy.rotate( Cube.Y_AXIS, slice_n=i, distance=1 )
                cube_copy.rotate( Cube.Y_AXIS, slice_n=i, distance=1 )

        return presolution, cube_copy

    def get_kociemba_string( self ):
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

        presolution, cube_copy = self.get_presolution()
        
        lines_split = cube_copy.lines.split( "\n" )

        current_string = ""
        for location_name in location_names:
            location = location_spots[location_name]
            current_color = lines_split[location[1]][location[0]]
            current_name = color_map[current_color]
            current_string += current_name

        return presolution, current_string

    def get_solution( self ):
        presolution, current_string = self.get_kociemba_string()
        return presolution + kociemba.solve( current_string )

    def get_reverse_solution( self ):
        normal_string = Cube(size=3).get_kociemba_string()[1]
        current_string = self.get_kociemba_string()[1]

        return kociemba.solve( normal_string, current_string )

    def solve_from( self, other ):
        other_presolution, other_string = other.get_kociemba_string()
        my_string = self.get_kociemba_string()[1]

        return other_presolution + kociemba.solve( other_string, my_string )

    def do_command( self, command ):
        done = False
        if command == "L":
            #reverse direction because clockwise is backwards on left.
            self.rotate( Cube.X_AXIS, slice_n=0, distance=-1 )
        elif command == "L'":
            self.rotate( Cube.X_AXIS, slice_n=0, distance=1 )
        elif command == "L2":
            self.rotate( Cube.X_AXIS, slice_n=0, distance=2 )
        elif command == "R":
            self.rotate( Cube.X_AXIS, slice_n=-1, distance=1 )
        elif command == "R'":
            self.rotate( Cube.X_AXIS, slice_n=-1, distance=-1 )
        elif command == "R2":
            self.rotate( Cube.X_AXIS, slice_n=-1, distance=2 )
        elif command == "U":
            self.rotate( Cube.Y_AXIS, slice_n=-1, distance=1 )
        elif command == "U'":
            self.rotate( Cube.Y_AXIS, slice_n=-1, distance=-1 )
        elif command == "U2":
            self.rotate( Cube.Y_AXIS, slice_n=-1, distance=2 )
        elif command == "D":
            self.rotate( Cube.Y_AXIS, slice_n=0, distance=-1 )
        elif command == "D'":
            self.rotate( Cube.Y_AXIS, slice_n=0, distance=1 )
        elif command == "D2":
            self.rotate( Cube.Y_AXIS, slice_n=0, distance=2 )
        elif command == "F":
            self.rotate( Cube.Z_AXIS, slice_n=-1, distance=1 )
        elif command == "F'":
            self.rotate( Cube.Z_AXIS, slice_n=-1, distance=-1 )
        elif command == "F2":
            self.rotate( Cube.Z_AXIS, slice_n=-1, distance=2 )
        elif command == "B":
            self.rotate( Cube.Z_AXIS, slice_n=0, distance=-1 )
        elif command == "B'":
            self.rotate( Cube.Z_AXIS, slice_n=0, distance=1 )
        elif command == "B2":
            self.rotate( Cube.Z_AXIS, slice_n=0, distance=2 )
        elif command == "x":
            for i in range( self.size ):
                self.rotate( Cube.X_AXIS, slice_n=i, distance=1 )
        elif command == "x'":
            for i in range( self.size ):
                self.rotate( Cube.X_AXIS, slice_n=i, distance=-1 )
        elif command == "x2":
            for i in range( self.size ):
                self.rotate( Cube.X_AXIS, slice_n=i, distance=2 )
        elif command == "y":
            for i in range( self.size ):
                self.rotate( Cube.Y_AXIS, slice_n=i, distance=1 )
        elif command == "y'":
            for i in range( self.size ):
                self.rotate( Cube.Y_AXIS, slice_n=i, distance=-1 )
        elif command == "y2":
            for i in range( self.size ):
                self.rotate( Cube.Y_AXIS, slice_n=i, distance=2 )
        elif command == "z":
            for i in range( self.size ):
                self.rotate( Cube.Z_AXIS, slice_n=i, distance=1 )
        elif command == "z'":
            for i in range( self.size ):
                self.rotate( Cube.Z_AXIS, slice_n=i, distance=-1 )
        elif command == "z2":
            for i in range( self.size ):
                self.rotate( Cube.Z_AXIS, slice_n=i, distance=2 )
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
        elif command == "reverse solve":
            print( "yellow on top and red in front" )
            print( self.get_reverse_solution() )
        elif command == "set":
            lines = []
            read_line = input( "" )
            while read_line != "":
                lines.append( read_line )
                read_line = input( "" )
            size = int(len( lines ) / 3)
            self.size = size
            self.lines = "\n".join( lines )
        elif command == "solve from":
            lines = []
            read_line = input( "" )
            while read_line != "":
                lines.append( read_line )
                read_line = input( "" )
            size = int(len( lines ) / 3)
            _from = Cube( size )
            _from.size = size
            _from.lines = "\n".join( lines )

            print(self.solve_from( _from ))

        elif command == "to string" or command == "get string":
            print( cubeToString( self ) )
        elif command == "from string" or command == "set string":
            string = input( "? " )
            string_cube = stringToCube( string )
            self.size = string_cube.size
            self.lines = string_cube.lines
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

#def sentence_to_cube( string ):
    # as_number = huffy_code.to_number( string )
    # assert as_number < 43252003274489856000, "string too long"
    # as_cube = numberToCube( as_number )
    # print( as_cube )
    # back_as_number = cubeToNumber( as_cube )
    # assert as_number == back_as_number, f"{as_number} != {back_as_number}"
    # back_as_string = huffy_code.from_number( as_number )
    # assert string == back_as_string, f"{string} != {back_as_string}"
    # print( "Done" )


def stringToCube( string ):
    as_number = huffy_code.to_number( string )
    if as_number >= 43252003274489856000: print( "string too long" )
    return numberToCube( as_number )

def cubeToString( cube ):
    as_number = cubeToNumber( cube )
    return huffy_code.from_number( as_number )

def test_sentence_to_cube_and_back():
    string = "i love jesus"
    as_number = huffy_code.to_number( string )
    assert as_number < 43252003274489856000, "string too long"
    as_cube = numberToCube( as_number )
    print( as_cube )
    back_as_number = cubeToNumber( as_cube )
    assert as_number == back_as_number, f"{as_number} != {back_as_number}"
    back_as_string = huffy_code.from_number( as_number )
    assert string == back_as_string, f"{string} != {back_as_string}"
    print( "Done" )



def testNumberToCubeSolvability():
    random.seed( 0 )
    for _ in range( 100 ):
        i = random.randint( 0, 43252003274489855999 )
        try:
            cube = numberToCube( i, talk_skipped=True )
            print( f"{i} yes" )
        except:
            print( f"{i} no" )

if __name__ == "__main__":
    main()
    # cube = numberToCube( 1 )
    # print( cube )
    # print( cube.get_solution() )
    #test_cube_to_locations()
    #test_sentence_to_cube_and_back()
