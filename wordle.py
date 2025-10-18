import tkinter as tk
import random
from tkinter import messagebox

# Màu sắc và cài đặt
BG_COLOR = "#121213"
FG_COLOR = "#FFFFFF"
FONT_NORMAL = ("Helvetica", 24, "bold")

WORD_LENGTH = 5
MAX_GUESSES = 6

COLOR_CORRECT = "#538d4e"      # Xanh lá: đúng chữ, đúng vị trí
COLOR_PRESENT = "#b59f3b"      # Vàng: đúng chữ, sai vị trí
COLOR_ABSENT = "#3a3a3c"       # Xám: chữ không có trong từ
COLOR_DEFAULT = "#121213"     # Màu nền mặc định của ô
COLOR_BORDER = "#565758"     # Màu viền của ô

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game App")
        self.geometry("1000x600")
        self.config(bg=BG_COLOR)

        self.wordList = self.load_words("words.txt")
        self.secretWord = ""  # Từ bí mật
        self.curRow = 0 # Dòng đoán hiện tại
        self.curCol = 0 # Cột đoán hiện tại
        self.curGuess = "" # Chuỗi đoán hiện tại

        self.keyboard = {}

        self.create_widgets()
        self.start_game()

    def load_words(self, file_path):
        try:
            with open(file_path, 'r') as f:
                words = []
                for line in f:
                    word = line.strip().lower()
                    if len(word) == WORD_LENGTH:
                        words.append(word)
            # print(words)
            return words
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file '{file_path}'. Vui lòng tạo file này.")
            self.destroy()
            return []

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(pady=20, padx=10, expand=True, fill="both")

        self.grid = []
        for i in range(MAX_GUESSES):
            row = []
            frame_row = tk.Frame(main_frame, bg=BG_COLOR)
            frame_row.pack()
            for j in range(WORD_LENGTH):
                cell = tk.Label(frame_row, text="", width=2, height=1, font=FONT_NORMAL,
                                 bg=COLOR_DEFAULT, fg=FG_COLOR, highlightbackground=COLOR_BORDER, highlightthickness=1)
                cell.pack(side="left", padx=3, pady=3)
                row.append(cell)
            self.grid.append(row)

        # Keyboard frame

        keyboard_frame = tk.Frame(self, bg=BG_COLOR)
        keyboard_frame.pack(pady=10, padx=10)

        keyboard_layout = [
            "qwertyuiop",
            "asdfghjkl",
            # "zxcvbnm"
        ]

        for row in keyboard_layout:
            frame_row = tk.Frame(keyboard_frame, bg=BG_COLOR)
            frame_row.pack()
            for char in row:
                btn = tk.Button(frame_row, text=char.upper(), width=4, height=2,
                                bg="#818384", fg=FG_COLOR, font=("Helvetica", 12, "bold"),
                                command=lambda c=char: self.on_key_press(c))
                btn.pack(side="left", padx=5, pady=5)
                self.keyboard[char] = btn

        last_row = tk.Frame(keyboard_frame, bg=BG_COLOR)
        last_row.pack()
        
        enter_button = tk.Button(last_row, text="Enter", command=self.process_guess,
                                 width=6, height=2, bg="#818384", fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        enter_button.pack(side="left", padx=5)

        for char in "zxcvbnm":
            btn = tk.Button(last_row, text=char.upper(), width=4, height=2,
                            bg="#818384", fg=FG_COLOR, font=("Helvetica", 12, "bold"),
                            command=lambda c=char: self.on_key_press(c))
            btn.pack(side="left", padx=5, pady=5)
            self.keyboard[char] = btn

        backspace_button = tk.Button(last_row, text="⌫", command=self.on_backspace, width=6, height=2, bg="#818384", fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        backspace_button.pack(side="left", padx=5)


        self.bind_all("<KeyPress>", self.key_press_from_keyboard)
    
    def key_press_from_keyboard(self, event):
        if 'a' <= event.char.lower() <= 'z':
            self.on_key_press(event.char.lower())
        elif event.keysym == "Return":
            self.process_guess()
        elif event.keysym == "BackSpace":
            self.on_backspace()

    def process_guess(self): # Press Enter
        if (self.curCol == WORD_LENGTH) and (self.curRow < MAX_GUESSES):
            guess = ''.join([self.grid[self.curRow][c].cget("text").lower() for c in range(WORD_LENGTH)])

            if (guess not in self.wordList):
                messagebox.showwarning("Cảnh báo", "Từ không hợp lệ!")
                # for c in range(WORD_LENGTH):
                #     self.grid[self.curRow][c].config(bg=COLOR_DEFAULT)
                return

            print(f'Processing guess: {guess}')
            self.curRow += 1
            self.curCol = 0

            for i in range(WORD_LENGTH):
                letter = guess[i]
                cell = self.grid[self.curRow - 1][i]
                if letter == self.secretWord[i]:
                    cell.config(bg=COLOR_CORRECT)
                    self.keyboard[letter].config(bg=COLOR_CORRECT)
                elif letter in self.secretWord:
                    cell.config(bg=COLOR_PRESENT)
                    if self.keyboard[letter].cget("bg") != COLOR_CORRECT:
                        self.keyboard[letter].config(bg=COLOR_PRESENT)
                else:
                    cell.config(bg=COLOR_ABSENT)
                    self.keyboard[letter].config(bg=COLOR_ABSENT)

            if (guess == self.secretWord):
                messagebox.showinfo("Chúc mừng!", "Bạn đã đoán đúng từ!")
                return
            elif (guess != self.secretWord) and (self.curRow == MAX_GUESSES):
                messagebox.showinfo("Kết thúc!", f"Bạn đã hết lượt đoán! Từ đúng là: {self.secretWord}")
                return
            
    
    def on_backspace(self): # Press Backspace
        if (self.curCol > 0) and (self.curRow < MAX_GUESSES):
            self.curCol -= 1
            self.grid[self.curRow][self.curCol].config(text="")

    def on_key_press(self, char):
        if (self.curCol < WORD_LENGTH) and (self.curRow < MAX_GUESSES):
            self.grid[self.curRow][self.curCol].config(text=char.upper())
            self.curCol += 1

    def start_game(self):
        self.secretWord = random.choice(self.wordList)
        print(f'Secret word: {self.secretWord}') 
        self.curRow = 0
        self.curCol = 0
        self.curGuess = ""
        self.reset_game()

    def reset_game(self):
        for r in range(MAX_GUESSES):
            for c in range(WORD_LENGTH):
                self.grid[r][c].config(text="", bg=COLOR_DEFAULT)
        for key in self.keyboard:
            self.keyboard[key].config(bg=COLOR_DEFAULT)
        self.curRow = 0
        self.curCol = 0
        self.curGuess = ""

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()