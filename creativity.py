from tkinter import * 
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import re
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk


class CreativeCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("إدارة شركة كريتيفتي كود")
        self.users = self.load_users()  # تحميل بيانات المستخدمين من الملف
        self.customers=self.load_customers()
        self.create_widgets()

    def create_widgets(self):
        # وسائل التواصل الاجتماعي
        social_media_frame = LabelFrame(self.root, text="وسائل التواصل الاجتماعي", bg="#0e0b0b", fg="white")
        social_media_frame.pack(padx=10, pady=10, fill="x")

        b1=Button(social_media_frame, text="YouTube", bg="#aa20d3", fg="white", command=lambda: self.open_link("https://www.youtube.com")).grid(row=0, column=0, padx=5, pady=5)
        b2=Button(social_media_frame, text="Instagram", bg="#aa20d3", fg="white", command=lambda: self.open_link("https://www.instagram.com")).grid(row=0, column=1, padx=5, pady=5)
        b3=Button(social_media_frame, text="Facebook", bg="#aa20d3", fg="white", command=lambda: self.open_link("https://www.facebook.com")).grid(row=0, column=2, padx=5, pady=5)
        b4=Button(social_media_frame, text="WhatsApp", bg="#aa20d3", fg="white", command=lambda: self.open_link("https://www.whatsapp.com")).grid(row=0, column=3, padx=5, pady=5)
        b5=Button(social_media_frame, text="LinkedIn", bg="#aa20d3", fg="white", command=lambda: self.open_link("https://www.linkedin.com")).grid(row=0, column=4, padx=5, pady=5)

        # معلومات رؤساء الشركة
        executives_frame = LabelFrame(self.root, text="معلومات رؤساء الشركة", bg="#0e0b0b", fg="white")
        executives_frame.pack(padx=10, pady=10, fill="x")

        b3=Label(executives_frame, text="رئيس التنفيذي للشركة: المهندس احمد ابراهيم", fg="white", bg="#0e0b0b").pack(padx=5, pady=5)
        b3=Label(executives_frame, text="المدير التنفيذي للشركة: المهندس احمد لطفي", fg="white", bg="#0e0b0b").pack(padx=5, pady=5)

        # صورة الشركة
        logo_frame = LabelFrame(self.root, text="صورة الشركة", bg="#0e0b0b", fg="white")
        logo_frame.pack(padx=10, pady=10, fill="x")

        self.logo_label = Label(logo_frame)
        self.logo_label.pack(padx=5, pady=5)
        self.display_logo("D:\\programming project\\python\\kivy\\kivyproject\\login\\lo.png")  

        # تسجيل الدخول وإنشاء حساب جديد
        auth_frame = LabelFrame(self.root, text="تسجيل الدخول/إنشاء حساب جديد", bg="#0e0b0b", fg="white")
        auth_frame.pack(padx=10, pady=10, fill="x")

        b6=Label(auth_frame, text="اسم المستخدم:", bg="#0e0b0b", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = Entry(auth_frame, width=40)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        b7=Label(auth_frame, text="كلمة المرور:", bg="#0e0b0b", fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = Entry(auth_frame, width=40, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = Button(auth_frame, text="تسجيل الدخول", bg="#aa20d3", fg="white", command=self.login)
        self.login_button.grid(row=2, column=0, padx=5, pady=5)

        self.signup_button = Button(auth_frame, text="إنشاء حساب جديد", bg="#aa20d3", fg="white", command=self.signup)
        self.signup_button.grid(row=2, column=1, padx=5, pady=5)

    def open_link(self, url):
        webbrowser.open(url)

    def display_logo(self, path):
        try:
            image = Image.open(path)
            image = image.resize((200, 200))
            self.logo_img = ImageTk.PhotoImage(image)
            self.logo_label.config(image=self.logo_img)
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن تحميل الصورة: {e}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.open_main_window()
        else:
            messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not re.match("^[A-Za-z]+$", username):
            messagebox.showerror("خطأ", "اسم المستخدم يجب أن يحتوي على حروف فقط")
        elif not re.match("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            messagebox.showerror("خطأ", "كلمة المرور يجب أن تحتوي على حروف وأرقام وتكون بطول 8 أحرف على الأقل")
        elif username in self.users:
            messagebox.showerror("خطأ", "اسم المستخدم موجود بالفعل")
        else:
            self.users[username] = password
            self.save_users()  # حفظ بيانات المستخدمين إلى الملف
            messagebox.showinfo("إنشاء حساب جديد", f"تم إنشاء حساب جديد بنجاح للمستخدم: {username}")
            self.open_main_window()

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                return json.load(file)
        return {}

    def save_users(self):
        with open("users.json", "w") as file:
            json.dump(self.users, file)
    def load_customers(self):
        if os.path.exists("customers.json"):
            with open("customers.json", "r") as file:
                return json.load(file)
        return {}

    def save_customers(self):
        with open("customers.json", "w") as file:
            json.dump(self.customers, file)

    def open_main_window(self):
        main_window = Toplevel(self.root)
        main_window.title("الصفحة الرئيسية")
        main_window.geometry("1350x680+5+5".format(main_window.winfo_screenwidth(), main_window.winfo_screenheight()))
        main_window.resizable(False,False)
        main_window.configure(bg="#0e0b0b")

        # إنشاء شريط منيو في الأعلى
        menu_bar = Menu(main_window, bg="#aa20d3", fg="white")
        main_window.config(menu=menu_bar)

        # إضافة خيارات القائمة
        menu_bar.add_command(label="الصفحة الرئيسية", command=self.open_main_window)
        menu_bar.add_command(label="العملاء", command=self.open_customer_window)
        menu_bar.add_command(label="الموظفين", command=self.open_employee_window)
        menu_bar.add_command(label="الادارين", command=self.Open_manager_window)
        menu_bar.add_command(label="الخدمات", command=self.open_services_interface)
        menu_bar.add_command(label="المعاملات", command=self.transaction_interface)
        menu_bar.add_command(label="الحسابات", command=self.open_accounting_interface)
        menu_bar.add_command(label="إغلاق", command=main_window.quit)  # زر إغلاق
        f1=Frame(main_window,bd=2,width=675,height=340,bg="#0e0b0b")
        f1.place(x=0,y=0)
        # fc=tk.Frame(main_window,width=1350,height=680,bd=2,background="white")
        # fc.place(x=0,y=0)
        # # تعريف عن الشركة
        main_l=("Our company specializes in all programming languages and projects, including Python, Java, R, C#, C++, Dart, PHP Laravel, JavaScript, CSS and HTML")
        ma1=("We have top specialists in web development, game development, computer programs, mobile apps, and artificial intelligence including machine")
        ma2=(" learning, deep learning, data science, data analysis, mechatronics, and robotics. The company was founded by Ahmed Ibrahim and Ahmed Lotfy.")
        


        main_l1=Label(f1, text="CREATIVITY CODE مرحباً بك في شركة", font=("tajawal", 14,"bold"), bg="#0e0b0b", fg="#aa20d3").place(x=215,y=20)
        main_l2=Label(f1, text=main_l,bg="#0e0b0b", fg="white", justify="center", font=("tajawal", 7)).place(x=0,y=80)
        main_l3=Label(f1, text=ma1,bg="#0e0b0b", fg="white", justify="center", font=("tajawal", 7)).place(x=0,y=115)
        main_l4=Label(f1 ,text=ma2,bg="#0e0b0b",fg="white", justify="center", font=("tajawal", 7)).place(x=0,y=150)
        # عرض صورة الشركة
        
        image = Image.open("D:\\programming project\\python\\kivy\\kivyproject\\login\\lo.png")
        image = image.resize((200, 200))
        self.logo_img_main = ImageTk.PhotoImage(image)

        # إنشاء العنصر Label
        img = Label(f1, image=self.logo_img_main, bg="#0e0b0b")
        # تعيين مكان العنصر
        img.place(x=210, y=170)
        #صفحة العملاء داخل الرئيسية 
        scroll_x=Scrollbar(main_window,orient="horizontal")
        scroll_y=Scrollbar(main_window,orient="vertical")
        xscrollcommand=scroll_x.set
        yscrollcommand=scroll_y.set
        scroll_x.config(command=main_window)
        scroll_y.config(command=main_window)
        scroll_x.pack(fill="x",side="bottom")
        scroll_y.pack(fill="y",side="right")
        fasel1=Label(main_window,text="-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",bg="#0e0b0b",fg="white",justify="center", font=("tajawal", 14))
        fasel1.place(x=0,y=450)
       
        #=====================================قسم العملاء ====================================
        f2=Frame(main_window,bd=2,width=675,height=200,bg="#0e0b0b")
        f2.place(x=676,y=0)
        tit=Label(f2,text="قسم العملاء",bg="#0e0b0b", fg="#aa20d3", justify="center", font=("tajawal", 14,"bold"))
        tit.place(x=310,y=20)
        x1="This section is dedicated to clients and will include everything related to their information, accounts, financial transactions, the services they have received,\n when they will receive their services, how contracts and financial dealings are managed, and customer service."
        lbl=Label(f2,text=x1,  bg="#0e0b0b", fg="white", justify="center", font=("tajawal", 7))
        lbl.place(x=0,y=80)
        btn=Button(f2,text="قسم العملاء ",bg="#aa20d3", fg="#0e0b0b",font=("tajawal",10,"bold"),command=self.open_customer_window)
        btn.place(x=310,y=150)
        
        #=====================================قسم الموظفين==========================================
        f3=Frame(main_window,bd=2,width=675,height=200,bg="#0e0b0b")
        f3.place(x=676,y=201)
        tit11=Label(f3,text="قسم الموظفين",bg="#0e0b0b", fg="#aa20d3", justify="center", font=("tajawal", 14,"bold"))
        tit11.place(x=310,y=20)
        x11="The employee department is a special section for the company's employees and their data and work, whether they are programmers,,\n freelancers, or marketing staff, each with their own part-time job"
        lbl11=Label(f3,text=x11,  bg="#0e0b0b", fg="white", justify="center", font=("tajawal", 8))
        lbl11.place(x=0,y=80)
        btn11=Button(f3,text="قسم الموظفين ",bg="#aa20d3", fg="#0e0b0b",font=("tajawal",10,"bold"),command=self.open_employee_window)
        btn11.place(x=310,y=150)
        #===================================قسم الادارين ====================================================
        f4=Frame(main_window,bd=2,width=675,height=200,bg="#0e0b0b")
        f4.place(x=0,y=341)
        tit11=Label(f4,text="قسم الادارين",bg="#0e0b0b", fg="#aa20d3", justify="center", font=("tajawal", 14,"bold"))
        tit11.place(x=275,y=20)
        x11="The Administrative Section is the part dedicated to everyone who holds an administrative position in the company, \n whether they are the CEO Executive Director, Marketing and Media Manager, Public Relations Manager, or others."
        lbl11=Label(f4,text=x11,  bg="#0e0b0b", fg="white", justify="center", font=("tajawal", 9))
        lbl11.place(x=0,y=80)
        btn11=Button(f4,text="قسم الادارين ",bg="#aa20d3", fg="#0e0b0b",font=("tajawal",10,"bold"),command=self.Open_manager_window)
        btn11.place(x=290,y=150)
        #======================================قسم الخدمات ===================================================
        f5=Frame(main_window,bd=2,width=675,height=200,bg="#0e0b0b")
        f5.place(x=0,y=543)
        tit12=Label(f5,text="قسم الخدمات",bg="#0e0b0b", fg="#aa20d3", justify="center", font=("tajawal", 14,"bold"))
        tit12.place(x=280,y=0)
        x112="The Services Department is dedicated to providing information about the types of services we offer and also allows you to ,\n request any service from the same department. The service is approved, and then work on it begins."
        lbl112=Label(f5,text=x112,  bg="#0e0b0b", fg="white", justify="center", font=("tajawal", 8))
        lbl112.place(x=0,y=40)
        btn112=Button(f5,text="قسم الخدمات ",bg="#aa20d3", fg="#0e0b0b",font=("tajawal",10,"bold"),command=self.open_services_interface)
        btn112.place(x=290,y=80)
        #========================================قسم المعاملات ================================================
        f6=Frame(main_window,bd=2,width=675,height=200,bg="#0e0b0b")
        f6.place(x=676,y=402)
        tit1111=Label(f6,text="قسم المعاملات",bg="#0e0b0b", fg="#aa20d3", justify="center", font=("tajawal", 14,"bold"))
        tit1111.place(x=310,y=0)
        x1111="The Transactions Department will display all transactions between the company and the clients, including  \n completed, requested, and finalized services.."
        lbl1111=Label(f6,text=x1111,  bg="#0e0b0b", fg="white", justify="center", font=("tajawal", 9))
        lbl1111.place(x=0,y=40)
        btn1111=Button(f6,text="قسم المعاملات ",bg="#aa20d3", fg="#0e0b0b",font=("tajawal",10,"bold"),command=self.transaction_interface)
        btn1111.place(x=310,y=90)
        #==========================================قسم الحسابات===================================================
        f7=Frame(main_window,bd=2,width=675,height=200,bg="#0e0b0b")
        f7.place(x=676,y=522)
        tit112=Label(f7,text="قسم الحسابات",bg="#0e0b0b", fg="#aa20d3", justify="center", font=("tajawal", 14,"bold"))
        tit112.place(x=310,y=0)
        x111="The Accounts Department will show the company's complete financial accounts, including incoming and outgoing funds,  \n salaries, advertisements,and the net balance—everything related to the company's finances."
        lbl111=Label(f7,text=x111,  bg="#0e0b0b", fg="white", justify="center", font=("tajawal", 9))
        lbl111.place(x=0,y=40)
        btn111=Button(f7,text="قسم الحسابات ",bg="#aa20d3", fg="#0e0b0b",font=("tajawal",10,"bold"),command=self.open_accounting_interface)
        btn111.place(x=310,y=90)
    def open_customer_window(self):
        customer_window = Toplevel(self.root)
        customer_window.title("صفحة العملاء")
        customer_window.geometry("1350x680+5+5".format(customer_window.winfo_screenwidth(), customer_window.winfo_screenheight()))
        customer_window.resizable(False, False)
        customer_window.configure(bg="#0e0b0b")
        scroll_x=Scrollbar(customer_window,orient="horizontal")
        scroll_y=Scrollbar(customer_window,orient="vertical")
        xscrollcommand=scroll_x.set
        yscrollcommand=scroll_y.set
        scroll_x.config(command=customer_window)
        scroll_y.config(command=customer_window)
        scroll_x.pack(fill="x",side="bottom")
        scroll_y.pack(fill="y",side="right")

        customer_frame = LabelFrame(customer_window, text="بيانات العملاء", bg="#0e0b0b", fg="white", width=675, height=340)
        customer_frame.place(x=0, y=0)

        scroll_x = Scrollbar(customer_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(customer_frame, orient=VERTICAL)

        self.tree = ttk.Treeview(customer_frame, columns=("name", "phone", "email", "transactions", "address", "rating", "amount"), show='headings',
                                xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set, height=15)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview)

        self.tree.heading("name", text="اسم العميل")
        self.tree.heading("phone", text="رقم الهاتف")
        self.tree.heading("email", text="الإيميل")
        self.tree.heading("transactions", text="عدد التعاملات")
        self.tree.heading("address", text="عنوان العميل")
        self.tree.heading("rating", text="تقييم العميل")
        self.tree.heading("amount", text="المبلغ الذي صرفه")

        self.tree.pack(fill=BOTH, expand=True)

        # إضافة إطار لإدخال البيانات
        input_frame = LabelFrame(customer_window, text="إدخال البيانات", bg="#0e0b0b", fg="white", width=675, height=340)
        input_frame.place(x=0, y=360)  # حرك الفريم للأسفل بمقدار 20 بكسل

        Label(input_frame, text="اسم العميل:", bg="#0e0b0b", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.customer_name_entry = Entry(input_frame)
        self.customer_name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="رقم الهاتف:", bg="#0e0b0b", fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.customer_phone_entry = Entry(input_frame)
        self.customer_phone_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(input_frame, text="الإيميل:", bg="#0e0b0b", fg="white").grid(row=2, column=0, padx=5, pady=5)
        self.customer_email_entry = Entry(input_frame)
        self.customer_email_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(input_frame, text="عدد التعاملات:", bg="#0e0b0b", fg="white").grid(row=3, column=0, padx=5, pady=5)
        self.customer_transactions_entry = Entry(input_frame)
        self.customer_transactions_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(input_frame, text="عنوان العميل:", bg="#0e0b0b", fg="white").grid(row=4, column=0, padx=5, pady=5)
        self.customer_address_entry = Entry(input_frame)
        self.customer_address_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(input_frame, text="تقييم العميل:", bg="#0e0b0b", fg="white").grid(row=5, column=0, padx=5, pady=5)
        self.customer_rating_entry = Entry(input_frame)
        self.customer_rating_entry.grid(row=5, column=1, padx=5, pady=5)

        Label(input_frame, text="المبلغ الذي صرفه:", bg="#0e0b0b", fg="white").grid(row=6, column=0, padx=5, pady=5)
        self.customer_amount_entry = Entry(input_frame)
        self.customer_amount_entry.grid(row=6, column=1, padx=5, pady=5)

        Button(input_frame, text="إضافة", bg="#aa20d3", fg="white", command=self.add_customer).grid(row=7, column=0, padx=5, pady=5)
        Button(input_frame, text="تعديل", bg="#aa20d3", fg="white", command=self.edit_customer).grid(row=7, column=1, padx=5, pady=5)
        Button(input_frame, text="حذف", bg="#aa20d3", fg="white", command=self.delete_customer).grid(row=7, column=2, padx=5, pady=5)
        Button(input_frame, text="إفراغ الحقول", bg="#aa20d3", fg="white", command=self.clear_fields).grid(row=7, column=3, padx=5, pady=5)
        stats_frame = Frame(customer_window, bg="#0e0b0b",width=675, height=350)

        stats_frame.place(x=380, y=375)
        # رسم بياني لتقييم العملاء
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        names = list(self.customers.keys())
        ratings = [float(self.customers[name]['rating']) for name in names]
        ax1.bar(names, ratings, color='skyblue')
        ax1.set_xlabel('clint name')
        ax1.set_ylabel('rating')
        ax1.set_title('clint rating')
        # ax1.set_xticklabels(names, rotation=90)
        canvas1 = FigureCanvasTkAgg(fig1, master=stats_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        stats_frame1 = Frame(customer_window, bg="#0e0b0b",width=675, height=350)
        
        stats_frame1.place(x=790,y=375)
        # رسم بياني للمبالغ التي صرفها العملاء
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        amounts = [float(self.customers[name]['amount']) for name in names]
        ax2.bar(names, amounts, color='salmon')
        ax2.set_xlabel('clint name')
        ax2.set_ylabel('the amount he spent')
        ax2.set_title('Amounts spent by customers')
        # ax2.set_xticklabels(names, rotation=90)

        canvas2 = FigureCanvasTkAgg(fig2, master=stats_frame1)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.update_customer_table()

    def clear_fields(self):
        self.customer_name_entry.delete(0, END)
        self.customer_phone_entry.delete(0, END)
        self.customer_email_entry.delete(0, END)
        self.customer_transactions_entry.delete(0, END)
        self.customer_address_entry.delete(0, END)
        self.customer_rating_entry.delete(0, END)
        self.customer_amount_entry.delete(0, END)

    def update_customer_table(self):
        # مسح البيانات القديمة من الجدول
        for row in self.tree.get_children():
            self.tree.delete(row)

        # إضافة البيانات الجديدة
        for name, data in self.customers.items():
            self.tree.insert("", END, values=(
                name,
                data.get("phone", ""),
                data.get("email", ""),
                data.get("transactions", ""),
                data.get("address", ""),
                data.get("rating", ""),
                data.get("amount", "")
            ))

    def add_customer(self):
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        transactions = self.customer_transactions_entry.get()
        address = self.customer_address_entry.get()
        rating = self.customer_rating_entry.get()
        amount = self.customer_amount_entry.get()

        if name in self.customers:
            messagebox.showerror("خطأ", "العميل موجود بالفعل")
            return

        self.customers[name] = {
            "phone": phone,
            "email": email,
            "transactions": transactions,
            "address": address,
            "rating": rating,
            "amount": amount
        }
        self.save_customers()
        self.update_customer_table()
        messagebox.showinfo("نجاح", "تم إضافة العميل بنجاح")

    def edit_customer(self):
        name = self.customer_name_entry.get()
        if name not in self.customers:
            messagebox.showerror("خطأ", "العميل غير موجود")
            return

        self.customers[name].update({
            "phone": self.customer_phone_entry.get(),
            "email": self.customer_email_entry.get(),
            "transactions": self.customer_transactions_entry.get(),
            "address": self.customer_address_entry.get(),
            "rating": self.customer_rating_entry.get(),
            "amount": self.customer_amount_entry.get()
        })
        self.save_customers()
        self.update_customer_table()
        messagebox.showinfo("نجاح", "تم تعديل بيانات العميل بنجاح")

    def delete_customer(self):
        name = self.customer_name_entry.get()
        if name not in self.customers:
            messagebox.showerror("خطأ", "العميل غير موجود")
            return

        del self.customers[name]
        self.save_customers()
        self.update_customer_table()
        messagebox.showinfo("نجاح", "تم حذف العميل بنجاح")


    


    def show_message(self, message):
        messagebox.showinfo("معلومات", message)

 

    def open_employee_window(self):
        # Creating and configuring the employee window
        employee_window = Toplevel(self.root)
        employee_window.title("قسم الموظفين")
        employee_window.geometry("1350x680+5+5")
        employee_window.resizable(False, False)
        employee_window.configure(bg="#0e0b0b")
        
        # Adding scrollbars
        scroll_x = Scrollbar(employee_window, orient=HORIZONTAL)
        scroll_y = Scrollbar(employee_window, orient=VERTICAL)
        
        employee_frame = LabelFrame(employee_window, text="بيانات الموظفين", bg="#0e0b0b", fg="white", width=675, height=340)
        employee_frame.place(x=0, y=0)
        
        # Creating TreeView to display employee data
        self.tree_employee = ttk.Treeview(employee_frame, columns=("name", "phone", "email", "age", "experience", "assignments", "role"), 
                                        show='headings', xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set, height=15)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.tree_employee.xview)
        scroll_y.config(command=self.tree_employee.yview)

        # Configuring TreeView column headings
        self.tree_employee.heading("name", text="اسم الموظف")
        self.tree_employee.heading("phone", text="رقم الهاتف")
        self.tree_employee.heading("email", text="الإيميل")
        self.tree_employee.heading("age", text="العمر")
        self.tree_employee.heading("experience", text="سنوات الخبرة")
        self.tree_employee.heading("assignments", text="عدد المهام")
        self.tree_employee.heading("role", text="الدور الوظيفي")

        self.tree_employee.pack(fill=BOTH, expand=True)

        # Loading employee data from JSON
        self.load_employee_data()

        # Creating input frame for data entry
        input_frame = LabelFrame(employee_window, text="إدخال البيانات", bg="#0e0b0b", fg="white", width=675, height=340)
        input_frame.place(x=0, y=360) 

        # Creating input fields
        Label(input_frame, text="اسم الموظف:", bg="#0e0b0b", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.employee_name_entry = Entry(input_frame)
        self.employee_name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="رقم الهاتف:", bg="#0e0b0b", fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.employee_phone_entry = Entry(input_frame)
        self.employee_phone_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(input_frame, text="الإيميل:", bg="#0e0b0b", fg="white").grid(row=2, column=0, padx=5, pady=5)
        self.employee_email_entry = Entry(input_frame)
        self.employee_email_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(input_frame, text="العمر:", bg="#0e0b0b", fg="white").grid(row=3, column=0, padx=5, pady=5)
        self.employee_age_entry = Entry(input_frame)
        self.employee_age_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(input_frame, text="سنوات الخبرة:", bg="#0e0b0b", fg="white").grid(row=4, column=0, padx=5, pady=5)
        self.employee_experience_entry = Entry(input_frame)
        self.employee_experience_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(input_frame, text="عدد المهام:", bg="#0e0b0b", fg="white").grid(row=5, column=0, padx=5, pady=5)
        self.employee_assignments_entry = Entry(input_frame)
        self.employee_assignments_entry.grid(row=5, column=1, padx=5, pady=5)

        Label(input_frame, text="الدور الوظيفي:", bg="#0e0b0b", fg="white").grid(row=6, column=0, padx=5, pady=5)
        self.employee_role_combobox = ttk.Combobox(input_frame, values=[
            "Web Developer", "Mobile Developer", "Desktop Developer", 
            "Data Analyst", "AI Specialist", "Web Scraping", 
            "Hacker", "Cybersecurity Specialist", "Freelancer", "Marketer"
        ])
        self.employee_role_combobox.grid(row=6, column=1, padx=5, pady=5)

        # Adding buttons for adding, editing, searching, deleting, and clearing data
        Button(input_frame, text="إضافة", bg="#aa20d3", fg="white", command=self.add_employee).grid(row=7, column=0, padx=5, pady=5)
        Button(input_frame, text="تعديل", bg="#aa20d3", fg="white", command=self.edit_employee).grid(row=7, column=1, padx=5, pady=5)
        Button(input_frame, text="بحث", bg="#aa20d3", fg="white", command=self.search_employee).grid(row=7, column=2, padx=5, pady=5)
        Button(input_frame, text="حذف", bg="#aa20d3", fg="white", command=self.delete_employee).grid(row=7, column=3, padx=5, pady=5)
        Button(input_frame, text="إفراغ الحقول", bg="#aa20d3", fg="white", command=self.clear_fields).grid(row=7, column=4, padx=5, pady=5)

    # Helper functions

    def load_employee_data(self):
        """Load employee data from a JSON file and display it in the TreeView."""
        if os.path.exists('employees.json'):
            with open('employees.json', 'r', encoding='utf-8') as file:
                employees = json.load(file)
                for employee in employees:
                    self.tree_employee.insert('', 'end', values=(
                        employee['name'], employee['phone'], employee['email'], employee['age'], 
                        employee['experience'], employee['assignments'], employee['role']
                    ))

    def save_employee_data(self):
        """Save the current employee data to a JSON file."""
        employees = []
        for item in self.tree_employee.get_children():
            employee = self.tree_employee.item(item)['values']
            employees.append({
                'name': employee[0],
                'phone': employee[1],
                'email': employee[2],
                'age': employee[3],
                'experience': employee[4],
                'assignments': employee[5],
                'role': employee[6],
            })
        with open('employees.json', 'w', encoding='utf-8') as file:
            json.dump(employees, file, ensure_ascii=False, indent=4)

    def add_employee(self):
        """Add a new employee to the TreeView and save it to the JSON file."""
        employee_data = (
            self.employee_name_entry.get(),
            self.employee_phone_entry.get(),
            self.employee_email_entry.get(),
            self.employee_age_entry.get(),
            self.employee_experience_entry.get(),
            self.employee_assignments_entry.get(),
            self.employee_role_combobox.get()
        )
        self.tree_employee.insert('', 'end', values=employee_data)
        self.save_employee_data()
        self.clear_fields()

    def edit_employee(self):
        """Edit the selected employee's data and save it to the JSON file."""
        selected_item = self.tree_employee.selection()
        if selected_item:
            self.tree_employee.item(selected_item, values=(
            self.employee_name_entry.get(),
            self.employee_phone_entry.get(),
            self.employee_email_entry.get(),
            self.employee_age_entry.get(),
            self.employee_experience_entry.get(),
            self.employee_assignments_entry.get(),
            self.employee_role_combobox.get()
            ))
            self.save_employee_data()
            self.clear_fields()

    def delete_employee(self):
        """Delete the selected employee from the TreeView and the JSON file."""
        selected_item = self.tree_employee.selection()
        if selected_item:
            self.tree_employee.delete(selected_item)
            self.save_employee_data()
            self.clear_fields()


    def search_employee(self):
        """Search for an employee by name and populate the entry fields with their data."""
        name = self.employee_name_entry.get()
        for item in self.tree_employee.get_children():
            employee = self.tree_employee.item(item)['values']
            if employee[0] == name:
                self.employee_name_entry.delete(0, END)
                self.employee_phone_entry.delete(0, END)
                self.employee_email_entry.delete(0, END)
                self.employee_age_entry.delete(0, END)
                self.employee_experience_entry.delete(0, END)
                self.employee_assignments_entry.delete(0, END)
                self.employee_role_combobox.set('')

                self.employee_name_entry.insert(0, employee[0])
                self.employee_phone_entry.insert(0, employee[1])
                self.employee_email_entry.insert(0, employee[2])
                self.employee_age_entry.insert(0, employee[3])
                self.employee_experience_entry.insert(0, employee[4])
                self.employee_assignments_entry.insert(0, employee[5])
                self.employee_role_combobox.set(employee[6])
                break

    # def delete_employee(self):
    #     """Delete the selected employee from the TreeView and the JSON file."""
    #     selected_item = self.tree_employee.selection()
    #     if selected_item:
    #         self.tree_employee.delete(selected_item)
    #         self.save_employee_data()
    #         self.clear_fields()

    def clear_fields(self):
        """Clear all entry fields."""
        self.employee_name_entry.delete(0, END)
        self.employee_phone_entry.delete(0, END)
        self.employee_email_entry.delete(0, END)
        self.employee_age_entry.delete(0, END)
        self.employee_experience_entry.delete(0, END)
        self.employee_assignments_entry.delete(0, END)
        self.employee_role_combobox.set('')



    def Open_manager_window(self):
        manger_window = Toplevel(self.root)
        manger_window.title("قسم الإداريين")
        manger_window.geometry("1350x680+5+5")
        manger_window.resizable(False, False)
        manger_window.configure(bg="#0e0b0b")

        # تحميل بيانات الإداريين
        self.admins = self.load_admins()

        # إضافة الـ Scrollbars
        scroll_x = Scrollbar(manger_window, orient=HORIZONTAL)
        scroll_y = Scrollbar(manger_window, orient=VERTICAL)
        self.tree22 = ttk.Treeview(manger_window, columns=("name", "role", "phone", "email", "duration", "start_date", "end_date"), 
                                show='headings', height=10, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        # إعداد رؤوس الأعمدة
        self.tree22.heading("name", text="اسم الإداري")
        self.tree22.heading("role", text="وظيفة الإداري")
        self.tree22.heading("phone", text="رقم الهاتف")
        self.tree22.heading("email", text="إيميل الإداري")
        self.tree22.heading("duration", text="مدة العمل")
        self.tree22.heading("start_date", text="تاريخ التعيين")
        self.tree22.heading("end_date", text="تاريخ انتهاء العقد")

        # ضبط الـ Scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.tree22.xview)
        scroll_y.config(command=self.tree22.yview)
        
        self.tree22.pack(fill=BOTH, expand=1)
        self.update_treeview()

        # حقول الإدخال
        self.frame = LabelFrame(manger_window, text="إدخال البيانات", bg="#0e0b0b", fg="white", width=675, height=340)
        self.frame.place(x=0, y=360) 

        Label(self.frame, text="اسم الإداري", bg="#0e0b0b", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(self.frame, text="وظيفة الإداري", bg="#0e0b0b", fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.role_entry = Entry(self.frame)
        self.role_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(self.frame, text="رقم الهاتف", bg="#0e0b0b", fg="white").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = Entry(self.frame)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(self.frame, text="إيميل الإداري", bg="#0e0b0b", fg="white").grid(row=3, column=0, padx=5, pady=5)
        self.email_entry = Entry(self.frame)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(self.frame, text="مدة العمل", bg="#0e0b0b", fg="white").grid(row=4, column=0, padx=5, pady=5)
        self.duration_entry = Entry(self.frame)
        self.duration_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(self.frame, text="تاريخ التعيين", bg="#0e0b0b", fg="white").grid(row=5, column=0, padx=5, pady=5)
        self.start_date_entry = Entry(self.frame)
        self.start_date_entry.grid(row=5, column=1, padx=5, pady=5)

        Label(self.frame, text="تاريخ انتهاء العقد", bg="#0e0b0b", fg="white").grid(row=6, column=0, padx=5, pady=5)
        self.end_date_entry = Entry(self.frame)
        self.end_date_entry.grid(row=6, column=1, padx=5, pady=5)

        # أزرار العمليات
        Button(self.frame, text="إضافة", bg="#aa20d3", command=self.add_admin).grid(row=7, column=0, padx=5, pady=5)
        Button(self.frame, text="بحث", bg="#aa20d3", command=self.search_admin).grid(row=7, column=1, padx=5, pady=5)
        Button(self.frame, text="تعديل", bg="#aa20d3", command=self.update_admin).grid(row=7, column=2, padx=5, pady=5)
        Button(self.frame, text="حذف", bg="#aa20d3", command=self.delete_admin).grid(row=7, column=3, padx=5, pady=5)
        Button(self.frame, text="إفراغ الحقول", bg="#aa20d3", command=self.clear_fields).grid(row=7, column=4, padx=5, pady=5)

        # الدوال الخاصة بالإداريين
    def load_admins(self):
            # تحميل البيانات من ملف JSON
        try:
            with open('admins.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_admins(self):
            # حفظ البيانات في ملف JSON
        with open('admins.json', 'w', encoding='utf-8') as file:
            json.dump(self.admins, file, ensure_ascii=False, indent=4)

    def update_treeview(self):
            # تحديث TreeView بعد كل عملية
        self.tree22.delete(*self.tree22.get_children())
        for admin in self.admins:
            self.tree22.insert('', 'end', values=(admin['name'], admin['role'], admin['phone'], admin['email'], admin['duration'], admin['start_date'], admin['end_date']))

    def add_admin(self):
            # إضافة إداري جديد
        admin = {
                "name": self.name_entry.get(),
                "role": self.role_entry.get(),
                "phone": self.phone_entry.get(),
                "email": self.email_entry.get(),
                "duration": self.duration_entry.get(),
                "start_date": self.start_date_entry.get(),
                "end_date": self.end_date_entry.get()
            }
        self.admins.append(admin)
        self.save_admins()
        self.update_treeview()
        self.clear_fields()
        messagebox.showinfo("تمت الإضافة", "تمت إضافة الإداري بنجاح!")

    def search_admin(self):
            # البحث عن إداري وعرض بياناته
        name = self.name_entry.get()
        for admin in self.admins:
            if admin['name'] == name:
                self.role_entry.delete(0, END)
                self.role_entry.insert(0, admin['role'])
                self.phone_entry.delete(0, END)
                self.phone_entry.insert(0, admin['phone'])
                self.email_entry.delete(0, END)
                self.email_entry.insert(0, admin['email'])
                self.duration_entry.delete(0, END)
                self.duration_entry.insert(0, admin['duration'])
                self.start_date_entry.delete(0, END)
                self.start_date_entry.insert(0, admin['start_date'])
                self.end_date_entry.delete(0, END)
                self.end_date_entry.insert(0, admin['end_date'])
                return
            messagebox.showerror("خطأ", "لم يتم العثور على الإداري!")

    def update_admin(self):
            # تحديث بيانات الإداري
        name = self.name_entry.get()
        for admin in self.admins:
            if admin['name'] == name:
                admin['role'] = self.role_entry.get()
                admin['phone'] = self.phone_entry.get()
                admin['email'] = self.email_entry.get()
                admin['duration'] = self.duration_entry.get()
                admin['start_date'] = self.start_date_entry.get()
                admin['end_date'] = self.end_date_entry.get()
                self.save_admins()
                self.update_treeview()
                self.clear_fields()
                messagebox.showinfo("تم التحديث", "تم تحديث بيانات الإداري بنجاح!")
                return
            messagebox.showerror("خطأ", "لم يتم العثور على الإداري!")

    def delete_admin(self):
            # حذف إداري
        name = self.name_entry.get()
        self.admins = [admin for admin in self.admins if admin['name'] != name]
        self.save_admins()
        self.update_treeview()
        self.clear_fields()
        messagebox.showinfo("تم الحذف", "تم حذف الإداري بنجاح!")

    def clear_fields(self):
            # إفراغ حقول الإدخال
        self.name_entry.delete(0, END)
        self.role_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.duration_entry.delete(0, END)
        self.start_date_entry.delete(0, END)
        self.end_date_entry.delete(0, END)



    def open_services_interface(self):
        # إنشاء نافذة جديدة
        service_window = Toplevel(self.root)
        service_window.title("الخدمات")
        service_window.geometry("1350x680+5+5")
        service_window.resizable(False, False)
        service_window.configure(bg="#0e0b0b")
        
        # تقسيم النافذة إلى قسمين
        left_frame = Frame(service_window, width=850, height=600, bg="#0e0b0b")
        left_frame.pack(side="left", fill="y")
        
        right_frame = Frame(service_window, width=450, height=600, bg="#0e0b0b")
        right_frame.pack(side="right", fill="y")
        
        # الخدمات التي ستظهر في الصفوف الثلاثة
        services = [
            [{"name": "برامج الديسكتوب", "levels": [100, 200, 300]},
            {"name": "برامج الموبايل", "levels": [120, 220, 340, 500]},
            {"name": "برمجة مواقع الويب", "levels": [100, 180, 260, 340, 500, 700]}],
            
            [{"name": "برمجة نموذج الذكاء الاصطناعي", "levels": [250, 500, 750, 1000]},
            {"name": "تحليل البيانات", "levels": [80, 160, 300]},
            {"name": "الاسكربتات", "levels": [80, 120, 160]}],
            
            [{"name": "الويب سكرايبنج وتجميع البيانات", "levels": [70, 120, 150]},
            {"name": "نظام الاشتراك مع الشركة", "levels": [39, 60, 96], "details": "اشتراك 3 أشهر، 6 أشهر، سنة"}]
        ]
        
        # توزيع الخدمات على الفريمات
        for row, service_row in enumerate(services):
            frame_row = Frame(left_frame, bg="#0e0b0b")
            frame_row.pack(anchor="w", pady=10)
            for service in service_row:
                service_frame =Frame(frame_row, bg="#0e0b0b")
                service_frame.pack(side="left", padx=10)
                Label(service_frame, text=f"{service['name']}", font=("Arial", 12, "bold"), fg="white", bg="#0e0b0b").pack(anchor="w")
                for idx, price in enumerate(service['levels']):
                    level_text = f"المستوى {idx + 1}: {price} دولار"
                    if 'details' in service:
                        level_text += f" ({service['details'].split('،')[idx]})"
                    Label(service_frame, text=level_text, fg="white", bg="#0e0b0b").pack(anchor="w")
        
        # القسم الثاني: إدخال بيانات العميل
        Label(right_frame, text="اسم العميل:", fg="white", bg="#0e0b0b").pack(anchor="w", pady=5)
        client_name = Entry(right_frame, bg="#ffffff", fg="black", font=("Arial", 10))
        client_name.pack(anchor="w", pady=5, fill="x")
        
        Label(right_frame, text="هاتف العميل:", fg="white", bg="#0e0b0b").pack(anchor="w", pady=5)
        client_phone = Entry(right_frame, bg="#ffffff", fg="black", font=("Arial", 10))
        client_phone.pack(anchor="w", pady=5, fill="x")
        
        Label(right_frame, text="إيميل العميل:", fg="white", bg="#0e0b0b").pack(anchor="w", pady=5)
        client_email = Entry(right_frame, bg="#ffffff", fg="black", font=("Arial", 10))
        client_email.pack(anchor="w", pady=5, fill="x")
        
        Label(right_frame, text="الخدمة المطلوبة:", fg="white", bg="#0e0b0b").pack(anchor="w", pady=5)
        client_service = Entry(right_frame, bg="#ffffff", fg="black", font=("Arial", 10))
        client_service.pack(anchor="w", pady=5, fill="x")
        
        Label(right_frame, text="سعر الخدمة:", fg="white", bg="#0e0b0b").pack(anchor="w", pady=5)
        client_price = Entry(right_frame, bg="#ffffff", fg="black", font=("Arial", 10))
        client_price.pack(anchor="w", pady=5, fill="x")
        
        Label(right_frame, text="المسؤول عن العميل:", fg="white", bg="#0e0b0b").pack(anchor="w", pady=5)
        client_responsible = Entry(right_frame, bg="#ffffff", fg="black", font=("Arial", 10))
        client_responsible.pack(anchor="w", pady=5, fill="x")
        
        Label(right_frame, text="وقت الانتهاء من الخدمة:", fg="white", bg="#0e0b0b").pack(anchor="w", pady=5)
        client_end_time = Entry(right_frame, bg="#ffffff", fg="black", font=("Arial", 10))
        client_end_time.pack(anchor="w", pady=5, fill="x")
        
        # دالة لحفظ البيانات في ملف JSON
        def save_data():
            client_data = {
                "name": client_name.get(),
                "phone": client_phone.get(),
                "email": client_email.get(),
                "service": client_service.get(),
                "price": client_price.get(),
                "responsible": client_responsible.get(),
                "end_time": client_end_time.get()
            }
            
            try:
                with open('client_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            data.append(client_data)
            
            with open('client_data.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            messagebox.showinfo("تم الحفظ", "تم حفظ بيانات العميل بنجاح!")
        
        # زر لإضافة طلب الخدمة
        add_service_button = Button(right_frame, text="إضافة طلب الخدمة", command=save_data, bg="#aa20d3", fg="black", font=("Arial", 12))
        add_service_button.pack(anchor="w", pady=10, fill="x")


 

    def transaction_interface(self):
    # إنشاء نافذة جديدة للمعاملات
        transaction_window = Toplevel(self.root)
        transaction_window.title("المعاملات")
        transaction_window.geometry("1350x680+5+5")
        transaction_window.resizable(True, True)  # السماح بتغيير حجم النافذة
        transaction_window.configure(bg="#0e0b0b")

        # إنشاء إطار للتري فيو
        transaction_frame = Frame(transaction_window)
        transaction_frame.pack(padx=10, pady=10, fill="both", expand=True)  # السماح للإطار بالتوسع

        # تحديد الأعمدة
        columns = ("name", "phone", "email", "service", "price", "responsible", "end_time")
        transaction_tree = ttk.Treeview(transaction_frame, columns=columns, show="headings")
        transaction_tree.heading("name", text="اسم العميل")
        transaction_tree.heading("phone", text="هاتف العميل")
        transaction_tree.heading("email", text="إيميل العميل")
        transaction_tree.heading("service", text="الخدمة")
        transaction_tree.heading("price", text="السعر")
        transaction_tree.heading("responsible", text="المسؤول")
        transaction_tree.heading("end_time", text="وقت الانتهاء")

        # ضبط عرض الأعمدة
        transaction_tree.column("name", width=150)
        transaction_tree.column("phone", width=150)
        transaction_tree.column("email", width=200)
        transaction_tree.column("service", width=150)
        transaction_tree.column("price", width=100)
        transaction_tree.column("responsible", width=150)
        transaction_tree.column("end_time", width=150)

        transaction_tree.pack(fill="both", expand=True)

        # إنشاء حقول الإدخال
        input_frame = Frame(transaction_frame, bg="white")
        input_frame.pack(pady=20)

        Label(input_frame, text="اسم العميل:", bg="white", fg="#0e0b0b").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        client_name_entry = Entry(input_frame)
        client_name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="هاتف العميل:", bg="white", fg="#0e0b0b").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        client_phone_entry = Entry(input_frame)
        client_phone_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(input_frame, text="إيميل العميل:", bg="white", fg="#0e0b0b").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        client_email_entry = Entry(input_frame)
        client_email_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(input_frame, text="الخدمة:", bg="white", fg="#0e0b0b").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        client_service_entry = Entry(input_frame)
        client_service_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(input_frame, text="السعر:", bg="white", fg="#0e0b0b").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        client_price_entry = Entry(input_frame)
        client_price_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(input_frame, text="المسؤول:", bg="white", fg="#0e0b0b").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        client_responsible_entry = Entry(input_frame)
        client_responsible_entry.grid(row=5, column=1, padx=5, pady=5)

        Label(input_frame, text="وقت الانتهاء:", bg="white", fg="#0e0b0b").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        client_end_time_entry = Entry(input_frame)
        client_end_time_entry.grid(row=6, column=1, padx=5, pady=5)

        # دالة لتحديث التري فيو من قاعدة البيانات
        def update_treeview():
            for i in transaction_tree.get_children():
                transaction_tree.delete(i)
            try:
                with open('client_data.json', 'r') as f:
                    transactions = json.load(f)
            except FileNotFoundError:
                transactions = []
            for trans in transactions:
                transaction_tree.insert("", "end", values=(
                    trans["name"], trans["phone"], trans["email"], trans["service"],
                    trans["price"], trans["responsible"], trans["end_time"]
                ))

        # دالة لتفريغ حقول الإدخال
        def clear_fields():
            client_name_entry.delete(0, END)
            client_phone_entry.delete(0, END)
            client_email_entry.delete(0, END)
            client_service_entry.delete(0, END)
            client_price_entry.delete(0, END)
            client_responsible_entry.delete(0, END)
            client_end_time_entry.delete(0, END)

        # دالة لحذف معاملة
        def delete_transaction():
            client_name = client_name_entry.get().strip()
            try:
                with open('client_data.json', 'r') as f:
                    transactions = json.load(f)
            except FileNotFoundError:
                transactions = []
            
            transactions = [trans for trans in transactions if trans["name"] != client_name]
            
            with open('client_data.json', 'w') as f:
                json.dump(transactions, f, ensure_ascii=False, indent=4)
            
            update_treeview()
            messagebox.showinfo("تم الحذف", "تم حذف بيانات العميل بنجاح!")
        
        # دالة لتحديث معاملة
        def update_transaction():
            client_name = client_name_entry.get().strip()
            try:
                with open('client_data.json', 'r') as f:
                    transactions = json.load(f)
            except FileNotFoundError:
                transactions = []
            
            for trans in transactions:
                if trans["name"] == client_name:
                    trans["phone"] = client_phone_entry.get().strip()
                    trans["email"] = client_email_entry.get().strip()
                    trans["service"] = client_service_entry.get().strip()
                    trans["price"] = client_price_entry.get().strip()
                    trans["responsible"] = client_responsible_entry.get().strip()
                    trans["end_time"] = client_end_time_entry.get().strip()
                    break
            
            with open('client_data.json', 'w') as f:
                json.dump(transactions, f, ensure_ascii=False, indent=4)
            
            update_treeview()
            messagebox.showinfo("تم التعديل", "تم تعديل بيانات العميل بنجاح!")

        # دالة للبحث عن معاملة
        def search_transaction():
            client_name = client_name_entry.get().strip()
            try:
                with open('client_data.json', 'r') as f:
                    transactions = json.load(f)
            except FileNotFoundError:
                transactions = []
            
            for trans in transactions:
                if trans["name"] == client_name:
                    client_phone_entry.delete(0, END)
                    client_phone_entry.insert(0, trans["phone"])
                    client_email_entry.delete(0, END)
                    client_email_entry.insert(0, trans["email"])
                    client_service_entry.delete(0, END)
                    client_service_entry.insert(0, trans["service"])
                    client_price_entry.delete(0, END)
                    client_price_entry.insert(0, trans["price"])
                    client_responsible_entry.delete(0, END)
                    client_responsible_entry.insert(0, trans["responsible"])
                    client_end_time_entry.delete(0, END)
                    client_end_time_entry.insert(0, trans["end_time"])
                    break

        # إضافة أزرار التحكم
        button_frame = Frame(transaction_window,bg="#0e0b0b")
        button_frame.pack(pady=10)

        Button(button_frame, text="إفراغ الحقول",  bg="#aa20d3",command=clear_fields).grid(row=0, column=0, padx=5, pady=5)
        Button(button_frame, text="حذف المعاملة", bg="#aa20d3",command=delete_transaction).grid(row=0, column=1, padx=5, pady=5)
        Button(button_frame, text="تعديل المعاملة",bg="#aa20d3", command=update_transaction).grid(row=0, column=2, padx=5, pady=5)
        Button(button_frame, text="بحث",bg="#aa20d3", command=search_transaction).grid(row=0, column=3, padx=5, pady=5)

        # تحميل البيانات في التري فيو عند بدء التشغيل
        update_treeview()



    def open_accounting_interface(self):
        # إنشاء نافذة جديدة للحسابات
        accounting_window = Toplevel(self.root)
        accounting_window.title("الحسابات")
        accounting_window.geometry("1350x680+5+5")
        accounting_window.resizable(True, True)
        accounting_window.configure(bg="#0e0b0b")

        # تقسيم النافذة إلى قسمين
        left_frame = Frame(accounting_window, width=850, height=600, bg="#0e0b0b")
        left_frame.pack(side="left", fill="y")

        right_frame = Frame(accounting_window, width=450, height=600, bg="#0e0b0b")
        right_frame.pack(side="right", fill="y")

        # قسم الدواخل
        self.create_incomes_section(left_frame)

        # قسم الخوارج
        self.create_outcomes_section(right_frame)

        # قسم الإجماليات
        self.create_summary_frame(left_frame)

    def create_incomes_section(self, parent_frame):
        # إنشاء إطار للدواخل
        income_frame = Frame(parent_frame, bg="#0e0b0b")
        income_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # تحديد الأعمدة للتري فيو
        columns = ("client_name", "service", "total_amount", "paid_amount", "remaining_amount", "payment_date")
        income_tree = ttk.Treeview(income_frame, columns=columns, show="headings")
        income_tree.heading("client_name", text="اسم العميل")
        income_tree.heading("service", text="الخدمة")
        income_tree.heading("total_amount", text="السعر الكلي")
        income_tree.heading("paid_amount", text="المبلغ المدفوع")
        income_tree.heading("remaining_amount", text="المبلغ المتبقي")
        income_tree.heading("payment_date", text="تاريخ الدفع")

        # ضبط عرض الأعمدة
        income_tree.column("client_name", width=150)
        income_tree.column("service", width=150)
        income_tree.column("total_amount", width=100)
        income_tree.column("paid_amount", width=100)
        income_tree.column("remaining_amount", width=100)
        income_tree.column("payment_date", width=150)

        income_tree.pack(fill="both", expand=True)

        # إنشاء حقول الإدخال
        input_frame = Frame(income_frame, bg="white")
        input_frame.pack(pady=20)

        Label(input_frame, text="اسم العميل:", bg="white", fg="#0e0b0b").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.client_name_entry = Entry(input_frame)
        self.client_name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="الخدمة:", bg="white", fg="#0e0b0b").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.service_entry = Entry(input_frame)
        self.service_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(input_frame, text="السعر الكلي:", bg="white", fg="#0e0b0b").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.total_amount_entry = Entry(input_frame)
        self.total_amount_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(input_frame, text="المبلغ المدفوع:", bg="white", fg="#0e0b0b").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.paid_amount_entry = Entry(input_frame)
        self.paid_amount_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(input_frame, text="المبلغ المتبقي:", bg="white", fg="#0e0b0b").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.remaining_amount_entry = Entry(input_frame)
        self.remaining_amount_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(input_frame, text="تاريخ الدفع:", bg="white", fg="#0e0b0b").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.payment_date_entry = Entry(input_frame)
        self.payment_date_entry.grid(row=5, column=1, padx=5, pady=5)

        # دالة لتحديث التري فيو من قاعدة البيانات
        def update_income_treeview():
            for i in income_tree.get_children():
                income_tree.delete(i)
            try:
                with open('income_data.json', 'r') as f:
                    incomes = json.load(f)
            except FileNotFoundError:
                incomes = []
            for income in incomes:
                income_tree.insert("", "end", values=(
                    income["client_name"], income["service"], income["total_amount"], income["paid_amount"],
                    income["remaining_amount"], income["payment_date"]
                ))

        # دالة للتحقق من وجود العميل في قاعدة بيانات العملاء
        def validate_client(client_name):
            try:
                with open('client_data.json', 'r') as f:
                    clients = json.load(f)
            except FileNotFoundError:
                clients = []
            return any(client["name"] == client_name for client in clients)

        # دالة لحفظ بيانات الدخل
        def save_income():
            client_name = self.client_name_entry.get().strip()
            if not validate_client(client_name):
                messagebox.showerror("خطأ", "اسم العميل غير مسجل في قاعدة البيانات!")
                return
            
            income_data = {
                "client_name": client_name,
                "service": self.service_entry.get().strip(),
                "total_amount": self.total_amount_entry.get().strip(),
                "paid_amount": self.paid_amount_entry.get().strip(),
                "remaining_amount": self.remaining_amount_entry.get().strip(),
                "payment_date": self.payment_date_entry.get().strip()
            }
            
            try:
                with open('income_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            data.append(income_data)
            
            with open('income_data.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            update_income_treeview()
            self.update_summary()
            messagebox.showinfo("تم الحفظ", "تم حفظ بيانات الدخل بنجاح!")

        # دالة لتفريغ حقول الإدخال
        def clear_income_fields():
            self.client_name_entry.delete(0, END)
            self.service_entry.delete(0, END)
            self.total_amount_entry.delete(0, END)
            self.paid_amount_entry.delete(0, END)
            self.remaining_amount_entry.delete(0, END)
            self.payment_date_entry.delete(0, END)

        # دالة لحذف دخل
        def delete_income():
            client_name = self.client_name_entry.get().strip()
            try:
                with open('income_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            data = [income for income in data if income["client_name"] != client_name]
            
            with open('income_data.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            update_income_treeview()
            self.update_summary()
            messagebox.showinfo("تم الحذف", "تم حذف بيانات الدخل بنجاح!")

        # دالة لتحديث دخل
        def update_income():
            client_name = self.client_name_entry.get().strip()
            try:
                with open('income_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            for income in data:
                if income["client_name"] == client_name:
                    income["service"] = self.service_entry.get().strip()
                    income["total_amount"] = self.total_amount_entry.get().strip()
                    income["paid_amount"] = self.paid_amount_entry.get().strip()
                    income["remaining_amount"] = self.remaining_amount_entry.get().strip()
                    income["payment_date"] = self.payment_date_entry.get().strip()
                    break
            
            with open('income_data.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            update_income_treeview()
            self.update_summary()
            messagebox.showinfo("تم التعديل", "تم تعديل بيانات الدخل بنجاح!")

        # دالة للبحث عن دخل
        def search_income():
            client_name = self.client_name_entry.get().strip()
            try:
                with open('income_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            for income in data:
                if income["client_name"] == client_name:
                    self.service_entry.delete(0, END)
                    self.service_entry.insert(0, income["service"])
                    self.total_amount_entry.delete(0, END)
                    self.total_amount_entry.insert(0, income["total_amount"])
                    self.paid_amount_entry.delete(0, END)
                    self.paid_amount_entry.insert(0, income["paid_amount"])
                    self.remaining_amount_entry.delete(0, END)
                    self.remaining_amount_entry.insert(0, income["remaining_amount"])
                    self.payment_date_entry.delete(0, END)
                    self.payment_date_entry.insert(0, income["payment_date"])
                    break
            else:
                messagebox.showinfo("لم يتم العثور على بيانات", "لم يتم العثور على بيانات للدخل!")

        # أزرار التفاعل مع قسم الدخل
        Button(input_frame, text="حفظ", command=save_income, bg="#d9e2ec").grid(row=6, column=0, padx=5, pady=5, sticky="ew")
        Button(input_frame, text="تحديث", command=update_income, bg="#d9e2ec").grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        Button(input_frame, text="حذف", command=delete_income, bg="#d9e2ec").grid(row=7, column=0, padx=5, pady=5, sticky="ew")
        Button(input_frame, text="بحث", command=search_income, bg="#d9e2ec").grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        Button(input_frame, text="تفريغ", command=clear_income_fields, bg="#d9e2ec").grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # تحديث التري فيو عند فتح النافذة
        update_income_treeview()

    def create_outcomes_section(self, parent_frame):
        outcome_frame = Frame(parent_frame, bg="#0e0b0b")
        outcome_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("outcome_party", "amount", "manager")
        outcome_tree = ttk.Treeview(outcome_frame, columns=columns, show="headings")
        outcome_tree.heading("outcome_party", text="الطرف المستفيد")
        outcome_tree.heading("amount", text="المبلغ")
        outcome_tree.heading("manager", text="المدير")

        outcome_tree.column("outcome_party", width=200)
        outcome_tree.column("amount", width=100)
        outcome_tree.column("manager", width=200)

        outcome_tree.pack(fill="both", expand=True)

        input_frame = Frame(outcome_frame, bg="white")
        input_frame.pack(pady=20)

        Label(input_frame, text="الطرف المستفيد:", bg="white", fg="#0e0b0b").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.outcome_party_entry = Entry(input_frame)
        self.outcome_party_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="المبلغ:", bg="white", fg="#0e0b0b").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(input_frame, text="المدير:", bg="white", fg="#0e0b0b").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.manager_entry = Entry(input_frame)
        self.manager_entry.grid(row=2, column=1, padx=5, pady=5)

        def update_outcome_treeview():
            for i in outcome_tree.get_children():
                outcome_tree.delete(i)
            try:
                with open('outcome_data.json', 'r') as f:
                    outcomes = json.load(f)
            except FileNotFoundError:
                outcomes = []
            for outcome in outcomes:
                outcome_tree.insert("", "end", values=(
                    outcome["outcome_party"], outcome["amount"], outcome["manager"]
                ))

        def save_outcome():
            outcome_data = {
                "outcome_party": self.outcome_party_entry.get().strip(),
                "amount": self.amount_entry.get().strip(),
                "manager": self.manager_entry.get().strip()
            }
            
            try:
                with open('outcome_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            data.append(outcome_data)
            
            with open('outcome_data.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            update_outcome_treeview()
            self.update_summary()
            messagebox.showinfo("تم الحفظ", "تم حفظ بيانات الخرج بنجاح!")

        def clear_outcome_fields():
            self.outcome_party_entry.delete(0, END)
            self.amount_entry.delete(0, END)
            self.manager_entry.delete(0, END)

        def delete_outcome():
            outcome_party = self.outcome_party_entry.get().strip()
            try:
                with open('outcome_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            data = [outcome for outcome in data if outcome["outcome_party"] != outcome_party]
            
            with open('outcome_data.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            update_outcome_treeview()
            self.update_summary()
            messagebox.showinfo("تم الحذف", "تم حذف بيانات الخرج بنجاح!")

        def update_outcome():
            outcome_party = self.outcome_party_entry.get().strip()
            try:
                with open('outcome_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            for outcome in data:
                if outcome["outcome_party"] == outcome_party:
                    outcome["amount"] = self.amount_entry.get().strip()
                    outcome["manager"] = self.manager_entry.get().strip()
                    break
            
            with open('outcome_data.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            update_outcome_treeview()
            self.update_summary()
            messagebox.showinfo("تم التعديل", "تم تعديل بيانات الخرج بنجاح!")

        def search_outcome():
            outcome_party = self.outcome_party_entry.get().strip()
            try:
                with open('outcome_data.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            
            for outcome in data:
                if outcome["outcome_party"] == outcome_party:
                    self.amount_entry.delete(0, END)
                    self.amount_entry.insert(0, outcome["amount"])
                    self.manager_entry.delete(0, END)
                    self.manager_entry.insert(0, outcome["manager"])
                    break
            else:
                messagebox.showinfo("لم يتم العثور على بيانات", "لم يتم العثور على بيانات للخرج!")

        Button(input_frame, text="حفظ", command=save_outcome, bg="#d9e2ec").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        Button(input_frame, text="تحديث", command=update_outcome, bg="#d9e2ec").grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        Button(input_frame, text="حذف", command=delete_outcome, bg="#d9e2ec").grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        Button(input_frame, text="بحث", command=search_outcome, bg="#d9e2ec").grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        Button(input_frame, text="تفريغ", command=clear_outcome_fields, bg="#d9e2ec").grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        update_outcome_treeview()

    def create_summary_frame(self, parent_frame):
        summary_frame = Frame(parent_frame, bg="#0e0b0b")
        summary_frame.pack(pady=20)

        self.total_incomes_label = Label(summary_frame, text="إجمالي الدخل:", bg="#0e0b0b", fg="white")
        self.total_incomes_label.pack()

        self.total_outcomes_label = Label(summary_frame, text="إجمالي الخرج:", bg="#0e0b0b", fg="white")
        self.total_outcomes_label.pack()

        self.net_balance_label = Label(summary_frame, text="الرصيد الصافي:", bg="#0e0b0b", fg="white")
        self.net_balance_label.pack()

    def update_summary(self):
        try:
            with open('income_data.json', 'r') as f:
                income_data = json.load(f)
        except FileNotFoundError:
            income_data = []
        
        total_incomes = sum(float(income["total_amount"]) for income in income_data)
        
        try:
            with open('outcome_data.json', 'r') as f:
                outcome_data = json.load(f)
        except FileNotFoundError:
            outcome_data = []
        
        total_outcomes = sum(float(outcome["amount"]) for outcome in outcome_data)
        
        net_balance = total_incomes - total_outcomes

        self.total_incomes_label.config(text=f"إجمالي الدخل: {total_incomes}")
        self.total_outcomes_label.config(text=f"إجمالي الخرج: {total_outcomes}")
        self.net_balance_label.config(text=f"الرصيد الصافي: {net_balance}")


    def show_message(self, message):
        messagebox.showinfo("معلومات", f"تم النقر على {message}")

if __name__ == "__main__":
    root = Tk()
    app = CreativeCodeApp(root)
    root.mainloop()
