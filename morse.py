import tkinter as tk
from tkinter import messagebox

# -----------------------------
# 1. 한글 ↔ 자판 ↔ 모스부호
# -----------------------------
CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JONGSUNG_LIST = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

HANGUL_TO_ENG = {
    'ㅂ':'q','ㅃ':'Q','ㅈ':'w','ㅉ':'W','ㄷ':'e','ㄸ':'E','ㄱ':'r','ㄲ':'R','ㅅ':'t','ㅆ':'T',
    'ㅛ':'y','ㅕ':'u','ㅑ':'i','ㅐ':'o','ㅒ':'O','ㅔ':'p','ㅖ':'P',
    'ㅁ':'a','ㄴ':'s','ㅇ':'d','ㄹ':'f','ㅎ':'g','ㅗ':'h','ㅓ':'j','ㅏ':'k','ㅣ':'l',
    'ㅋ':'z','ㅌ':'x','ㅊ':'c','ㅍ':'v','ㅠ':'b','ㅜ':'n','ㅡ':'m'
}

MORSE_CODE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....',
    'I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.',
    'Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--',
    'X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---',
    '3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.'
}
MORSE_TO_ENG = {v: k for k, v in MORSE_CODE.items()}

def decompose_hangul(ch):
    code = ord(ch) - 0xAC00
    cho = code // 588
    jung = (code % 588) // 28
    jong = code % 28
    return CHOSUNG_LIST[cho], JUNGSUNG_LIST[jung], JONGSUNG_LIST[jong]

def korean_to_keyboard(text):
    result = ''
    for ch in text:
        if '가' <= ch <= '힣':
            cho, jung, jong = decompose_hangul(ch)
            for j in [cho, jung, jong]:
                if j != '':
                    result += HANGUL_TO_ENG.get(j, '')
        elif ch in HANGUL_TO_ENG:
            result += HANGUL_TO_ENG[ch]
        elif ch == ' ':
            result += ' '
        else:
            result += ch
    return result

def text_to_morse(text):
    result = []
    for c in text.upper():
        if c == ' ':
            result.append('/')
        elif c in MORSE_CODE:
            result.append(MORSE_CODE[c])
        else:
            result.append('?')
    return ' '.join(result)

def morse_to_text(morse):
    words = morse.strip().split(' / ')
    decoded_words = []
    for word in words:
        letters = word.split()
        decoded_letters = [MORSE_TO_ENG.get(l, '?') for l in letters]
        decoded_words.append(''.join(decoded_letters))
    return ' '.join(decoded_words)

# -----------------------------
# 2. 기능 함수
# -----------------------------
def convert_text():
    text = input_entry.get().strip()
    if not text:
        messagebox.showwarning("입력 필요", "내용을 입력하세요.")
        return
    
    # 모스부호인지 판별 (., -, / 만 포함되어 있으면)
    if all(c in ".-/ " for c in text):
        result = morse_to_text(text)
    else:
        eng = korean_to_keyboard(text)
        result = text_to_morse(eng)
    
    output_entry.config(state="normal")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, result)
    output_entry.config(state="readonly")

def copy_to_clipboard():
    text = output_entry.get().strip()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        messagebox.showinfo("복사 완료", "결과가 클립보드에 복사되었습니다!")
    else:
        messagebox.showwarning("내용 없음", "복사할 내용이 없습니다.")

# -----------------------------
# 3. GUI
# -----------------------------
root = tk.Tk()
root.title("모스부호 ↔ 한글 변환기")
root.geometry("440x100")
root.resizable(False, False)

input_entry = tk.Entry(root, width=50, font=("맑은 고딕", 10))
input_entry.grid(row=0, column=0, padx=(10,5), pady=(15,5), sticky="we")

convert_btn = tk.Button(root, text="변환", width=8, height=1, command=convert_text)
convert_btn.grid(row=0, column=1, padx=(0,10), pady=(15,5), sticky="e")

output_entry = tk.Entry(root, width=50, font=("Consolas", 10), state="readonly")
output_entry.grid(row=1, column=0, padx=(10,5), pady=(5,15), sticky="we")

copy_btn = tk.Button(root, text="복사", width=8, height=1, command=copy_to_clipboard)
copy_btn.grid(row=1, column=1, padx=(0,10), pady=(5,15), sticky="e")

root.mainloop()
