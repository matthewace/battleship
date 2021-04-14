"""This package contains the objects needed to play a game of Battleship.

AttackBoard
ShipBoard
Ship
"""
from .gameboards import AttackBoard, ShipBoard
from .ship import Ship
from .player import Player, CPU, Human
from .battleship import Battleship

__all__ = ["AttackBoard", "Ship", "ShipBoard", "Player",
           "CPU", "Human", "Battleship"]
