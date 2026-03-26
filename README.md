## Text RPG (Python + Tkinter)

WIP - Currently in active development

## Overview

This is a text based RPG built with Python and Tkinter as I continue learning how to create more structured, interactive, and data driven applications.

The game uses a graphical interface for turn based combat and relies on JSON files for storing moves, enemies, items, and save data. The project has gradually grown from a simple combat idea into a small multi file RPG with progression, enemy generation, save/load support, and a cleaner GUI driven flow.

## Purpose

This project was created to move beyond basic scripts and start building a more complete application with multiple files, connected systems, reusable logic, and a GUI.

It focuses on practicing:

- game logic
- state management
- event driven programming
- GUI design with Tkinter
- JSON based data handling
- debugging across multiple files
- separating interface code from gameplay logic

A major goal has been learning how to organize a project so it stays readable as more systems are added.

## Current Features

## GUI Based Game Flow

The game uses a Tkinter interface instead of the console, allowing the player to navigate the game through menus, buttons, and different game states.

Current GUI flow includes:

- main menu
- character creation
- combat screen
- attack selection menu
- hub screen between encounters
- level up screen
- game over screen

The GUI has been cleaned up so it handles interface flow while combat logic is increasingly handled in separate system files.

## Character Creation

The game includes a character creation screen where the player can:

- choose a name
- distribute stat points
- customize starting attack
- customize starting speed
- customize starting armor

This helps make the start of a run feel more interactive and gives the player some control over how their character begins.

## Combat System

The core gameplay loop is built around turn based combat.

Players can:

- attack using learned moves
- heal with items
- check their backpack
- attempt to run from combat

Combat uses move data loaded from JSON, making it easier to expand behavior without hardcoding every move directly into the interface.

## Move Based Combat

Moves are selected through a dedicated attack menu and support multiple effect types.

Current supported move behavior includes:

- damage
- heal
- buff
- drain
- status effects

This allows different moves to feel distinct while keeping the combat system data driven and easier to expand.

## Status Effects

The game supports status effects that can be applied and processed over time.

Current status related systems include:

- applying status effects through moves
- processing status effects at the start of turns
- updating status durations during combat

This gives combat more variety and adds flexibility for future move design.

## Enemy Generation

Enemies are generated from JSON data rather than hardcoded directly in combat logic.

Current enemy generation supports:

- loading enemies from JSON
- scaling enemy stats by player level
- weighted enemy selection for encounter variety

This makes balancing easier and allows new enemies to be added without major code changes.

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

## Reward and Progression System

Defeating enemies grants rewards that feed directly into the game loop.

Current combat rewards include:

- experience points
- gold

This creates a basic progression loop where combat leads to stronger characters and more move options over time.

## Level System

The player has a level based progression system tied to earned experience.

Leveling up currently includes:

- increased max health
- increased attack
- full heal on level up
- increased XP requirement for future levels

This helps the game feel more progressive and gives fights a sense of growth over time.

## Level Up Move Choices

When the player levels up, the game can offer random move choices from the move pool.

This system currently supports:

- pulling random moves from available moves
- preventing duplicate move choices from already learned moves
- learning new moves on level up
- move cap handling in the GUI

This was one of the bigger recent additions and helps the project feel more RPG like.

## Inventory System

The inventory stores item IDs tied to JSON item data.

This keeps item handling simple while supporting future expansion.

The system currently supports:

- storing items in inventory
- checking backpack contents
- using healing items in combat

## Save and Load System

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

The project also includes a start menu flow for loading an existing player or creating a new one.

## Data Driven Design

A major goal of the project is to separate data from logic wherever possible.

Game content is stored in JSON files, including:

- enemies
- moves
- items
- player save data

This makes the project easier to expand and helps keep balance changes separate from the main gameplay code.

## Project Structure

The project is split across multiple files so responsibilities are separated more clearly.

Current structure includes files such as:

- `gui.py` for menus, button rendering, and interface state flow
- `systems/combat.py` for encounter flow, turn resolution, and combat helpers
- `systems/enemy.py` for enemy behavior and stats
- `systems/status_effects.py` for applying and updating statuses
- `player.py` for player data, progression, inventory, and move learning
- `save_load.py` for save and load handling

This separation has helped clean up the GUI and move repeated combat logic into the combat system where it belongs.

## What I Learned

This project has helped me practice:

- structuring a multi file Python project
- working with Tkinter for GUI development
- managing game state in an event driven application
- reading and writing JSON data
- designing data driven combat systems
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
- enter combat
- fight enemies through the GUI
- gain gold and XP
- level up
- choose new moves
- return to the hub
- continue into the next encounter

The current focus is less on adding huge new systems and more on:

- stabilizing the game loop
- improving balance
- cleaning up the GUI
- refining progression
- polishing combat behavior
- improving readability and maintainability