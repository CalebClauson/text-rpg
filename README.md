# Text RPG (Python + Tkinter)

A text-based RPG built with Python and Tkinter as I continue learning how to create more structured, interactive, and data-driven applications.

## Overview

This project started as a simple combat idea and gradually grew into a multi-file RPG with a graphical interface, turn-based combat, progression systems, shop mechanics, save/load support, and a more organized state-driven GUI flow.

The game uses JSON files for storing moves, enemies, and items, which helps keep the project flexible and easier to expand. It also now includes packaging-friendly file handling so the project can be shared and run more reliably outside of my own workspace.

## Purpose

This project was created to move beyond basic scripts and start building a more complete application with multiple files, connected systems, reusable logic, and a GUI.

It focuses on practicing:

- game logic
- state management
- event-driven programming
- GUI design with Tkinter
- JSON-based data handling
- debugging across multiple files
- separating interface code from gameplay logic
- refactoring as a project grows
- preparing a Python project for packaging and sharing

A major goal has been learning how to organize a project so it stays readable and maintainable as more systems are added.

## Current Features

### GUI-Based Game Flow

The game uses a Tkinter interface instead of the console, allowing the player to move through the game using menus, buttons, and different game states.

Current GUI flow includes:

- main menu
- character creation
- combat screen
- attack selection menu
- hub screen between encounters
- shop screen
- level-up screen
- game-over screen

The GUI has been cleaned up so it better handles screen transitions and overall interface flow while more gameplay logic is moved into separate system files.

### Character Creation

The game includes a character creation screen where the player can:

- choose a name
- distribute stat points
- customize starting attack
- customize starting speed
- customize starting armor

This makes the start of a run feel more interactive and gives the player control over their starting build.

### Combat System

The core gameplay loop is built around turn-based combat.

Players can:

- attack using learned moves
- heal with items
- check their backpack
- attempt to run from combat

Combat uses move data loaded from JSON, making it easier to expand move behavior without hardcoding everything directly into the interface.

### Move-Based Combat

Moves are selected through a dedicated attack menu and support multiple effect types.

Current supported move behavior includes:

- damage
- heal
- buff
- drain
- status effects

This allows different moves to feel more distinct while keeping combat data-driven and easier to expand.

### Status Effects

The game supports status effects that can be applied and processed over time.

Current status-related systems include:

- applying status effects through moves
- processing status effects at the start of turns
- updating status durations during combat

This adds more variety to combat and gives future move design more flexibility.

### Enemy Generation

Enemies are generated from JSON data rather than being hardcoded directly into combat logic.

Current enemy generation supports:

- loading enemies from JSON
- scaling enemy stats by player level
- scaling enemy gold rewards by player level
- weighted enemy selection for encounter variety

Example enemies include:

- Slime
- Goblin
- Wolf
- Spider
- Skeleton
- Bandit
- Orc
- Mage
- Zombie
- Dragon

This makes balancing easier and allows new enemies to be added without major code changes.

### Reward and Progression System

Defeating enemies grants rewards that feed directly into the gameplay loop.

Current combat rewards include:

- experience points
- gold

This creates a progression loop where combat leads to stronger characters, better rewards, and more options over time.

### Level System

The player has a level-based progression system tied to earned experience.

Leveling up currently includes:

- increased max health
- increased attack
- full heal on level up
- increased XP requirement for future levels

This helps fights feel meaningful and gives the run a stronger sense of progression.

### Level-Up Move Choices

When the player levels up, the game can offer random move choices from the move pool.

This system currently supports:

- pulling random moves from available moves
- preventing duplicate move choices from already learned moves
- learning new moves on level up
- move cap handling in the GUI
- skipping a move choice if the player does not want to learn one

This helps the project feel more RPG-like and gives progression a little more player choice.

### Inventory System

The inventory stores item IDs tied to JSON item data.

The system currently supports:

- storing items in inventory
- checking backpack contents
- using healing items in combat
- scaling potion healing based on player level

This keeps item handling simple while still supporting future expansion.

### Shop System

The game now includes a shop that gives the player another way to interact with progression between fights.

The shop currently supports:

- buying potions
- buying stat upgrades
- spending gold earned from combat
- scaling costs based on player level

This helps connect combat rewards to player progression and adds another decision point between encounters.

### Save and Load System

Player data is stored in JSON so progress can persist between sessions.

Current saved data includes:

- name
- health
- max health
- attack
- speed
- armor
- moves
- inventory
- gold
- level
- xp
- xp needed for next level

The project also includes a main menu flow for loading an existing player or creating a new one.

### Data-Driven Design

A major goal of the project is to separate data from logic wherever possible.

Game content is stored in JSON files, including:

- enemies
- moves
- items

This makes the project easier to expand and helps keep balance changes separate from core gameplay code.

## Project Structure

The project is split across multiple files so responsibilities are separated more clearly.

Current structure includes files such as:

- `gui.py` for menus, button rendering, interface state flow, and screen transitions
- `systems/combat.py` for encounter flow, turn resolution, and combat helpers
- `systems/enemy.py` for enemy behavior and stats
- `systems/status_effects.py` for applying and updating statuses
- `player.py` for player data, progression, inventory, and move learning
- `save_load.py` for save and load handling
- `paths.py` for safer asset and save-file path handling across normal runs and packaged builds

This separation has helped clean up the GUI and move repeated combat logic into dedicated systems where it belongs.

## Recent Improvements

Some of the more recent improvements to the project include:

- cleaner GUI state handling
- smoother transitions between menu, hub, shop, and combat
- reduced Tkinter flicker during character creation
- reduced shop flicker by updating values directly instead of rerendering the full screen
- improved handling for returning from the shop back to the hub
- added skip support on level-up move selection
- improved item scaling such as level-based potion healing
- added packaging-safe file path handling for assets
- moved save file handling to a more reliable writable location for packaged builds
- continued cleanup of combat and interface responsibilities

These updates helped the game feel more stable and made the UI behavior more consistent across systems.

## Packaging and Running

The project can be run normally in Python from the project folder.

Basic run command for Linux:
```bash
python main.py

Packaged Windows:
For the packaged Windows version, download the release ZIP, extract it, and run main.exe located in the dist folder.