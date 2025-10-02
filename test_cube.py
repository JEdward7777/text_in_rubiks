import random
from cube import Cube


def main():
    #so in theory if we rotate the cube to the side and do operations there it should do the same
    #as though we didn't rotate the cube.

    #make the cubes
    size = 4
    cubeA = Cube(size)
    cubeB = Cube(size)

    for i in range( 1000 ):
        slice = random.randint( 0, size-1 )
        rotation_distance = random.choice( [-3, -2, -1, 1, 2, 3] )

        cube_rotate_axis = random.choice( [Cube.X_AXIS, Cube.Y_AXIS, Cube.Z_AXIS] )


        if cube_rotate_axis == Cube.X_AXIS:
            cubeA.do_command( "z" )
            #rotate the x axis on cubeA and the y axis on cubeB.
            cubeA.rotate( Cube.X_AXIS, slice=slice, distance=rotation_distance )
            cubeB.rotate( Cube.Y_AXIS, slice=slice, distance=rotation_distance )
            #spin the cubeA so that the X axis becomes the Y axis.
            cubeA.do_command( "z'" )

            #now assert that cubeA == cubeB
            assert cubeA == cubeB

        elif cube_rotate_axis == Cube.Y_AXIS:
            cubeA.do_command( "y" )
            #rotate the z axis on cubeA and the x axis on cubeB.
            cubeA.rotate( Cube.Z_AXIS, slice=slice, distance=rotation_distance )
            cubeB.rotate( Cube.X_AXIS, slice=slice, distance=rotation_distance )
            #spin the cubeA so that the Z axis becomes the X axis.
            cubeA.do_command( "y'" )

            #now assert that cubeA == cubeB
            assert cubeA == cubeB

        else:
            cubeA.do_command( "x" )
            #rotate the y axis on cubeA and the z axis on cubeB.
            cubeA.rotate( Cube.Y_AXIS, slice=slice, distance=rotation_distance )
            cubeB.rotate( Cube.Z_AXIS, slice=slice, distance=rotation_distance )
            #spin the cubeA so that the Y axis becomes the Z axis.
            cubeA.do_command( "x'" )

            #now assert that cubeA == cubeB
            assert cubeA == cubeB


    print( "all good" )

if __name__ == "__main__":
    main()