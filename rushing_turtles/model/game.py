import random

from typing import List
from itertools import repeat, chain, product

from rushing_turtles.model.card import Card
from rushing_turtles.model.player import Player
from rushing_turtles.model.board import Board
from rushing_turtles.model.action import Action
from rushing_turtles.model.card_stacks import CardStacks
from rushing_turtles.model.person import Person
from rushing_turtles.model.turtle import Turtle

HAND_SIZE = 5


class Game(object):
    cards: List[Card]
    stacks: CardStacks
    turtles: List[Turtle]
    board: Board
    players: List[Player]
    active_player: Player

    def __init__(self, people: List[Person], turtles: List[Turtle],
                 cards: List[Card]):
        if len(people) < 2:
            raise ValueError(
                'There are at least 2 players required to start the game')
        if len(cards) < HAND_SIZE * len(people):
            raise ValueError(f'Not enough cards for {len(people)} players')

        self.cards = cards
        self.stacks = CardStacks(cards)
        self.turtles = turtles
        self.board = Board(turtles)
        self.players = self._init_players(people, turtles)
        self.active_player = self.players[0]

        self._ensure_player_can_move(self.active_player)

    def _init_players(self, people: List[Person], turtles: List[Turtle]):
        random.shuffle(turtles)
        return [self._init_player(person, turtle)
                for person, turtle in zip(people, turtles)]

    def _init_player(self, person: Person, turtle: Turtle):
        return Player(person, turtle, self.stacks.get_new_cards(HAND_SIZE))

    def _ensure_player_can_move(self, player: Player):
        while not self._can_player_move(player):
            player.cards = self.stacks.get_new_cards(HAND_SIZE)

    def _can_player_move(self, player: Player):
        return any([self.board.is_move_with_card_possible(card)
                    for card in player.cards])

    def play(self, person: Person, action: Action) -> None:
        player = self._find_player(person)
        if player != self.active_player:
            raise ValueError(f"It is not {person}'s turn yet")
        if not player.has_card(action.card):
            raise ValueError("Player doesn't have given card")

        self._move_turtle(action)
        self._update_player_cards_and_stacks(player, action)

        if self._has_winner():
            return self._get_ranking()

        self._change_active_player()
        self._ensure_player_can_move(self.active_player)

    def _find_player(self, person: Person):
        for player in self.players:
            if player.person == person:
                return player
        raise ValueError(f'Person {person} does not play in this game')

    def _move_turtle(self, action: Action):
        turtle = self._find_turtle(action.get_color())
        if action.does_move_last_turtle() and not self.board.is_last(turtle):
            raise ValueError(
                'Arrow card can move only the last turtle.' +
                f'Turtle {turtle} is not one of the last turtles'
            )

        self.board.move(turtle, action.get_offset())

    def _find_turtle(self, color: str):
        for turtle in self.turtles:
            if turtle.color == color:
                return turtle
        raise ValueError(f'{color} turtle doesnt exist in this game')

    def get_card(self, id: int):
        for card in self.cards:
            if card.id == id:
                return card
        raise ValueError(f'Card with id {id} does not exist in this game')

    def _update_player_cards_and_stacks(self, player: Player, action: Action):
        self.stacks.put(action.card)
        player.remove_card(action.card)
        new_card = self.stacks.get_new()
        player.add_card(new_card)

    def _has_winner(self):
        return self.board.has_anyone_finished()

    def _get_ranking(self):
        ranking = self.board.get_ranking()
        player_turtles = [player.turtle for player in self.players]
        return [self._find_player_by_turtle(turtle).person
                for turtle in ranking if turtle in player_turtles]

    def _find_player_by_turtle(self, turtle: Turtle):
        for player in self.players:
            if player.turtle == turtle:
                return player
        raise ValueError(f'No player with given turtle: {turtle}')

    def _change_active_player(self):
        active_player_idx = self._find_player_idx(self.active_player)
        next_idx = (active_player_idx + 1) % len(self.players)
        self.active_player = self.players[next_idx]

    def _find_player_idx(self, player: Player):
        for idx, current in enumerate(self.players):
            if current == player:
                return idx
        raise ValueError(f'Player {player} does not play in this game')

    def get_person_idx(self, person: Person):
        for idx, player in enumerate(self.players):
            if player.person == person:
                return idx
        raise ValueError(f'Person {person} is not in this game')

    def get_persons_cards(self, person: Person):
        player = self._find_player(person)
        return player.cards

    # TODO: co, jeśli zostanie tylko jeden gracz?
    def remove_player(self, person: Person):
        player = self._find_player(person)
        if self.active_player == player:
            self._change_active_player()
        self.players.remove(player)


def create_game(people: List[Person]):
    turtles = [Turtle('RED'), Turtle('GREEN'), Turtle('BLUE'),
               Turtle('PURPLE'), Turtle('YELLOW')]
    cards = create_cards()
    random.shuffle(cards)
    return Game(people, turtles, cards)


def create_cards():
    colors = ['BLUE', 'RED', 'GREEN', 'YELLOW', 'PURPLE']
    actions = ['PLUS_PLUS', 'PLUS', 'MINUS', 'ARROW', 'ARROW_ARROW']

    regular_repetitions = [1, 5, 2, 0, 0]
    rainbow_repetitions = [0, 5, 2, 3, 2]

    regular_actions = chain.from_iterable((
        repeat(action, rep) for action, rep
        in zip(actions, regular_repetitions)
    ))

    rainbow_actions = chain.from_iterable((
        repeat(action, rep) for action, rep
        in zip(actions, rainbow_repetitions)
    ))

    all_combinations = chain(
      product(colors, regular_actions),
      product(['RAINBOW'], rainbow_actions))

    return [Card(idx, color, symbol)
            for idx, (color, symbol)
            in enumerate(all_combinations)]
