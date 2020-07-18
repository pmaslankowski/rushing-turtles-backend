from rushing_turtles.model.card import Card

def generate_cards_for_given_color(first_card_id, color, actions, action_repetition):
    list_of_cards = []
    card_id = first_card_id

    for action_idx, action in enumerate(actions):
        for i in range(action_repetition[action_idx]):
            list_of_cards.append(Card(card_id, color, action))
            card_id += 1
    
    return list_of_cards, card_id


if __name__ == "__main__":
    colors = ['BLUE', 'RED', 'GREEN', 'YELLOW', 'PURPLE', 'RAINBOW']
    actions = ['PLUS_PLUS', 'PLUS', 'MINUS', 'ARROW', 'ARROW_ARROW']

    color_action_repetition = [1, 5, 2, 0, 0]
    rainbow_action_repetition = [0, 5, 2, 3, 2]

    list_of_cards = []
    card_id = 1

    for color in colors[:-1]:
        list_of_cards_in_color, card_id = generate_cards_for_given_color(card_id, color, actions, color_action_repetition)
        list_of_cards += list_of_cards_in_color

    list_of_cards_rainbow, last_card_id = generate_cards_for_given_color(card_id, colors[-1], actions, rainbow_action_repetition)
    list_of_cards += list_of_cards_rainbow

    
    for card in list_of_cards:
        print(card)