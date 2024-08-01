# Marine-Chat

## Overview

Marine-Chat is a Q&A chatbot utilizing a Retrieval-Augmented Generation (RAG) workflow built with LangChain. It is designed to provide accurate and relevant answers to user queries in a maritime context.
## Features

- User Authentication: Secure login and registration for staff and administrators.
- Chatbot Integration: Conversational AI that answers queries based on maritime documents and provides clickable references.
- Document Management: PDF documents are stored and indexed for easy retrieval.

## Tech Stack

- Backend: Django
- Frontend: JavaScript
- AI/ML: Gemini 1.5, LangChain
- Vector Store: ChromaDB
- Database: SQLite3

## Installation

1. Clone the Repository

   ```sh
   git clone https://github.com/nigelmj/marine-chat
   cd marine-chat
   ```

2. Install Dependencies

   ```sh
   pip install -r requirements.txt`
   ```

3. Run Migrations

   ```sh
   python manage.py migrate
   ```

4. Start the Development Server

   ```sh
   python manage.py runserver
   ```

## Usage

- Login/Register: Access the system by logging in or creating a new account.
- Interact with Chatbot: Ask questions related to maritime documents, and the chatbot will provide responses with references.
- View Documents: Access and view documents available in the system.

## Contribution

Contributions are welcome! Please feel free to open issues or submit pull requests.
