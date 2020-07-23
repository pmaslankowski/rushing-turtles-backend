import pytest
import random

from rushing_turtles.game_controller import GameController, MAX_PLAYERS_IN_ROOM
from rushing_turtles.messages import MsgToSend
from rushing_turtles.messages import HelloServerMsg
from rushing_turtles.messages import WantToJoinMsg
from rushing_turtles.messages import StartGameMsg
from rushing_turtles.messages import ReadyToReceiveGameState
from rushing_turtles.messages import PlayCardMsg
from rushing_turtles.model.turtle import Turtle


@pytest.fixture(autouse=True)
def init_rand_seed():
    random.seed(0)


def test_should_emit_can_create_when_first_player_joins():
    controller = GameController()

    actual = controller.handle(HelloServerMsg(0, 'Piotr'), 0)

    expected = MsgToSend(
        0,
        message='hello client',
        status='can create',
        list_of_players_in_room=[]
    )

    assert actual == expected


def test_should_raise_when_player_with_given_id_is_already_connected():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)

    with pytest.raises(ValueError):
        controller.handle(HelloServerMsg(0, 'Piotr'), 0)


def test_should_raise_when_player_tries_to_create_room_but_is_not_in_lounge():
    controller = GameController()

    with pytest.raises(ValueError):
        controller.handle(WantToJoinMsg(0), 0)


def test_should_emit_room_updated_when_player_creates_the_room():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    actual = controller.handle(WantToJoinMsg(0), 0)
    expected_msg = MsgToSend(
        0,
        message='room update',
        list_of_players_in_room=['Piotr']
    )

    assert expected_msg in actual


def test_should_broadcast_room_updated_when_player_creates_the_room():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    actual = controller.handle(WantToJoinMsg(0), 0)

    expected_msgs = [
        MsgToSend(
            0,
            message='room update',
            list_of_players_in_room=['Piotr']
        ),
        MsgToSend(
            1,
            message='room update',
            list_of_players_in_room=['Piotr']
        )
    ]

    for msg in expected_msgs:
        assert msg in actual


def test_should_emit_can_join_when_another_player_connects():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(WantToJoinMsg(0), 0)

    actual = controller.handle(HelloServerMsg(1, 'Marta'), 1)

    expected = MsgToSend(
        1,
        message='hello client',
        status='can join',
        list_of_players_in_room=['Piotr']
    )

    assert actual == expected


def test_raises_when_player_wants_to_join_the_room_but_is_not_connected():
    controller = GameController()

    with pytest.raises(ValueError):
        controller.handle(WantToJoinMsg(0), 0)


def test_raises_when_player_wants_to_join_room_that_they_are_already_in():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(WantToJoinMsg(0), 0)

    with pytest.raises(ValueError):
        controller.handle(WantToJoinMsg(0), 0)


def test_should_broadcast_room_update_when_another_player_joins_the_room():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    actual = controller.handle(WantToJoinMsg(1), 1)

    expected = [
        MsgToSend(0, message='room update',
                  list_of_players_in_room=['Piotr', 'Marta']),
        MsgToSend(1, message='room update',
                  list_of_players_in_room=['Piotr', 'Marta'])
    ]

    for msg in expected:
        assert msg in actual


def test_should_broadcast_room_update_to_all_other_players():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)

    actual = controller.handle(WantToJoinMsg(0), 0)

    expected = MsgToSend(
        1,
        message='hello client',
        status='can join',
        list_of_players_in_room=['Piotr']
    )

    assert expected in actual


def test_shouldnt_send_can_join_msg_to_player_who_created_the_room():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)

    actual = controller.handle(WantToJoinMsg(0), 0)

    not_expected = MsgToSend(
        0,
        message='hello client',
        status='can join',
        list_of_players_in_room=['Piotr']
    )

    assert not_expected not in actual


def test_should_emit_limit_on_hello_server_when_there_are_five_players():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Player_0'), 0)
    controller.handle(WantToJoinMsg(0), 0)

    for i in range(1, MAX_PLAYERS_IN_ROOM):
        controller.handle(HelloServerMsg(i, f'Player_{i}'), i)
        controller.handle(WantToJoinMsg(i), i)

    actual = controller.handle(HelloServerMsg(5, 'Player_5'), 5)

    assert actual == MsgToSend(
        5,
        message='hello client',
        status='limit',
        list_of_players_in_room=[f'Player_{i}' for i in range(5)]
    )


def test_should_raise_when_player_tries_to_join_full_room():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Player_0'), 0)
    controller.handle(WantToJoinMsg(0), 0)

    for i in range(1, MAX_PLAYERS_IN_ROOM):
        controller.handle(HelloServerMsg(i, f'Player_{i}'), i)
        controller.handle(WantToJoinMsg(i), i)

    controller.handle(HelloServerMsg(5, 'Player_5'), 5)
    with pytest.raises(ValueError):
        controller.handle(WantToJoinMsg(5), 5)


def test_should_raise_when_player_tries_to_pose_as_somebody_else_on_join():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)

    with pytest.raises(ValueError):
        controller.handle(WantToJoinMsg(1), 0)


def test_should_emit_can_resume_when_player_disconnects_and_reconnects():
    controller = GameController()
    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(WantToJoinMsg(0), 0)

    controller.disconnected(0)

    actual = controller.handle(HelloServerMsg(0, 'Piotr'), 1)

    assert actual == MsgToSend(
        1,
        message='hello client',
        status='can resume',
        list_of_players_in_room=['Piotr']
    )


def test_should_raise_when_player_who_is_not_in_room_tries_to_start_the_game():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    with pytest.raises(ValueError):
        controller.handle(StartGameMsg(0), 0)


def test_should_raise_when_not_first_player_tries_to_start_the_game():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)

    with pytest.raises(ValueError):
        controller.handle(StartGameMsg(1), 1)


def test_raises_when_player_tries_to_pose_as_somebody_else_on_start_game():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)

    with pytest.raises(ValueError):
        controller.handle(StartGameMsg(0), 1)


def test_should_emit_ongoing_when_new_player_connects_after_game_started():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)
    controller.handle(StartGameMsg(0), 0)

    actual = controller.handle(HelloServerMsg(2, 'Other'), 2)

    assert actual == MsgToSend(
        2,
        message='hello client',
        status='ongoing',
        list_of_players_in_room=['Piotr', 'Marta']
    )


def test_should_broadcast_ongoing_to_all_outside_the_room_after_game_start():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(HelloServerMsg(2, 'Other'), 2)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)

    actual = controller.handle(StartGameMsg(0), 0)

    expected_msg = MsgToSend(
        2,
        message='hello client',
        status='ongoing',
        list_of_players_in_room=['Piotr', 'Marta']
    )

    assert expected_msg in actual


def test_should_broadcast_game_ready_to_start_to_all_in_room_after_start():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)

    actual = controller.handle(StartGameMsg(0), 0)

    expected = [
        MsgToSend(0, message='game ready to start', player_idx=0),
        MsgToSend(1, message='game ready to start', player_idx=1)
    ]

    for msg in expected:
        assert msg in actual


def test_should_rasie_when_player_tries_to_join_to_ongoing_game():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)
    controller.handle(StartGameMsg(0), 0)
    controller.handle(HelloServerMsg(2, 'Other'), 2)

    with pytest.raises(ValueError):
        controller.handle(WantToJoinMsg(2), 2)


def test_raises_when_player_tries_to_pose_as_sb_else_on_ready_to_receive():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)
    controller.handle(StartGameMsg(0), 0)

    with pytest.raises(ValueError):
        controller.handle(ReadyToReceiveGameState(0), 1)


def test_raises_on_ready_to_receive_game_state_when_game_is_not_active():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)

    with pytest.raises(ValueError):
        controller.handle(ReadyToReceiveGameState(0), 0)


def test_should_emit_full_game_state_on_ready_to_receive_game_state():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)
    controller.handle(StartGameMsg(0), 0)

    actual = controller.handle(ReadyToReceiveGameState(0), 0)

    expected = MsgToSend(
        0,
        message='full game state',
        board={
            'turtles_in_game_positions': [[] for _ in range(9)],
            'turtles_on_start_positions': [['RED'], ['GREEN'], ['BLUE'],
                                           ['PURPLE'], ['YELLOW']],
        },
        players_names=['Piotr', 'Marta'],
        active_player_idx=0,
        player_cards=[
            {"card_id": 28, "color": "YELLOW", "action": "PLUS"},
            {"card_id": 12, "color": "RED", "action": "PLUS"},
            {"card_id": 45, "color": "RAINBOW", "action": "MINUS"},
            {"card_id": 41, "color": "RAINBOW", "action": "PLUS"},
            {"card_id": 38, "color": "PURPLE", "action": "MINUS"}],
        player_turtle_color='GREEN',
        recently_played_card=None
    )

    assert actual == expected


def test_raises_when_player_tries_to_pose_as_sb_else_on_play_card_msg():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)

    with pytest.raises(ValueError):
        controller.handle(PlayCardMsg(0, 0, None), 1)


def test_raises_when_player_tries_to_play_card_but_game_has_not_started():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)

    with pytest.raises(ValueError):
        controller.handle(PlayCardMsg(0, 0, None), 0)


def test_should_emit_player_cards_updated_to_player_who_played_the_card():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)
    controller.handle(StartGameMsg(0), 0)

    actual = controller.handle(PlayCardMsg(0, 28, None), 0)

    expected = MsgToSend(
        0,
        message='player cards updated',
        player_cards=[
            {"card_id": 33, "color": "PURPLE", "action": "PLUS"},
            {"card_id": 12, "color": "RED", "action": "PLUS"},
            {"card_id": 45, "color": "RAINBOW", "action": "MINUS"},
            {"card_id": 41, "color": "RAINBOW", "action": "PLUS"},
            {"card_id": 38, "color": "PURPLE", "action": "MINUS"}
        ]
    )

    assert expected in actual


def test_should_broadcast_game_state_update_after_player_moved():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)
    controller.handle(StartGameMsg(0), 0)

    actual = controller.handle(PlayCardMsg(0, 28, None), 0)

    expected_msgs = [
        MsgToSend(
            0,
            message='game state updated',
            board={
                'turtles_in_game_positions': [['YELLOW']] +
                                             [[] for _ in range(8)],
                'turtles_on_start_positions': [['RED'], ['GREEN'], ['BLUE'],
                                               ['PURPLE']],
            },
            active_player_idx=1,
            recently_played_card={
                "card_id": 28,
                "color": "YELLOW",
                "action": "PLUS"
            }
        ),
        MsgToSend(
            1,
            message='game state updated',
            board={
                'turtles_in_game_positions': [['YELLOW']] +
                                             [[] for _ in range(8)],
                'turtles_on_start_positions': [['RED'], ['GREEN'], ['BLUE'],
                                               ['PURPLE']],
            },
            active_player_idx=1,
            recently_played_card={
                "card_id": 28,
                "color": "YELLOW",
                "action": "PLUS"
            }
        ),
    ]

    for expected_msg in expected_msgs:
        assert expected_msg in actual


def test_should_broadcast_game_won_when_someone_wins():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)
    controller.handle(StartGameMsg(0), 0)

    controller.game.board.move(Turtle('YELLOW'), 8)

    actual = controller.handle(PlayCardMsg(0, 28, None), 0)

    expected_msgs = [
        MsgToSend(
            0,
            message='game won',
            winner_name='Marta',
            sorted_list_of_player_places=['Marta', 'Piotr'],
            sorted_list_of_players_turtle_colors=['YELLOW', 'GREEN']
        ),
        MsgToSend(
            1,
            message='game won',
            winner_name='Marta',
            sorted_list_of_player_places=['Marta', 'Piotr'],
            sorted_list_of_players_turtle_colors=['YELLOW', 'GREEN']
        )
    ]

    for expected_msg in expected_msgs:
        assert expected_msg in actual


def test_clear_disconnected_should_remove_players_from_room():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(HelloServerMsg(1, 'Marta'), 1)
    controller.handle(WantToJoinMsg(0), 0)
    controller.handle(WantToJoinMsg(1), 1)
    controller.disconnected(0)
    controller.clear_disconnected()

    actual = controller.handle(HelloServerMsg(2, 'Piotr'), 2)

    assert actual == MsgToSend(
        2,
        message='hello client',
        status='can join',
        list_of_players_in_room=['Marta']
    )


def test_clear_disconnected_should_clear_game_when_no_players_left_in_room():
    controller = GameController()

    controller.handle(HelloServerMsg(0, 'Piotr'), 0)
    controller.handle(WantToJoinMsg(0), 0)
    controller.disconnected(0)
    controller.clear_disconnected()

    actual = controller.handle(HelloServerMsg(2, 'Piotr'), 2)

    assert actual == MsgToSend(
        2,
        message='hello client',
        status='can create',
        list_of_players_in_room=[]
    )
