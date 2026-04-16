import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import tkinter as tk
from tkinter import messagebox
import os

# -----------------------------
# COLORS
# -----------------------------
BG_COLOR = "#1e1e2f"
BTN_COLOR = "#4CAF50"
BTN_HOVER = "#45a049"
TEXT_COLOR = "white"

FILE_NAME = "tv_data.xlsx"

# -----------------------------
# CREATE FILE IF NOT EXISTS
# -----------------------------
def create_file():
    if not os.path.exists(FILE_NAME):
        data = pd.DataFrame({
            "Name": ["Asha","Raj","Neha","Aman","Pooja"],
            "Age": [20,22,19,21,23],
            "Gender": ["Female","Male","Female","Male","Female"],
            "Location": ["Bhopal","Delhi","Mumbai","Bhopal","Delhi"],
            "Show": ["Dance Show","Singing Show","Drama Show","Dance Show","Singing Show"],
            "Comment": ["Amazing performance","Not good","Loved it","Very entertaining","Boring show"]
        })
        data.to_excel(FILE_NAME, index=False)

# -----------------------------
# SENTIMENT FUNCTION
# -----------------------------
def get_sentiment(comment):
    analysis = TextBlob(str(comment))
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative"

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    create_file()
    try:
        data = pd.read_excel(FILE_NAME)
        data['Sentiment'] = data['Comment'].apply(get_sentiment)
        return data
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# -----------------------------
# DASHBOARD GRAPH (ALL IN ONE)
# -----------------------------
def show_graphs():
    data = load_data()

    if data is None or data.empty:
        messagebox.showerror("Error", "No data available!")
        return

    # Popularity calculation
    popularity = data.groupby('Show')['Sentiment'].value_counts().unstack().fillna(0)

    if 'Positive' not in popularity:
        popularity['Positive'] = 0
    if 'Negative' not in popularity:
        popularity['Negative'] = 0

    popularity['Score'] = popularity['Positive'] - popularity['Negative']

    # Create Dashboard
    plt.figure(figsize=(12, 8))

    # 1. Sentiment
    plt.subplot(2, 2, 1)
    data['Sentiment'].value_counts().plot(kind='bar', color=['green','red'])
    plt.title("Sentiment Analysis")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")

    # 2. Gender
    plt.subplot(2, 2, 2)
    data['Gender'].value_counts().plot(
        kind='pie',
        autopct='%1.1f%%',
        colors=['#ff9999','#66b3ff','#99ff99']
    )
    plt.title("Gender Distribution")
    plt.ylabel("")

    # 3. Location
    plt.subplot(2, 2, 3)
    data['Location'].value_counts().plot(kind='bar', color='orange')
    plt.title("Location Distribution")
    plt.xlabel("Location")
    plt.ylabel("Count")

    # 4. Popularity
    plt.subplot(2, 2, 4)
    popularity['Score'].plot(kind='bar', color='purple')
    plt.title("TV Show Popularity")
    plt.xlabel("Show")
    plt.ylabel("Score")

    plt.tight_layout()
    plt.show()

# -----------------------------
# BUTTON HOVER EFFECT
# -----------------------------
def on_enter(e):
    e.widget['background'] = BTN_HOVER

def on_leave(e):
    e.widget['background'] = BTN_COLOR

# -----------------------------
# ADD ENTRY
# -----------------------------
def add_entry():
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    location = entry_location.get()
    show = entry_show.get()
    comment = entry_comment.get()

    if not name or not comment:
        messagebox.showerror("Error", "Name and Comment required!")
        return

    new_data = pd.DataFrame([[name, age, gender, location, show, comment]],
                            columns=['Name','Age','Gender','Location','Show','Comment'])

    old_data = load_data()
    updated = pd.concat([old_data.drop(columns=['Sentiment'], errors='ignore'), new_data], ignore_index=True)

    updated.to_excel(FILE_NAME, index=False)

    messagebox.showinfo("Success", "Entry Added!")

# -----------------------------
# ADMIN PANEL
# -----------------------------
def admin_panel():
    admin = tk.Toplevel(root)
    admin.title("Admin Panel")
    admin.geometry("400x500")
    admin.configure(bg=BG_COLOR)

    global entry_name, entry_age, entry_gender, entry_location, entry_show, entry_comment

    def label(text):
        return tk.Label(admin, text=text, bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 10, "bold"))

    def entry():
        return tk.Entry(admin, width=30)

    label("Name").pack(pady=2)
    entry_name = entry()
    entry_name.pack()

    label("Age").pack(pady=2)
    entry_age = entry()
    entry_age.pack()

    label("Gender").pack(pady=2)
    entry_gender = entry()
    entry_gender.pack()

    label("Location").pack(pady=2)
    entry_location = entry()
    entry_location.pack()

    label("Show").pack(pady=2)
    entry_show = entry()
    entry_show.pack()

    label("Comment").pack(pady=2)
    entry_comment = entry()
    entry_comment.pack()

    btn_add = tk.Button(admin, text="Add Entry", bg=BTN_COLOR, fg="white", width=20, command=add_entry)
    btn_add.pack(pady=10)
    btn_add.bind("<Enter>", on_enter)
    btn_add.bind("<Leave>", on_leave)

    btn_graph = tk.Button(admin, text="View Dashboard", bg=BTN_COLOR, fg="white", width=20, command=show_graphs)
    btn_graph.pack(pady=10)
    btn_graph.bind("<Enter>", on_enter)
    btn_graph.bind("<Leave>", on_leave)

# -----------------------------
# VISITOR PANEL
# -----------------------------
def visitor_panel():
    visitor = tk.Toplevel(root)
    visitor.title("Visitor Panel")
    visitor.geometry("300x200")
    visitor.configure(bg=BG_COLOR)

    tk.Label(visitor, text="TV Show Popularity Dashboard",
             bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 12, "bold")).pack(pady=20)

    btn = tk.Button(visitor, text="Show Dashboard", bg=BTN_COLOR, fg="white", width=20, command=show_graphs)
    btn.pack()

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# -----------------------------
# MAIN WINDOW
# -----------------------------
root = tk.Tk()
root.title("TV Show Popularity System")
root.geometry("350x250")
root.configure(bg=BG_COLOR)

tk.Label(root, text="TV Show Popularity System",
         bg=BG_COLOR, fg="white", font=("Arial", 16, "bold")).pack(pady=20)

btn_admin = tk.Button(root, text="Admin Panel", bg=BTN_COLOR, fg="white", width=20, command=admin_panel)
btn_admin.pack(pady=10)
btn_admin.bind("<Enter>", on_enter)
btn_admin.bind("<Leave>", on_leave)

btn_visitor = tk.Button(root, text="Visitor Panel", bg=BTN_COLOR, fg="white", width=20, command=visitor_panel)
btn_visitor.pack(pady=10)
btn_visitor.bind("<Enter>", on_enter)
btn_visitor.bind("<Leave>", on_leave)

root.mainloop()