import tkinter as tk
import random
from tkinter import messagebox

# Màu sắc và cài đặt
BG_COLOR = "#121213"
FG_COLOR = "#FFFFFF"
FONT_NORMAL = ("Helvetica", 24, "bold")
FONT_TITLE = ("Helvetica", 40, "bold")
FONT_BUTTON = ("Helvetica", 16, "bold")
FONT_NORMAL_SMALL = ("Helvetica", 12, "bold")

# WORD_LENGTH = 5
# MAX_GUESSES = 6

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

WORD_BASE_FILE = "words/"
WORD_LENGTHS_FILE = WORD_BASE_FILE + "word_lengths.txt"

class GameApp(tk.Tk):
    def __init__(self):
        """Khởi tạo ứng dụng game."""
        super().__init__()
        self.title("Game App")
        self.geometry("1000x600")
        self.config(bg=BG_COLOR)

        # self.wordList = self.load_words("words.txt")

        self.wordListCache = {} # (length, [list words])

        # Thông tin game hiện tại
        self.wordList = []
        self.wordLength = 0
        self.maxGuesses = 0
        
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

        # Canvas và Scrollbar cho lưới
        self.gameCanvas = None
        self.scrollbar = None
        self.h_scrollbar = None
        self.grid_frame = None
        self.canvas_window = None

        # Bắt đầu với màn hình start
        self.show_start_screen()

    def load_words(self, length):
        file_path = WORD_BASE_FILE + f"wordle-{length}.txt"
        try:
            with open(file_path, 'r') as f:
                words = []
                for line in f:
                    word = line.strip().lower()
                    if len(word) == length:
                        words.append(word)
            if not words:
                messagebox.showerror("Lỗi", f"File '{file_path}' không có từ nào có độ dài {length}.")
                self.destroy()
                return None
            return words
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file '{file_path}'. Vui lòng tạo file này.")
            self.destroy()
            return None

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
        self.unbind_all("<KeyPress>")

    def show_start_screen(self):
        """Hiển thị màn hình bắt đầu với thiết kế đẹp mắt."""
        self.clear_screen()
        
        self.startFrame = tk.Frame(self, bg=BG_COLOR)
        self.startFrame.pack(expand=True, fill="both")

        # Container chính cho nội dung
        content_frame = tk.Frame(self.startFrame, bg=BG_COLOR)
        content_frame.pack(expand=True)

        # Tiêu đề với màu sắc đa dạng
        title_frame = tk.Frame(content_frame, bg=BG_COLOR)
        title_frame.pack(pady=(30, 10))
        
        title_colors = ["#538d4e", "#b59f3b", "#538d4e", "#b59f3b", "#538d4e", "#b59f3b"]
        title_text = "WORDLE"
        for char, color in zip(title_text, title_colors):
            char_label = tk.Label(
                title_frame, 
                text=char, 
                font=("Helvetica", 50, "bold"),
                bg=BG_COLOR, 
                fg=color,
                padx=5
            )
            char_label.pack(side="left")

        # Phụ đề
        subtitle = tk.Label(
            content_frame,
            text="🎮 TRÒ CHƠI ĐOÁN TỪ 🎮",
            font=("Helvetica", 20, "bold"),
            bg=BG_COLOR,
            fg="#b59f3b"
        )
        subtitle.pack(pady=(0, 8))

        def load_word_lengths(file_path):
            with open(file_path, 'r') as f:
                lengths = []
                for line in f:
                    length = line.strip()
                    if length.isdigit():
                        lengths.append(int(length))
            return lengths

        wordLengths = load_word_lengths(WORD_LENGTHS_FILE)
        
        # Khung cho phần chọn độ dài
        selection_frame = tk.Frame(content_frame, bg="#1e1e1e", relief="ridge", bd=3)
        selection_frame.pack(pady=20, padx=50, ipadx=20, ipady=20)
        
        instruction_label = tk.Label(
            selection_frame,
            text="⭐ CHỌN ĐỘ DÀI TỪ ⭐",
            font=("Helvetica", 16, "bold"),
            bg="#1e1e1e",
            fg="#FFD700"
        )
        instruction_label.pack(pady=(10, 10))
        
        # Listbox với style đẹp hơn
        self.listbox = tk.Listbox(
            selection_frame,
            font=("Helvetica", 14, "bold"),
            bg="#2d2d2d",
            fg="#FFFFFF",
            selectbackground="#538d4e",
            selectforeground="#FFFFFF",
            activestyle="none",
            justify="center",
            height=min(len(wordLengths), 8),
            width=20,
            relief="flat",
            highlightthickness=2,
            highlightbackground="#b59f3b",
            highlightcolor="#538d4e"
        )
        for length in wordLengths:
            self.listbox.insert(tk.END, f"🔤 {length} chữ cái")

        self.listbox.pack(pady=(0, 15), padx=10)

        # Chọn mặc định mục đầu tiên
        self.listbox.selection_set(0)

        # Hướng dẫn
        hint_label = tk.Label(
            selection_frame,
            text="Nhấn ENTER để bắt đầu ↵",
            font=("Helvetica", 12, "bold"),
            bg="#1e1e1e",
            fg="#b59f3b"
        )
        hint_label.pack(pady=(0, 10))

        # Gắn sự kiện nhấn Enter để bắt đầu game
        def on_enter(event):
            selection = self.listbox.curselection()
            if selection:
                index = selection[0]
                length = wordLengths[index]
                self.listbox.unbind("<Return>")
                self.setup_new_game(length)

        # Bắt sự kiện phím Enter
        self.listbox.bind("<Return>", on_enter)

        # Cho phép di chuyển bằng phím lên/xuống
        self.listbox.focus_set()

    def setup_new_game(self, length):
        """Thiết lập game mới với độ dài từ (length) đã chọn."""
        self.wordLength = length
        self.maxGuesses = length + 1  # Số lượt đoán = min(độ dài từ + 1, số từ trong danh sách)

        # Kiểm tra cache
        if (length in self.wordListCache):
            self.wordList = self.wordListCache[length]
        else:
            words = self.load_words(length)
            if (words):
                self.wordList = words
                self.wordListCache[length] = words
            else:
                self.show_start_screen()
                return
        self.maxGuesses = min(self.maxGuesses, len(self.wordList))
        self.show_game_screen()

    def show_game_screen(self):
        """Hiển thị màn hình chơi game."""
        self.clear_screen()
        self.create_game_widgets()
        self.start_game()

    def show_end_screen(self, win):
        """Hiển thị màn hình kết thúc với thiết kế đẹp mắt."""
        self.clear_screen()

        self.endFrame = tk.Frame(self, bg=BG_COLOR)
        self.endFrame.pack(expand=True, fill="both")

        # Container chính
        content_frame = tk.Frame(self.endFrame, bg=BG_COLOR)
        content_frame.pack(expand=True)

        if win:
            # Màn hình THẮNG
            # Icon và tiêu đề
            icon_label = tk.Label(
                content_frame,
                text="🎉🏆🎉",
                font=("Helvetica", 60),
                bg=BG_COLOR,
                fg="#FFD700"
            )
            icon_label.pack(pady=(30, 10))
            
            message_label = tk.Label(
                content_frame,
                text="CHIẾN THẮNG!",
                font=("Helvetica", 45, "bold"),
                bg=BG_COLOR,
                fg="#538d4e"
            )
            message_label.pack(pady=10)
            
            congrats_label = tk.Label(
                content_frame,
                text="Chúc mừng! Bạn đã đoán đúng từ! 🎊",
                font=("Helvetica", 18, "bold"),
                bg=BG_COLOR,
                fg="#b59f3b"
            )
            congrats_label.pack(pady=5)
            
            # Hiển thị từ đúng với màu đẹp
            word_frame = tk.Frame(content_frame, bg="#1e1e1e", relief="raised", bd=3, width=300)
            word_frame.pack(pady=20, padx=30)
            
            # Tạo container bên trong để căn giữa nội dung
            inner_frame = tk.Frame(word_frame, bg="#1e1e1e")
            inner_frame.pack(padx=15, pady=10)
            
            word_title = tk.Label(
                inner_frame,
                text="Từ đúng:",
                font=("Helvetica", 14, "bold"),
                bg="#1e1e1e",
                fg="#FFFFFF"
            )
            word_title.pack()
            
            word_label = tk.Label(
                inner_frame,
                text=self.secretWord.upper(),
                font=("Helvetica", 35, "bold"),
                bg="#1e1e1e",
                fg="#538d4e"
            )
            word_label.pack(pady=5)
            
        else:
            # Màn hình THUA
            # Icon và tiêu đề
            icon_label = tk.Label(
                content_frame,
                text="😢💔😢",
                font=("Helvetica", 60),
                bg=BG_COLOR,
                fg="#FF4500"
            )
            icon_label.pack(pady=(30, 10))
            
            message_label = tk.Label(
                content_frame,
                text="HẾT LƯỢT!",
                font=("Helvetica", 45, "bold"),
                bg=BG_COLOR,
                fg="#ff6b6b"
            )
            message_label.pack(pady=10)
            
            try_label = tk.Label(
                content_frame,
                text="Đừng bỏ cuộc! Hãy thử lại nhé! 💪",
                font=("Helvetica", 18, "bold"),
                bg=BG_COLOR,
                fg="#b59f3b"
            )
            try_label.pack(pady=5)
            
            # Hiển thị từ đúng
            word_frame = tk.Frame(content_frame, bg="#1e1e1e", relief="raised", bd=3, width=300)
            word_frame.pack(pady=20, padx=30)
            
            # Tạo container bên trong để căn giữa nội dung
            inner_frame = tk.Frame(word_frame, bg="#1e1e1e")
            inner_frame.pack(padx=15, pady=10)
            
            word_title = tk.Label(
                inner_frame,
                text="Từ đúng là:",
                font=("Helvetica", 14, "bold"),
                bg="#1e1e1e",
                fg="#FFFFFF"
            )
            word_title.pack()
            
            word_label = tk.Label(
                inner_frame,
                text=self.secretWord.upper(),
                font=("Helvetica", 35, "bold"),
                bg="#1e1e1e",
                fg="#b59f3b"
            )
            word_label.pack(pady=5)

        # Khung nút bấm
        buttons_frame = tk.Frame(content_frame, bg=BG_COLOR)
        buttons_frame.pack(pady=30)

        # Chiều rộng cố định cho tất cả các nút
        button_width = 300

        # Nút Chơi lại với màu xanh lá
        play_again_button = tk.Button(
            buttons_frame,
            text="🔄 CHƠI LẠI",
            font=("Helvetica", 14, "bold"),
            bg="#538d4e",
            fg="#FFFFFF",
            activebackground="#6aaa64",
            activeforeground="#FFFFFF",
            relief="raised",
            bd=3,
            cursor="hand2",
            width=button_width,
            command=self.show_game_screen
        )
        play_again_button.pack(pady=8, ipady=12)
        play_again_button.config(width=0)  # Reset width để dùng pixels
        play_again_button.pack_configure(ipadx=(button_width - play_again_button.winfo_reqwidth()) // 2)
        
        # Hiệu ứng hover cho nút Chơi lại
        play_again_button.bind("<Enter>", lambda e: play_again_button.config(bg="#6aaa64"))
        play_again_button.bind("<Leave>", lambda e: play_again_button.config(bg="#538d4e"))

        # Nút Trang chủ với màu vàng
        home_button = tk.Button(
            buttons_frame,
            text="🏠 TRANG CHỦ",
            font=("Helvetica", 14, "bold"),
            bg="#b59f3b",
            fg="#FFFFFF",
            activebackground="#c9b458",
            activeforeground="#FFFFFF",
            relief="raised",
            bd=3,
            cursor="hand2",
            width=button_width,
            command=self.show_start_screen
        )
        home_button.pack(pady=8, ipady=12)
        home_button.config(width=0)  # Reset width để dùng pixels
        home_button.pack_configure(ipadx=(button_width - home_button.winfo_reqwidth()) // 2)
        
        # Hiệu ứng hover cho nút Trang chủ
        home_button.bind("<Enter>", lambda e: home_button.config(bg="#c9b458"))
        home_button.bind("<Leave>", lambda e: home_button.config(bg="#b59f3b"))

        # Nút Thoát với màu đỏ
        exit_button = tk.Button(
            buttons_frame,
            text="❌ THOÁT",
            font=("Helvetica", 14, "bold"),
            bg="#FD0000",
            fg="#FFFFFF",
            activebackground="#FD4242",
            activeforeground="#FFFFFF",
            relief="raised",
            bd=3,
            cursor="hand2",
            width=button_width,
            command=self.destroy
        )
        exit_button.pack(pady=8, ipady=12)
        exit_button.config(width=0)  # Reset width để dùng pixels
        exit_button.pack_configure(ipadx=(button_width - exit_button.winfo_reqwidth()) // 2)
        
        # Hiệu ứng hover cho nút Thoát
        exit_button.bind("<Enter>", lambda e: exit_button.config(bg="#FD4242"))
        exit_button.bind("<Leave>", lambda e: exit_button.config(bg="#FD0000"))

    def create_game_widgets(self):
        """Tạo các widget cho màn hình game (grid và keyboard)."""
        
        self.gameMainFrame = tk.Frame(self, bg=BG_COLOR)
        self.gameMainFrame.pack(pady=20, padx=10, expand=True, fill="both")

        self.gameCanvas = tk.Canvas(self.gameMainFrame, bg=BG_COLOR, highlightthickness=0)
        
        self.scrollbar = tk.Scrollbar(self.gameMainFrame, orient="vertical", command=self.gameCanvas.yview)
        # self.h_scrollbar = tk.Scrollbar(self.gameMainFrame, orient="horizontal", command=self.gameCanvas.xview)
        
        self.gameCanvas.configure(
            yscrollcommand=self.scrollbar.set
            # xscrollcommand=self.h_scrollbar.set
        )

        self.scrollbar.pack(side="right", fill="y")     
        # self.h_scrollbar.pack(side="bottom", fill="x")   
        self.gameCanvas.pack(side="left", fill="both", expand=True)

        self.grid_frame = tk.Frame(self.gameCanvas, bg=BG_COLOR)

        self.canvas_window = self.gameCanvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        def update_canvas_layout(event=None):
            """
            Hàm này làm 2 việc:
            1. Cập nhật 'scrollregion' để canvas biết nó cần cuộn bao xa.
            2. Căn giữa 'grid_frame' theo chiều ngang nếu nó nhỏ hơn canvas.
            """
            
            self.gameCanvas.configure(scrollregion=self.gameCanvas.bbox("all"))

            canvas_width = self.gameCanvas.winfo_width() 
            frame_width = self.grid_frame.winfo_reqwidth() 
            
            new_x = (canvas_width - frame_width) // 2
            
            if new_x < 0:
                new_x = 0
            
            self.gameCanvas.coords(self.canvas_window, (new_x, 0))

        self.grid_frame.bind("<Configure>", update_canvas_layout)
        self.gameCanvas.bind("<Configure>", update_canvas_layout)

        # Grid Frame
        self.grid = []
        for i in range(self.maxGuesses):
            row = []
            frame_row = tk.Frame(self.grid_frame, bg=BG_COLOR)
            frame_row.pack() 
            for j in range(self.wordLength):
                cell = tk.Label(frame_row, text="", width=2, height=1, font=FONT_NORMAL,
                                 bg=COLOR_DEFAULT, fg=FG_COLOR, highlightbackground=COLOR_BORDER, highlightthickness=1)
                cell.pack(side="left", padx=3, pady=3)
                row.append(cell)
            self.grid.append(row)

        # Keyboard Frame
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
                                bg=COLOR_KEYBOARD, fg=FG_COLOR, font=FONT_NORMAL_SMALL,
                                command=lambda c=char: self.on_key_press(c))
                btn.pack(side="left", padx=5, pady=5)
                self.keyboard[char] = btn

        last_row = tk.Frame(self.keyboardFrame, bg=BG_COLOR)
        last_row.pack()

        home_button = tk.Button(last_row, text="🏠", command=self.show_start_screen, width=6, height=2, bg=COLOR_KEYBOARD, fg=FG_COLOR, font=FONT_NORMAL_SMALL)
        home_button.pack(side="left", padx=5)

        enter_button = tk.Button(last_row, text="Enter", command=self.process_guess,
                                 width=6, height=2, bg=COLOR_KEYBOARD, fg=FG_COLOR, font=FONT_NORMAL_SMALL)
        enter_button.pack(side="left", padx=5)

        for char in "zxcvbnm":
            btn = tk.Button(last_row, text=char.upper(), width=4, height=2,
                            bg=COLOR_KEYBOARD, fg=FG_COLOR, font=FONT_NORMAL_SMALL,
                            command=lambda c=char: self.on_key_press(c))
            btn.pack(side="left", padx=5, pady=5)
            self.keyboard[char] = btn

        backspace_button = tk.Button(last_row, text="⌫", command=self.on_backspace, width=6, height=2, bg=COLOR_KEYBOARD, fg=FG_COLOR, font=FONT_NORMAL_SMALL)
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
        if (self.curRow < self.maxGuesses) and (self.curCol < self.wordLength):
            self.trigger_error_toast("Chưa nhập đủ chữ cái!")
            return
        if (self.curCol == self.wordLength) and (self.curRow < self.maxGuesses):
            guess = ''.join([self.grid[self.curRow][c].cget("text").lower() for c in range(self.wordLength)])

            if (guess not in self.wordList):
                self.trigger_error_toast("Từ không hợp lệ!")
                return

            print(f'Processing guess: {guess}')
            
            # Đánh giá từ đoán
            for i in range(self.wordLength):
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
            elif (guess != self.secretWord) and (self.curRow == self.maxGuesses):
                # messagebox.showinfo("Kết thúc!", f"Bạn đã hết lượt đoán! Từ đúng là: {self.secretWord}")
                self.after(500, lambda: self.show_end_screen(win=False))
                return
            
    def on_backspace(self): # Press Backspace
        if (self.curCol > 0) and (self.curRow < self.maxGuesses):
            self.curCol -= 1
            self.grid[self.curRow][self.curCol].config(text="")

    def on_key_press(self, char):
        if (self.curCol < self.wordLength) and (self.curRow < self.maxGuesses):
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
        for r in range(self.maxGuesses):
            for c in range(self.wordLength):
                self.grid[r][c].config(text="", bg=COLOR_DEFAULT)
        for key in self.keyboard:
            self.keyboard[key].config(bg=COLOR_KEYBOARD) 
        self.curRow = 0
        self.curCol = 0

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()