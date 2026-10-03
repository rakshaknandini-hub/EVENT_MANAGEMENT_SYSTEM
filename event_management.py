import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime


# ==========================================================
# COLORS / THEME
# ==========================================================

BG_COLOR = "#F4F7FC"
HEADER_COLOR = "#4F46E5"
BLUE = "#3B82F6"
GREEN = "#10B981"
PURPLE = "#8B5CF6"
ORANGE = "#F59E0B"
RED = "#EF4444"
GREY = "#64748B"
DARK = "#1E293B"
WHITE = "#FFFFFF"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def connect_database():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nandini@2007",
            database="event_management"
        )

        return connection

    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not connect to MySQL.\n\n{e}"
        )
        return None


# ==========================================================
# CLEAR SCREEN
# ==========================================================

def clear_screen():

    for widget in root.winfo_children():
        widget.destroy()


# ==========================================================
# LOGIN
# ==========================================================

def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "admin" and password == "admin123":

        messagebox.showinfo(
            "Login",
            "Login Successful!"
        )

        dashboard()

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password."
        )


# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    result = messagebox.askyesno(
        "Logout",
        "Do you want to logout?"
    )

    if result:
        login_page()


# ==========================================================
# LOGIN PAGE
# ==========================================================

def login_page():

    clear_screen()

    root.configure(bg=BG_COLOR)

    # Header
    header = tk.Frame(
        root,
        bg=HEADER_COLOR,
        height=120
    )
    header.pack(fill="x")

    tk.Label(
        header,
        text="EVENT MANAGEMENT SYSTEM",
        font=("Arial", 25, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=(22, 5))

    tk.Label(
        header,
        text="Manage • Organize • Track Events",
        font=("Arial", 11),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack()

    # Login card
    login_card = tk.Frame(
        root,
        bg=WHITE,
        padx=45,
        pady=35
    )
    login_card.pack(pady=50)

    tk.Label(
        login_card,
        text="Welcome Back!",
        font=("Arial", 21, "bold"),
        bg=WHITE,
        fg=DARK
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        pady=(0, 25)
    )

    # Username
    tk.Label(
        login_card,
        text="Username",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).grid(
        row=1,
        column=0,
        sticky="w",
        pady=5
    )

    global username_entry

    username_entry = tk.Entry(
        login_card,
        width=32,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )
    username_entry.grid(
        row=2,
        column=0,
        columnspan=2,
        ipady=7,
        pady=(0, 15)
    )

    # Password
    tk.Label(
        login_card,
        text="Password",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).grid(
        row=3,
        column=0,
        sticky="w",
        pady=5
    )

    global password_entry

    password_entry = tk.Entry(
        login_card,
        width=32,
        font=("Arial", 11),
        show="*",
        relief="solid",
        bd=1
    )
    password_entry.grid(
        row=4,
        column=0,
        columnspan=2,
        ipady=7,
        pady=(0, 20)
    )

    # Login button
    tk.Button(
        login_card,
        text="LOGIN",
        width=25,
        height=2,
        font=("Arial", 11, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground="#2563EB",
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=login
    ).grid(
        row=5,
        column=0,
        columnspan=2
    )

    tk.Label(
        login_card,
        text="Demo Login: admin / admin123",
        font=("Arial", 9),
        bg=WHITE,
        fg=GREY
    ).grid(
        row=6,
        column=0,
        columnspan=2,
        pady=(15, 0)
    )


# ==========================================================
# EVENT COUNTS
# ==========================================================

def get_event_counts():

    total = 0
    upcoming = 0

    connection = connect_database()

    if connection is None:
        return total, upcoming

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM events"
        )
        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM events WHERE event_date >= CURDATE()"
        )
        upcoming = cursor.fetchone()[0]

    except Error:
        pass

    finally:

        cursor.close()
        connection.close()

    return total, upcoming


# ==========================================================
# DASHBOARD
# ==========================================================

def dashboard():

    clear_screen()

    root.configure(bg=BG_COLOR)

    # Header
    header = tk.Frame(
        root,
        bg=HEADER_COLOR,
        height=90
    )
    header.pack(fill="x")

    tk.Label(
        header,
        text="EVENT MANAGEMENT SYSTEM",
        font=("Arial", 23, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(pady=(15, 2))

    tk.Label(
        header,
        text="Dashboard",
        font=("Arial", 11),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack()

    # Statistics
    total_events, upcoming_events = get_event_counts()

    stats_frame = tk.Frame(
        root,
        bg=BG_COLOR
    )
    stats_frame.pack(pady=25)

    # Total events
    total_card = tk.Frame(
        stats_frame,
        bg=WHITE,
        padx=45,
        pady=15
    )
    total_card.grid(
        row=0,
        column=0,
        padx=15
    )

    tk.Label(
        total_card,
        text="TOTAL EVENTS",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=GREY
    ).pack()

    tk.Label(
        total_card,
        text=str(total_events),
        font=("Arial", 25, "bold"),
        bg=WHITE,
        fg=BLUE
    ).pack()

    # Upcoming events
    upcoming_card = tk.Frame(
        stats_frame,
        bg=WHITE,
        padx=45,
        pady=15
    )
    upcoming_card.grid(
        row=0,
        column=1,
        padx=15
    )

    tk.Label(
        upcoming_card,
        text="UPCOMING EVENTS",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=GREY
    ).pack()

    tk.Label(
        upcoming_card,
        text=str(upcoming_events),
        font=("Arial", 25, "bold"),
        bg=WHITE,
        fg=GREEN
    ).pack()

    # Buttons
    button_frame = tk.Frame(
        root,
        bg=BG_COLOR
    )
    button_frame.pack(pady=10)

    create_button(
        button_frame,
        "ADD EVENT",
        GREEN,
        add_event,
        0,
        0
    )

    create_button(
        button_frame,
        "VIEW EVENTS",
        BLUE,
        view_events,
        0,
        1
    )

    create_button(
        button_frame,
        "SEARCH EVENT",
        PURPLE,
        search_event,
        1,
        0
    )

    create_button(
        button_frame,
        "UPDATE EVENT",
        ORANGE,
        update_event,
        1,
        1
    )

    create_button(
        button_frame,
        "DELETE EVENT",
        RED,
        delete_event,
        2,
        0
    )

    create_button(
        button_frame,
        "LOGOUT",
        GREY,
        logout,
        2,
        1
    )


# ==========================================================
# COLORED BUTTON
# ==========================================================

def create_button(
    parent,
    text,
    color,
    command,
    row,
    column
):

    tk.Button(
        parent,
        text=text,
        width=20,
        height=2,
        font=("Arial", 11, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=command
    ).grid(
        row=row,
        column=column,
        padx=15,
        pady=10
    )


# ==========================================================
# ADD EVENT
# ==========================================================

def add_event():

    clear_screen()

    root.configure(bg=BG_COLOR)

    # Header
    header = tk.Frame(
        root,
        bg=GREEN,
        height=90
    )
    header.pack(fill="x")

    tk.Label(
        header,
        text="ADD NEW EVENT",
        font=("Arial", 24, "bold"),
        bg=GREEN,
        fg=WHITE
    ).pack(pady=(15, 2))

    tk.Label(
        header,
        text="Create and save a new event",
        font=("Arial", 11),
        bg=GREEN,
        fg=WHITE
    ).pack()

    # Form
    form_card = tk.Frame(
        root,
        bg=WHITE,
        padx=40,
        pady=25
    )
    form_card.pack(pady=25)

    tk.Label(
        form_card,
        text="Event Information",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=DARK
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="w",
        pady=(0, 15)
    )

    create_form_fields(form_card)

    tk.Label(
        form_card,
        text="Date format: YYYY-MM-DD  (Example: 2026-10-15)",
        font=("Arial", 9),
        bg=WHITE,
        fg=GREY
    ).grid(
        row=7,
        column=1,
        sticky="w",
        padx=10
    )

    # Buttons
    button_frame = tk.Frame(
        root,
        bg=BG_COLOR
    )
    button_frame.pack(pady=5)

    tk.Button(
        button_frame,
        text="SAVE EVENT",
        width=16,
        height=2,
        font=("Arial", 10, "bold"),
        bg=GREEN,
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=save_event
    ).grid(
        row=0,
        column=0,
        padx=8
    )

    tk.Button(
        button_frame,
        text="CLEAR",
        width=16,
        height=2,
        font=("Arial", 10, "bold"),
        bg=GREY,
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=clear_form
    ).grid(
        row=0,
        column=1,
        padx=8
    )

    tk.Button(
        button_frame,
        text="BACK",
        width=16,
        height=2,
        font=("Arial", 10, "bold"),
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=dashboard
    ).grid(
        row=0,
        column=2,
        padx=8
    )


# ==========================================================
# FORM FIELDS
# ==========================================================

def create_form_fields(parent):

    global event_name_entry
    global event_type_entry
    global event_date_entry
    global venue_entry
    global organizer_entry
    global contact_entry
    global description_entry

    labels = [
        "Event Name:",
        "Event Type:",
        "Event Date:",
        "Venue:",
        "Organizer:",
        "Contact:",
        "Description:"
    ]

    entries = []

    for i, label in enumerate(labels, start=1):

        tk.Label(
            parent,
            text=label,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=DARK
        ).grid(
            row=i,
            column=0,
            sticky="w",
            padx=10,
            pady=7
        )

        entry = tk.Entry(
            parent,
            width=38,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        entry.grid(
            row=i,
            column=1,
            padx=10,
            pady=7,
            ipady=4
        )

        entries.append(entry)

    event_name_entry = entries[0]
    event_type_entry = entries[1]
    event_date_entry = entries[2]
    venue_entry = entries[3]
    organizer_entry = entries[4]
    contact_entry = entries[5]
    description_entry = entries[6]


# ==========================================================
# CLEAR ADD EVENT FORM
# ==========================================================

def clear_form():

    event_name_entry.delete(0, tk.END)
    event_type_entry.delete(0, tk.END)
    event_date_entry.delete(0, tk.END)
    venue_entry.delete(0, tk.END)
    organizer_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)


# ==========================================================
# SAVE EVENT
# ==========================================================

def save_event():

    event_name = event_name_entry.get().strip()
    event_type = event_type_entry.get().strip()
    event_date = event_date_entry.get().strip()
    venue = venue_entry.get().strip()
    organizer = organizer_entry.get().strip()
    contact = contact_entry.get().strip()
    description = description_entry.get().strip()

    # Required field
    if event_name == "":
        messagebox.showwarning(
            "Validation",
            "Please enter Event Name."
        )
        return

    if event_date == "":
        messagebox.showwarning(
            "Validation",
            "Please enter Event Date."
        )
        return

    # Date validation
    try:

        datetime.strptime(
            event_date,
            "%Y-%m-%d"
        )

    except ValueError:

        messagebox.showwarning(
            "Invalid Date",
            "Please enter date in YYYY-MM-DD format."
        )
        return

    # Contact validation
    if contact != "" and not contact.isdigit():

        messagebox.showwarning(
            "Invalid Contact",
            "Contact must contain digits only."
        )
        return

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        query = """
        INSERT INTO events
        (
            event_name,
            event_type,
            event_date,
            venue,
            organizer,
            contact,
            description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            event_name,
            event_type,
            event_date,
            venue,
            organizer,
            contact,
            description
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Event saved successfully!"
        )

        clear_form()

    except Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# VIEW EVENTS
# ==========================================================

def view_events():

    clear_screen()

    root.configure(bg=BG_COLOR)

    tk.Label(
        root,
        text="ALL EVENTS",
        font=("Arial", 23, "bold"),
        bg=BG_COLOR,
        fg=DARK
    ).pack(pady=15)

    table_frame = tk.Frame(
        root,
        bg=WHITE
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
        "ID",
        "Event Name",
        "Type",
        "Date",
        "Venue",
        "Organizer",
        "Contact",
        "Description"
    )

    global event_table

    event_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=15
    )

    for column in columns:

        event_table.heading(
            column,
            text=column
        )

    event_table.column("ID", width=50)
    event_table.column("Event Name", width=130)
    event_table.column("Type", width=100)
    event_table.column("Date", width=100)
    event_table.column("Venue", width=120)
    event_table.column("Organizer", width=120)
    event_table.column("Contact", width=110)
    event_table.column("Description", width=180)

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=event_table.yview
    )

    event_table.configure(
        yscrollcommand=scrollbar.set
    )

    event_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    load_events()

    tk.Button(
        root,
        text="BACK TO DASHBOARD",
        width=20,
        height=2,
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        font=("Arial", 10, "bold"),
        command=dashboard
    ).pack(pady=15)


# ==========================================================
# LOAD EVENTS
# ==========================================================

def load_events():

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM events ORDER BY event_date"
        )

        records = cursor.fetchall()

        for record in records:

            event_table.insert(
                "",
                tk.END,
                values=record
            )

    except Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# SEARCH EVENT
# ==========================================================

def search_event():

    clear_screen()

    root.configure(bg=BG_COLOR)

    tk.Label(
        root,
        text="SEARCH EVENT",
        font=("Arial", 23, "bold"),
        bg=BG_COLOR,
        fg=DARK
    ).pack(pady=20)

    search_frame = tk.Frame(
        root,
        bg=WHITE,
        padx=20,
        pady=20
    )
    search_frame.pack()

    tk.Label(
        search_frame,
        text="Search:",
        font=("Arial", 11, "bold"),
        bg=WHITE
    ).grid(
        row=0,
        column=0,
        padx=10
    )

    global search_entry

    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Arial", 11)
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=10,
        ipady=5
    )

    tk.Button(
        search_frame,
        text="SEARCH",
        width=12,
        bg=PURPLE,
        fg=WHITE,
        relief="flat",
        command=perform_search
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    # Table
    table_frame = tk.Frame(
        root,
        bg=WHITE
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    columns = (
        "ID",
        "Event Name",
        "Type",
        "Date",
        "Venue",
        "Organizer",
        "Contact"
    )

    global search_table

    search_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    for column in columns:

        search_table.heading(
            column,
            text=column
        )

        search_table.column(
            column,
            width=120
        )

    search_table.pack(
        fill="both",
        expand=True
    )

    tk.Button(
        root,
        text="BACK",
        width=15,
        height=2,
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        command=dashboard
    ).pack(pady=10)


# ==========================================================
# PERFORM SEARCH
# ==========================================================

def perform_search():

    search_text = search_entry.get().strip()

    for item in search_table.get_children():
        search_table.delete(item)

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        query = """
        SELECT
            event_id,
            event_name,
            event_type,
            event_date,
            venue,
            organizer,
            contact
        FROM events
        WHERE event_name LIKE %s
           OR event_type LIKE %s
           OR venue LIKE %s
           OR organizer LIKE %s
        """

        value = "%" + search_text + "%"

        cursor.execute(
            query,
            (value, value, value, value)
        )

        records = cursor.fetchall()

        for record in records:

            search_table.insert(
                "",
                tk.END,
                values=record
            )

        if not records:

            messagebox.showinfo(
                "Search",
                "No matching events found."
            )

    except Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# UPDATE EVENT
# ==========================================================

def update_event():

    clear_screen()

    root.configure(bg=BG_COLOR)

    tk.Label(
        root,
        text="UPDATE EVENT",
        font=("Arial", 23, "bold"),
        bg=BG_COLOR,
        fg=DARK
    ).pack(pady=15)

    form_frame = tk.Frame(
        root,
        bg=WHITE,
        padx=30,
        pady=20
    )
    form_frame.pack()

    # Event ID
    tk.Label(
        form_frame,
        text="Event ID:",
        font=("Arial", 11, "bold"),
        bg=WHITE
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=8
    )

    global update_id_entry

    update_id_entry = tk.Entry(
        form_frame,
        width=35,
        font=("Arial", 11)
    )

    update_id_entry.grid(
        row=0,
        column=1,
        pady=8
    )

    tk.Button(
        form_frame,
        text="LOAD EVENT",
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        command=load_event_for_update
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    global update_name_entry
    global update_type_entry
    global update_date_entry
    global update_venue_entry
    global update_organizer_entry
    global update_contact_entry
    global update_description_entry

    fields = [
        "Event Name:",
        "Event Type:",
        "Event Date:",
        "Venue:",
        "Organizer:",
        "Contact:",
        "Description:"
    ]

    entries = []

    for i, field in enumerate(fields, start=1):

        tk.Label(
            form_frame,
            text=field,
            font=("Arial", 11, "bold"),
            bg=WHITE
        ).grid(
            row=i,
            column=0,
            padx=10,
            pady=7,
            sticky="w"
        )

        entry = tk.Entry(
            form_frame,
            width=35,
            font=("Arial", 11)
        )

        entry.grid(
            row=i,
            column=1,
            columnspan=2,
            pady=7
        )

        entries.append(entry)

    update_name_entry = entries[0]
    update_type_entry = entries[1]
    update_date_entry = entries[2]
    update_venue_entry = entries[3]
    update_organizer_entry = entries[4]
    update_contact_entry = entries[5]
    update_description_entry = entries[6]

    button_frame = tk.Frame(
        root,
        bg=BG_COLOR
    )
    button_frame.pack(pady=15)

    tk.Button(
        button_frame,
        text="UPDATE",
        width=15,
        height=2,
        bg=ORANGE,
        fg=WHITE,
        relief="flat",
        font=("Arial", 10, "bold"),
        command=save_update
    ).grid(
        row=0,
        column=0,
        padx=8
    )

    tk.Button(
        button_frame,
        text="CLEAR",
        width=15,
        height=2,
        bg=GREY,
        fg=WHITE,
        relief="flat",
        font=("Arial", 10, "bold"),
        command=clear_update_form
    ).grid(
        row=0,
        column=1,
        padx=8
    )

    tk.Button(
        button_frame,
        text="BACK",
        width=15,
        height=2,
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        font=("Arial", 10, "bold"),
        command=dashboard
    ).grid(
        row=0,
        column=2,
        padx=8
    )


# ==========================================================
# LOAD EVENT FOR UPDATE
# ==========================================================

def load_event_for_update():

    event_id = update_id_entry.get().strip()

    if not event_id.isdigit():

        messagebox.showwarning(
            "Invalid ID",
            "Please enter a valid Event ID."
        )

        return

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM events WHERE event_id = %s",
            (event_id,)
        )

        record = cursor.fetchone()

        if record is None:

            messagebox.showwarning(
                "Not Found",
                "Event not found."
            )

            return

        update_name_entry.delete(0, tk.END)
        update_name_entry.insert(0, record[1])

        update_type_entry.delete(0, tk.END)
        update_type_entry.insert(0, record[2])

        update_date_entry.delete(0, tk.END)
        update_date_entry.insert(0, str(record[3]))

        update_venue_entry.delete(0, tk.END)
        update_venue_entry.insert(0, record[4])

        update_organizer_entry.delete(0, tk.END)
        update_organizer_entry.insert(0, record[5])

        update_contact_entry.delete(0, tk.END)
        update_contact_entry.insert(0, record[6])

        update_description_entry.delete(0, tk.END)
        update_description_entry.insert(0, record[7])

        messagebox.showinfo(
            "Loaded",
            "Event details loaded successfully."
        )

    except Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# SAVE UPDATE
# ==========================================================

def save_update():

    event_id = update_id_entry.get().strip()

    event_name = update_name_entry.get().strip()
    event_type = update_type_entry.get().strip()
    event_date = update_date_entry.get().strip()
    venue = update_venue_entry.get().strip()
    organizer = update_organizer_entry.get().strip()
    contact = update_contact_entry.get().strip()
    description = update_description_entry.get().strip()

    if not event_id.isdigit():

        messagebox.showwarning(
            "Invalid ID",
            "Please enter a valid Event ID."
        )

        return

    if event_name == "":

        messagebox.showwarning(
            "Validation",
            "Event Name cannot be empty."
        )

        return

    try:

        datetime.strptime(
            event_date,
            "%Y-%m-%d"
        )

    except ValueError:

        messagebox.showwarning(
            "Invalid Date",
            "Use YYYY-MM-DD format."
        )

        return

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        query = """
        UPDATE events
        SET
            event_name = %s,
            event_type = %s,
            event_date = %s,
            venue = %s,
            organizer = %s,
            contact = %s,
            description = %s
        WHERE event_id = %s
        """

        values = (
            event_name,
            event_type,
            event_date,
            venue,
            organizer,
            contact,
            description,
            event_id
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        if cursor.rowcount == 0:

            messagebox.showwarning(
                "Not Found",
                "Event ID does not exist."
            )

        else:

            messagebox.showinfo(
                "Success",
                "Event updated successfully!"
            )

            clear_update_form()

    except Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# CLEAR UPDATE FORM
# ==========================================================

def clear_update_form():

    update_id_entry.delete(0, tk.END)
    update_name_entry.delete(0, tk.END)
    update_type_entry.delete(0, tk.END)
    update_date_entry.delete(0, tk.END)
    update_venue_entry.delete(0, tk.END)
    update_organizer_entry.delete(0, tk.END)
    update_contact_entry.delete(0, tk.END)
    update_description_entry.delete(0, tk.END)


# ==========================================================
# DELETE EVENT
# ==========================================================

def delete_event():

    clear_screen()

    root.configure(bg=BG_COLOR)

    tk.Label(
        root,
        text="DELETE EVENT",
        font=("Arial", 23, "bold"),
        bg=BG_COLOR,
        fg=DARK
    ).pack(pady=35)

    card = tk.Frame(
        root,
        bg=WHITE,
        padx=50,
        pady=40
    )
    card.pack()

    tk.Label(
        card,
        text="Enter Event ID",
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(pady=10)

    global delete_id_entry

    delete_id_entry = tk.Entry(
        card,
        width=25,
        font=("Arial", 12)
    )
    delete_id_entry.pack(
        ipady=7,
        pady=10
    )

    tk.Button(
        card,
        text="DELETE EVENT",
        width=20,
        height=2,
        bg=RED,
        fg=WHITE,
        relief="flat",
        font=("Arial", 10, "bold"),
        command=perform_delete
    ).pack(pady=15)

    tk.Button(
        root,
        text="BACK",
        width=15,
        height=2,
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        command=dashboard
    ).pack(pady=20)


# ==========================================================
# PERFORM DELETE
# ==========================================================

def perform_delete():

    event_id = delete_id_entry.get().strip()

    if not event_id.isdigit():

        messagebox.showwarning(
            "Invalid ID",
            "Please enter a valid Event ID."
        )

        return

    confirmation = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete Event ID {event_id}?"
    )

    if not confirmation:
        return

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM events WHERE event_id = %s",
            (event_id,)
        )

        connection.commit()

        if cursor.rowcount == 0:

            messagebox.showwarning(
                "Not Found",
                "Event ID does not exist."
            )

        else:

            messagebox.showinfo(
                "Deleted",
                "Event deleted successfully!"
            )

            delete_id_entry.delete(
                0,
                tk.END
            )

    except Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title(
    "Event Management System"
)

root.geometry(
    "1000x650"
)

root.resizable(
    False,
    False
)


# ==========================================================
# TREEVIEW STYLE
# ==========================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    rowheight=30,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)

style.map(
    "Treeview",
    background=[
        ("selected", HEADER_COLOR)
    ],
    foreground=[
        ("selected", WHITE)
    ]
)


# ==========================================================
# START APPLICATION
# ==========================================================

login_page()

root.mainloop()