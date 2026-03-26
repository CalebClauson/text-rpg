## Text RPG (Python + Tkinter)

WIP - Currently in active development

## Overview

This is a text based RPG I developed using Python and Tkinter as I continue learning how to build more structured and interactive applications.

The game uses a graphical interface for turn based combat while relying on JSON files to store game data such as enemies, items, moves, and player save data.

## Purpose

This project was created to move beyond basic scripts and start building a more complete application with multiple files, connected systems, and a GUI.

It focuses on practicing game logic, state management, event driven programming, and external data handling while keeping the project organized and easier to expand as new systems are added.

## Current Features

## GUI Combat System

The game uses a Tkinter interface instead of the console, allowing the player to interact with the game using buttons and menus.

Combat actions such as attacking, healing, opening the backpack, and running are handled through the GUI.

## Move Based Combat

The combat system supports move selection through a dedicated attack panel.

Moves are loaded from JSON and can have different behavior types such as:

- damage
- heal
- buff
- status

This allows combat to expand without hardcoding every move directly into the interface.

## Enemy Generation

Enemies are dynamically generated from a JSON file, allowing new enemies to be added or balanced without changing the core combat code.

Enemy stats can also scale based on the player level, which helps combat feel more progressive.

Example enemies include:

- Goblin
- Orc
- Skeleton
- Bandit
- Dragon

## Reward System

Enemies can grant rewards after battle, including:

- experience points
- gold

This creates a progression loop where defeating enemies helps the player grow stronger over time.

## Level System

The player has a level based progression system tied to experience gained from combat.

Player stats such as health and attack can increase on level up, allowing future encounters to scale with progression.

## Inventory System

The player inventory stores item IDs that connect to item data in a JSON file.

This makes it easier to manage items and add new ones later without rewriting large sections of logic.

Example items include:

- Potion
- Sword

## Item Usage

Items such as healing potions can be used during combat to restore health.

The item system is structured so additional item effects can be added later through JSON driven design.

## Status Effects

The combat system includes status effect support.

Status effects can be applied, processed at the start of turns, and updated over time, which helps make battles more varied and gives move design more flexibility.

## Save and Load System

Player data is stored in a JSON file so progress can persist between runs.

Current saved data includes things such as:

- health
- max health
- moves
- inventory
- gold
- level
- xp
- xp needed for next level

## Data Driven Design

A major goal of the project is to separate data from logic as much as possible.

Game content is stored in JSON files, including:

- enemies
- items
- player save data
- moves

This makes the project easier to expand and helps keep the core Python code cleaner.

## Project Structure

The project is split across multiple files to separate responsibilities more clearly.

Examples include:

- `gui.py` for interface behavior
- `systems/combat.py` for battle flow and combat logic
- `systems/enemy.py` for enemy behavior and stats
- `systems/status_effects.py` for status effect handling
- `player.py` for player data and progression
- `save_load.py` for save and load handling

## What I Learned

This project has helped me practice:

- structuring a multi file Python project
- working with Tkinter for GUI development
- managing game state in an event driven application
- reading and writing JSON data
- building turn based combat logic
- separating data from logic
- designing systems that are easier to expand
- debugging interactions across multiple files
- improving code organization and readability

It also helped reinforce the pattern of:

load → modify → save

## Current Status

This project is still a work in progress and not all systems are fully complete or polished yet.

The main focus right now is improving combat flow, move effects, progression systems, status effect handling, and overall stability as the project continues to grow.