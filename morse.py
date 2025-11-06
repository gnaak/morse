import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import base64, os

# -----------------------------
# 키 로드 함수
# -----------------------------
def load_keys():
    if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem"):
        messagebox.showwarning("키 없음", "private_key.pem / public_key.pem 파일이 필요합니다.")
        return None, None
    try:
        with open("private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open("public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
        return private_key, public_key
    except Exception as e:
        messagebox.showerror("키 불러오기 실패", str(e))
        return None, None


private_key, public_key = load_keys()

# -----------------------------
# 암호화 / 복호화 함수
# -----------------------------
def encrypt_message(message: str) -> str:
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode('utf-8')


def decrypt_message(ciphertext_b64: str) -> str:
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')


# -----------------------------
# GUI 기능
# -----------------------------
def encrypt_action():
    text = input_entry.get().strip()
    if not text:
        messagebox.showwarning("입력 필요", "암호화할 내용을 입력하세요.")
        return
    try:
        result = encrypt_message(text)
        output_entry.config(state="normal")
        output_entry.delete(0, tk.END)
        output_entry.insert(0, result)
        output_entry.config(state="readonly")
    except Exception as e:
        messagebox.showerror("암호화 실패", str(e))


def decrypt_action():
    text = input_entry.get().strip()
    if not text:
        messagebox.showwarning("입력 필요", "복호화할 암호문을 입력하세요.")
        return
    try:
        result = decrypt_message(text)
        output_entry.config(state="normal")
        output_entry.delete(0, tk.END)
        output_entry.insert(0, result)
        output_entry.config(state="readonly")
    except Exception as e:
        messagebox.showerror("복호화 실패", str(e))


# -----------------------------
# GUI 구성
# -----------------------------
root = tk.Tk()
root.title("🔐 RSA 암호화/복호화 도구")
root.geometry("320x120")
root.resizable(False, False)

# 입력 라벨 + 입력창
tk.Label(root, text="입력", font=("맑은 고딕", 10)).grid(row=0, column=0, padx=5, pady=(15, 5), sticky="w")
input_entry = tk.Entry(root, width=30)
input_entry.grid(row=0, column=1, padx=10, pady=(15, 5))

# 결과 라벨 + 결과창
tk.Label(root, text="결과", font=("맑은 고딕", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
output_entry = tk.Entry(root, width=30, state="readonly")
output_entry.grid(row=1, column=1, padx=10, pady=5)

# 버튼 영역 (한 줄에 나란히)
btn_frame = tk.Frame(root)
btn_frame.grid(row=2, column=0, columnspan=2, pady=5)

encrypt_btn = tk.Button(btn_frame, text="암호화", width=15, command=encrypt_action)
encrypt_btn.pack(side="left", padx=20)

decrypt_btn = tk.Button(btn_frame, text="복호화", width=15, command=decrypt_action)
decrypt_btn.pack(side="right", padx=20)

root.mainloop()
