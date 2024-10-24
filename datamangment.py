import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import re
import mysql.connector
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import filedialog
import subprocess

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
    tree.heading("رقم الهوية", text="رقم المنظومة")
    tree.heading("الرقم القومي", text="الرقم القومي")
    tree.heading("المنطقة", text="المساحة")
    tree.heading("إجراء قانوني", text="إجراء قانوني")
    tree.heading("رقم القضية", text="رقم المحضر")
    tree.heading("حالة الدفع", text=" موقف السداد")
    tree.heading("المبلغ", text="المبلغ")
    tree.heading("تاريخ الدفع", text="تاريخ السداد")
    tree.heading("تم إصدار العقد", text="تم إصدار العقد")
    tree.heading("تاريخ العقد", text="تاريخ صدور العقد")
    tree.heading("الملفات", text="الملفات")
    tree.heading("القرية", text="اسم القرية")
    tree.heading("سبب الإجراء القانوني", text="سبب الإجراء القانوني")
    tree.heading("حالة الملف", text="موقف الملف")

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
        "اسم", "رقم المنظومة", "الرقم القومي", "المساحة", "إجراء قانوني", "رقم المحضر", 
        "موقف السداد", "المبلغ", "تاريخ السداد", "تم إصدار العقد", "تاريخ صدور العقد", 
        "الملفات", "اسم القرية", "سبب الإجراء القانوني", "موقف الملف"
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

    village_options = ["السواركة", "البياضية", "الرياح", "الروضة", "الشهيد خيري", "أبو خليفة", "أبو طفيلة", "النصر"]
    reason_options = ["  %عدم سداد 25", "عدم دفع رسوم المعاينة", "عدم دفع رسوم الفحص", "مرفوض"]
    status_options = ["مقبول", "مرفوض", "استيفاء"]
    
    village_menu = tk.OptionMenu(data_frame, village_var, *village_options)
    village_menu.grid(row=6, column=1)
    entries["اسم القرية"] = village_var
    
    reason_menu = tk.OptionMenu(data_frame, reason_var, *reason_options)
    reason_menu.grid(row=6, column=3)
    entries["سبب الإجراء القانوني"] = reason_var
    
    status_menu = tk.OptionMenu(data_frame, status_var, *status_options)
    status_menu.grid(row=6, column=5)
    entries["موقف الملف"] = status_var
    def on_tree_select(event):
        """Handles the event when a row is selected in the Treeview."""
        selected_item = tree.selection()
        if not selected_item:
            return

        item_values = tree.item(selected_item[0], 'values')
        # Populate the entry fields with the selected row's data
        entries["اسم"].delete(0, tk.END)
        entries["اسم"].insert(0, item_values[0])
        entries["رقم المنظومة"].delete(0, tk.END)
        entries["رقم المنظومة"].insert(0, item_values[1])
        entries["الرقم القومي"].delete(0, tk.END)
        entries["الرقم القومي"].insert(0, item_values[2])
        entries["المساحة"].delete(0, tk.END)
        entries["المساحة"].insert(0, item_values[3])
        entries["إجراء قانوني"].delete(0, tk.END)
        entries["إجراء قانوني"].insert(0, item_values[4])
        entries["رقم المحضر"].delete(0, tk.END)
        entries["رقم المحضر"].insert(0, item_values[5])
        entries["موقف السداد"].delete(0, tk.END)
        entries["موقف السداد"].insert(0, item_values[6])
        entries["المبلغ"].delete(0, tk.END)
        entries["المبلغ"].insert(0, item_values[7])
        entries["تاريخ السداد"].delete(0, tk.END)
        entries["تاريخ السداد"].insert(0, item_values[8])
        entries["تم إصدار العقد"].delete(0, tk.END)
        entries["تم إصدار العقد"].insert(0, item_values[9])
        entries["تاريخ صدور العقد"].delete(0, tk.END)
        entries["تاريخ صدور العقد"].insert(0, item_values[10])
        entries["الملفات"].delete(0, tk.END)
        entries["الملفات"].insert(0, item_values[11])
        village_var.set(item_values[12])
        reason_var.set(item_values[13])
        status_var.set(item_values[14])
        item_values = tree.item(selected_item[0], 'values')
    # Populate the entry fields with the selected row's data
        for i, field in enumerate(fields):
            entries[field].delete(0, 'end')

            entries[field].insert(0, item_values[i])
        
        # Open detailed view window
       

    # Add this line to bind the event to the TreeView
    tree.bind("<Double-1>", on_tree_select)
        # Bind the select event to the TreeView
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # File upload button

    def upload_file():
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file_path:  # تحقق من أن المستخدم اختار ملفًا
            entries["الملفات"].delete(0, tk.END)
            entries["الملفات"].insert(0, file_path)
            # فتح الملف باستخدام البرنامج الافتراضي للنظام
            if os.name == 'nt':  # نظام Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # نظام Unix (Linux/Mac)
                subprocess.run(['xdg-open', file_path])
    
    upload_button = tk.Button(data_frame, text="تحميل ملف", command=upload_file, bg="gold", fg="black")
    upload_button.grid(row=3, column=6)
    
    # Add, Update, Delete buttons
    def add_data():
        # Insert data into the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO data_management (name, id_number, national_id, area, legal_action, case_number, payment_status, amount, payment_date, contract_issued, contract_date, files, village, reason, file_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (entries["اسم"].get(), entries["رقم المنظومة"].get(), entries["الرقم القومي"].get(), entries["المساحة"].get(), 
             entries["إجراء قانوني"].get(), entries["رقم المحضر"].get(), entries["موقف السداد"].get(), entries["المبلغ"].get(), 
             entries["تاريخ السداد"].get(), entries["تم إصدار العقد"].get(), entries["تاريخ صدور العقد"].get(), 
             entries["الملفات"].get(), entries["اسم القرية"].get(), entries["سبب الإجراء القانوني"].get(), entries["موقف الملف"].get())
        )
        db.commit()
        db.close()
        messagebox.showinfo("تم إضافة البيانات", "تمت إضافة البيانات بنجاح!")
        update_treeview()
    
    def update_data():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "يرجى تحديد عنصر لتحديثه.")
            return
        
        item_values = tree.item(selected_item[0], 'values')
        id_number = item_values[1]
        
        # Update data in the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE data_management SET name=%s, national_id=%s, area=%s, legal_action=%s, case_number=%s, payment_status=%s, amount=%s, payment_date=%s, contract_issued=%s, contract_date=%s, files=%s, village=%s, reason=%s, file_status=%s WHERE id_number=%s",
            (entries["اسم"].get(), entries["الرقم القومي"].get(), entries["المساحة"].get(), entries["إجراء قانوني"].get(), 
             entries["رقم المحضر"].get(), entries["موقف السداد"].get(), entries["المبلغ"].get(), entries["تاريخ السداد"].get(), 
             entries["تم إصدار العقد"].get(), entries["تاريخ صدور العقد"].get(), entries["الملفات"].get(), 
             entries["اسم القرية"].get(), entries["سبب الإجراء القانوني"].get(), entries["موقف الملف"].get(), id_number)
        )
        db.commit()
        db.close()
        messagebox.showinfo("تم تحديث البيانات", "تمت تحديث البيانات بنجاح!")
        update_treeview()
    
    def delete_data():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "يرجى تحديد عنصر لحذفه.")
            return
        
        item_values = tree.item(selected_item[0], 'values')
        id_number = item_values[1]
        
        # Delete data from the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM data_management WHERE id_number=%s", (id_number,))
        db.commit()
        db.close()
        messagebox.showinfo("تم حذف البيانات", "تمت حذف البيانات بنجاح!")
        
        # Remove the selected row from the TreeView
        tree.delete(selected_item[0])

    
    def update_treeview():
        """Fetch data from the database and update the Treeview"""
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM data_management")
        rows = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", tk.END, values=row)
        db.close()
    
    # Load data into Treeview
    update_treeview()
    
    # Buttons for add, update, delete
    add_button = tk.Button(main_window, text="إضافة بيانات", command=add_data, bg="gold", fg="black")
    add_button.pack(side="left", padx=10)

    update_button = tk.Button(main_window, text="تحديث بيانات", command=update_data, bg="gold", fg="black")
    update_button.pack(side="left", padx=10)

    delete_button = tk.Button(main_window, text="حذف بيانات", command=delete_data, bg="gold", fg="black")
    delete_button.pack(side="left", padx=10)
    exite_button=tk.Button(main_window,text="اغلاق البرنامج",command=main_window.quit,bg="gold", fg="black")
    exite_button.pack(side="right", padx=10)
    def open_search_window():
        """Opens a new window for searching by name"""
        search_window = tk.Toplevel(main_window)
        search_window.title("بحث")
        search_window.geometry("800x600")
        search_window.resizable(False,False)
        search_window.configure(bg="#003366")
        
        # Search entry and button
        tk.Label(search_window, text="أدخل الاسم للبحث:",bg="#003366",fg="white").pack(pady=10)
        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)
        search_button = tk.Button(search_window, text="بحث",bg="gold",fg="#003366", command=lambda: search_data(search_entry.get(), search_window))
        search_button.pack(pady=10)
    # Search functionality
    def open_file(file_path):
        """Open the file using the default application"""
        if os.path.exists(file_path):
            try:
                if os.name == 'nt':  # For Windows
                    os.startfile(file_path)
                elif os.name == 'posix':  # For Unix-like systems
                    subprocess.call(('xdg-open', file_path))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
        else:
            messagebox.showerror("Error", "File not found.")

    def search_data(search_query, search_window):
        """Searches for data based on the input query and updates the search window"""
        if not search_query:
            messagebox.showwarning("تحذير", "يرجى إدخال نص البحث.")
            return
        
        # Create a frame for displaying results
        result_frame = tk.Frame(search_window,bg="#003366")
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Connect to the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM data_management WHERE name LIKE %s", ('%' + search_query + '%',))
        rows = cursor.fetchall()
        db.close()

        # Display results
        for row in rows:
            id_number, name, national_id, area, legal_action, case_number, payment_status, amount, payment_date, contract_issued, contract_date, files, village, reason, file_status = row

            # Create and pack labels for each piece of data
            tk.Label(result_frame,bg="gold",fg="#003366", text=f"اسم: {id_number}").pack(anchor="w",fill="x")
            tk.Label(result_frame,bg="white",fg="#003366", text=f"رقم المنظومة: {name}").pack(anchor="w",fill="x")
            tk.Label(result_frame, bg="gold",fg="#003366",text=f"الرقم القومي: {national_id}").pack(anchor="w",fill="x")
            tk.Label(result_frame,bg="white",fg="#003366", text=f"المساحة: {area}").pack(anchor="w",fill="x")
            tk.Label(result_frame,bg="gold",fg="#003366", text=f"إجراء قانوني: {legal_action}").pack(anchor="w",fill="x")
            tk.Label(result_frame, bg="white",fg="#003366",text=f"رقم المحضر: {case_number}").pack(anchor="w",fill="x")
            tk.Label(result_frame, bg="gold",fg="#003366",text=f"موقف السداد: {payment_status}").pack(anchor="w",fill="x")
            tk.Label(result_frame,bg="white",fg="#003366", text=f"المبلغ: {amount}").pack(anchor="w",fill="x")
            tk.Label(result_frame,bg="gold",fg="#003366", text=f"تاريخ السداد: {payment_date}").pack(anchor="w",fill="x")
            tk.Label(result_frame, bg="white",fg="#003366",text=f"تم إصدار العقد: {contract_issued}").pack(anchor="w",fill="x")
            tk.Label(result_frame, bg="gold",fg="#003366",text=f"تاريخ صدور العقد: {contract_date}").pack(anchor="w",fill="x")
            tk.Label(result_frame, bg="white",fg="#003366",text=f"اسم القرية: {village}").pack(anchor="w",fill="x")
            tk.Label(result_frame, bg="gold",fg="#003366",text=f"سبب الإجراء القانوني: {reason}").pack(anchor="w",fill="x")
            tk.Label(result_frame, bg="white",fg="#003366",text=f"موقف الملف: {file_status}").pack(anchor="w",fill="x")

            # Display image if file is an image
            if files:
                file_button = tk.Button(result_frame, text="عرض الملف",bg="gold",fg="#003366", command=lambda f=files: open_file(f))
                file_button.pack(pady=5)
                

                # Display PDF if file is a PDF
              
            tk.Label(result_frame, text="").pack()  # Add empty line for spacing
    
    # Search bar
    search_frame = tk.Frame(main_window, bg="#003366")
    search_frame.pack(fill="x", pady=10)
    
    search_label = tk.Label(search_frame, text="بحث:", bg="#003366", fg="white")
    search_label.pack(side="left", padx=5)
    
    entry_search = tk.Entry(search_frame)
    entry_search.pack(side="left", padx=5)
    
    search_button = tk.Button(search_frame, text="بحث",  bg="gold", fg="black",command=open_search_window)
    search_button.pack(side="left", padx=5)

    main_window.mainloop()

def open_login_window():
    """Opens the login window"""
    global entry_login_username, entry_login_password
    
    login_window = tk.Tk()
    login_window.title("تسجيل الدخول")
    login_window.geometry("600x600")
    login_window.configure(bg="#003366")  # Dark blue background

    tk.Label(login_window, text="اسم المستخدم:", bg="#003366", fg="white").pack(pady=5)
    entry_login_username = tk.Entry(login_window)
    entry_login_username.pack(pady=5)
    
    tk.Label(login_window, text="كلمة المرور:", bg="#003366", fg="white").pack(pady=5)
    entry_login_password = tk.Entry(login_window, show="*")
    entry_login_password.pack(pady=5)
    
    tk.Button(login_window, text="تسجيل الدخول", command=login, bg="gold", fg="black").pack(pady=10)
    tk.Button(login_window, text="إنشاء حساب", command=open_registration_window, bg="gold", fg="black").pack(pady=10)
    image_path = "D:\\programming project\\python\\desktopApp\\logo1.png"  # استبدل هذا بالمسار الفعلي للصورة
    image = Image.open(image_path)
    resized_image = image.resize((400, 300))
    photo = ImageTk.PhotoImage(resized_image)

    image_label = tk.Label(login_window, image=photo, bg="#003366")
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.pack(pady=10)
    login_window.mainloop()
    
def open_registration_window():
    """Opens the registration window"""
    global entry_username, entry_phone, entry_email, entry_password

    registration_window = tk.Tk()
    registration_window.title("إنشاء حساب")
    registration_window.geometry("600x600")
    registration_window.configure(bg="#003366")  # Dark blue background

    tk.Label(registration_window, text="اسم المستخدم:", bg="#003366", fg="white").pack(pady=5)
    entry_username = tk.Entry(registration_window)
    entry_username.pack(pady=5)
    
    tk.Label(registration_window, text="رقم الهاتف:", bg="#003366", fg="white").pack(pady=5)
    entry_phone = tk.Entry(registration_window)
    entry_phone.pack(pady=5)
    
    tk.Label(registration_window, text="البريد الإلكتروني:", bg="#003366", fg="white").pack(pady=5)
    entry_email = tk.Entry(registration_window)
    entry_email.pack(pady=5)
    
    tk.Label(registration_window, text="كلمة المرور:", bg="#003366", fg="white").pack(pady=5)
    entry_password = tk.Entry(registration_window, show="*")
    entry_password.pack(pady=5)
    
    tk.Button(registration_window, text="تسجيل", command=register, bg="gold", fg="black").pack(pady=10)
    tk.Button(registration_window, text="عودة إلى تسجيل الدخول", command=registration_window.destroy, bg="gold", fg="black").pack(pady=10)

    registration_window.mainloop()

# Open the login window
open_login_window()
