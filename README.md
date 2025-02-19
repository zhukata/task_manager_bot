# Task Manager Bot

Task Manager Bot is a Telegram bot designed to retrieve and display data from a Django application via its API. This bot facilitates seamless interaction with your task management system directly through Telegram.

## Features

- **Task Retrieval**: Fetch and display tasks assigned to the user.
- **Task Updates**: Receive notifications on task status changes.
- **User Authentication**: Secure access ensuring users can only view their respective tasks.

## Prerequisites

Before setting up the bot, ensure you have the following installed:

- **Python**: Version 3.9 or higher.
- **Poetry**: For dependency management and packaging.
- **Docker** (optional): For containerized deployment.

## Installation

Follow the steps below to set up and run the Task Manager Bot:

### 1. Clone the Repository

```bash
git clone https://github.com/zhukata/task_manager_bot.git
cd task_manager_bot
```

### 2. Install Dependencies
Using Poetry, install the required dependencies:

```bash
poetry install
```

### 3. Configuration
Create a .env file in the project root directory and add the following environment variables:

```
TOKEN="your_telegram_bot_token"
API_URL = "http://task-manager:8000/api/"
DATABASE_URL_BOT = "postgresql+asyncpg://user:password@postgres:5432/db_name"
DB_LITE_URL = 'sqlite+aiosqlite:///my_base.db' (in case you don't use postgres)
```
### 4. Running the Bot

```
make dev
```


## Usage
Once running, users can interact with the bot on Telegram to:

View their tasks.
Receive updates on task statuses.
Manage tasks as permitted by the Django application.