import logging
import json
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, ContextTypes
from credentials import TOKEN, CHAT_ID

"""
Make sure you have filled in the credentials.py file with your own bot token and chat id.
If you don't know how to get the chat id, you can run the get_id.py script.
"""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load tasks from JSON file
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save tasks to JSON file
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

# Add task command
async def add_task(update: Update, context: CallbackContext):
    try:
        task = context.args[0]
        due_date = datetime.datetime.strptime(context.args[1], "%Y-%m-%d").date()
        tasks = load_tasks()
        tasks[task] = str(due_date)
        save_tasks(tasks)
        await update.message.reply_text(f"Task '{task}' added for {due_date}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /add <task_name> <due_date YYYY-MM-DD>")

# Delete task command
async def delete_task(update: Update, context: CallbackContext):
    try:
        task_to_delete = context.args[0]
        due_date_to_delete = datetime.datetime.strptime(context.args[1], "%Y-%m-%d").date()
        tasks = load_tasks()

        # Check if the task with the specified due date exists
        if task_to_delete in tasks and tasks[task_to_delete] == str(due_date_to_delete):
            del tasks[task_to_delete]
            save_tasks(tasks)
            await update.message.reply_text(f"Task '{task_to_delete}' for {due_date_to_delete} deleted.")
        else:
            await update.message.reply_text(f"No task found with name '{task_to_delete}' for {due_date_to_delete}.")
    
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /delete <task_name> <due_date YYYY-MM-DD>")

# List all tasks command
async def list_tasks(update: Update, context: CallbackContext):
    tasks = load_tasks()
    message = "All Tasks:\n"

    if tasks:
        for task, due_date in tasks.items():
            message += f"- {task}: due {due_date}\n"
    else:
        message += "No tasks available."

    await update.message.reply_text(message)

# Daily reminder job
async def daily_reminder(context: CallbackContext):
    tasks = load_tasks()
    today = datetime.date.today()
    message = "Tasks Reminder:\n"
    has_task = False

    for task, due_date in list(tasks.items()):
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        if due_date < today:
            del tasks[task]  # Delete past tasks
        else:
            message += f"- {task}: due {due_date}\n"
            has_task = True

    save_tasks(tasks)

    if has_task:
        # Accessing chat_id from the job context
        chat_id = context.job.chat_id
        await context.bot.send_message(chat_id=chat_id, text=message)
        logging.info("Daily reminder sent.")
    else:
        logging.info("No daily reminder sent.")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    Hi! I'm a reminder bot. I can help you remember your tasks.
    Commands:
    /add <task_name> <due_date YYYY-MM-DD>
    /delete <task_name> <due_date YYYY-MM-DD>
    /list

    Example:
    /add Homework 2020-12-31
    /delete Homework 2020-12-31

    The bot will send you a daily reminder of your tasks.
    """
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


if __name__ == '__main__':
    token = TOKEN
    application = ApplicationBuilder().token(token).build()

    # Handlers
    start_handler = CommandHandler('start', start)
    add_task_handler = CommandHandler('add', add_task)
    delete_task_handler = CommandHandler('delete', delete_task)
    list_tasks_handler = CommandHandler('list', list_tasks)

    # Add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(add_task_handler)
    application.add_handler(delete_task_handler)
    application.add_handler(list_tasks_handler)

    # Add daily reminder job
    job_queue = application.job_queue
    chat_id = CHAT_ID
    # job_queue.run_daily(daily_reminder, time=datetime.time(hour=8), chat_id=chat_id) 

    # Testing purpose, send the messge after 1 minute
    job_queue.run_once(daily_reminder, when=60, chat_id=chat_id) 
    
    application.run_polling()