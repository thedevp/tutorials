# Python Telegram Bot Tutorial

## Overview

This repository contains a Python script for creating a Telegram bot, as detailed in my [Medium article](https://medium.com/@thedevpw/creating-a-telegram-reminder-bot-with-python-a280958b574b). This bot is built using the `python-telegram-bot` library and is designed to send reminders based on tasks you add.

## Prerequisites

- Python 3
- Telegram account

## Installation

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/thedevp/tutorials.git telegram-reminder-bot-example
    ```
2. **Set up python virtual environment**
    
    Make sure you navigate to the project directory before running the following commands.
    ```
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install Dependencies**
    
    - Install at once
        ```
        pip install -r requirements.txt
        ```
    - Manually
        ```
        pip install python-telegram-bot
        pip install "python-telegram-bot[job-queue]"
        ```