import customtkinter as ctk
import random
from getpass import getuser
import json
from tkinter import messagebox
from ascii import *

ascii_art_wellcome ="""
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>██╗>>██╗>█████╗>███╗>>>██╗>██████╗>███╗>>>███╗>█████╗>███╗>>>██╗>
>██║>>██║██╔══██╗████╗>>██║██╔════╝>████╗>████║██╔══██╗████╗>>██║>
>███████║███████║██╔██╗>██║██║>>███╗██╔████╔██║███████║██╔██╗>██║>
>██╔══██║██╔══██║██║╚██╗██║██║>>>██║██║╚██╔╝██║██╔══██║██║╚██╗██║>
>██║>>██║██║>>██║██║>╚████║╚██████╔╝██║>╚═╝>██║██║>>██║██║>╚████║>
>╚═╝>>╚═╝╚═╝>>╚═╝╚═╝>>╚═══╝>╚═════╝>╚═╝>>>>>╚═╝╚═╝>>╚═╝╚═╝>>╚═══╝>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
# FONT Consolas, otherwise it doesn't work

class Hangman(ctk.CTk):
    path_to_json_file = r"data.json"  
    lives_left = 5
    letters_used = ""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('800x800')
        self.title('Hangman')
        
        self.grid_columnconfigure([i for i in range(16)], weight=1, uniform= "pleasework") #col/row = 50pixels
        self.grid_rowconfigure([i for i in range(16)], weight=1, uniform= "pleasework")   
        self.resizable(False, False)
        
        self.welcome_label = ctk.CTkLabel(self, text= "", font=("Arial ", 20)) 
        self.ascii_welcome_label = ctk.CTkLabel(self, text= ascii_art_wellcome, font=("Consolas", 18), text_color="green", justify="center")
        
        self.welcome_msg_and_show_menu(seconds = 5)
    
    def welcome_msg_and_show_menu(self, seconds):
        self.welcome_label.configure(text=f"Hi {getuser()}! \n\n Welcome to my Hangman game.\n\nThe game will start in {seconds} seconds")
        
        if not self.welcome_label.winfo_ismapped():
            self.welcome_label.grid(row=5, rowspan = 2, column=5, columnspan=6, pady=2, sticky="ew")
            self.ascii_welcome_label.grid(row=0, rowspan = 4, column=0, columnspan=16, pady=2, sticky="ew")
        
        if seconds > 1:
            self.after(1000, self.welcome_msg_and_show_menu, seconds - 1)
        elif seconds == 1:
            self.welcome_label.configure(text = f"Be ready!\n\nThe game starts in {seconds} second \n\n Have fun!")
            self.after(1750, self.start_game)
            
                
    def start_game(self):
        self.welcome_label.grid_forget()
        self.ascii_welcome_label.grid_forget()
        
        #reset/get the variables
        self.lives_left = 5
        self.letters_used = ""
        self.word_to_guess_formated = ""
        XOX = self.get_hint_and_random_word_returns_a_list()
        self.hint, self.word = XOX[0] , XOX[1]
        self.word = self.word.upper()
        
        self.formating_the_word_to_guess()
        #build the game
        self.build_game()
        
    def formating_the_word_to_guess(self):
        if self.word_to_guess_formated == "":
            self.letters_used += self.word[0] + " "
            self.letters_used = self.letters_used.upper()
            
        self.word_to_guess_formated = ""
        for character in self.word:
            if character in self.letters_used:
                self.word_to_guess_formated += character
            elif character.isspace():
                self.word_to_guess_formated += "  "
            elif not character.isalpha():
                self.word_to_guess_formated += character
            elif character.isalpha():
                self.word_to_guess_formated += "_ "
        
    def build_game(self):
        self.hint_label = ctk.CTkLabel(self, text=f"Hint: {self.hint}", font=("Arial", 20), text_color= "red")
        self.hint_label.grid(row=9, rowspan = 2, column=7, columnspan=4, pady=2, sticky="news")
        
        self.letters_used_label = ctk.CTkLabel(self, text=f"Letters used: {self.letters_used}", compound="left", font=("Arial", 20), text_color= "red")
        self.letters_used_label.grid(row=10, column=0, columnspan=4, pady=2, sticky="ew")
        
        self.word_to_guess_label = ctk.CTkLabel(self, text= f"{self.word_to_guess_formated}", font=("Arial", 40), text_color= "green", wraplength= 800)
        self.word_to_guess_label.grid(row=12, rowspan = 3, column=0, columnspan=16, pady=2, sticky="ew")
        
        self.guillotine_label = ctk.CTkLabel(self, text= ascii_will_he_escape_, font=("Consolas", 20), text_color= "#8B0000")
        self.guillotine_label.grid(row=0, rowspan = 6, column=0, columnspan=10)
        
        self.hears_label = ctk.CTkLabel(self, text= self.help_hears(), font=("Consolas", 20), text_color= "pink")
        self.hears_label.grid(row=0, rowspan = 10, column=10, columnspan=6)
        
        self.bind("<Key>", self.key_pressed)
        self.focus_set()

    def help_hears(self):
        hearts = ""
        for _ in range(self.lives_left):
            hearts += "❤" + "\n\n"
        return hearts
    
    def key_pressed(self, event):
        letter = event.char.upper()
        if not letter.isalpha():
            self.show_message("You must enter a letter")
        elif letter.isalpha():
            if letter in self.letters_used:
                self.show_message("You have already used this letter")
            elif letter in self.word:
                self.letters_used += letter + " "
                self.formating_the_word_to_guess()
                self.word_to_guess_label.configure(text= f"{self.word_to_guess_formated}")
                if "_" not in self.word_to_guess_formated:
                    self.show_message("Congratulations! You won!")
                    self.after(2000, self.start_game)
            else:
                self.lives_left -= 1
                self.hears_label.configure(text= self.help_hears())
                self.letters_used += letter + " "
                self.letters_used_label.configure(text=f"Letters used: {self.letters_used}")
                if self.lives_left == 0:
                    randomm = random.choice([ascii_and_so_he_died_1, ascii_and_so_he_died_2, ascii_and_so_he_died_3, ascii_and_so_he_died_4, ascii_and_so_he_died_5])
                    self.guillotine_label.configure(text= randomm)
                    self.show_message(f"Game over! The word was: {self.word}\n Better luck next time!")
                    self.after(1500, self.start_game)
                    
    def show_message(self, message):
        messagebox.showwarning("Worning", message)
        
    def get_hint_and_random_word_returns_a_list(self):
        path_to_json_file = r"data.json"
        
        with open(path_to_json_file, "r") as file:
            data = json.load(file)
        
        keys = [key for key in data.keys() if key != "ascii art"]
        key_or_hint = random.choice(keys)
        random_word = random.choice(data[key_or_hint]).upper()
        return [key_or_hint, random_word]



if __name__ == '__main__':
    app = Hangman()
    app.mainloop()
