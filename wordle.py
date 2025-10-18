import tkinter as tk
import random
from tkinter import messagebox

# Màu sắc và cài đặt
BG_COLOR = "#121213"
FG_COLOR = "#FFFFFF"
FONT_NORMAL = ("Helvetica", 24, "bold")
FONT_TITLE = ("Helvetica", 40, "bold")
FONT_BUTTON = ("Helvetica", 16, "bold")

WORD_LENGTH = 5
MAX_GUESSES = 6

COLOR_CORRECT = "#538d4e"      # Xanh lá: đúng chữ, đúng vị trí
COLOR_PRESENT = "#b59f3b"      # Vàng: đúng chữ, sai vị trí
COLOR_ABSENT = "#3a3a3c"       # Xám: chữ không có trong từ
COLOR_DEFAULT = "#121213"     # Màu nền mặc định của ô
COLOR_BORDER = "#565758"     # Màu viền của ô
COLOR_KEYBOARD = "#818384"   # Màu bàn phím

# Màu sắc cho thông báo lỗi
COLOR_ERROR = "#ff0000"
TEXT_COLOR = "#FFFFFF"
FONT_ERROR = ("Helvetica", 12, "bold")

class GameApp(tk.Tk):
    def __init__(self):
        """Khởi tạo ứng dụng game."""
        super().__init__()
        self.title("Game App")
        self.geometry("1000x600")
        self.config(bg=BG_COLOR)

        self.wordList = self.load_words("words.txt")
        self.secretWord = ""  # Từ bí mật
        self.curRow = 0 # Dòng đoán hiện tại
        self.curCol = 0 # Cột đoán hiện tại

        self.keyboard = {}
        self.grid = []
        self.toastLabel = None

        # Các frame cho từng màn hình
        self.startFrame = None
        self.gameMainFrame = None
        self.keyboardFrame = None
        self.endFrame = None

        # Bắt đầu với màn hình start
        self.show_start_screen()

    def load_words(self, file_path):
        try:
            with open(file_path, 'r') as f:
                words = []
                for line in f:
                    word = line.strip().lower()
                    if len(word) == WORD_LENGTH:
                        words.append(word)
            if not words:
                messagebox.showerror("Lỗi", f"File '{file_path}' không có từ nào có độ dài {WORD_LENGTH}.")
                self.destroy()
                return []
            return words
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file '{file_path}'. Vui lòng tạo file này.")
            self.destroy()
            return []

    def clear_screen(self):
        """Xóa tất cả các widget trên màn hình hiện tại."""
        if self.startFrame:
            self.startFrame.destroy()
            self.startFrame = None
        if self.gameMainFrame:
            self.gameMainFrame.destroy()
            self.gameMainFrame = None
        if self.keyboardFrame:
            self.keyboardFrame.destroy()
            self.keyboardFrame = None
        if self.endFrame:
            self.endFrame.destroy()
            self.endFrame = None
        
        # Hủy bind phím khi không ở màn hình game
        self.unbind_all("<KeyPress>")

    def show_start_screen(self):
        """Hiển thị màn hình bắt đầu."""
        self.clear_screen()
        
        self.startFrame = tk.Frame(self, bg=BG_COLOR)
        self.startFrame.pack(expand=True, fill="both")

        title_label = tk.Label(self.startFrame, text="WORDLE", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
        title_label.pack(pady=50)

        start_button = tk.Button(self.startFrame, text="Bắt đầu chơi", font=FONT_BUTTON,
                                 bg=COLOR_KEYBOARD, fg=FG_COLOR,
                                 command=self.show_game_screen)
        start_button.pack(pady=20, ipady=10, ipadx=20)

    def show_game_screen(self):
        """Hiển thị màn hình chơi game."""
        self.clear_screen()
        self.create_game_widgets()
        self.start_game()

    def show_end_screen(self, win):
        """Hiển thị màn hình kết thúc (thắng hoặc thua)."""
        self.clear_screen()

        self.endFrame = tk.Frame(self, bg=BG_COLOR)
        self.endFrame.pack(expand=True, fill="both")

        if win:
            message = "Chúc mừng! Bạn đã đoán đúng!"
        else:
            message = f"Bạn đã hết lượt!\nTừ đúng là: {self.secretWord.upper()}"
        
        message_label = tk.Label(self.endFrame, text=message, font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR, justify="center")
        message_label.pack(pady=50)

        play_again_button = tk.Button(self.endFrame, text="Chơi lại", font=FONT_BUTTON,
                                      bg=COLOR_KEYBOARD, fg=FG_COLOR,
                                      command=self.show_game_screen) # Quay lại màn hình game
        play_again_button.pack(pady=20, ipady=10, ipadx=20)

        exit_button = tk.Button(self.endFrame, text="Thoát", font=FONT_BUTTON,
                                      bg=COLOR_KEYBOARD, fg=FG_COLOR,
                                      command=self.destroy) # Thoát game
        exit_button.pack(pady=20, ipady=10, ipadx=20)


    def create_game_widgets(self):
        """Tạo các widget cho màn hình chơi game (lưới và bàn phím)."""
        self.gameMainFrame = tk.Frame(self, bg=BG_COLOR)
        self.gameMainFrame.pack(pady=20, padx=10, expand=True, fill="both")

        self.grid = []
        for i in range(MAX_GUESSES):
            row = []
            frame_row = tk.Frame(self.gameMainFrame, bg=BG_COLOR)
            frame_row.pack()
            for j in range(WORD_LENGTH):
                cell = tk.Label(frame_row, text="", width=2, height=1, font=FONT_NORMAL,
                                 bg=COLOR_DEFAULT, fg=FG_COLOR, highlightbackground=COLOR_BORDER, highlightthickness=1)
                cell.pack(side="left", padx=3, pady=3)
                row.append(cell)
            self.grid.append(row)

        # Keyboard frame
        self.keyboardFrame = tk.Frame(self, bg=BG_COLOR)
        self.keyboardFrame.pack(pady=10, padx=10)

        keyboard_layout = [
            "qwertyuiop",
            "asdfghjkl",
        ]

        self.keyboard = {}

        for row in keyboard_layout:
            frame_row = tk.Frame(self.keyboardFrame, bg=BG_COLOR)
            frame_row.pack()
            for char in row:
                btn = tk.Button(frame_row, text=char.upper(), width=4, height=2,
                                bg=COLOR_KEYBOARD, fg=FG_COLOR, font=("Helvetica", 12, "bold"),
                                command=lambda c=char: self.on_key_press(c))
                btn.pack(side="left", padx=5, pady=5)
                self.keyboard[char] = btn

        last_row = tk.Frame(self.keyboardFrame, bg=BG_COLOR)
        last_row.pack()
        
        enter_button = tk.Button(last_row, text="Enter", command=self.process_guess,
                                 width=6, height=2, bg=COLOR_KEYBOARD, fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        enter_button.pack(side="left", padx=5)

        for char in "zxcvbnm":
            btn = tk.Button(last_row, text=char.upper(), width=4, height=2,
                            bg=COLOR_KEYBOARD, fg=FG_COLOR, font=("Helvetica", 12, "bold"),
                            command=lambda c=char: self.on_key_press(c))
            btn.pack(side="left", padx=5, pady=5)
            self.keyboard[char] = btn

        backspace_button = tk.Button(last_row, text="⌫", command=self.on_backspace, width=6, height=2, bg=COLOR_KEYBOARD, fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        backspace_button.pack(side="left", padx=5)

        self.bind_all("<KeyPress>", self.key_press_from_keyboard)
    
    def show_toast(self, message):
        if self.toastLabel:
            self.toastLabel.destroy()

        self.toastLabel = tk.Label(
            self,
            text=message,
            bg=COLOR_ERROR,
            fg=TEXT_COLOR,
            font=FONT_ERROR,
            padx=20,
            pady=10,
            relief="solid",
            borderwidth=1,
        )
        self.toastLabel.place(relx=0.5, rely=0.2, anchor="center")
        self.toastLabel.after(1000, self.toastLabel.destroy) # Tăng thời gian hiển thị lên 1s

    def trigger_error_toast(self, text):
        self.show_toast(f"{text}")

    def key_press_from_keyboard(self, event):
        if 'a' <= event.char.lower() <= 'z':
            self.on_key_press(event.char.lower())
        elif event.keysym == "Return":
            self.process_guess()
        elif event.keysym == "BackSpace":
            self.on_backspace()

    def process_guess(self): # Press Enter
        if (self.curRow < MAX_GUESSES) and (self.curCol < WORD_LENGTH):
            self.trigger_error_toast("Chưa nhập đủ chữ cái!")
            return
        if (self.curCol == WORD_LENGTH) and (self.curRow < MAX_GUESSES):
            guess = ''.join([self.grid[self.curRow][c].cget("text").lower() for c in range(WORD_LENGTH)])

            if (guess not in self.wordList):
                self.trigger_error_toast("Từ không hợp lệ!")
                return

            print(f'Processing guess: {guess}')
            
            # Đánh giá từ đoán
            for i in range(WORD_LENGTH):
                letter = guess[i]
                cell = self.grid[self.curRow][i]
                if letter == self.secretWord[i]:
                    cell.config(bg=COLOR_CORRECT)
                    self.keyboard[letter].config(bg=COLOR_CORRECT)
                elif letter in self.secretWord:
                    cell.config(bg=COLOR_PRESENT)
                    if self.keyboard[letter].cget("bg") != COLOR_CORRECT:
                        self.keyboard[letter].config(bg=COLOR_PRESENT)
                else:
                    cell.config(bg=COLOR_ABSENT)
                    if self.keyboard[letter].cget("bg") not in [COLOR_CORRECT, COLOR_PRESENT]:
                        self.keyboard[letter].config(bg=COLOR_ABSENT)

            # Chuyển sang hàng tiếp theo
            self.curRow += 1
            self.curCol = 0

            # Kiểm tra thắng/thua
            if (guess == self.secretWord):
                # messagebox.showinfo("Chúc mừng!", "Bạn đã đoán đúng từ!")
                self.after(500, lambda: self.show_end_screen(win=True))
                return
            elif (guess != self.secretWord) and (self.curRow == MAX_GUESSES):
                # messagebox.showinfo("Kết thúc!", f"Bạn đã hết lượt đoán! Từ đúng là: {self.secretWord}")
                self.after(500, lambda: self.show_end_screen(win=False))
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
        """Bắt đầu một lượt chơi mới (chọn từ, reset trạng thái)."""
        if not self.wordList:
             messagebox.showerror("Lỗi", "Không có danh sách từ để chơi.")
             self.show_start_screen()
             return
        
        self.secretWord = random.choice(self.wordList)
        print(f'Secret word: {self.secretWord}') 
        self.curRow = 0
        self.curCol = 0
        self.reset_game_ui()

    def reset_game_ui(self):
        """Reset giao diện game (lưới và bàn phím)."""
        for r in range(MAX_GUESSES):
            for c in range(WORD_LENGTH):
                self.grid[r][c].config(text="", bg=COLOR_DEFAULT)
        for key in self.keyboard:
            self.keyboard[key].config(bg=COLOR_KEYBOARD) 
        self.curRow = 0
        self.curCol = 0

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()