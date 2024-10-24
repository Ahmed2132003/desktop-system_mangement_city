import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import re
import mysql.connector
from PIL import Image, ImageTk

# Establish a connection to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Use your MySQL username
        password="",  # Use your MySQL password
        database="user_management"
    )

def check_password_strength(password):
    """Checks if the password meets the strength criteria"""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[@$!%*?&]", password):
        return False
    return True

def register():
    """Handles user registration"""
    username = entry_username.get()
    phone = entry_phone.get()
    email = entry_email.get()
    password = entry_password.get()

    if not check_password_strength(password):
        messagebox.showerror("كلمة مرور ضعيفة", "يجب أن تكون كلمة المرور على الأقل 8 أحرف، وتحتوي على أحرف كبيرة وصغيرة وأرقام ورموز خاصة.")
        return

    # Connect to the database
    db = connect_db()
    cursor = db.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        messagebox.showerror("خطأ في التسجيل", "اسم المستخدم موجود بالفعل.")
        db.close()
        return

    # Insert user data into the database
    cursor.execute(
        "INSERT INTO users (username, phone, email, password) VALUES (%s, %s, %s, %s)",
        (username, phone, email, password)
    )
    db.commit()
    db.close()
    messagebox.showinfo("نجاح التسجيل", "تم إنشاء الحساب بنجاح!")

def login():
    """Handles user login"""
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    # Check login credentials
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    db.close()
    
    if user:
        # Close login window and open main window
        open_main_window()
    else:
        messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة.")

def open_main_window():
    """Opens the main application window with the Treeview and data management options"""
    main_window = tk.Tk()
    main_window.title("نظام إدارة البيانات")
    main_window.geometry("1000x600")
    main_window.configure(bg="#003366")  # Dark blue background

    # Treeview for displaying data
    tree = ttk.Treeview(main_window, columns=("اسم", "رقم الهوية", "الرقم القومي", "المنطقة", "إجراء قانوني", "رقم القضية", "حالة الدفع", "المبلغ", "تاريخ الدفع", "تم إصدار العقد", "تاريخ العقد", "الملفات", "القرية", "سبب الإجراء القانوني", "حالة الملف"), show="headings")
    tree.heading("اسم", text="اسم")
    tree.heading("رقم الهوية", text="رقم الهوية")
    tree.heading("الرقم القومي", text="الرقم القومي")
    tree.heading("المنطقة", text="المنطقة")
    tree.heading("إجراء قانوني", text="إجراء قانوني")
    tree.heading("رقم القضية", text="رقم القضية")
    tree.heading("حالة الدفع", text="حالة الدفع")
    tree.heading("المبلغ", text="المبلغ")
    tree.heading("تاريخ الدفع", text="تاريخ الدفع")
    tree.heading("تم إصدار العقد", text="تم إصدار العقد")
    tree.heading("تاريخ العقد", text="تاريخ العقد")
    tree.heading("الملفات", text="الملفات")
    tree.heading("القرية", text="القرية")
    tree.heading("سبب الإجراء القانوني", text="سبب الإجراء القانوني")
    tree.heading("حالة الملف", text="حالة الملف")

    tree.pack(fill="both", expand=True)
    
    # Add Scrollbar
    scrollbar = tk.Scrollbar(main_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Data Entry Section
    data_frame = tk.Frame(main_window, bg="#003366")
    data_frame.pack(fill="x", pady=10)
    
    # Define and place entry fields and labels
    fields = [
        "اسم", "رقم الهوية", "الرقم القومي", "المنطقة", "إجراء قانوني", "رقم القضية", 
        "حالة الدفع", "المبلغ", "تاريخ الدفع", "تم إصدار العقد", "تاريخ العقد", 
        "الملفات", "القرية", "سبب الإجراء القانوني", "حالة الملف"
    ]
    
    entries = {}
    for i, field in enumerate(fields):
        label = tk.Label(data_frame, text=field + ":", bg="#003366", fg="white")
        label.grid(row=i//3, column=(i%3)*2, padx=5, pady=5, sticky="e")
        entry = tk.Entry(data_frame)
        entry.grid(row=i//3, column=(i%3)*2+1, padx=5, pady=5, sticky="w")
        entries[field] = entry
    
    # Dropdowns for specific fields with StringVar
    village_var = tk.StringVar()
    reason_var = tk.StringVar()
    status_var = tk.StringVar()

    village_options = ["السواركة", "البياضية", "الريح", "الروضة", "الشهيد خيري", "أبو خليفة", "أبو طفيلة", "النصر"]
    reason_options = ["عدم دفع 25%", "عدم دفع رسوم الفحص", "عدم دفع رسوم المسح", "مرفوض"]
    status_options = ["مقبول", "مرفوض", "معلق"]
    
    village_menu = tk.OptionMenu(data_frame, village_var, *village_options)
    village_menu.grid(row=6, column=1)
    entries["القرية"] = village_var
    
    reason_menu = tk.OptionMenu(data_frame, reason_var, *reason_options)
    reason_menu.grid(row=6, column=3)
    entries["سبب الإجراء القانوني"] = reason_var
    
    status_menu = tk.OptionMenu(data_frame, status_var, *status_options)
    status_menu.grid(row=6, column=5)
    entries["حالة الملف"] = status_var

    def on_tree_select(event):
        """Handles the event when a row is selected in the Treeview."""
        selected_item = tree.selection()
        if not selected_item:
            return

        item_values = tree.item(selected_item[0], 'values')
        # Populate the entry fields with the selected row's data
        for i, field in enumerate(fields):
            entries[field].delete(0, tk.END)
            entries[field].insert(0, item_values[i])
        
        village_var.set(item_values[12])
        reason_var.set(item_values[13])
        status_var.set(item_values[14])
        
        # Open detailed view window
        open_detail_window(item_values)

    # Bind the select event to the TreeView
    tree.bind("<Double-1>", on_tree_select)

    # File upload button
    def open_detail_window(item_values):
        """Opens a window displaying detailed information of the selected item."""
        detail_window = tk.Toplevel(main_window)
        detail_window.title("تفاصيل العنصر")
        detail_window.geometry("600x400")
        detail_window.configure(bg="#003366")  # Dark blue background
        
        # Display the item details
        labels_frame = tk.Frame(detail_window, bg="#003366")
        labels_frame.pack(pady=10)
        
        for i, field in enumerate(fields):
            label = tk.Label(labels_frame, text=f"{field}: {item_values[i]}", bg="#003366", fg="white")
            label.pack(pady=5, anchor="w")
        
        # Display the file if available
        file_path = item_values[11]
        if file_path:
            try:
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    img = Image.open(file_path)
                    img.thumbnail((200, 200))  # Resize the image
                    img = ImageTk.PhotoImage(img)
                    img_label = tk.Label(detail_window, image=img)
                    img_label.image = img
                    img_label.pack(pady=10)
                else:
                    file_label = tk.Label(detail_window, text=f"ملف: {file_path}", bg="#003366", fg="white")
                    file_label.pack(pady=10)
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل تحميل الملف: {e}")

    def update_data():
        """Updates the selected data in the Treeview."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "يرجى اختيار عنصر للتحديث.")
            return

        item_values = [entries[field].get() for field in fields]
        item_values.append(village_var.get())
        item_values.append(reason_var.get())
        item_values.append(status_var.get())
        
        # Update the item in the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            """UPDATE data SET
                name=%s, id_number=%s, national_id=%s, region=%s, legal_action=%s, case_number=%s,
                payment_status=%s, amount=%s, payment_date=%s, contract_issued=%s, contract_date=%s,
                files=%s, village=%s, legal_reason=%s, file_status=%s
                WHERE id=%s""",
            (*item_values, selected_item[0])
        )
        db.commit()
        db.close()
        # Update the Treeview
        tree.item(selected_item[0], values=item_values)
        messagebox.showinfo("نجاح", "تم تحديث البيانات بنجاح!")

    def delete_data():
        """Deletes the selected data from the Treeview."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "يرجى اختيار عنصر للحذف.")
            return

        # Delete the item from the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM data WHERE id=%s", (selected_item[0],))
        db.commit()
        db.close()
        # Remove the item from the Treeview
        tree.delete(selected_item[0])
        messagebox.showinfo("نجاح", "تم حذف البيانات بنجاح!")

    def clear_fields():
        """Clears all the entry fields."""
        for entry in entries.values():
            entry.delete(0, tk.END)
        village_var.set("")
        reason_var.set("")
        status_var.set("")

    # Buttons for add, update, delete, and clear
    button_frame = tk.Frame(main_window, bg="#003366")
    button_frame.pack(pady=10)

    btn_update = tk.Button(button_frame, text="تحديث", command=update_data)
    btn_update.grid(row=0, column=0, padx=5)

    btn_delete = tk.Button(button_frame, text="حذف", command=delete_data)
    btn_delete.grid(row=0, column=1, padx=5)

    btn_clear = tk.Button(button_frame, text="مسح", command=clear_fields)
    btn_clear.grid(row=0, column=2, padx=5)

    main_window.mainloop()

# Register window
def open_register_window():
    """Opens the registration window."""
    register_window = tk.Tk()
    register_window.title("تسجيل مستخدم")
    register_window.geometry("400x300")
    register_window.configure(bg="#003366")  # Dark blue background

    tk.Label(register_window, text="تسجيل مستخدم", bg="#003366", fg="white", font=("Arial", 16)).pack(pady=10)

    global entry_username
    global entry_phone
    global entry_email
    global entry_password

    tk.Label(register_window, text="اسم المستخدم:", bg="#003366", fg="white").pack(pady=5)
    entry_username = tk.Entry(register_window)
    entry_username.pack(pady=5)

    tk.Label(register_window, text="رقم الهاتف:", bg="#003366", fg="white").pack(pady=5)
    entry_phone = tk.Entry(register_window)
    entry_phone.pack(pady=5)

    tk.Label(register_window, text="البريد الإلكتروني:", bg="#003366", fg="white").pack(pady=5)
    entry_email = tk.Entry(register_window)
    entry_email.pack(pady=5)

    tk.Label(register_window, text="كلمة المرور:", bg="#003366", fg="white").pack(pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(register_window, text="تسجيل", command=register).pack(pady=10)

    register_window.mainloop()

# Login window
def open_login_window():
    """Opens the login window."""
    login_window = tk.Tk()
    login_window.title("تسجيل الدخول")
    login_window.geometry("400x300")
    login_window.configure(bg="#003366")  # Dark blue background

    tk.Label(login_window, text="تسجيل الدخول", bg="#003366", fg="white", font=("Arial", 16)).pack(pady=10)

    global entry_login_username
    global entry_login_password

    tk.Label(login_window, text="اسم المستخدم:", bg="#003366", fg="white").pack(pady=5)
    entry_login_username = tk.Entry(login_window)
    entry_login_username.pack(pady=5)

    tk.Label(login_window, text="كلمة المرور:", bg="#003366", fg="white").pack(pady=5)
    entry_login_password = tk.Entry(login_window, show="*")
    entry_login_password.pack(pady=5)

    tk.Button(login_window, text="تسجيل الدخول", command=login).pack(pady=10)
    tk.Button(login_window, text="فتح نافذة التسجيل", command=open_register_window).pack(pady=5)

    login_window.mainloop()

# Start with the login window
open_login_window()
