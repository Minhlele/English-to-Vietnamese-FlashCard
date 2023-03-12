import random
from tkinter import *

import pygame as pygame
from gtts import gTTS
import os
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

# Read from csv file
current_card = {}
viet_words_dict = {}


def process_csv_file():
    """
        Process the csv files for english to vietnamese translations
    :return: a list of dictionary of a common english phrase and its translation in vietnamese
    """
    try:
        df = pd.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        data = pd.read_csv("data/viettoenphrase.csv")
        viet_words_dict = data.to_dict(orient="records")
    else:
        viet_words_dict = df.to_dict(orient="records")

    # Remove names in the list of dictionaries
    # viet_words_dict = [card for card in viet_words_dict if (not card["English"][0].isupper())]
    return viet_words_dict


def next_word():
    """
        Retrive the next word from a given stack of cards
    """
    global current_card
    global flip_timer
    language = "en"
    window.after_cancel(flip_timer)
    current_card = random.choice(viet_words_dict)

    canvas.itemconfig(title_text, text="English", fill="black")
    canvas.itemconfig(word_text, text=current_card["English"], fill="black")
    canvas.itemconfig(canvas_img, image=card_front_img)
    window.after(100)
    audio_output = gTTS(text=current_card["English"], lang=language)
    audio_output.save("english_word.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("english_word.mp3")
    pygame.mixer.music.play()
    os.remove("english_word.mp3")
    flip_timer = window.after(3000, func=flip_card)


# Count down
def flip_card():
    """
            Flip the card after 3 seconds to reveal the vietnamese translation
    """
    language = "vi"
    canvas.itemconfig(title_text, text="Vietnamese", fill="white")
    canvas.itemconfig(word_text, text=current_card["Vietnamese"], fill="white")
    canvas.itemconfig(canvas_img, image=card_back_img)
    audio_output = gTTS(text=current_card["Vietnamese"], lang=language)
    audio_output.save("viet_word.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("viet_word.mp3")
    pygame.mixer.music.play()
    os.remove("viet_word.mp3")


def remove_card():
    """
            Remove the current phrase from stack of cards when user click the right button
        """
    global viet_words_dict
    global current_card
    viet_words_dict.remove(current_card)
    french_word_df = pd.DataFrame(viet_words_dict)
    french_word_df.to_csv("data/words_to_learn.csv", index=False)
    next_word()


# UI

#Set up tkinter
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR, highlightthickness=0)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(height=526, width=800, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

img_right_button = PhotoImage(file="images/right.png")
right_button = Button(image=img_right_button, highlightthickness=0, command=remove_card)
right_button.grid(row=1, column=0)
img_wrong_button = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=img_wrong_button, highlightthickness=0, command=next_word)
wrong_button.grid(row=1, column=1)
viet_words_dict = process_csv_file()
next_word()
window.mainloop()
