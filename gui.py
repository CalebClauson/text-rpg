import tkinter as tk
from combat import combat_encounter, handle_potion, handle_run, get_move, handle_move, enemy_turn


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


    #stats labels
    player_stats_label = tk.Label(top_frame, text="")
    player_stats_label.grid(row=0, column=0, padx=20)

    enemy_stats_label = tk.Label(top_frame, text="")
    enemy_stats_label.grid(row=0, column=1, padx=20)

    def refresh_stats():
        player_stats_label.config(
            text=f"{player.name}\nHP: {player.hp}/{player.max_hp}\nATK: {player.attack}\nARMOR: {player.armor}"
        )

        if current_enemy is not None:
            shown_hp = max(0, current_enemy.hp)
            enemy_stats_label.config(
                text=f"{current_enemy.name}\nHP: {shown_hp}/{current_enemy.max_hp}\nATK: {current_enemy.attack}\nARMOR: {current_enemy.armor}"
            )
        else:
            enemy_stats_label.config(text="")

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
                for i, move_id in enumerate(player.moves):
                    move = get_move(move_id)

                    btn = tk.Button(
                        bottom_frame,
                        text=move["name"],
                        command=lambda m_id=move_id: on_attack(m_id)
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

    #start and end of combat

    def start_combat():
        nonlocal in_combat, current_enemy, attack_panel
        current_enemy = combat_encounter(player, log)
        in_combat = True
        attack_panel = False
        refresh_stats()
        render_buttons()

    def end_combat():
        nonlocal in_combat, current_enemy, attack_panel
        in_combat = False
        current_enemy = None
        attack_panel = False
        render_buttons()

    #button for moves

    def attack_ui():
        nonlocal attack_panel
        attack_panel = True
        render_buttons()

    def close_attack_ui():
        nonlocal attack_panel
        attack_panel = False
        render_buttons()

    #combat helpers

    def on_attack(move_id):
        user = player
        other = current_enemy
        result = handle_move(user, other, move_id, log)
        refresh_stats()
        if result in ["enemy_dead", "player_dead"]:
            end_combat()
        else:
            enemy_turn(player, current_enemy, log)

    def on_heal():
        result = handle_potion(player, current_enemy, log)
        refresh_stats()
        if result in ["enemy_dead", "player_dead"]:
            end_combat()
        else:
            enemy_turn(player, current_enemy, log)

    def on_run():
        result = handle_run(player, current_enemy, log)
        refresh_stats()
        if result in ["escaped", "player_dead"]:
            end_combat()

    render_buttons()
    refresh_stats()
    root.mainloop()