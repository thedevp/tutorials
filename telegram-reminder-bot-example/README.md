# Python Telegram Bot Tutorial

## Overview

This repository contains a Python script for creating a Telegram bot, as detailed in my [Medium article](link-to-your-medium-article). This bot is built using the `python-telegram-bot` library and is designed to send reminders based on tasks you add.

## Prerequisites

- Python 3
- Telegram account

## Installation

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/thedevp/tutorials.git
    ```
2. **Set up python virtual environment**

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