import config

if __name__ == '__main__':

    #Do all setup initializations
    ptz = config.ptzcam()

#*****************************************************************************
# IP camera motion tests
#*****************************************************************************
    print 'Starting tests...'

    # move right -- (velocity, duration of move)
    ptz.move_pan(1.0, 2)

    # move left
    ptz.move_pan(-1.0, 2)

    # move down
    ptz.move_tilt(-1.0, 2)

    # Move up
    ptz.move_tilt(1.0, 2)

    # zoom in
    ptz.zoom(0.5, 2)

    # zoom out
    ptz.zoom(-0.5, 2)
	
    ptz.move_abspantilt(-1.0, 1.0, 1.0)
    ptz.move_abspantilt(1.0, -1.0, 1.0)


    exit()