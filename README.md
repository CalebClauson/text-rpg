# Text RPG (Python + Tkinter)

A text-based RPG built with Python and Tkinter as I continue learning how to create more structured, interactive, and data-driven applications.

## Overview

This project started as a simple combat idea and has gradually grown into a small multi-file RPG with a graphical interface, turn-based combat, progression systems, save/load support, and a more organized GUI-driven flow.

The game uses JSON files for storing moves, enemies, items, and save data, which helps keep the project flexible and easier to expand.

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

This was one of the bigger additions and helps the project feel more RPG-like.

### Inventory System

The inventory stores item IDs tied to JSON item data.

The system currently supports:

- storing items in inventory
- checking backpack contents
- using healing items in combat

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
- player save data

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

This separation has helped clean up the GUI and move repeated combat logic into dedicated systems where it belongs.

## Recent Improvements

Some of the more recent improvements to the project include:

- cleaner GUI state handling
- smoother transitions between menu, hub, shop, and combat
- reduced Tkinter flicker during character creation
- reduced shop flicker by updating values directly instead of rerendering the full screen
- improved handling for returning from the shop back to the hub
- continued cleanup of combat and interface responsibilities

These updates helped the game feel more stable and made the UI behavior more consistent across systems.

## What I Learned

This project has helped me practice:

- structuring a multi-file Python project
- working with Tkinter for GUI development
- managing game state in an event-driven application
- reading and writing JSON data
- designing data-driven combat systems
- separating UI logic from combat logic
- building progression systems
- debugging interactions across multiple files
- improving code organization and readability
- refactoring as a project grows

It also reinforced the importance of patterns like:

load → modify → save

and helped me understand how quickly a project can become harder to manage if systems are not separated well.

## Current Status

The project is still a work in progress, but it now has a much more complete gameplay loop than it did earlier.

Current playable flow includes:

- create or load a character
- customize starting stats
- enter combat
- fight enemies through the GUI
- gain gold and XP
- level up
- choose new moves
- return to the hub
- visit the shop
- continue into the next encounter

## Project Growth Record

This project started off much smaller and way simpler than what it turned into. Early on, it was mostly just me trying to get the core idea working. The focus was on basic combat, basic player and enemy interaction, and understanding how to make the game function at all. At that stage, the project felt more like a testbed for ideas than a full game.

Over time, it grew into something much more structured. Instead of keeping everything tightly packed together, the project gradually became split across multiple files with clearer responsibilities. Combat logic, save and load handling, player behavior, status effects, enemy generation, and GUI flow all became more organized. That alone made a huge difference because it stopped the project from feeling like one giant mess of code.

One of the biggest shifts was moving further into Tkinter and making the game feel like an actual application instead of just a script running logic in the background. The project now has a real menu flow, character creation, combat menus, attack selection, hub navigation, a shop, level-up choices, and a game-over state. Getting all of those states to work together took a lot more thought than I expected, especially when it came to hiding, restoring, and updating UI correctly.

Character creation became one of the first places where the project started to feel more polished. Instead of just making a default player and moving on, I added stat allocation and naming. Later, I improved that flow again by fixing how the UI updated so it no longer rebuilt the full character creation screen every time a stat changed. That was a good example of the project moving from “working” to “working better.”

Combat also grew a lot. It stopped being just a basic attack exchange and became move-based, with different effects like damage, healing, buffs, drain effects, and statuses. Using JSON for move data made the whole system feel much more expandable. The same thing happened with enemies. Instead of hardcoding encounters in a simple way, enemies became data-driven too, with scaling stats, weighted spawn chances, and reward values.

Progression became much stronger as the game improved. Adding XP, leveling, move learning, gold rewards, and a hub between encounters made the game loop feel more complete. Later, the shop pushed that even further because now gold actually had purpose. Potions and stat upgrades gave the player something to spend rewards on, which made fights feel more meaningful outside of just surviving the next one.

A big part of the growth of this project was not just adding features, but learning how to clean things up after the features were added. There were a lot of moments where something technically worked, but the code or the UI flow was clunky. That happened with combat turn handling, state transitions, shop rendering, and especially Tkinter flickering on Windows. Fixing those kinds of issues made the project feel more stable and also showed me how much I had improved compared to when I first started it.

One thing I’m proud of is that I kept building on it instead of stopping once it became complicated. The project now has a real gameplay loop and a much stronger foundation than it did at the start. It went from a small experiment into something that actually feels like a game project with direction. Even outside of balance changes, there is a clear record of improvement in both the code and the design thinking behind it.

Looking back, the biggest progress was not just in the amount of code, but in how I think about building software. I got better at separating systems, reworking weak parts instead of ignoring them, debugging across multiple files, and recognizing when something should be updated in place instead of rerendered from scratch. This project is a good marker of how much I improved just by continuing to work through problems and clean things up as I went.

The current focus is less on adding huge new systems and more on:

- stabilizing the game loop
- improving balance
- cleaning up the GUI
- refining progression
- polishing combat behavior
- improving readability and maintainability