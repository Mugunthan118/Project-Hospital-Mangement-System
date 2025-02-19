import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk

# Database Connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mukund200@',
    database='hospital_management'
)
cursor = conn.cursor()

# Create Table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(20),
    disease VARCHAR(100)
)''')
conn.commit()

# GUI Setup
root = Tk()
root.title("Hospital Management System")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

frame = Frame(root, padx=20, pady=20, bg="#ffffff")
frame.pack(pady=20)

Label(frame, text="Patient Name", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky=W)
name_entry = Entry(frame, width=30)
name_entry.grid(row=0, column=1, pady=5)

Label(frame, text="Age", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky=W)
age_entry = Entry(frame, width=30)
age_entry.grid(row=1, column=1, pady=5)

Label(frame, text="Gender", font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky=W)
gender_var = StringVar(value="Male")  # Default selection

male_rb = Radiobutton(frame, text="Male", variable=gender_var, value="Male", font=("Arial", 10))
female_rb = Radiobutton(frame, text="Female", variable=gender_var, value="Female", font=("Arial", 10))

male_rb.grid(row=2, column=1, sticky=W)
female_rb.grid(row=2, column=1, sticky=E)

Label(frame, text="Contact", font=("Arial", 12)).grid(row=3, column=0, pady=5, sticky=W)
contact_entry = Entry(frame, width=30)
contact_entry.grid(row=3, column=1, pady=5)

Label(frame, text="Disease", font=("Arial", 12)).grid(row=4, column=0, pady=5, sticky=W)
disease_entry = Entry(frame, width=30)
disease_entry.grid(row=4, column=1, pady=5)

# Function to Add Patient
def add_patient():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get()
    contact = contact_entry.get().strip()
    disease = disease_entry.get().strip()
    
    # Input Validations
    if not name or not age or not gender or not contact or not disease:
        messagebox.showwarning("Error", "All fields are required")
        return
    
    if not age.isdigit() or int(age) <= 0:
        messagebox.showwarning("Error", "Invalid age. Enter a positive number.")
        return
    
    if not contact.isdigit() or len(contact) < 10:
        messagebox.showwarning("Error", "Invalid contact number. Enter at least 10 digits.")
        return
    
    # Insert into Database
    try:
        cursor.execute("INSERT INTO patients (name, age, gender, contact, disease) VALUES (%s, %s, %s, %s, %s)",
                       (name, int(age), gender, contact, disease))
        conn.commit()
        messagebox.showinfo("Success", "Patient Added Successfully")
        clear_fields()
        view_patients()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {str(e)}")

# Function to Clear Fields
def clear_fields():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_var.set("Male")  # Reset radio button selection
    contact_entry.delete(0, END)
    disease_entry.delete(0, END)

# Function to View Patients
def view_patients():
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    
    # Clear Table
    for row in tree.get_children():
        tree.delete(row)
    
    # Insert Data into Treeview
    for row in rows:
        tree.insert("", END, values=row)

# Buttons
btn_frame = Frame(root, bg="#ffffff")
btn_frame.pack()

Button(btn_frame, text="Add Patient", command=add_patient, font=("Arial", 12), bg="#4caf50", fg="white", padx=10).grid(row=0, column=0, padx=10, pady=10)
Button(btn_frame, text="View Patients", command=view_patients, font=("Arial", 12), bg="#2196f3", fg="white", padx=10).grid(row=0, column=1, padx=10, pady=10)

# Patient List Table
tree_frame = Frame(root)
tree_frame.pack(pady=10)

columns = ("ID", "Name", "Age", "Gender", "Contact", "Disease")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack()

# Load Data Initially
view_patients()

# Close connection when closing the app
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
