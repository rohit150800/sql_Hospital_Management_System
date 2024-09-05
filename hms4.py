import tkinter as tk
from tkinter import ttk
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="nandu1508",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create the patient_doctor table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS patient_doctor (
    patient_id INTEGER REFERENCES patients(id),
    doctor_id INTEGER REFERENCES doctors(id),
    PRIMARY KEY (patient_id, doctor_id)
)
""")
conn.commit()

# Functions for Patients
def add_patient():
    try:
        name = patient_name_var.get()
        age = patient_age_var.get()
        gender = patient_gender_var.get()
        dob = patient_dob_var.get()
        contact_no = patient_contact_no_var.get()
        address = patient_address_var.get()
        cur.execute("INSERT INTO patients (name, age, gender, dob, contact_no, address) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, age, gender, dob, contact_no, address))
        conn.commit()
        fetch_patients()
        fetch_patient_doctor_info()
    except Exception as e:
        print(f"Error in add_patient: {e}")
        conn.rollback()

def fetch_patients():
    try:
        cur.execute("SELECT * FROM patients")
        rows = cur.fetchall()
        for row in patient_table.get_children():
            patient_table.delete(row)
        for row in rows:
            patient_table.insert('', tk.END, values=row)
    except Exception as e:
        print(f"Error in fetch_patients: {e}")

def clear_patient_fields():
    patient_name_var.set("")
    patient_age_var.set("")
    patient_gender_var.set("")
    patient_dob_var.set("")
    patient_contact_no_var.set("")
    patient_address_var.set("")

def delete_patient():
    try:
        selected_items = patient_table.selection()
        if selected_items:
            patient_id = patient_table.item(selected_items[0])['values'][0]
            cur.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
            cur.execute("DELETE FROM patient_doctor WHERE patient_id = %s", (patient_id,))
            conn.commit()
            fetch_patients()
            fetch_patient_doctor_info()
        else:
            print("No patient selected")
    except Exception as e:
        print(f"Error in delete_patient: {e}")
        conn.rollback()

# Functions for Doctors
def add_doctor():
    try:
        name = doctor_name_var.get()
        specialization = doctor_specialization_var.get()
        contact_no = doctor_contact_no_var.get()
        cur.execute("INSERT INTO doctors (name, specialization, contact_no) VALUES (%s, %s, %s)", (name, specialization, contact_no))
        conn.commit()
        fetch_doctors()
        fetch_patient_doctor_info()
    except Exception as e:
        print(f"Error in add_doctor: {e}")
        conn.rollback()

def fetch_doctors():
    try:
        cur.execute("SELECT * FROM doctors")
        rows = cur.fetchall()
        for row in doctor_table.get_children():
            doctor_table.delete(row)
        for row in rows:
            doctor_table.insert('', tk.END, values=row)
    except Exception as e:
        print(f"Error in fetch_doctors: {e}")

def clear_doctor_fields():
    doctor_name_var.set("")
    doctor_specialization_var.set("")
    doctor_contact_no_var.set("")

def delete_doctor():
    try:
        selected_items = doctor_table.selection()
        if selected_items:
            doctor_id = doctor_table.item(selected_items[0])['values'][0]
            cur.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
            cur.execute("DELETE FROM patient_doctor WHERE doctor_id = %s", (doctor_id,))
            conn.commit()
            fetch_doctors()
            fetch_patient_doctor_info()
        else:
            print("No doctor selected")
    except Exception as e:
        print(f"Error in delete_doctor: {e}")
        conn.rollback()

# Function to Assign Doctor to Patient
def assign_doctor_to_patient():
    try:
        selected_patient = patient_table.selection()
        selected_doctor = doctor_table.selection()
        if selected_patient and selected_doctor:
            patient_id = patient_table.item(selected_patient[0])['values'][0]
            doctor_id = doctor_table.item(selected_doctor[0])['values'][0]
            cur.execute("INSERT INTO patient_doctor (patient_id, doctor_id) VALUES (%s, %s)", (patient_id, doctor_id))
            conn.commit()
            fetch_patient_doctor_info()
        else:
            print("Please select both a patient and a doctor")
    except Exception as e:
        print(f"Error in assign_doctor_to_patient: {e}")
        conn.rollback()

def fetch_patient_doctor_info():
    try:
        query = """
        SELECT patients.id, patients.name, patients.age, patients.gender, patients.dob, patients.contact_no, patients.address, 
               doctors.name AS doctor_name, doctors.specialization
        FROM patients
        LEFT JOIN patient_doctor ON patients.id = patient_doctor.patient_id
        LEFT JOIN doctors ON patient_doctor.doctor_id = doctors.id
        """
        cur.execute(query)
        rows = cur.fetchall()
        for row in patient_doctor_table.get_children():
            patient_doctor_table.delete(row)
        for row in rows:
            patient_doctor_table.insert('', tk.END, values=row)
    except Exception as e:
        print(f"Error in fetch_patient_doctor_info: {e}")

win = tk.Tk()
win.geometry("1350x700+0+0")
win.title("Hospital Management System")

title_label = tk.Label(win, text="Hospital Management System", font=("caliber", 30), border=1, relief=tk.GROOVE, bg="lavender", foreground="black")
title_label.pack(side=tk.TOP, fill=tk.X)

# Patient Details Frame
patient_frame = tk.LabelFrame(win, text="Patient Details", font=("ariel", 18, "italic"), bd=0, relief=tk.FLAT, bg="white", foreground="blue")
patient_frame.place(x=20, y=90, width=420, height=575)

# Doctor Details Frame
doctor_frame = tk.LabelFrame(win, text="Doctor Details", font=("ariel", 18, "italic"), bd=0, relief=tk.FLAT, bg="white", foreground="blue")
doctor_frame.place(x=460, y=90, width=420, height=575)

# Data Frame for Tables
data_frame = tk.Frame(win, bd=8, bg="white", relief=tk.FLAT)
data_frame.place(x=900, y=90, width=420, height=575)

# Variables for Patients
patient_name_var = tk.StringVar()
patient_age_var = tk.StringVar()
patient_gender_var = tk.StringVar()
patient_dob_var = tk.StringVar()
patient_contact_no_var = tk.StringVar()
patient_address_var = tk.StringVar()

# Variables for Doctors
doctor_name_var = tk.StringVar()
doctor_specialization_var = tk.StringVar()
doctor_contact_no_var = tk.StringVar()

# Patient Details Entry
tk.Label(patient_frame, text="Name", font=('Arial', 17), bg="white").grid(row=0, column=0, padx=2, pady=2)
tk.Entry(patient_frame, bd=2, font=('arial', 15), width=12, textvariable=patient_name_var).grid(row=0, column=1, padx=2, pady=2)

tk.Label(patient_frame, text="Age", font=('Arial', 17), bg="white").grid(row=1, column=0, padx=2, pady=2)
tk.Entry(patient_frame, bd=7, font=('arial', 17), width=17, textvariable=patient_age_var).grid(row=1, column=1, padx=2, pady=2)

tk.Label(patient_frame, text="Gender", font=('Arial', 17), bg="white").grid(row=2, column=0, padx=2, pady=2)
tk.Entry(patient_frame, bd=7, font=('arial', 17), width=6, textvariable=patient_gender_var).grid(row=2, column=1, padx=2, pady=2)

tk.Label(patient_frame, text="D.O.B", font=('Arial', 17), bg="white").grid(row=3, column=0, padx=2, pady=2)
tk.Entry(patient_frame, bd=7, font=('arial', 17), width=17, textvariable=patient_dob_var).grid(row=3, column=1, padx=2, pady=2)

tk.Label(patient_frame, text="Contact No.", font=('Arial', 17), bg="white").grid(row=4, column=0, padx=2, pady=2)
tk.Entry(patient_frame, bd=7, font=('arial', 17), width=17, textvariable=patient_contact_no_var).grid(row=4, column=1, padx=2, pady=2)

tk.Label(patient_frame, text="Address", font=('Arial', 17), bg="white").grid(row=5, column=0, padx=2, pady=2)
tk.Entry(patient_frame, bd=7, font=('arial', 17), width=17, textvariable=patient_address_var).grid(row=5, column=1, padx=2, pady=2)

# Buttons for Patients
patient_btn_frame = tk.Frame(patient_frame, bg='lightgrey', bd=6, relief=tk.GROOVE)
patient_btn_frame.place(x=30, y=400, width=360, height=60)

tk.Button(patient_btn_frame, bg="lightgreen", text="Add", bd=7, font=("arial", 13), width=7, command=add_patient).grid(row=0, column=0, padx=2, pady=2)
tk.Button(patient_btn_frame, bg="lightgrey", text="Clear", bd=7, font=("arial", 13), width=7, command=clear_patient_fields).grid(row=0, column=1, padx=2, pady=2)
tk.Button(patient_btn_frame, bg="red", text="Delete", bd=7, font=("arial", 13), width=7, command=delete_patient).grid(row=0, column=2, padx=2, pady=2)

# Doctor Details Entry
tk.Label(doctor_frame, text="Name", font=('Arial', 17), bg="white").grid(row=0, column=0, padx=2, pady=2)
tk.Entry(doctor_frame, bd=2, font=('arial', 15), width=12, textvariable=doctor_name_var).grid(row=0, column=1, padx=2, pady=2)

tk.Label(doctor_frame, text="Specialization", font=('Arial', 17), bg="white").grid(row=1, column=0, padx=2, pady=2)
tk.Entry(doctor_frame, bd=7, font=('arial', 17), width=17, textvariable=doctor_specialization_var).grid(row=1, column=1, padx=2, pady=2)

tk.Label(doctor_frame, text="Contact No.", font=('Arial', 17), bg="white").grid(row=2, column=0, padx=2, pady=2)
tk.Entry(doctor_frame, bd=7, font=('arial', 17), width=17, textvariable=doctor_contact_no_var).grid(row=2, column=1, padx=2, pady=2)

# Buttons for Doctors
doctor_btn_frame = tk.Frame(doctor_frame, bg='lightgrey', bd=6, relief=tk.GROOVE)
doctor_btn_frame.place(x=30, y=400, width=360, height=60)

tk.Button(doctor_btn_frame, bg="lightgreen", text="Add", bd=7, font=("arial", 13), width=7, command=add_doctor).grid(row=0, column=0, padx=2, pady=2)
tk.Button(doctor_btn_frame, bg="lightgrey", text="Clear", bd=7, font=("arial", 13), width=7, command=clear_doctor_fields).grid(row=0, column=1, padx=2, pady=2)
tk.Button(doctor_btn_frame, bg="red", text="Delete", bd=7, font=("arial", 13), width=7, command=delete_doctor).grid(row=0, column=2, padx=2, pady=2)

# Patient-Doctor Assignment Button
assign_btn_frame = tk.Frame(doctor_frame, bg='lightgrey', bd=6, relief=tk.GROOVE)
assign_btn_frame.place(x=30, y=470, width=360, height=60)

tk.Button(assign_btn_frame, bg="lightblue", text="Assign Doctor", bd=7, font=("arial", 13), width=20, command=assign_doctor_to_patient).grid(row=0, column=0, padx=2, pady=2)

# Patient Table
patient_table = ttk.Treeview(data_frame, columns=("id", "name", "age", "gender", "dob", "contact_no", "address"), show='headings')
patient_table.heading("id", text="ID")
patient_table.heading("name", text="Name")
patient_table.heading("age", text="Age")
patient_table.heading("gender", text="Gender")
patient_table.heading("dob", text="D.O.B")
patient_table.heading("contact_no", text="Contact No.")
patient_table.heading("address", text="Address")
patient_table.pack(fill=tk.BOTH, expand=1)

# Doctor Table
doctor_table = ttk.Treeview(data_frame, columns=("id", "name", "specialization", "contact_no"), show='headings')
doctor_table.heading("id", text="ID")
doctor_table.heading("name", text="Name")
doctor_table.heading("specialization", text="Specialization")
doctor_table.heading("contact_no", text="Contact No.")
doctor_table.pack(fill=tk.BOTH, expand=1)

# Patient-Doctor Info Table
patient_doctor_table = ttk.Treeview(data_frame, columns=("patient_id", "patient_name", "age", "gender", "dob", "contact_no", "address", "doctor_name", "specialization"), show='headings')
patient_doctor_table.heading("patient_id", text="Patient ID")
patient_doctor_table.heading("patient_name", text="Patient Name")
patient_doctor_table.heading("age", text="Age")
patient_doctor_table.heading("gender", text="Gender")
patient_doctor_table.heading("dob", text="D.O.B")
patient_doctor_table.heading("contact_no", text="Contact No.")
patient_doctor_table.heading("address", text="Address")
patient_doctor_table.heading("doctor_name", text="Doctor Name")
patient_doctor_table.heading("specialization", text="Specialization")
patient_doctor_table.pack(fill=tk.BOTH, expand=1)

fetch_patients()
fetch_doctors()
fetch_patient_doctor_info()

win.mainloop()
