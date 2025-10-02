#can we solve a cube by randomly turning it and then sorting by how many faces are in the correct side?


import random
from cube import Cube

solved_cube = Cube(3)
def points( cube ):
    # just gives points for how many colors are in the right place ignoring if it is the right edge or whatever.
    result = 0
    for char1,char2 in zip( cube.lines, solved_cube.lines ):
        if char1 != ' ':
            if char1 != char2:
                result += 1
    return result


def main():
    cubes_to_keep = 1000

    cubes = [Cube(3).scramble()]

    print( f"solving the cube\n{cubes[0]}." )
    
    
    done = False
    iteration = 0

    while not done:
        new_cubes = []
        for cube_n, cube in enumerate(cubes):
            for _ in range( 100 if cube_n == 0 else 10 if cube_n < 10 else 1 ):
                new_cubes.append( cube.clone().scramble( steps=random.randint( 1, 10 ) ) )
        cubes.extend( new_cubes )
        

        for cube in cubes:
            if cube.is_solved():
                print( cube )
                done = True
                break

        #now remove duplicates.
        cubes = list( set( cubes ) )

        #now sort the list
        cubes.sort( key=points )

        #and truncate it.
        cubes = cubes[0:cubes_to_keep]

        #now print off the top 10 scores.
        if iteration % 10 == 0:
            print( f"iteration {iteration}" )
            for cube in cubes[0:10]:
                print( f"{points(cube)}", end=' ' )
            print()



        iteration += 1

if __name__ == "__main__":
    main()