import tkinter as tk
from combat import *

def start_gui(player, enemy):
    current_enemy = None
    in_combat = False
    attack_panel = False

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
            if attack_panel:
                for i, move in enumerate(player.moves):
                    btn = tk.Button(
                    bottom_frame,
                    text=move["name"],
                    command=lambda m=move: on_attack(m)
                    )
                    btn.grid(row=i // 2, column=i % 2)

                    btn_back = tk.Button(bottom_frame, text="Back", command=close_attack_ui)
                    btn_back.grid(row=(len(player.moves) // 2) + 1, column=0, columnspan=2)

            else:
                btn1 = tk.Button(bottom_frame, text="Attack!", command=attack_ui)
                btn2 = tk.Button(bottom_frame, text="Heal!", command=on_heal)
                btn3 = tk.Button(bottom_frame, text="Backpack!", command=lambda: player.backpack(log))
                btn4 = tk.Button(bottom_frame, text="Run!", command=on_run)

                btn1.grid(row=0, column=0)
                btn2.grid(row=0, column=1)
                btn3.grid(row=1, column=0)
                btn4.grid(row=1, column=1)

        else:
            btn1 = tk.Button(bottom_frame, text="Left!")
            btn2 = tk.Button(bottom_frame, text="Right!", command=start_combat)

            btn1.grid(row=0, column=0)
            btn2.grid(row=0, column=1)

    #combat helpers

    def start_combat():
        nonlocal in_combat, current_enemy
        current_enemy = combat_encounter(log)
        in_combat = True
        render_buttons()

    def end_combat():
        nonlocal in_combat, current_enemy

        in_combat = False
        current_enemy = None
        render_buttons()

    
    #button commands
    
    def attack_ui():
        nonlocal attack_panel
        attack_panel = True
        print(f"Attack_panel = {attack_panel}")
        render_buttons()

    def close_attack_ui():
        nonlocal attack_panel
        attack_panel = False
        render_buttons()


    def on_attack(move):
        result = handle_attack(player, current_enemy, move, log)

        if result in ["enemy_dead", "player_dead"]:
            end_combat()

    def on_heal():
        result = handle_heal(player, current_enemy, log)

        if result in ["enemy_dead", "player_dead"]:
            end_combat()

    def on_run():
        result = handle_run(player, current_enemy, log)

        if result in ["escaped", "player_dead"]:
            end_combat()

        

    render_buttons()
    root.mainloop()