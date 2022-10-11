import random
from typing import List, Dict
"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict],
                  possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[
        1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"][
        "head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"][
        "body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(
    #     f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~"
    # )
    print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    board_height = data["board"]["height"]
    board_width = data["board"]["width"]
    def avoid_walls(head, height, width, possible_moves):
        if head["x"]==0:
            possible_moves.remove("left")
        if head["y"]==0:
            possible_moves.remove("down")
        if head["x"]==width-1:
            possible_moves.remove("right")
        if head["y"]==height-1:
            possible_moves.remove("up")
        return possible_moves


    possible_moves = avoid_walls(my_head, board_height, board_width, possible_moves)
    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body
    def bodysafe(data, head, possible_moves):
        for snake in data["board"]["snakes"]:
            for body in snake["body"]:
                if body["x"] == my_head["x"]+1 and body["y"] == my_head["y"]:
                    if "right" in possible_moves:
                        possible_moves.remove("right")
                if body["x"] == my_head["x"]-1 and body["y"] == my_head["y"]:
                    if "left" in possible_moves:
                        possible_moves.remove("left")
                if body["y"] == my_head["y"]+1 and body["x"] == my_head["x"]:
                    if "up" in possible_moves:
                        possible_moves.remove("up")
                if body["y"] == my_head["y"]-1 and body["x"] == my_head["x"]:
                    if "down" in possible_moves:
                        possible_moves.remove("down")
        return possible_moves
    possible_moves = bodysafe(data, my_head, possible_moves)
    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board
    def moves(x1,y1,x2,y2):
        return abs(x2-x1) + abs(y2-y1)
    def SnakeFood(data):
        hx = data["you"]["head"]["x"]
        hy = data["you"]["head"]["y"]
        food = data["board"]["food"]
        near = 0
        coords=[]
        for i in range(1,len(food)):
            fx,fy = food[i]["x"], food[i]["y"]
            if moves(hx,hy,fx,fy) < moves(hx,hy,food[near]["x"],food[near]["y"]):
                near = i
        coords.append(food[near]["x"])
        coords.append(food[near]["y"])
        return coords
    if bool(data["board"]["food"])!=False:
        if "left" in possible_moves and SnakeFood(data)[0]<my_head["x"]:
            possible_moves=["left"]
        if "right" in possible_moves and SnakeFood(data)[0]>my_head["x"]:
            possible_moves=["right"]
        if "down" in possible_moves and SnakeFood(data)[1]<my_head["y"]:
            possible_moves=["down"]
        if "up" in possible_moves and SnakeFood(data)[1]>my_head["y"]:
            possible_moves=["up"]

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}"
    )

    return move
