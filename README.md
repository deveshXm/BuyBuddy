# E-Commerce Bot Documentation
The Ecommerce Chatbot is a Python application that utilizes the ChatGPT language model to provide users with information and assistance related to online shopping and e-commerce. It is designed to engage in natural language conversations and help users with various e-commerce-related queries, such as finding products, making purchase recommendations, answering shopping-related questions, and more. This documentation outlines how to set up, configure, and use the Ecommerce Chatbot.
## Table of Contents
### 1. [Introduction](#introduction)
### 2. [Installation](#installation)
### 3. [Configuration](#configuration)
### 4. [Usage](#usage)
### 5. [Contributions](#contributions)
## Introduction
The Ecommerce Chatbot is a conversational AI application built using the ChatGPT language model developed by OpenAI. Its primary purpose is to assist users with e-commerce-related inquiries and engage in meaningful conversations to provide shopping recommendations, tips, and information.
### Features
- Natural Language Understanding: The bot is trained to understand and respond to a wide range of e-commerce and shopping-related queries in natural language.

- Product Recommendations: The bot can suggest products based on user preferences, search queries, or browsing history.

- Shopping Assistance: Users can ask for assistance with making purchases, finding the best deals, and tracking orders.

- Product Information: The bot can provide detailed information about products, including specifications, prices, and customer reviews.

- Shopping Tips: Users can inquire about shopping tips, discount codes, and online shopping best practices.

## Installation
### Prerequisites
- Python 3.6 or later
- OpenAI GPT-3 API Key (Sign up on the OpenAI website to obtain an API key)
- Textbase - Textbase is a framework for building chatbots using NLP and ML.
- Poetry (you might have to install [Poetry]('https://python-poetry.org/docs/#installing-with-the-official-installer') first).

### Installation Steps

#### 1. Clone the repository from GitHub:
```
git clone https://github.com/deveshXm/E-Commerce-Chatbot.git
poetry shell
poetry install
```

#### 2. Navigate to the project directory:
```
cd travel-bot
```

#### 3. Install Dependencies
```
poetry shell
poetry install
```
## Configuration

Before running the Travel Bot, you need to configure the API key for the OpenAI GPT-3 API, Airtable Key, Rapid API Key

Replace the following with API Keys in .env

```
OPENAI_API_KEY="openai_api_key"
RAPID_API_KEY="rapid_api_key"
```

## Usage

### Running the Bot:
```
poetry run python textbase/textbase_cli.py test main.py
```
 Now go to http://localhost:4000 and start chatting with your bot! The bot will automatically reload when you change the code.

### User Interactions
Engage in natural language conversations with the bot. For example:

- "I want to buy a shaving creamm?"
## Contributions
Contributions are welcome! Please open an issue or a pull request.


