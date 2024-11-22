import math
import random
from tkinter import *
import tkinter as tk
import pickle

filename = 'my_pickle.pk'

card_list = []
with open(filename, 'rb') as fi:
    card_list = pickle.load(fi)


# Adding a card
def add_card(card):
    card_list.append(card)
    update_card_list()


def remove_card():
    for card in card_list:
        if str(remove_name_in.get()) in card:
            card_list.remove(card)
    update_card_list()


def remove_all_cards_check():
    clear_button.config(state=NORMAL)
    check_label = create_label("Are you sure you want to remove ALL of the cards?", 6, 1)


def remove_all_cards():
    card_list.clear()
    update_card_list()


def create_label(labelText, col, row):
    the_label = tk.Label(window, text=labelText)
    assign_to_grid(the_label, col, row)
    return the_label


def create_input(col, row):
    the_input = tk.Entry(window)
    assign_to_grid(the_input, col, row)
    return the_input


def create_label_input_combo(labelText, col, row):
    out_label = create_label(labelText, col, row)
    out_input = create_input(col+1, row)
    return out_label, out_input


def assign_to_grid(obj, col, row):
    obj.grid(column=col, row=row)


def update_card_list():
    with open(filename, 'wb') as fi:
        pickle.dump(card_list, fi)
    display_text = ",\n ".join(str(x) for x in card_list)
    list_label.config(text=display_text)


def build_deck():
    # Setting the ratio for land cards and the remainder
    land_ratio = 40
    remaining = 100 - land_ratio

    unrefined_ratios = sorted([random.uniform(0, remaining) for i in range(4)])

    # Getting the ratios for each type of card and taking the floor
    creature_ratio = math.floor(unrefined_ratios[0])
    sorcery_ratio = math.floor(unrefined_ratios[1] - unrefined_ratios[0])
    artifact_ratio = math.floor(unrefined_ratios[2] - unrefined_ratios[1])
    enchantment_ratio = math.floor(unrefined_ratios[3] - unrefined_ratios[2])
    wild_card_ratio = math.floor(remaining - unrefined_ratios[3])
    total = creature_ratio + sorcery_ratio + artifact_ratio + enchantment_ratio + wild_card_ratio + land_ratio

    # If the total of ratios is not 100 then add 1 to creature_ratio until it is
    while total != 100:
        creature_ratio += 1
        total = creature_ratio + sorcery_ratio + artifact_ratio + enchantment_ratio + wild_card_ratio + land_ratio

    # Assigning the new ratios to a new array
    refined_ratios = [land_ratio, creature_ratio, sorcery_ratio, artifact_ratio, enchantment_ratio, wild_card_ratio]

    deck_size = deck_count_i.get()
    colors = [deck_colors_i1.get(), deck_colors_i2.get()]
    for i in range(0, 2):
        if colors[i] == '':
            colors.remove(colors[i])
    if '' in colors:
        colors.remove('')
    card_totals = []

    for ratio in refined_ratios:
        card_totals.append(float(deck_size) * (ratio/100))

    def get_total_cards(card_totals_arr):
        total_cards = 0
        final_total_cards = []
        for cards_amount in card_totals_arr:
            cards_amount = math.floor(cards_amount)
            final_total_cards.append(cards_amount)
            total_cards += cards_amount
        return total_cards, final_total_cards

    total_amount_of_cards, pre_final_totals = get_total_cards(card_totals)

    while total_amount_of_cards != int(deck_size):
        card_totals[5] += 1
        total_amount_of_cards, pre_final_totals = get_total_cards(card_totals)

    card_type_arr = ["Land", "Creature", "Sorcery", "Artifact", "Enchantment", "Wild Cards"]
    card_type_arr_counter = 0
    color_1_total = 0
    color_2_total = 0
    one_final_totals = pre_final_totals
    one_color_string = ""
    two_color_string = ""

    # if there is only one color in the deck
    if len(colors) == 1:
        for i in range(len(one_final_totals)):
            one_color_string += (card_type_arr[i] + ": ")
            one_color_string += str(one_final_totals[i]) + "\n"
        random_deck_l.config(text=one_color_string)

    # If there are two colors in the deck
    if len(colors) == 2:
        two_final_totals = []

        for num in pre_final_totals:
            divi = random.randrange(0, num + 1)
            sub = num - divi
            two_final_totals.append(divi)
            two_final_totals.append(sub)

        for i in range(2, len(two_final_totals)):
            if i % 2 == 0:
                color_1_total += two_final_totals[i]
            if i % 2 == 1:
                color_2_total += two_final_totals[i]

        # Check to see if one color has more mana need than the land provided
        if two_final_totals[0] <= 2:
            two_final_totals[0] += 5
            two_final_totals[1] -= 5
        if two_final_totals[1] <= 2:
            two_final_totals[1] += 5
            two_final_totals[0] -= 5
        if color_1_total > color_2_total:
            if two_final_totals[0] < two_final_totals[1]:
                two_final_totals[0] += 7
                two_final_totals[1] -= 7
        else:
            if two_final_totals[0] > two_final_totals[1]:
                two_final_totals[0] -= 7
                two_final_totals[1] += 7

        for i in range(len(two_final_totals)):
            if i % 2 == 0:
                two_color_string += (card_type_arr[card_type_arr_counter] + ": ")
                card_type_arr_counter += 1
            if i % 2 == 0:
                two_color_string += (colors[0] + ": " + str(two_final_totals[i]) + ", ")
            if i % 2 == 1:
                two_color_string += (colors[1] + ": " + str(two_final_totals[i]))
                two_color_string += "\n"

        random_deck_l.config(text=two_color_string)


if __name__ == '__main__':
    # Create the main window
    window = tk.Tk()
    window.title("Simple Tkinter App")
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))
    window.grid()

    # Create a label and place it in the window
    label = tk.Label(window, text="Welcome to MTG thing!")
    label.grid(column=0, row=0)

    # Creating inputs and their labels
    create_label("", 0, 1)

    color_label, color_in = create_label_input_combo("Enter the color", 0, 2)
    name_label, name_in = create_label_input_combo("Enter the name", 0, 3)
    type_label, type_in = create_label_input_combo("Enter the card type (Creature, Instant, ect)", 0, 4)
    remove_name_label, remove_name_in = create_label_input_combo("Enter a card name to remove", 2, 2)

    list_label = create_label("", 0, 5)
    list_label.config(wraplength=225)
    update_card_list()

    # Create a button and place it in the window
    add_button = tk.Button(window, text="Add a card?", command=lambda: add_card([color_in.get(),
                                                                             name_in.get(),
                                                                             type_in.get()]))
    add_button.grid(column=1, row=0)
    remove_button = tk.Button(window, text="Remove a card?", command=remove_card)
    remove_button.grid(column=3, row=0)
    check_button = tk.Button(window, text="Clear all cards?", command=remove_all_cards_check)
    check_button.grid(column=5, row=0)
    clear_button = tk.Button(window, text="DO IT", state=DISABLED, command=remove_all_cards)
    clear_button.grid(column=6, row=0)

    buffer = create_label("=====Random Deck Builder=====", 0, 5)

    # Code for deck builder section
    build_deck_button = tk.Button(window, text="Build deck?", command=build_deck)
    build_deck_button.grid(column=0, row=6)

    deck_count_l, deck_count_i = create_label_input_combo("Card amount:", 0, 7)
    deck_colors_l, deck_colors_i1 = create_label_input_combo("Deck color(s):", 0, 8)
    deck_colors_i2 = create_input(2, 8)
    # Potential eventual addition of a third color
    # deck_colors_i3 = create_input(3, 8)
    random_deck_l = create_label("", 0, 10)

    # Start the Tkinter event loop
    window.mainloop()
