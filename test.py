import tkinter as tk

# Biến toàn cục để lưu trữ toast_label, giúp dễ dàng quản lý
toast_label = None

def show_toast(message):
    global toast_label

    # Nếu đang có toast, hủy nó đi trước khi tạo cái mới
    if toast_label:
        toast_label.destroy()

    # 1. Tạo Label làm "toast"
    toast_label = tk.Label(
        root,
        text=message,
        bg="#c0392b",  # Màu đỏ đậm cho lỗi
        fg="white",     # Chữ trắng
        font=("Arial", 10, "bold"),
        padx=20,
        pady=10,
        relief="solid", # Viền
        borderwidth=1,
        # bordercolor="white", # (Không hỗ trợ trực tiếp, dùng relief)
    )

    # 2. Đặt vị trí cho toast (mấu chốt)
    # relx=0.5 -> Căn giữa theo chiều ngang (50% chiều rộng)
    # rely=0.9 -> Đặt ở gần đáy (90% chiều cao)
    # anchor="center" -> Đặt tâm của label tại điểm (relx, rely)
    toast_label.place(relx=0.5, rely=0.9, anchor="center")

    # 3. Lên lịch tự hủy
    # Gọi hàm 'destroy' của chính toast_label sau 2500ms (2.5 giây)
    toast_label.after(500, toast_label.destroy)

def trigger_error_toast():
    show_toast("Lỗi: Không thể kết nối tới server!")

# --- Thiết lập cửa sổ chính ---
root = tk.Tk()
root.title("Toast Notification Demo")
root.geometry("500x400")

# --- Widget nền (để thấy rõ overlay) ---
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True)

info_text = tk.Label(main_frame, text="Nội dung chính của ứng dụng ở đây.\nBạn vẫn có thể tương tác khi toast hiện lên.", font=("Arial", 12), bg="white")
info_text.pack(pady=50)

text_area = tk.Text(main_frame, height=10, width=50)
text_area.pack(padx=20, pady=10)

# --- Nút kích hoạt ---
trigger_button = tk.Button(
    main_frame,
    text="Hiển thị Toast Lỗi",
    command=trigger_error_toast
)
trigger_button.pack(pady=20)


root.mainloop()