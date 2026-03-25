import tkinter as tk
from combat import combat_encounter, handle_potion, handle_run, get_move, handle_move, enemy_turn
from status_effects import process_status_start_turn, update_status_durations

BG_MAIN = "#1e1e1e"       # main window background
BG_PANEL = "#2a2a2a"      # frames / panels
BG_WIDGET = "#3a3a3a"     # buttons / entry boxes
BG_ACTIVE = "#4a4a4a"     # button hover / active

TEXT_MAIN = "#f0f0f0"     # main text
TEXT_SECONDARY = "#bfbfbf" # softer text

ACCENT_BLUE = "#5c7cfa"   # main accent
ACCENT_GREEN = "#4caf50"  # heal / success
ACCENT_RED = "#e57373"    # danger / enemy / errors
ACCENT_GOLD = "#d4a017"   # special / highlight

BORDER = "#555555"        # subtle borders


def start_gui(player, enemy):
    current_enemy = None
    in_combat = False
    attack_panel = False

    root = tk.Tk()
    root.title("Text RPG")

    root.geometry("900x600")
    root.minsize(700, 500)

    top_frame = tk.Frame(root, bg=BG_MAIN, padx=15, pady=15)
    top_frame.pack(fill="x")

    middle_frame = tk.Frame(root, bg=BG_PANEL, padx=15, pady=15)
    middle_frame.pack(fill="both", expand=True)

    bottom_frame = tk.Frame(root, bg=BG_PANEL, padx=15, pady=15)
    bottom_frame.pack(fill="x")

    text_box = tk.Text(middle_frame, height=10, width=50, bg=BG_PANEL, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=0, relief="flat", highlightthickness=1, wrap="word", padx=10, pady=10)
    text_box.pack(expand=True)

    text_box.tag_config("player", foreground="#5c7cfa")
    text_box.tag_config("enemy", foreground="#e57373")
    text_box.tag_config("heal", foreground="#4caf50")
    text_box.tag_config("warn", foreground="#d4a017")
    text_box.tag_config("normal", foreground=TEXT_MAIN)


    #stats labels
    player_stats_label = tk.Label(top_frame, text="", bg=BG_PANEL, fg=TEXT_MAIN, highlightthickness=1, highlightbackground=BORDER, font=("Arial", 12), justify="left", anchor="w", padx=12, pady=12, width=20)
    player_stats_label.grid(row=0, column=0, sticky="w", padx=(10, 0))

    enemy_stats_label = tk.Label(top_frame, text="", bg=BG_PANEL, fg=TEXT_MAIN, highlightthickness=1, highlightbackground=BORDER, font=("Arial", 12), justify="left", anchor="w", padx=12, pady=12, width=20)
    enemy_stats_label.grid(row=0, column=2, padx=20)

    top_frame.grid_columnconfigure(1, weight=1)

    #button helper
    def make_button(parent, text, command, bg=BG_WIDGET):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=TEXT_MAIN,
            activebackground=BG_ACTIVE,
            activeforeground=TEXT_MAIN,
            relief="flat",
            bd=0,
            font=("Arial", 12, "bold"),
            padx=18,
            pady=14,
            width=20
        )

    def refresh_stats():
        player_stats_label.config(
            text=f"{player.name}\nHP: {player.hp}/{player.max_hp}\nATK: {player.attack}\nARMOR: {player.armor}"
        )

        if current_enemy is not None:
            shown_hp = max(0, current_enemy.hp)

            enemy_stats_label.config(
                text=f"{current_enemy.name}\nHP: {shown_hp}/{current_enemy.max_hp}\nATK: {current_enemy.attack}\nARMOR: {current_enemy.armor}"
            )

            enemy_stats_label.grid(row=0, column=2, sticky="e", padx=10)
        else:
            enemy_stats_label.grid_remove()

    def log(message, tag="normal"):
        text_box.config(state="normal")
        text_box.insert(tk.END, message + "\n", tag)
        text_box.config(state="disabled")
        text_box.see(tk.END)

    def render_buttons():
        for widget in bottom_frame.winfo_children():
            widget.destroy()

        if in_combat:
            if attack_panel:
                moves_frame = tk.Frame(bottom_frame, bg=BG_PANEL, padx=10, pady=6)
                moves_frame.grid(row=0, column=0, columnspan=2, pady=(10, 6))

                moves_frame.grid_columnconfigure(0, weight=1)
                moves_frame.grid_columnconfigure(1, weight=1)

                for i, move_id in enumerate(player.moves):
                    move = get_move(move_id)

                    btn = make_button(
                        moves_frame,
                        move["name"],
                        lambda m_id=move_id: on_attack(m_id),
                        bg=ACCENT_BLUE
                    )
                    btn.grid(row=i // 2, column=i % 2, padx=14, pady=10, sticky="ew")

                btn_back = make_button(bottom_frame, "Back", close_attack_ui, bg=ACCENT_RED)
                btn_back.grid(row=1, column=0, columnspan=2, padx=14, pady=(10, 8), sticky="ew")

            else:
                btn1 = make_button(bottom_frame, "Attack!", attack_ui, bg=ACCENT_BLUE)
                btn2 = make_button(bottom_frame, "Heal!", on_heal, bg=ACCENT_GREEN)
                btn3 = make_button(bottom_frame, "Backpack!", lambda: player.backpack(log), bg=BG_WIDGET)
                btn4 = make_button(bottom_frame, "Run!", on_run, bg=ACCENT_RED)

                btn1.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
                btn2.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
                btn3.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
                btn4.grid(row=1, column=1, padx=8, pady=8, sticky="ew")
            bottom_frame.grid_columnconfigure(0, weight=1)
            bottom_frame.grid_columnconfigure(1, weight=1)

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
        refresh_stats()
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
    def begin_player_turn():
        stunned = process_status_start_turn(player, log)
        refresh_stats()
        if not player.is_alive():
            end_combat()
            return "player_dead"
        if stunned:
            update_status_durations(player, log)
            refresh_stats()
            enemy_turn(player, current_enemy, log)
            return "turn_skipped"

        return "continue"

    def on_attack(move_id):
        start_result = begin_player_turn()
        if start_result in ["player_dead", "turn_skipped"]:
            return
        user = player
        other = current_enemy
        result = handle_move(user, other, move_id, log, "player")
        update_status_durations(player, log)
        refresh_stats()
        if result in ["enemy_dead", "player_dead"]:
            end_combat()
        else:
            enemy_turn(player, current_enemy, log)

    def on_heal():
        result = handle_potion(player, current_enemy, log)
        update_status_durations(player, log)
        refresh_stats()
        if result in ["enemy_dead", "player_dead"]:
            end_combat()
        else:
            enemy_turn(player, current_enemy, log)

    def on_run():
        result = handle_run(player, current_enemy, log)
        update_status_durations(player, log)
        refresh_stats()
        if result in ["escaped", "player_dead"]:
            end_combat()

    render_buttons()
    refresh_stats()
    root.mainloop()