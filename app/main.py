import json
import os
import random
import bottle
import numpy as np
from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    #print(json.dumps(data))

    color = "#EAD3F0"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #print(json.dumps(data))
    turn = data['turn']
    whole_body = data['you']['body']
    body = whole_body[1:]
    directions = ['up', 'down', 'left', 'right']
    head = whole_body[0]   
    board = data['board']
    board_width = data['board']['width']
    board_height = data['board']['height']
    food = data['board']['food']
    health = data['you']['health']
    #distances from food
    currentX = data['you']['body'][0]['x']
    #current Y position of the head
    currentY = data['you']['body'][0]['y']
    foodDistances = convert_to_list(data['board']['food'])
    #Current locations
    cur = convert_to_list(data['you']['body'])[0]
    #calculation
    ed = calculate_euclidean_distance(cur,foodDistances)
    #closest food
    if len(foodDistances) == 0:
      closestFood = [[0,0]]
    else:
      closestFood = foodDistances[np.argsort(ed)][0]
    #number of food
    numFood = len(food)
    #gets your health
    myHealth = health
    
    
    
    #delete later. just testing ideally make this go towards closest wall? then go for food when needed or when falling under threshhold? <|o_o|>
    direction = 'right'
    previous_direction = direction
    
    #-------I made it so it will only go for food if desperate rn - Erik------------------------------------------------------------------------------------------------------------------------------
    if myHealth < 30:
      if len(food) != 0: 
        if closestFood[0] < currentX and previous_direction != 'right':
          direction = 'left'
          previous_direction = 'left'
          print("food is less than the current x")
        if closestFood[0] > currentX and previous_direction != 'left':
          print("food is more than the current x")
          direction = 'right'
          previous_direction = 'right'
        if closestFood[0] == currentX:
          print("food is on the current x")
        if closestFood[1] < currentY and previous_direction != 'down':
          print("food is less than the current y")
          direction = 'up'
          previous_direction = 'up'

        if closestFood[1] > currentY and previous_direction != 'up':
          print("food is more than the current y")
          direction = 'down'
          previous_direction = 'down'
    #------------------------------------------------------------------------------------------------------------------
    
    
    if currentY == board_height - 1:
      direction = 'left'
      previous_direction = 'left'
      print("on the bottom wall")
   
    # WALLS
    if currentX == 0:
      direction = 'up'
      previous_direction = 'up'
      print("on the left wall")
    #top wall
    if currentY == 0:
      direction = 'right'
      previous_direction = 'right'
      print("on the top wall")
    #right wall
    if currentX == board_width - 1:
      if direction == 'right':
        direction = 'down'
        previous_direction = 'down'
        print("on the right wall")
        
  
    #***************************************************************************************************************************************
    #***************************************************************************************************************************************
    print("**************************************************************************************************************************************")
    print("snake head information")
    print(head)
    print("snake body info")
    print(whole_body)
    print("body info")
    print(body)
    print("current direction " + direction)
    print("last direction " + previous_direction)
    print("current X:")
    print(currentX)
    print ("current Y:")
    print(currentY)
    print("number of food")
    print(len(food))
    print("closest food distance")
    print(closestFood)
    print("current turn")
    print(turn)
    print("**************************************************************************************************************************************")
    return move_response(direction)
    #***************************************************************************************************************************************
    #***************************************************************************************************************************************

    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Clear Check. basically a big vibe check <|o_o|>
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def isNorthClear(currentX,currentY,boardW,boardH):
    if currentY == 0:
      print("north isnt clear")
      return false
    print("north is clear")
    return true
    
def isSouthClear(currentX,currentY,boardW,boardH):
    if currentY == 13:
      print("south isnt clear")
      return false
    print("south is clear")
    return true
def isEastClear(currentX,currentY,boardW,boardH):
    if currentX == 13:
      print("east isnt clear")
      return false
    print("east is clear")
    return true
def isWestClear(currentX,currentY,boardW,boardH):
    if currentX == 0:
      print("west isn't clear")
      return false
    print("west is clear :D")
    return true
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




def convert_to_list(arr):
    ret = []
    for a in arr:
        y, x = a['y'], a['x']
        ret.append((x, y))
    return np.array(ret)
def calculate_euclidean_distance(cur, lst):
    ret = []
    x1, y1 = cur
    for x2, y2 in lst:
        ret.append(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    return ret
  
@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
