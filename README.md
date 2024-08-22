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

## Demo

<video width="600" src="https://github.com/user-attachments/assets/e42de9df-d698-4426-b750-63878b69f55d">
</video>

## Setup

1. Create a Project in the Google Cloud Console and download the JSON key file. 

2. Create a folder named `documents` for storing the PDF files and another named `pdf_embeddings` in the root directory for storing the indexed documents.

3. Copy the contents of the `.env.example` file to a `.env` file and set the environment variables.

4. Create the tables in the database by running the following commands:

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Add your documents to the `Documents` table using the shell.

6. Index the documents you have added using the command:

   ```sh
   python manage.py index
   ```

## Installation

1. Clone the Repository

   ```sh
   git clone https://github.com/nigelmj/marine-chat
   cd marine-chat
   ```

2. Install Dependencies

   ```sh
   pip install -r requirements.txt
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
