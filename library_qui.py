import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from Library import Library
from User import User
from Book import Book
from library_db import LibraryDB

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # ตั้งค่าขนาดและตำแหน่งหน้าจอ
        self.root.geometry("400x300+500+200")  # กว้าง x สูง + ตำแหน่ง X + ตำแหน่ง Y

        # เฟรมสำหรับช่องข้อความชื่อผู้ใช้และรหัสผ่าน
        self.frame = tk.Frame(root)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label_username = tk.Label(self.frame, text="Username:")
        self.label_password = tk.Label(self.frame, text="Password:")

        self.entry_username = tk.Entry(self.frame)
        self.entry_password = tk.Entry(self.frame, show="*")

        self.label_username.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.label_password.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        # ปุ่มเข้าสู่ระบบ
        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "admin":

            self.open_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_main_menu(self):
        self.root.destroy() # ปิดหน้าจอเข้าสู่ระบบ

        # สร้างเมนูหลัก
        main_menu_root = tk.Tk()
        main_menu_app = LibraryGUI(main_menu_root)
        main_menu_root.protocol("WM_DELETE_WINDOW", main_menu_app.destroy)
        main_menu_root.mainloop()


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        # ตั้งค่าขนาดหน้าจอ
        self.root.geometry("800x600")

        # ตั้งค่าตำแหน่งหน้าจอ
        self.root.geometry("+300+100")

        self.library = Library()

        # สร้างเฟรมสำหรับปุ่มบนหน้าจอหลัก
        self.main_menu_frame = tk.Frame(root)
        self.main_menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        book_operations_button = tk.Button(self.main_menu_frame, text="Book Operations", width=20,
                                           command=self.show_book_operations)
        book_operations_button.grid(row=0, pady=5)

        user_operations_button = tk.Button(self.main_menu_frame, text="User Operations", width=20,
                                           command=self.show_user_operations)
        user_operations_button.grid(row=1, pady=5)

    def show_book_operations(self):
        book_operations_gui = BookOperationsGUI(self.root, self.library, self.show_main_menu)

    def show_user_operations(self):
        user_operations_gui = UserOperationsGUI(self.root, self.library, self.show_main_menu)

    def show_main_menu(self):
        # ใช้คลาส LibraryGUI อีกครั้งเพื่อแสดงเมนูหลัก
        self.main_menu_frame.grid()

    def destroy(self):
        self.root.destroy()


class BookOperationsGUI:
    def __init__(self, root, library, show_main_menu_method):
        self.root = root
        self.root.title("Book Operations")

        self.root.geometry("1000x600")

        self.root.geometry("+300+100")

        self.library = library
        self.library_db = LibraryDB()

        # สร้างเฟรมสำหรับจัดการหนังสือ
        self.book_operations_frame = tk.Frame(root)
        self.book_operations_frame.place(relx=0.1, rely=0.5, anchor=tk.W, relwidth=0.8, relheight=0.8)

        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # แสดงรายการหนังสือใน Treeview widget
        self.tree = ttk.Treeview(self.right_frame,
                                 columns=("Title", "Author", "ISBN", "Category", "is_borrowed", "Borrower"), height=20)
        self.tree.heading("#0", text=" ")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Category", text="Category")
        self.tree.heading("is_borrowed", text="Is Borrowed")
        self.tree.heading("Borrower", text="Borrower")

        self.tree.column("#0", stretch=tk.NO, width=0)
        self.tree.column("Title", stretch=tk.YES, width=150)
        self.tree.column("Author", stretch=tk.YES, width=150)
        self.tree.column("ISBN", stretch=tk.YES, width=100)
        self.tree.column("Category", stretch=tk.YES, width=100)
        self.tree.column("is_borrowed", stretch=tk.YES, width=100)
        self.tree.column("Borrower", stretch=tk.YES, width=100)

        self.tree.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky=tk.W)

        title_label = tk.Label(self.right_frame, text="LIST OF BOOKS", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, pady=10, columnspan=3)

        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.add_book_frame = tk.Frame(self.left_frame)
        self.add_book_frame.grid(row=2, column=0, pady=10, columnspan=3, sticky=tk.E)

        # เพิ่มปุ่ม "Add book"
        title_label = tk.Label(self.add_book_frame, text="Title:")
        title_label.grid(row=0, column=0, pady=10, sticky=tk.W)

        self.title_var = tk.StringVar()
        title_entry = tk.Entry(self.add_book_frame, textvariable=self.title_var)
        title_entry.grid(row=0, column=1, pady=10, sticky=tk.W)

        author_label = tk.Label(self.add_book_frame, text="Author:")
        author_label.grid(row=1, column=0, pady=10, sticky=tk.W)

        self.author_var = tk.StringVar()
        author_entry = tk.Entry(self.add_book_frame, textvariable=self.author_var)
        author_entry.grid(row=1, column=1, pady=10, sticky=tk.W)

        isbn_label = tk.Label(self.add_book_frame, text="ISBN:")
        isbn_label.grid(row=2, column=0, pady=10, sticky=tk.W)

        self.isbn_var = tk.StringVar()
        isbn_entry = tk.Entry(self.add_book_frame, textvariable=self.isbn_var)
        isbn_entry.grid(row=2, column=1, pady=10, sticky=tk.W)

        category_label = tk.Label(self.add_book_frame, text="Category:")
        category_label.grid(row=3, column=0, pady=10, sticky=tk.W)

        self.category_var = tk.StringVar()
        category_entry = tk.Entry(self.add_book_frame, textvariable=self.category_var)
        category_entry.grid(row=3, column=1, pady=10, sticky=tk.W)

        self.is_borrowed_var = tk.IntVar(value=0)

        is_borrowed_checkbutton = tk.Checkbutton(
            self.add_book_frame,
            text="Is Borrowed",
            variable=self.is_borrowed_var
        )
        is_borrowed_checkbutton.grid(row=4, column=0, pady=10, sticky=tk.W)

        # ดึงข้อมูลรายการหนังสือ
        add_book_button_inside = tk.Button(self.add_book_frame, text="Add Book",
                                           command=lambda: self.add_book_action(self.title_var.get(),
                                                                                self.author_var.get(),
                                                                                self.isbn_var.get(),
                                                                                self.category_var.get(),
                                                                                self.is_borrowed_var.get()))
        add_book_button_inside.grid(row=4, column=1, pady=10, sticky=tk.W)

        availability_button = tk.Button(self.right_frame, text="Change Availability", width=20,
                                        command=self.toggle_availability)
        availability_button.grid(row=2, column=0, pady=5, padx=5, sticky=tk.S)

        remove_book_button = tk.Button(self.right_frame, text="Remove a Book", width=20,
                                       command=self.remove_selected_book)
        remove_book_button.grid(row=2, column=1, pady=5, padx=5, sticky=tk.S)

        back_button = tk.Button(self.right_frame, text="Back to Main Menu", width=20, command=self.back_to_main_menu)
        back_button.grid(row=2, column=2, pady=5, padx=5, sticky=tk.S)

        self.list_books()

    def list_books(self):
        books_list = self.library_db.list_books()

        # แสดงรายการหนังสืv
        self.tree.delete(*self.tree.get_children())  # ล้างรายการ

        if books_list:
            for i, book in enumerate(books_list):
                if book:
                    title = book.get('title', '')[:30]
                    author = book.get('author', '')[:30]
                    isbn = book.get('ISBN', '')[:25]
                    category = book.get('category', '')[:25]
                    is_borrowed = book.get('is_borrowed', '')
                    borrower = book.get('borrower', '') if is_borrowed else ""

                    # เพิ่มข้อมูลหนังสือแต่ละเล่มลงใน Treeview widget
                    item_id = self.tree.insert("", i, values=(title, author, isbn, category, is_borrowed, borrower))

                    # เก็บ ID ของหนังสือที่เพิ่มใหม่เป็น tag
                    self.tree.item(item_id, tags=(book.get('id'),))

    def clear_add_book_fields(self):
        # ล้างข้อมูลในช่องป้อนข้อมูล
        self.title_var.set("")
        self.author_var.set("")
        self.isbn_var.set("")
        self.category_var.set("")
        self.is_borrowed_var.set(0)

    def add_book_action(self, title, author, isbn, category, is_borrowed):
        borrower_name = None

        if is_borrowed == 1:
            # ตรวจสอบว่าหนังสือถูกยืมหรือไม่ รับข้อมูลผู้ยืมจากผู้ใช้
            borrower_name = simpledialog.askstring("Borrower Information", "Enter the borrower's name:")

        # สร้างวัตถุหนังสือ
        new_book = Book(title, author, isbn, category, is_borrowed, borrower_name)

        # เพิ่มหนังสือในไลบรารี
        self.library.add_book(new_book)

        # อัปเดตรายการหนังสือบนหน้าจอหากหนังสือถูกเพิ่มสำเร็จ
        self.list_books()

        self.clear_add_book_fields()

    def remove_selected_book(self):
        # ลบหนังสือที่เลือกเมื่อคลิกปุ่ม "Remove a Book"
        selected_item = self.tree.selection()

        if selected_item:
            # ดึงดัชนีของรายการที่เลือก
            item_id = selected_item[0]

            # ลบรายการที่เลือกออกจาก Treeview และฐานข้อมูล
            book_id = self.tree.item(item_id, 'tags')[0]  # เก็บ ID ของหนังสือที่เพิ่มใหม่
            self.tree.delete(item_id)
            self.library_db.remove_book_by_id(book_id)

            messagebox.showinfo("Success", f"Selected Book Removed")

    def toggle_availability(self):
        # เปลี่ยนสถานะของหนังสือที่เลือกเมื่อคลิกปุ่ม "Toggle Availability"
        selected_item = self.tree.selection()

        if selected_item:
            # เปลี่ยนสถานะของหนังสือที่เลือก
            item_id = selected_item[0]
            book_id = self.tree.item(item_id, 'tags')[0]  # เก็บ ID ของหนังสือที่เพิ่มใหม่
            current_availability = self.tree.item(item_id, 'values')[4]  # ดึงค่า "is_borrowed" ของหนังสือ

            # เปลี่ยนสถานะของหนังสือ (จาก "ยืมได้" เป็น "ยืมไม่ได้" หรือจาก "ยืมไม่ได้" เป็น "ยืมได้")
            new_availability = 1 if current_availability == 0 else 0

            # อัปเดตค่า "is_borrowed" ของหนังสือในฐานข้อมูล
            self.tree.item(item_id, values=(
                    self.tree.item(item_id, 'values')[0:4] + (new_availability,) + self.tree.item(item_id,
                                                                                                  'values')[5:]))

            # เพิ่มหรือลบข้อมูลผู้ยืมตามสถานะของหนังสือ
            if new_availability == 1:
                # เปลี่ยนสถานะหนังสือจาก "ยืมไม่ได้" เป็น "ยืมได้" และรับชื่อผู้ยืม 
                borrower_name = simpledialog.askstring("Borrower Information", "Enter the borrower's name:")
                self.tree.item(item_id, values=(self.tree.item(item_id, 'values')[0:5] + (borrower_name,)))
            else:
                # เปลี่ยนสถานะหนังสือจาก "ยืมได้" เป็น "ยืมไม่ได้" และลบชื่อผู้ยืม
                self.tree.item(item_id, values=(self.tree.item(item_id, 'values')[0:5] + ("",)))

            # อัปเดตฐานข้อมูล
            self.library_db.toggle_availability(book_id)

            self.list_books()

    def back_to_main_menu(self):
        self.root.destroy()  #  ปิดหน้าจอ Book Operations

        # สร้างเมนูหลัก
        main_menu_root = tk.Tk()
        main_menu_app = LibraryGUI(main_menu_root)
        main_menu_root.protocol("WM_DELETE_WINDOW", main_menu_app.destroy)
        main_menu_root.mainloop()


class UserOperationsGUI:
    def __init__(self, root, library, back_to_main_menu_method):
        self.root = root
        self.root.title("User Operations")
        self.root.geometry("600x400")
        self.root.geometry("+300+100")

        self.library = library
        self.library_db = LibraryDB()

        self.user_operations_frame = tk.Frame(root)
        self.user_operations_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        list_users_button = tk.Button(self.user_operations_frame, text="List All Users", width=20,
                                      command=self.list_users)
        list_users_button.grid(row=0, column=0, pady=5)

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        add_user_button = tk.Button(self.user_operations_frame, text="Add a User", width=20, command=self.add_user)
        add_user_button.grid(row=4, column=0, pady=5, sticky=tk.E)

        self.users_frame = tk.Frame(self.user_operations_frame)
        self.users_frame.grid(row=3, column=0, pady=10, columnspan=3)

        users_list_label = tk.Label(self.users_frame, text="List of All Users", font=("Helvetica", 16, "bold"))
        users_list_label.pack()

        self.users_listbox = tk.Listbox(self.users_frame, selectmode=tk.MULTIPLE, height=10, width=60)
        self.users_listbox.pack()

        remove_user_button = tk.Button(self.user_operations_frame, text="Remove Selected Users", width=20,
                                       command=self.remove_selected_users)
        remove_user_button.grid(row=4, column=1, pady=10, columnspan=3, sticky=tk.W)

        search_name_label = tk.Label(self.user_operations_frame, text="Enter name to search:")
        search_name_label.grid(row=2, column=0, pady=5)

        self.search_name_var = tk.StringVar()
        search_name_entry = tk.Entry(self.user_operations_frame, textvariable=self.search_name_var)
        search_name_entry.grid(row=2, column=1, pady=5)

        search_button = tk.Button(self.user_operations_frame, text="Search by Name", width=20,
                                  command=self.search_users_by_name)
        search_button.grid(row=2, column=2, pady=5)

        back_button = tk.Button(self.user_operations_frame, text="Back to Main Menu", width=20,
                                command=self.back_to_main_menu)
        back_button.grid(row=4, column=2, pady=10, sticky=tk.SW)

    def clear_entry_fields(self):
        self.name_var.set("")
        self.email_var.set("")

    def add_user(self):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Add a User")

        name_label = tk.Label(add_user_window, text="Name:")
        name_label.grid(row=0, column=0, pady=10)

        name_entry = tk.Entry(add_user_window, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, pady=10)

        email_label = tk.Label(add_user_window, text="Email:")
        email_label.grid(row=1, column=0, pady=10)

        email_entry = tk.Entry(add_user_window, textvariable=self.email_var)
        email_entry.grid(row=1, column=1, pady=10)

        add_button = tk.Button(add_user_window, text="Add", command=self.add_user_action)
        add_button.grid(row=2, column=1, pady=10)

    def add_user_action(self):
        name = self.name_var.get()
        email = self.email_var.get()

        if name and email:
            new_user = User(name, email)
            result = self.library.add_user(new_user)

            if result:
                messagebox.showinfo("Success", f"{name} added as a user.")
                self.clear_entry_fields()
            else:
                messagebox.showwarning("Warning", "User with the same name already exists.")
        else:
            messagebox.showwarning("Warning", "Please enter both name and email.")

    def list_users(self):
        users_window = tk.Toplevel(self.root)
        users_window.title("List of All Users")

        users_text = tk.Text(users_window, height=0, width=0)
        users_text.grid(row=0, column=0, padx=10, pady=10)

        users_list = self.library_db.list_users()
        if users_list:
            self.users_listbox.insert(tk.END, "{:<30} {:<30}".format("Name", "Email"))
            self.users_listbox.insert(tk.END, "-" * 60)

            for user in users_list:
                self.users_listbox.insert(tk.END, f"{user['name']} - {user['email']}")
        else:
            users_text.insert(tk.END, "No users in the library.")

    def remove_selected_users(self):
        selected_indices = self.users_listbox.curselection()

        if selected_indices:
            for index in selected_indices[::-1]:  # วนลูปผ่านข้อมูลผู้ใช้ในลำดับที่ย้อนกลับเพื่อป้องกันการเปลี่ยนแปลงดัชนีระหว่างการลบ
                username = self.users_listbox.get(index).split(" - ")[0]
                self.library_db.remove_user_by_name(username)
                self.users_listbox.delete(index)

    def search_users_by_name(self):
        search_name = self.search_name_var.get().strip()
        if search_name:
            result_window = tk.Toplevel(self.root)
            result_window.title("Search Result by Name")

            result_text = tk.Text(result_window, height=5, width=30)
            result_text.grid(row=0, column=0, pady=10)

            # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
            users_list = self.library_db.list_users()

            found_users = [user for user in users_list if search_name.lower() in user['name'].lower()]
            if found_users:
                result_text.insert(tk.END, "Search Result:\n")
                for user in found_users:
                    result_text.insert(tk.END, f"{user['name']} - {user['email']}\n")
            else:
                result_text.insert(tk.END, f"No result found for '{search_name}'")
        else:
            messagebox.showwarning("Warning", "Please enter a name to search.")

    def back_to_main_menu(self):
        self.root.destroy()  # ปิดหน้าจอ Book Operations

        # สร้างเมนูหลัก
        main_menu_root = tk.Tk()
        main_menu_app = LibraryGUI(main_menu_root)
        main_menu_root.protocol("WM_DELETE_WINDOW", main_menu_app.destroy)
        main_menu_root.mainloop()
