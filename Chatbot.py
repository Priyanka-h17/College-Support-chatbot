import json
import nltk
import random
import re
import webbrowser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('wordnet')

# Load intents from the external JSON file
def load_intents(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        if 'intents' not in data:
            raise ValueError("JSON file must contain 'intents' key.")
        for intent in data['intents']:
            if not all(k in intent for k in ('tag', 'patterns', 'responses')):
                raise ValueError("Each intent must contain 'tag', 'patterns', and 'responses' keys.")
        print(f"Loaded {len(data['intents'])} intents.")
        return data
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {filename} is not a valid JSON file.")
        return {}
    except ValueError as e:
        print(f"Error in JSON structure: {e}")
        return {}

# Load JSON data for table display
def load_table_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        if 'table' not in data:
            raise ValueError("JSON file must contain 'table' key.")
        if not all(isinstance(entry, dict) for entry in data['table']):
            raise ValueError("Each entry in 'table' must be a dictionary.")
        print(f"Loaded table with {len(data['table'])} rows.")
        return data.get('table', [])
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {filename} is not a valid JSON file.")
        return []
    except ValueError as e:
        print(f"Error in JSON structure: {e}")
        return []

# Define preprocessing functions
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence.lower())
    return sentence_words

def train_classifier(sentences, labels):
    # Initialize TfidfVectorizer with custom tokenizer
    vectorizer = TfidfVectorizer(tokenizer=lambda text: nltk.word_tokenize(text.lower()))
    X = vectorizer.fit_transform(sentences).toarray()

    # Encode labels
    lb = LabelEncoder()
    y = lb.fit_transform(labels)
    
    # Train a Support Vector Classifier (SVC)
    model = SVC(kernel='linear', probability=True)
    model.fit(X, y)
    
    return model, vectorizer, lb

# Define response functions
def classify(sentence, model, vectorizer, lb):
    input_data = vectorizer.transform([sentence]).toarray()
    prediction = model.predict(input_data)[0]
    intent = lb.inverse_transform([prediction])[0]
    print(f"Classified Intent: {intent}")  # Debugging print
    return intent

def response(sentence):
    intent = classify(sentence, model, vectorizer, lb)
    
    for i in intents['intents']:
        if i['tag'] == intent:
            print(f"Selected Responses for {intent}: {i['responses']}")  # Debugging print
            if i['responses']:
                return random.choice(i['responses'])
            else:
                return "I don't have a response for this intent."
    
    return "Sorry, I don't understand!"

# Define GUI using Tkinter
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NCET(CSE) Chatbot")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create chatbot tab
        self.chat_frame = tk.Frame(self.notebook)
        self.notebook.add(self.chat_frame, text="Chatbot")

        # Create table tab
        self.table_frame = tk.Frame(self.notebook)
        self.notebook.add(self.table_frame, text="Table Data")

        self.create_chat_ui()
        self.create_table_ui()

    def create_chat_ui(self):
        # Create chat log area
        self.chat_log = tk.Text(self.chat_frame, bd=0, bg="white", font=("Arial", 12))
        self.chat_log.config(state=tk.DISABLED)

        # Create scrollbar for chat log
        self.scrollbar = tk.Scrollbar(self.chat_frame, command=self.chat_log.yview)
        self.chat_log['yscrollcommand'] = self.scrollbar.set

        # Create send button
        self.send_button = tk.Button(self.chat_frame, font=("Verdana", 12, 'bold'), text="Send", width=12, height=2,
                                     bd=1, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                                     command=self.send)

        # Create entry box for user input
        self.entry_box = tk.Text(self.chat_frame, bd=1, bg="white", font=("Arial", 12), wrap=tk.WORD, height=3)

        # Place widgets using grid
        self.chat_log.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.scrollbar.grid(row=0, column=2, sticky='ns')
        self.entry_box.grid(row=1, column=0, sticky='nsew', padx=(10, 5), pady=(5, 0))
        self.send_button.grid(row=1, column=1, sticky='se', padx=(0, 10), pady=(5, 10))

        # Configure grid weights for resizing
        self.chat_frame.grid_rowconfigure(0, weight=1)  # Chat log row
        self.chat_frame.grid_rowconfigure(1, weight=0)  # Entry box and button row
        self.chat_frame.grid_columnconfigure(0, weight=1)  # Expand entry box and chat log
        self.chat_frame.grid_columnconfigure(1, weight=0)  # Button column
        self.chat_frame.grid_columnconfigure(2, weight=0)  # Scrollbar

        # Bind URL tags to open links
        self.chat_log.tag_bind("url", "<Button-1>", self.open_link)

    def create_table_ui(self):
        # Load and display table data
        data = load_table_data("C:/Users/Priyanka H/Desktop/College Chatbot/table.json")

        if not data:
            print("No table data to display.")
            return

        # Create table view using Treeview
        self.table = ttk.Treeview(self.table_frame, columns=list(data[0].keys()), show='headings')

        # Define columns
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, anchor='w')

        # Insert data into table
        for row in data:
            self.table.insert('', 'end', values=list(row.values()))

        self.table.pack(fill=tk.BOTH, expand=True)

    def send(self, event=None):
        msg = self.entry_box.get("1.0", 'end-1c').strip()
        self.entry_box.delete("0.0", tk.END)
        
        if msg != '':
            self.chat_log.config(state=tk.NORMAL)
            self.chat_log.insert(tk.END, "You: " + msg + '\n\n')
            self.chat_log.config(foreground="#442265", font=("Verdana", 12))
            
            res = response(msg)
            if isinstance(res, dict) and 'table' in res:
                # Handle table format response
                self.display_table(res['table'])
                res_str = "Table displayed above."
            else:
                # Handle regular text response
                res_str = self.add_links_to_text(str(res))
            
            self.chat_log.insert(tk.END, "CSE Bot: " + res_str + '\n\n')
            self.chat_log.insert(tk.END, "\n")  # Add an extra blank line below the bot's response
                
            self.chat_log.config(state=tk.DISABLED)
            self.chat_log.yview(tk.END)

    def add_links_to_text(self, text):
        # Define URL pattern
        link_pattern = re.compile(r'(https?://\S+)')
        matches = link_pattern.findall(text)
        
        if not matches:
            return text
        
        # Create a new text widget content with URL tags
        new_text = text
        for match in matches:
            # Replace the URL with a placeholder format for tagging
            new_text = new_text.replace(match, f'{{{{ {match} }}}}')
        
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.delete("1.0", tk.END)
        self.chat_log.insert(tk.END, new_text)
        
        # Add a tag for each URL
        for match in matches:
            start_idx = self.chat_log.search(f'{{{{ {match} }}}}', '1.0', tk.END)
            end_idx = f'{start_idx}+{len(match)+4}c'
            self.chat_log.tag_add("url", start_idx, end_idx)
        
        self.chat_log.config(state=tk.DISABLED)
        return new_text

    def open_link(self, event):
        try:
            index = self.chat_log.index(f"@{event.x},{event.y}")
            tag_ranges = self.chat_log.tag_ranges("url")
            for i in range(0, len(tag_ranges), 4):
                start = tag_ranges[i]
                end = tag_ranges[i+1]
                if self.chat_log.compare(start, '<=', index) and self.chat_log.compare(index, '<=', end):
                    url = self.chat_log.get(start, end).strip('{} ')
                    if url:
                        webbrowser.open(url)
                    return
        except Exception as e:
            print(f"Failed to open link: {e}")

    def display_table(self, table_data):
        # Clear any existing table view
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Create table view using Treeview
        self.table = ttk.Treeview(self.table_frame, columns=list(table_data[0].keys()), show='headings')

        # Define columns
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, anchor='w')

        # Insert data into table
        for row in table_data:
            self.table.insert('', 'end', values=list(row.values()))

        self.table.pack(fill=tk.BOTH, expand=True)

if __name__== "__main__":
    intents = load_intents("C:/Users/Priyanka H/Desktop/College Chatbot/intents .json")
    
    if not intents:
        print("Failed to load intents. Exiting...")
        exit()

    # Prepare training data
    sentences = []
    labels = []

    for intent in intents['intents']:
        for pattern in intent["patterns"]:
            sentences.append(pattern)
            labels.append(intent["tag"])

    # Check if sentences and labels have the same length
    if len(sentences) != len(labels):
        print(f"Error: Number of sentences ({len(sentences)}) does not match number of labels ({len(labels)}). Exiting...")
        exit()

    print("Sentences:", sentences[:10])  # Debugging print - show only first 10
    print("Labels:", labels[:10])  # Debugging print - show only first 10

    model, vectorizer, lb = train_classifier(sentences, labels)

    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
