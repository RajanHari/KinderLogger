# KinderLogger
An AI Assistant with RAG and FastAPI



KinderLogger is an AI-powered assistant designed to help parents stay informed about their child’s daily school activities. The system allows teachers to record audio updates about students, which are then processed, moderated, and stored in a searchable format. Parents can interact with the system by asking questions, and the AI retrieves relevant information from the stored updates.



## Features

- **AI-Powered Retrieval:** Parents can ask questions, and the assistant searches stored teacher updates to provide relevant answers.
- **Content Moderation:** Uses OpenAI's Moderation API to ensure safety and appropriateness of content during both upload and response phases.
- **FastAPI Backend:** Handles API requests efficiently with an asynchronous, lightweight framework.
- **OpenAI Assistant Integration:** Manages conversations using OpenAI’s Assistant API.
- **Document Handling:** Teacher updates are uploaded, processed, and stored in a vector database for efficient search.



## Installation
Clone the repository:

```bash
https://github.com/RajanHari/KinderLogger.git
```

and install dependencies:

```bash
pip install -r requirements.txt
```
