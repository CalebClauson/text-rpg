import tkinter as tk
from combat import combat_encounter

def start_gui(player, enemy, combat):
    current_enemy = None
    in_combat = False

    root = tk.Tk()
    root.title("Text RPG")

    top_frame = tk.Frame(root)
    top_frame.pack(fill="both", expand=True)

    middle_frame = tk.Frame(root)
    middle_frame.pack(fill="both", expand=True)

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(fill="x")

    text_box = tk.Text(middle_frame, height=10, width=50)
    text_box.pack(expand=True)

    def log(message):
        text_box.config(state="normal")
        text_box.insert(tk.END, message + "\n")
        text_box.config(state="disabled")
        text_box.see(tk.END)

    def render_buttons():
        for widget in bottom_frame.winfo_children():
            widget.destroy()

        if in_combat:
            btn1 = tk.Button(bottom_frame, text="Attack!", command=lambda: player.attack_enemy(current_enemy, log))
            btn2 = tk.Button(bottom_frame, text="Heal!", command=lambda: player.use_item("potion", log))
            btn3 = tk.Button(bottom_frame, text="Backpack!", command=lambda: player.backpack(log))
            btn4 = tk.Button(bottom_frame, text="Run!", command=lambda: player.run(current_enemy, combat, log))

            btn1.grid(row=0, column=0)
            btn2.grid(row=0, column=1)
            btn3.grid(row=1, column=0)
            btn4.grid(row=1, column=1)
        else:
            btn1 = tk.Button(bottom_frame, text="Left!")
            btn2 = tk.Button(bottom_frame, text="Right!", command=start_combat)

            btn1.grid(row=0, column=0)
            btn2.grid(row=0, column=1)

    def start_combat():
        nonlocal in_combat, current_enemy
        current_enemy = combat_encounter(log)
        in_combat = True
        render_buttons()

    render_buttons()
    root.mainloop()