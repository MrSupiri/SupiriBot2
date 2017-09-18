def solveMaze(movements):
    """
    #Inspiration from https://github.com/Mjrovai/MJRoBot-Maze-Solver
    Simple Algorithm to Solve Maze
    1st Chuck the all the Movements Robot Made to list starting with 3 elements and keep adding move by move
    While Adding Moves Check element before last element is Turn Back (B)
        If it's Simplify last movements by calculate how much Robot has Turn in last 3 Turn
        Then Select a Movement that needed be Done and remove last 3 elements from the list and add the calculate movement to the list
    :param movements-Movements Robot Made:
    :return:
    """
    pathLength = 0
    path = []
    for movement in movements:
        path.append(movement)
        pathLength+=1
        if pathLength < 3 or path[-2] != 'NL':
            continue
        totalAngle = 0
        for i in range(-1, -4, -1):
            if path[i] == 'RT':
                totalAngle += 90
            elif path[i] == 'LT':
                totalAngle += 270
            elif path[i] == 'NL':
                totalAngle += 180
        totalAngle = totalAngle % 360
        path = path[:-2]
        if totalAngle == 0:
            path[-1] = 'FW'
        elif totalAngle == 90:
            path[-1] = 'RT'
        elif totalAngle == 180:
            path[-1] = 'NL'
        elif totalAngle == 270:
            path[-1] = 'LT'



    return path

#                                    #                        #                             #
path = ['RT','LT','RT','FW','NL','LT','LT','RT','NL','LT','LT','FW','LT','LT','NL','RT','FW','LT','NL','LT','LT','RT']
print(path)
print(solveMaze(path))

#RLRFBLLRBLLFLLBRFLBLLL