from groq import Groq
import pyperclip
import keyboard
import tkinter as tk
from tkinter import messagebox
import time
import json
from colorama import Fore

convo = []

def call(content):
    time.sleep(0.1)
    pyperclip.copy("")
    client = Groq(api_key="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")

    convo.append({"role": "user", "content": content})

    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=convo,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    print(Fore.LIGHTYELLOW_EX + f"You:\n{response}" + Fore.RESET)
    convo.append({"role": "assistant", "content": response})

    if response is not None:
        pyperclip.copy(response)
        if instantpaste:
            keyboard.press("ctrl"); keyboard.press("v"); keyboard.release("ctrl"); keyboard.release("v")
    else:
        pyperclip.copy("[No Response Sent]") 
        
    print(Fore.LIGHTBLUE_EX + f"\nAI:\n{response}" + Fore.RESET)
    

def on_press():
    global active
    time.sleep(0.1)
    if active:
        content = pyperclip.paste()
        call(content)
    else:
        return

def change_mode():
    global active
    time.sleep(0.1)
    if active == False:
        active = True
        root = tk.Tk()
        root.withdraw()  
        root.attributes('-topmost', True)  
        messagebox.showinfo('Schoollama Enabled', 'Schoollama Copy-Paste Enabled\n[ctrl+shift+x] to Disable')
        root.destroy()
    else:
        active = False
        root = tk.Tk()
        root.withdraw()  
        root.attributes('-topmost', True)  
        messagebox.showinfo('Schoollama Disabled', 'Schoollama Copy-Paste Disabled\n[ctrl+shift+x] to Re-Enable')
        root.destroy()

    print(active)


active = False


with open("config.json") as f:
    cfg = json.load(f)

if cfg["prompt"] is not None and cfg["prompt"] !="":
    convo.append({"role": "user", "content": cfg["prompt"]})

if cfg["instant_paste"] == "True":
    instantpaste = True
else:
    instantpaste = False
print('Running')

keyboard.add_hotkey("alt+x", change_mode)
keyboard.add_hotkey("ctrl+c", on_press)

keyboard.wait()