from .enums.direction import Direction

BOARDS = [{'tiles_per_row': 10, 'rem_per_tile': 3, 'tiles_per_column': 10,
           'path': '/static/boards/snakes_and_ladders_1.png',
           'interactive_objects':
               [
                   {
                       'initialPosition': 15,
                       'finalPosition': 26,
                       'direction': Direction.RIGHT.value,
                       'yMovement': 1,
                       'xMovement': 0
                   },
                   {
                       'initialPosition': 22,
                       'finalPosition': 18,
                       'direction': Direction.LEFT.value,
                       'yMovement': -1,
                       'xMovement': 1
                   },
                   {
                       'initialPosition': 66,
                       'finalPosition': 38,
                       'direction': Direction.RIGHT.value,
                       'yMovement': -3,
                       'xMovement': -3
                   },
                   {
                       'initialPosition': 76,
                       'finalPosition': 28,
                       'direction': Direction.RIGHT.value,
                       'yMovement': -5,
                       'xMovement': 3
                   },
                   {
                       'initialPosition': 49,
                       'finalPosition': 72,
                       'direction': Direction.LEFT.value,
                       'yMovement': 3,
                       'xMovement': 0
                   },
                   {
                       'initialPosition': 59,
                       'finalPosition': 83,
                       'direction': Direction.RIGHT.value,
                       'yMovement': 3,
                       'xMovement': 1
                   }
               ]
           },
          {'tiles_per_row': 10, 'rem_per_tile': 3, 'tiles_per_column': 10,
           'path': '/static/boards/snakes_and_ladders_2.png',
           'interactive_objects':
               [
                   {
                       'initialPosition': 17,
                       'finalPosition': 3,
                       'direction': Direction.RIGHT.value,
                       'yMovement': -1,
                       'xMovement': -1
                   },
                   {
                       'initialPosition': 32,
                       'finalPosition': 6,
                       'direction': Direction.RIGHT.value,
                       'yMovement': -3,
                       'xMovement': -3
                   },
                   {
                       'initialPosition': 23,
                       'finalPosition': 55,
                       'direction': Direction.LEFT.value,
                       'yMovement': 3,
                       'xMovement': 3
                   },
                   {
                       'initialPosition': 77,
                       'finalPosition': 46,
                       'direction': Direction.RIGHT.value,
                       'yMovement': 3,
                       'xMovement': 2
                   },
                   {
                       'initialPosition': 84,
                       'finalPosition': 97,
                       'direction': Direction.LEFT.value,
                       'yMovement': 1,
                       'xMovement': 0
                   }
               ]
           }
          ]
