# Conversational AI Chatbot

This project consists of a conversational AI chatbot built using the OpenAI GPT-3.5 model. The chatbot allows users to engage in text-based conversations with various personalities and manage conversations with saved data.

## Getting Started

### Prerequisites

Before running the project, ensure you have the following:

- Python 3.x installed
- An OpenAI API key
- `config.json` file containing your API key
- Access to `gpt-3.5-turbo` model from OpenAI

### Installation

1. Clone this repository to your local machine.

2. Navigate to the project directory.

3. Install the required Python packages using `pip`.

```bash
pip install -r requirements.txt
``` 

4. Create a `config.json` file in the project directory and add your OpenAI API key:

```json
{
    "api_keys": {
        "open_ai": "your_api_key_here"
    }
}
```

5. Add any desired new personalities into the personalities.json file:

```json
{
    "personality_name": {
            "starting_message": "personality opening message",
            "characteristic": "personality description"
    }
}
```

6. ```python conversation_manager.py``` to run the project.

You will be prompted to choose between continuing a conversation or starting a new one.

Selecting a Personality
If starting a new conversation, you can select a personality from the available options.

Continuing a Conversation
If continuing a conversation, you can choose from the available conversations to resume.

Interacting with the Chatbot
Once in a conversation, you can interact with the chatbot by entering your messages. To end the conversation, simply type "exit".

Saved Conversations
Conversations are saved in the conversations directory. Each conversation is stored as a JSON file with meta-information and messages.

