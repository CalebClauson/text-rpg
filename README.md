# Text RPG (Python + Tkinter)

##WIP - Currently not fully functional

## Overview

This is a simple text based RPG I developed using Python and Tkinter as I continue learning how to build more structured applications.

The game allows the player to engage in turn based combat through a graphical interface while using JSON files to store game data such as enemies, items, and player saves.

## Purpose

This project was created to move beyond basic scripts and start building a more complete application with multiple files, systems, and a GUI.

It focuses on practicing game logic, state management, and working with external data while keeping the project organized and scalable.

## Features

### GUI Combat System

The game uses a Tkinter interface instead of the console, allowing the player to interact with the game using buttons.

Combat actions such as attack, heal, run, and viewing inventory are handled through the GUI.

### Enemy Generation

Enemies are dynamically generated from a JSON file, allowing for easy expansion without modifying the core code.

Example:

Goblin  
Orc  
Skeleton

### Inventory System

The player inventory stores item IDs which are linked to data in a JSON file.

This allows items to have different effects without hardcoding logic.

Example:

Potion  
Sword

### Item Usage

Items such as potions can be used during combat to restore health.

The system is designed so new item types can be added easily through JSON.

### Save and Load System

Player data such as health, inventory, and gold is stored in a JSON file.

This allows progress to persist between application runs.

## What I Learned

This project helped me practice:

* Structuring a multi file Python project
* Working with Tkinter for GUI development
* Managing game state without using blocking loops
* Reading and writing JSON data
* Separating data from logic
* Handling user interaction through event driven programming
* Improving code organization and readability

It also helped reinforce the pattern of:

```text
load → modify → save