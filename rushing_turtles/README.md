# Rushing turtles client-server communication

# Starting and joining the game [MainActivity communication]

### 1. Client first message
``` python 
message: "hello server"  
player_id: {id}
player_name: f"{name}"  
```

### 2. Server possible response
``` python
message: "hello client"
status: f"{status}"
list_of_players_in_room: [f"{names_of_players_in_the_room}"]
```

- 2.1 Player can create new game  
    ``` python
    status: "can create"
    list_of_players_in_room: []  # empty list - no players in the game
    ```

- 2.2 Player can join already created game
    ``` python
    status: "can join"
    ```

- 2.3 Player can't join the game, because of to many players in the watinig room
    ``` python
    status: "limit"
    ```

- 2.4 Player can't join the game, because it has already started without him 
    ``` python
    status: "ongoing"
    ```

- 2.5 Player can resume game (he was already playing and then he left the game/lost connection)
    ``` python
    status: "can resume"
    ```

### 3. Client probable response - after client's button click
``` python
message: "want to join the game"
status: f"{status}"
player_id: {id}
```

- 3.1 Player creates the game and the room
    ``` python
    status: "create the game"
    ```

- 3.2 Player joins the game and the room
    ``` python
    status: "join the game"
    ```

- 3.3 Player resumes the game and want to join again 
    ``` python
    status: "resume the game"
    ```

### 4. Client possible response - first player wants to start the game
``` python
message: "start the game"
player_id: {id}
```

### 5. Server response (broadcast)
``` python 
message: "game ready to start"
player_idx: {idx}  # player index in the list of players 
```

### <span style="color:red"> TODO - when client wants to leave the room </span>

### 6. Server broadcast messages to all clients

6.1 Server updates the room when new player joins the game (or leaves the game)
``` python 
message: "room update"
list_of_players_in_room: [f"{names_of_players_in_the_room}"]
```


# Playing the game [GameActivity communication]

### 1. Client initial message from GameActivity - ready to receive game state
``` python
message: "ready to receive game state"
player_id: {id}
```

### 2. Server response - all required initial information about the game state
``` python
message: "full game state"
board: Board()  # two lists of turtles positions
players_names: [f"{names_of_all_players_in_the_game}"]  # sorted list
active_player_idx = {player_idx}  
player_cards = [Card()] * 5  
player_turtle_color: f"{color}"
recently_played_card = Card() 
```

### <span style="color:red"> TODO when player leaves the game/losts connection with server </span>

## Client-server communication when *this* player moves

### 3. Client request - send picked card
``` python
message: "play card"
player_id: {id}
card_id: {card_id}
picked_color: {card_color} or None
```

### 4. Server response - updated game state

4.1 Server updates player card in his hand 
``` python
message: "player cards updated"
player_cards = [Card()] * 5  # one new and four old cards
```

4.2 Server updates game state (broadcast message)
``` python 
message: "game state updated"
board: Board()  # two lists of turtles positions
active_player_idx = {player_idx}  # next player id
recently_played_card = Card()  # card just played by the player
```

## Client-server communication when *other* player moves

### 5. Server updates the game state
The same message as in section 4.2


## Client-server communication when the game is won

### 6. Server message - after card played by client (section 3)
``` python
message: "game won"
winner_name: f"{name}"
sorted_list_of_player_places: [{player_idxs}]  # sorted - first player is the winner
sorted_list_of_players_turtle_colors: [f"{players_turtle_colors}"] 
```

## Other server messages

### Server message - ERROR as a response to client's invalid request
``` python
message: "error"
description: f"{description}"
```