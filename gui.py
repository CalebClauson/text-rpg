import tkinter as tk
from tkinter import ttk

from player import Player
from systems.combat import combat_encounter, process_victory, resolve_player_turn, get_move
from save_load import load_player, save_player, delete_player_save

BG_MAIN = "#1e1e1e"
BG_PANEL = "#2a2a2a"
BG_WIDGET = "#3a3a3a"
BG_ACTIVE = "#4a4a4a"

TEXT_MAIN = "#f0f0f0"
TEXT_SECONDARY = "#bfbfbf"

ACCENT_BLUE = "#5c7cfa"
ACCENT_GREEN = "#4caf50"
ACCENT_RED = "#e57373"
ACCENT_GOLD = "#d4a017"

BORDER = "#555555"


def start_gui(player):
    current_enemy = None
    game_state = "menu"

    dead_player_name = ""
    player_stats_label = None
    level_label = None
    xp_label = None
    xp_left_label = None
    xp_bar = None
    enemy_stats_label = None
    pending_move_choices = []
    name_entry = None
    gold_label = None

    temp_name = ""
    stat_points = 3
    temp_attack = 10
    temp_speed = 5
    temp_armor = 5

    char_frame = None
    points_label = None
    atk_label = None
    spd_label = None
    arm_label = None

    root = tk.Tk()
    root.title("Text RPG")
    root.geometry("900x600")
    root.minsize(800, 700)
    root.configure(bg=BG_MAIN)

    top_frame = tk.Frame(root, bg=BG_MAIN, padx=15, pady=15)
    top_frame.pack_forget()

    middle_frame = tk.Frame(root, bg=BG_PANEL, padx=15, pady=15)
    middle_frame.pack(fill="both", expand=True)

    bottom_frame = tk.Frame(root, bg=BG_PANEL, padx=15, pady=15)
    bottom_frame.pack(fill="x")

    text_box = tk.Text(
        middle_frame,
        height=10,
        width=50,
        bg=BG_PANEL,
        fg=TEXT_MAIN,
        insertbackground=TEXT_MAIN,
        bd=0,
        relief="flat",
        highlightthickness=1,
        wrap="word",
        padx=10,
        pady=10
    )
    text_box.tag_config("player", foreground="#5c7cfa")
    text_box.tag_config("enemy", foreground="#e57373")
    text_box.tag_config("heal", foreground="#4caf50")
    text_box.tag_config("warn", foreground="#d4a017")
    text_box.tag_config("normal", foreground=TEXT_MAIN)
    text_box.pack(fill="x", pady=10)
    text_box.pack_forget()

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
            padx=14,
            pady=6,
            width=16
        )

    def log(message, tag="normal"):
        text_box.config(state="normal")
        text_box.insert(tk.END, message + "\n", tag)
        text_box.config(state="disabled")
        text_box.see(tk.END)

    def show_text_box():
        if not text_box.winfo_ismapped():
            text_box.pack(fill="x", pady=10)
        text_box.config(state="normal")
        text_box.delete("1.0", tk.END)
        text_box.config(state="disabled")

    def hide_text_box():
        if text_box.winfo_ismapped():
            text_box.pack_forget()

    def show_top_frame():
        if not top_frame.winfo_ismapped():
            top_frame.pack(fill="x", before=middle_frame)

    def hide_top_frame():
        if top_frame.winfo_ismapped():
            top_frame.pack_forget()

    def build_stats_ui():
        nonlocal player_stats_label, level_label, xp_label, xp_left_label, xp_bar, enemy_stats_label

        show_top_frame()

        if player_stats_label is not None:
            return

        player_stats_label = tk.Label(
            top_frame,
            text="",
            bg=BG_PANEL,
            fg=TEXT_MAIN,
            highlightthickness=1,
            highlightbackground=BORDER,
            font=("Arial", 12),
            justify="left",
            anchor="w",
            padx=12,
            pady=12,
            width=20
        )
        player_stats_label.grid(row=0, column=0, sticky="w", padx=(10, 0))

        xp_frame = tk.Frame(top_frame, bg=BG_MAIN)
        xp_frame.grid(row=1, column=0, sticky="w", padx=(10, 0), pady=(8, 0))

        level_label = tk.Label(xp_frame, text="", bg=BG_MAIN, fg=TEXT_MAIN, font=("Arial", 11, "bold"))
        level_label.pack(anchor="w")

        xp_label = tk.Label(xp_frame, text="", bg=BG_MAIN, fg=TEXT_MAIN, font=("Arial", 10))
        xp_label.pack(anchor="w")

        xp_left_label = tk.Label(xp_frame, text="", bg=BG_MAIN, fg=TEXT_SECONDARY, font=("Arial", 10))
        xp_left_label.pack(anchor="w")

        xp_bar = ttk.Progressbar(xp_frame, orient="horizontal", length=220, mode="determinate")
        xp_bar.pack(anchor="w", pady=(6, 0))

        enemy_stats_label = tk.Label(
            top_frame,
            text="",
            bg=BG_PANEL,
            fg=TEXT_MAIN,
            highlightthickness=1,
            highlightbackground=BORDER,
            font=("Arial", 12),
            justify="left",
            anchor="w",
            padx=12,
            pady=12,
            width=20
        )
        enemy_stats_label.grid(row=0, column=2, padx=20)

        top_frame.grid_columnconfigure(1, weight=1)

    def refresh_xp():
        if not player or xp_bar is None:
            return

        level_label.config(text=f"Level: {player.level}")
        xp_label.config(text=f"XP: {player.xp}/{player.xp_to_next}")
        xp_left_label.config(text=f"{player.xp_to_next - player.xp} XP until next level")
        xp_bar.config(maximum=player.xp_to_next, value=player.xp)

    def refresh_stats():
        if not player or player_stats_label is None:
            return

        player_stats_label.config(
            text=f"{player.name}\nHP: {player.hp}/{player.max_hp}\nATK: {player.attack}\nARMOR: {player.armor}\nSPD: {player.speed}\nGOLD: {player.gold}"
        )
        refresh_xp()

        if current_enemy is not None:
            shown_hp = max(0, current_enemy.hp)
            enemy_stats_label.config(
                text=f"{current_enemy.name}\nHP: {shown_hp}/{current_enemy.max_hp}\nATK: {current_enemy.attack}\nARMOR: {current_enemy.armor}\nSPD: {current_enemy.speed}"
            )
            enemy_stats_label.grid(row=0, column=2, padx=20)
        else:
            enemy_stats_label.grid_remove()

    def clear_menu_area():
        nonlocal char_frame, name_entry, points_label, atk_label, spd_label, arm_label, gold_label

        for widget in bottom_frame.winfo_children():
            widget.destroy()

        for widget in middle_frame.winfo_children():
            if widget is not text_box:
                widget.destroy()

        char_frame = None
        name_entry = None
        points_label = None
        atk_label = None
        spd_label = None
        arm_label = None
        gold_label = None

    def refresh_char_creator():
        nonlocal temp_name

        if char_frame is None or not char_frame.winfo_exists():
            return

        points_label.config(text=f"Points Remaining: {stat_points}")
        atk_label.config(text=f"Attack: {temp_attack}")
        spd_label.config(text=f"Speed: {temp_speed}")
        arm_label.config(text=f"Armor: {temp_armor}")

        if name_entry is not None and name_entry.winfo_exists():
            temp_name = name_entry.get()

    def build_char_creator():
        nonlocal char_frame, name_entry, points_label, atk_label, spd_label, arm_label

        if char_frame is not None and char_frame.winfo_exists():
            refresh_char_creator()
            return

        char_frame = tk.Frame(middle_frame, bg=BG_PANEL, padx=28, pady=28)
        char_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(
            char_frame,
            text="Create Character",
            bg=BG_PANEL,
            fg=TEXT_MAIN,
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 16))

        name_label = tk.Label(char_frame, text="Name:", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 11))
        name_label.grid(row=1, column=0, sticky="w", pady=(0, 8))

        name_entry = tk.Entry(
            char_frame,
            bg=BG_WIDGET,
            fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN,
            relief="flat"
        )
        name_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=(0, 8))
        name_entry.insert(0, temp_name)

        points_label = tk.Label(char_frame, text="", bg=BG_PANEL, fg=TEXT_SECONDARY, font=("Arial", 10))
        points_label.grid(row=2, column=0, columnspan=3, pady=(0, 16))

        atk_label = tk.Label(char_frame, text="", bg=BG_PANEL, fg=TEXT_MAIN)
        atk_label.grid(row=3, column=0, sticky="w", pady=6)
        make_button(char_frame, "-", lambda: remove_stat("attack"), bg=ACCENT_RED).grid(
            row=3, column=1, sticky="ew", padx=(10, 5), pady=6
        )
        make_button(char_frame, "+", lambda: add_stat("attack"), bg=ACCENT_GOLD).grid(
            row=3, column=2, sticky="ew", padx=(5, 0), pady=6
        )

        spd_label = tk.Label(char_frame, text="", bg=BG_PANEL, fg=TEXT_MAIN)
        spd_label.grid(row=4, column=0, sticky="w", pady=6)
        make_button(char_frame, "-", lambda: remove_stat("speed"), bg=ACCENT_RED).grid(
            row=4, column=1, sticky="ew", padx=(10, 5), pady=6
        )
        make_button(char_frame, "+", lambda: add_stat("speed"), bg=ACCENT_GOLD).grid(
            row=4, column=2, sticky="ew", padx=(5, 0), pady=6
        )

        arm_label = tk.Label(char_frame, text="", bg=BG_PANEL, fg=TEXT_MAIN)
        arm_label.grid(row=5, column=0, sticky="w", pady=6)
        make_button(char_frame, "-", lambda: remove_stat("armor"), bg=ACCENT_RED).grid(
            row=5, column=1, sticky="ew", padx=(10, 5), pady=6
        )
        make_button(char_frame, "+", lambda: add_stat("armor"), bg=ACCENT_GOLD).grid(
            row=5, column=2, sticky="ew", padx=(5, 0), pady=6
        )

        confirm_btn = make_button(char_frame, "Confirm", confirm_new_char, bg=ACCENT_BLUE)
        back_btn = make_button(char_frame, "Back", back_to_menu, bg=ACCENT_RED)

        confirm_btn.grid(row=6, column=1, pady=(18, 0), padx=(10, 5), sticky="ew")
        back_btn.grid(row=6, column=2, pady=(18, 0), padx=(5, 0), sticky="ew")

        char_frame.grid_columnconfigure(0, weight=1, minsize=180)
        char_frame.grid_columnconfigure(1, weight=1, minsize=70)
        char_frame.grid_columnconfigure(2, weight=1, minsize=70)

        refresh_char_creator()

    def back_to_menu():
        nonlocal game_state, current_enemy, player
        game_state = "menu"
        current_enemy = None
        player = None
        hide_text_box()
        hide_top_frame()
        render_buttons()

    def add_stat(stat_name):
        nonlocal stat_points, temp_attack, temp_speed, temp_armor, temp_name

        if name_entry is not None and name_entry.winfo_exists():
            temp_name = name_entry.get()

        if stat_points <= 0:
            return

        if stat_name == "attack":
            temp_attack += 1
        elif stat_name == "speed":
            temp_speed += 1
        elif stat_name == "armor":
            temp_armor += 1

        stat_points -= 1
        refresh_char_creator()

    def remove_stat(stat_name):
        nonlocal stat_points, temp_attack, temp_speed, temp_armor, temp_name

        if name_entry is not None and name_entry.winfo_exists():
            temp_name = name_entry.get()

        if stat_name == "attack" and temp_attack > 10:
            temp_attack -= 1
            stat_points += 1
        elif stat_name == "speed" and temp_speed > 5:
            temp_speed -= 1
            stat_points += 1
        elif stat_name == "armor" and temp_armor > 5:
            temp_armor -= 1
            stat_points += 1

        refresh_char_creator()

    def confirm_new_char():
        nonlocal player
        name = name_entry.get().strip() if name_entry else ""
        if not name:
            name = "Hero"

        player = Player.new_character(name, attack=temp_attack, speed=temp_speed, armor=temp_armor)
        save_player(player)
        build_stats_ui()
        show_text_box()
        refresh_stats()
        refresh_xp()
        start_combat()

    def new_game():
        nonlocal game_state, stat_points, temp_attack, temp_speed, temp_armor, temp_name
        game_state = "new_char"
        stat_points = 3
        temp_attack = 10
        temp_speed = 5
        temp_armor = 5
        temp_name = ""
        hide_text_box()
        hide_top_frame()
        clear_menu_area()
        build_char_creator()

    def load_game():
        nonlocal player
        loaded_player = load_player()

        if not loaded_player:
            return

        player = loaded_player
        build_stats_ui()
        show_text_box()
        refresh_stats()
        refresh_xp()
        start_combat()

    def enter_hub():
        nonlocal game_state, current_enemy
        save_player(player)
        game_state = "hub"
        current_enemy = None
        show_top_frame()
        show_text_box()
        refresh_stats()
        refresh_xp()
        render_buttons()

    def enter_shop():
        nonlocal game_state
        hide_text_box()
        hide_top_frame()
        game_state = "shop"
        render_buttons()

    def buy_potion(potion_cost):
        if player.gold < potion_cost:
            return
        player.gold -= potion_cost
        player.inventory.append("potion")
        save_player(player)
        if gold_label is not None:
            gold_label.config(text=f"Gold: {player.gold}")
        refresh_stats()

    def buy_attack_upgrade(attack_cost):
        if player.gold < attack_cost:
            return
        player.attack += 1
        player.gold -= attack_cost
        save_player(player)
        if gold_label is not None:
            gold_label.config(text=f"Gold: {player.gold}")
        refresh_stats()

    def buy_speed_upgrade(speed_cost):
        if player.gold < speed_cost:
            return
        player.speed += 1
        player.gold -= speed_cost
        save_player(player)
        if gold_label is not None:
            gold_label.config(text=f"Gold: {player.gold}")
        refresh_stats()

    def buy_armor_upgrade(armor_cost):
        if player.gold < armor_cost:
            return
        player.armor += 1
        player.gold -= armor_cost
        save_player(player)
        if gold_label is not None:
            gold_label.config(text=f"Gold: {player.gold}")
        refresh_stats()

    def level_up(move_choices):
        nonlocal game_state, current_enemy, pending_move_choices
        pending_move_choices = move_choices
        game_state = "level_up"
        current_enemy = None
        show_text_box()
        save_player(player)
        refresh_stats()
        refresh_xp()
        render_buttons()

    def learn_move(move_id):
        if len(player.moves) < 4:
            player.learn_move(move_id)
        else:
            player.moves[-1] = move_id

        save_player(player)
        enter_hub()

    def start_combat():
        nonlocal game_state, current_enemy

        current_enemy, result = combat_encounter(player, log)

        if result == "player_dead":
            handle_player_death()
            return

        game_state = "combat"
        refresh_stats()
        refresh_xp()
        render_buttons()

    def end_combat():
        enter_hub()

    def handle_post_combat():
        move_choices = process_victory(player, current_enemy, log)
        refresh_stats()
        refresh_xp()

        if move_choices:
            level_up(move_choices)
        else:
            end_combat()

    def attack_ui():
        nonlocal game_state
        game_state = "attack_menu"
        render_buttons()

    def close_attack_ui():
        nonlocal game_state
        game_state = "combat"
        render_buttons()

    def handle_turn_result(result):
        refresh_stats()
        refresh_xp()

        if result == "enemy_dead":
            handle_post_combat()
            return

        if result == "player_dead":
            handle_player_death()
            return

        if result == "escaped":
            end_combat()
            return

        render_buttons()

    def on_attack(move_id):
        result = resolve_player_turn(player, current_enemy, "attack", log, move_id)
        handle_turn_result(result)

    def on_heal():
        result = resolve_player_turn(player, current_enemy, "heal", log)
        handle_turn_result(result)

    def on_run():
        result = resolve_player_turn(player, current_enemy, "run", log)
        handle_turn_result(result)

    def handle_player_death():
        nonlocal current_enemy, game_state, player, dead_player_name

        dead_player_name = player.name
        log(f"{dead_player_name} has fallen. Run over.", tag="warn")
        delete_player_save()
        current_enemy = None
        game_state = "game_over"
        hide_text_box()
        player = None
        refresh_stats()
        refresh_xp()
        render_buttons()

    def render_buttons():
        nonlocal gold_label
        clear_menu_area()

        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        if game_state == "menu":
            menu_frame = tk.Frame(middle_frame, bg=BG_PANEL, padx=36, pady=32)
            menu_frame.place(relx=0.5, rely=0.5, anchor="center")

            title_label = tk.Label(menu_frame, text="Text RPG", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 24, "bold"))
            title_label.grid(row=0, column=0, columnspan=2, pady=(0, 22))

            subtitle_label = tk.Label(
                menu_frame,
                text="Start a new run or load your saved character",
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=("Arial", 10)
            )
            subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 18))

            btn1 = make_button(menu_frame, "New Game", new_game, bg=ACCENT_GOLD)
            btn2 = make_button(menu_frame, "Load Player", load_game, bg=ACCENT_BLUE)
            btn3 = make_button(menu_frame, "Quit", root.destroy, bg=ACCENT_RED)

            btn1.grid(row=2, column=0, padx=10, pady=8, sticky="ew")
            btn2.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
            btn3.grid(row=3, column=0, columnspan=2, padx=10, pady=(12, 0), sticky="ew")

            menu_frame.grid_columnconfigure(0, weight=1, minsize=180)
            menu_frame.grid_columnconfigure(1, weight=1, minsize=180)

        elif game_state == "new_char":
            build_char_creator()

        elif game_state == "combat":
            btn1 = make_button(bottom_frame, "Attack!", attack_ui, bg=ACCENT_BLUE)
            btn2 = make_button(bottom_frame, "Heal", on_heal, bg=ACCENT_GREEN)
            btn3 = make_button(bottom_frame, "Backpack", lambda: player.backpack(log), bg=BG_WIDGET)
            btn4 = make_button(bottom_frame, "Run!", on_run, bg=ACCENT_RED)

            btn1.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
            btn2.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
            btn3.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
            btn4.grid(row=1, column=1, padx=8, pady=8, sticky="ew")

        elif game_state == "attack_menu":
            moves_frame = tk.Frame(bottom_frame, bg=BG_PANEL, padx=10, pady=6)
            moves_frame.grid(row=0, column=0, columnspan=2, pady=(10, 6), sticky="ew")

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

        elif game_state == "hub":
            btn1 = make_button(bottom_frame, "Next Encounter", start_combat, bg=ACCENT_GOLD)
            btn2 = make_button(bottom_frame, "Save", lambda: save_player(player), bg=ACCENT_BLUE)
            btn3 = make_button(bottom_frame, "Shop", enter_shop, bg=ACCENT_GREEN)
            btn4 = make_button(bottom_frame, "Quit", root.destroy, bg=ACCENT_RED)

            btn1.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
            btn2.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
            btn3.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
            btn4.grid(row=1, column=1, padx=8, pady=8, sticky="ew")

        elif game_state == "shop":
            attack_cost = 15 + ((player.level - 1) * 5)
            speed_cost = 15 + ((player.level - 1) * 5)
            armor_cost = 15 + ((player.level - 1) * 5)
            potion_cost = 10 + ((player.level - 1) * 5)

            shop_frame = tk.Frame(middle_frame, bg=BG_PANEL, padx=28, pady=28)
            shop_frame.place(relx=0.5, rely=0.5, anchor="center")

            title_label = tk.Label(shop_frame, text="Shop", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 20, "bold"))
            title_label.grid(row=0, column=0, columnspan=3, pady=(0, 8))

            gold_label = tk.Label(
                shop_frame,
                text=f"Gold: {player.gold}",
                bg=BG_PANEL,
                fg=ACCENT_GOLD,
                font=("Arial", 11, "bold")
            )
            gold_label.grid(row=1, column=0, columnspan=3, pady=(0, 18))

            section1_label = tk.Label(
                shop_frame,
                text="Items",
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=("Arial", 11, "bold")
            )
            section1_label.grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, 8))

            potion_name = tk.Label(shop_frame, text="Potion", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 11))
            potion_name.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=6)

            potion_price_label = tk.Label(
                shop_frame,
                text=f"{potion_cost} Gold",
                bg=BG_PANEL,
                fg=TEXT_MAIN,
                font=("Arial", 11)
            )
            potion_price_label.grid(row=3, column=1, sticky="w", padx=(0, 10), pady=6)

            buy_potion_btn = make_button(shop_frame, "Buy", lambda: buy_potion(potion_cost), bg=ACCENT_GREEN)
            buy_potion_btn.grid(row=3, column=2, sticky="ew", pady=6)

            section2_label = tk.Label(
                shop_frame,
                text="Stat Upgrades",
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=("Arial", 11, "bold")
            )
            section2_label.grid(row=4, column=0, columnspan=3, sticky="w", pady=(18, 8))

            atk_name = tk.Label(shop_frame, text="+1 Attack", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 11))
            atk_name.grid(row=5, column=0, sticky="w", padx=(0, 10), pady=6)

            atk_price_label = tk.Label(shop_frame, text=f"{attack_cost} Gold", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 11))
            atk_price_label.grid(row=5, column=1, sticky="w", padx=(0, 10), pady=6)

            buy_atk_btn = make_button(shop_frame, "Buy", lambda: buy_attack_upgrade(attack_cost), bg=ACCENT_BLUE)
            buy_atk_btn.grid(row=5, column=2, sticky="ew", pady=6)

            spd_name = tk.Label(shop_frame, text="+1 Speed", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 11))
            spd_name.grid(row=6, column=0, sticky="w", padx=(0, 10), pady=6)

            spd_price_label = tk.Label(shop_frame, text=f"{speed_cost} Gold", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 11))
            spd_price_label.grid(row=6, column=1, sticky="w", padx=(0, 10), pady=6)

            buy_spd_btn = make_button(shop_frame, "Buy", lambda: buy_speed_upgrade(speed_cost), bg=ACCENT_BLUE)
            buy_spd_btn.grid(row=6, column=2, sticky="ew", pady=6)

            arm_name = tk.Label(shop_frame, text="+1 Armor", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 11))
            arm_name.grid(row=7, column=0, sticky="w", padx=(0, 10), pady=6)

            arm_price_label = tk.Label(shop_frame, text=f"{armor_cost} Gold", bg=BG_PANEL, fg=TEXT_MAIN, font=("Arial", 11))
            arm_price_label.grid(row=7, column=1, sticky="w", padx=(0, 10), pady=6)

            buy_arm_btn = make_button(shop_frame, "Buy", lambda: buy_armor_upgrade(armor_cost), bg=ACCENT_BLUE)
            buy_arm_btn.grid(row=7, column=2, sticky="ew", pady=6)

            back_btn = make_button(shop_frame, "Back", enter_hub, bg=ACCENT_RED)
            back_btn.grid(row=8, column=0, columnspan=3, sticky="ew", pady=(18, 0))

            shop_frame.grid_columnconfigure(0, weight=1, minsize=180)
            shop_frame.grid_columnconfigure(1, weight=1, minsize=100)
            shop_frame.grid_columnconfigure(2, weight=1, minsize=120)

        elif game_state == "level_up":
            info_label = tk.Label(
                middle_frame,
                text="Choose a new move",
                bg=BG_PANEL,
                fg=TEXT_MAIN,
                font=("Arial", 16, "bold")
            )
            info_label.place(relx=0.5, rely=0.25, anchor="center")

            for i, move_id in enumerate(pending_move_choices):
                move = get_move(move_id)
                btn = make_button(
                    bottom_frame,
                    move["name"],
                    lambda m_id=move_id: learn_move(m_id),
                    bg=ACCENT_GOLD
                )
                btn.grid(row=0, column=i, padx=8, pady=8, sticky="ew")

        elif game_state == "game_over":
            gameover_frame = tk.Frame(middle_frame, bg=BG_PANEL, padx=36, pady=32)
            gameover_frame.place(relx=0.5, rely=0.5, anchor="center")

            title_label = tk.Label(
                gameover_frame,
                text="Game Over",
                bg=BG_PANEL,
                fg=ACCENT_RED,
                font=("Arial", 24, "bold")
            )
            title_label.grid(row=0, column=0, columnspan=2, pady=(0, 16))

            subtitle_label = tk.Label(
                gameover_frame,
                text=f"{dead_player_name} has fallen.",
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=("Arial", 11)
            )
            subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 18))

            btn1 = make_button(gameover_frame, "Return to Menu", back_to_menu, bg=ACCENT_GOLD)
            btn2 = make_button(gameover_frame, "Quit", root.destroy, bg=ACCENT_RED)

            btn1.grid(row=2, column=0, padx=10, pady=8, sticky="ew")
            btn2.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

            gameover_frame.grid_columnconfigure(0, weight=1, minsize=180)
            gameover_frame.grid_columnconfigure(1, weight=1, minsize=180)

    render_buttons()
    root.mainloop()