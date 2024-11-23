# College Support Chatbot

A Python-based chatbot designed to assist college students and staff with common queries. The chatbot uses machine learning for intent classification and features a graphical user interface (GUI) built with Tkinter.

---

## Features

- **Natural Language Processing**: Understands and responds to user queries using intent classification.
- **GUI Interface**: A Tkinter-based interface with tabs for chatbot interaction and tabular data display.
- **Custom Responses**: Responds to various intents such as greetings, goodbyes, and more.
- **Hyperlink Support**: Recognizes and opens URLs in chatbot responses.
- **Dynamic Table View**: Displays tabular data stored in JSON format.

---

## Technologies Used

- **Python**: Programming language.
- **Tkinter**: For creating a user-friendly graphical interface.
- **NLTK**: Natural Language Toolkit for tokenizing and preprocessing text.
- **Scikit-learn**: Used for intent classification with TF-IDF and Support Vector Classifier (SVC).
- **JSON**: Data format for storing intents and table data.

---
## **Project Setup**

### **Prerequisites**

1. **Python 3.x** installed on your system.
2. Required Python libraries:
   ```bash
   pip install nltk scikit-learn
3. **Download the necessary NLTK data**

   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('wordnet')
   
## **How to Run**

1. Ensure you have `intents.json` in the project directory.
2. Run the chatbot application:
   ```bash
   python chatbot.py

## **Project Structure**

```plaintext
├── chatbot.py          # Main application script
├── intents.json        # Contains chatbot intents and responses
├── table.json          # JSON data for table display
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignored files and directories
├── README.md           # Project description and instructions







