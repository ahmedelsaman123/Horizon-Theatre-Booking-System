import tkinter as tk
from tkinter import ttk
import mysql.connector
import datetime
import uuid
from tkinter import messagebox
import tkinter.messagebox as mb


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.configure(bg='#808080')  # Grey background

        # Create a frame to hold the login form
        self.login_frame = tk.Frame(self.root, bg='#808080')  # Grey frame
        self.login_frame.pack(padx=50, pady=50)

        # Username label and entry
        self.label_user = tk.Label(self.login_frame, text="Username", bg='#808080', fg='#FFFFFF')  # White text on grey background
        self.label_user.grid(row=0, column=0, sticky='e', pady=(0,10))
        self.entry_user = tk.Entry(self.login_frame)
        self.entry_user.grid(row=0, column=1, pady=(0,10))

        # Password label and entry
        self.label_pass = tk.Label(self.login_frame, text="Password", bg='#808080', fg='#FFFFFF')  # White text on grey background
        self.label_pass.grid(row=1, column=0, sticky='e')
        self.entry_pass = tk.Entry(self.login_frame, show="*")
        self.entry_pass.grid(row=1, column=1)

        # Login button
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg='#0000FF', fg='#FFFFFF')  # White text on blue background
        self.login_button.grid(row=2, column=0, columnspan=2, pady=(10,0))


    def login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()

        # Check if the username or password fields are empty
        if not user or not password:
            messagebox("Error: Username and password cannot be empty.")
            return

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="horizon",
            charset='utf8mb4'
        )

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user, password))

        result = cursor.fetchone()
        if result is None:
            messagebox("Error: Invalid username or password.")
            return

        # If result is not None, assign values to user_id and is_manager
        user_id = result[0]  # Assume user_id is the first element of result
        role = result[1]  # Assume role field is the fourth element of result

        # Convert role string into boolean value
        is_manager = True if role == 'manager1' else False

        for widget in self.root.winfo_children():
            widget.destroy()

        self.app = ShowList(self.root, self.reinitialize, self.reinitialize, user_id, is_manager)



    
    def reinitialize(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)
        
class AddTheatreWindow:
    def __init__(self, master, user_id):
        self.master = master
        self.master.title("Manage Theatre")
        self.master.geometry("400x250")
        self.user_id = user_id
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # create a variable for the operation type
        self.operation = tk.StringVar()

        self.label_Theatre_ID = tk.Label(self.frame, text="Theatre ID: ")
        self.label_Theatre_ID.pack()
        self.Theatre_ID_entry = tk.Entry(self.frame)
        self.Theatre_ID_entry.pack()

        self.label_Theatre_Name = tk.Label(self.frame, text="Theatre Name: ")
        self.label_Theatre_Name.pack()
        self.Theatre_Name_entry = tk.Entry(self.frame)
        self.Theatre_Name_entry.pack()

        self.label_City_ID = tk.Label(self.frame, text="City ID: ")
        self.label_City_ID.pack()
        self.City_ID_entry = tk.Entry(self.frame)
        self.City_ID_entry.pack()

        self.label_City_Name = tk.Label(self.frame, text="City Name: ")
        self.label_City_Name.pack()
        self.City_Name_entry = tk.Entry(self.frame)
        self.City_Name_entry.pack()

        # create radio buttons for the user to choose the operation type
        self.add_radio = tk.Radiobutton(self.frame, text="Add Theatre", value="add", variable=self.operation)
        self.add_radio.pack()
        self.remove_radio = tk.Radiobutton(self.frame, text="Remove Theatre", value="remove", variable=self.operation)
        self.remove_radio.pack()
        self.update_radio = tk.Radiobutton(self.frame, text="Update Theatre", value="update", variable=self.operation)
        self.update_radio.pack()

        self.execute_button = tk.Button(self.frame, text="Execute", command=self.execute_operation)
        self.execute_button.pack()

    def execute_operation(self):
        operation = self.operation.get()

        if operation == "add":
            self.add_theatre()
        elif operation == "remove":
            self.remove_theatre()
        elif operation == "update":
            self.update_theatre()
        else:
            messagebox.showinfo("Error", "Please select an operation")

    def add_theatre(self):
        theatre_id = self.Theatre_ID_entry.get()
        theatre_name = self.Theatre_Name_entry.get()
        city_id = self.City_ID_entry.get()
        city_name = self.City_Name_entry.get()
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='horizon',
                                                 user='root',
                                                 password='') # replace with your password
            if connection.is_connected():
                cursor = connection.cursor()
                query = "INSERT INTO theatres (Theatre_ID, Theatre_Name, City_ID, City_Name) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (theatre_id, theatre_name, city_id, city_name))
                connection.commit()
                messagebox.showinfo("Success", "Theatre successfully added")
        except mysql.connector.Error as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    def remove_theatre(self):
        theatre_id = self.Theatre_ID_entry.get()
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='horizon',
                                                 user='root',
                                                 password='') # replace with your password
            if connection.is_connected():
                cursor = connection.cursor()
                query = "DELETE FROM theatres WHERE Theatre_ID = %s"
                cursor.execute(query, (theatre_id,))
                connection.commit()
                messagebox.showinfo("Success", "Theatre successfully removed")
        except mysql.connector.Error as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    def update_theatre(self):
        theatre_id = self.Theatre_ID_entry.get()
        theatre_name = self.Theatre_Name_entry.get()
        city_id = self.City_ID_entry.get()
        city_name = self.City_Name_entry.get()
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='horizon',
                                                 user='root',
                                                 password='') # replace with your password
            if connection.is_connected():
                cursor = connection.cursor()
                query = "UPDATE theatres SET Theatre_Name = %s, City_ID = %s, City_Name = %s WHERE Theatre_ID = %s"
                cursor.execute(query, (theatre_name, city_id, city_name, theatre_id))
                connection.commit()
                messagebox.showinfo("Success", "Theatre successfully updated")
        except mysql.connector.Error as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class AddCityWindow:
    def __init__(self, master, user_id):
        self.master = master
        self.master.title("Manage City")
        self.master.geometry("400x250")
        self.user_id = user_id
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # create a variable for the operation type
        self.operation = tk.StringVar()

        self.label_City_ID = tk.Label(self.frame, text="City ID: ")
        self.label_City_ID.pack()
        self.City_ID_entry = tk.Entry(self.frame)
        self.City_ID_entry.pack()

        self.label_City_Name = tk.Label(self.frame, text="City Name: ")
        self.label_City_Name.pack()
        self.City_Name_entry = tk.Entry(self.frame)
        self.City_Name_entry.pack()
        
        self.label_Theatre_ID = tk.Label(self.frame, text="Theatre ID: ")
        self.label_Theatre_ID.pack()
        self.Theatre_ID_entry = tk.Entry(self.frame)
        self.Theatre_ID_entry.pack()
        
        # create radio buttons for the user to choose the operation type
        self.add_radio = tk.Radiobutton(self.frame, text="Add City", value="add", variable=self.operation)
        self.add_radio.pack()
        self.remove_radio = tk.Radiobutton(self.frame, text="Remove City", value="remove", variable=self.operation)
        self.remove_radio.pack()
        self.update_radio = tk.Radiobutton(self.frame, text="Update City", value="update", variable=self.operation)
        self.update_radio.pack()

        self.execute_button = tk.Button(self.frame, text="Execute", command=self.execute_operation_city)
        self.execute_button.pack()

    def execute_operation_city(self):
        operation = self.operation.get()

        if operation == "add":
            self.add_city()
        elif operation == "remove":
            self.remove_city()
        elif operation == "update":
            self.update_city()
        else:
            messagebox.showinfo("Error", "Please select an operation")

    def add_city(self):
        city_id = self.City_ID_entry.get()
        city_name = self.City_Name_entry.get()
        theatre_id = self.Theatre_ID_entry.get()
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='horizon',
                                                 user='root',
                                                 password='') # replace with your password
            if connection.is_connected():
                cursor = connection.cursor()
                query = "INSERT INTO city (City_ID, City_Name, Theatre_ID) VALUES (%s, %s, %s)"
                cursor.execute(query, (city_id, city_name, theatre_id))
                connection.commit()
                messagebox.showinfo("Success", "City successfully added")
        except mysql.connector.Error as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    def remove_city(self):
        city_id = self.City_ID_entry.get()
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='horizon',
                                                 user='root',
                                                 password='') # replace with your password
            if connection.is_connected():
                cursor = connection.cursor()
                query = "DELETE FROM city WHERE City_ID = %s"
                cursor.execute(query, (city_id,))
                connection.commit()
                messagebox.showinfo("Success", "City successfully removed")
        except mysql.connector.Error as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    def update_city(self):
        city_id = self.City_ID_entry.get()
        city_name = self.City_Name_entry.get()
        theatre_id = self.Theatre_ID_entry.get()
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='horizon',
                                                 user='root',
                                                 password='') # replace with your password
            if connection.is_connected():
                cursor = connection.cursor()
                query = "UPDATE city SET City_ID = %s, City_Name = %s WHERE Theatre_ID = %s"
                cursor.execute(query, (city_id, city_name, theatre_id))
                connection.commit()
                messagebox.showinfo("Success", "City successfully updated")
        except mysql.connector.Error as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class ManageTheatreWindow:
    
    def __init__(self, db):
        self.db = db

        self.root = tk.Tk()
        self.root.title("Manage Theatre")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="City ID")
        self.label.pack()
        self.city_id_entry = tk.Entry(self.frame)
        self.city_id_entry.pack()

        self.label = tk.Label(self.frame, text="City Name")
        self.label.pack()
        self.city_name_entry = tk.Entry(self.frame)
        self.city_name_entry.pack()
        
        self.label = tk.Label(self.frame, text="Theatre ID")
        self.label.pack()
        self.theatre_id_entry = tk.Entry(self.frame)
        self.theatre_id_entry.pack()

        self.add_button = tk.Button(self.frame, text="Add City", command=self.add_city)
        self.add_button.pack()

        self.remove_button = tk.Button(self.frame, text="Remove City", command=self.remove_city)
        self.remove_button.pack()

        self.update_button = tk.Button(self.frame, text="Update City", command=self.update_city)
        self.update_button.pack()

        self.root.mainloop()

    def add_city(self):
        try:
            cursor = self.db.cursor()
            query = """INSERT INTO theatres (City_ID, City_Name, Theatre_ID) 
                        VALUES (%s, %s, %s)"""
            cursor.execute(query, (self.city_id_entry.get(), self.city_name_entry.get()), self.theatre_id_entry.get())
            self.db.commit()
            mb.showinfo("Information", "City added successfully!")
        except Exception as e:
            mb.showinfo("Error", str(e))

    def remove_city(self):
        try:
            cursor = self.db.cursor()
            query = """DELETE FROM city WHERE Theatre_ID = %s"""
            cursor.execute(query, (self.theatre_id_entry.get(),))
            self.db.commit()
            mb.showinfo("Information", "City removed successfully!")
        except Exception as e:
            mb.showinfo("Error", str(e))

    def update_city(self):
        try:
            cursor = self.db.cursor()
            query = """UPDATE city SET City_ID = %s, City_Name = %s WHERE Theatre_ID = %s"""
            cursor.execute(query, (self.city_id_entry.get(), self.city_name_entry.get(), self.theatre_id_entry.get()))
            self.db.commit()
            mb.showinfo("Information", "Theatre updated successfully!")
        except Exception as e:
            mb.showinfo("Error", str(e))
        
class BookingWindow:
    def __init__(self, root, return_callback, logout_callback, user_id):
        self.root = root
        self.root.geometry("800x600")
        self.logout_callback = logout_callback
        self.user_id = user_id

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="horizon",
            charset='utf8mb4'
        )
        self.my_cursor = self.mydb.cursor()


        frame = ttk.Frame(self.root)
        frame.pack()

        ttk.Label(frame, text="City: ").grid(row=1, column=0, padx=5, pady=5)

        # Query to fetch Cities
        self.my_cursor.execute("SELECT DISTINCT City_Name FROM city")  # Adjust this query based on your database structure
        self.cities = [city[0] for city in self.my_cursor.fetchall()]
        self.city_var = tk.StringVar(frame)
        self.city_var.set(self.cities[0])  # set the initial option
        self.city_drop = tk.OptionMenu(frame, self.city_var, *self.cities)
        self.city_drop.grid(row=1, column=1, padx=5, pady=5)
        
        # Bind the update_theatre_dropdown method to the city dropdown variable
        self.city_var.trace('w', self.update_theatre_dropdown)

        ttk.Label(frame, text="Show: ").grid(row=2, column=0, padx=5, pady=5)

        # Query to fetch Shows
        self.my_cursor.execute("SELECT DISTINCT Show_Name FROM shows")  # Adjust this query based on your database structure
        self.shows = [show[0] for show in self.my_cursor.fetchall()]
        self.show_var = tk.StringVar(frame)
        self.show_var.set(self.shows[0])  # set the initial option
        self.show_drop = tk.OptionMenu(frame, self.show_var, *self.shows)
        self.show_drop.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Theatre: ").grid(row=3, column=0, padx=5, pady=5)

        # Query to fetch Theatres
        self.my_cursor.execute("SELECT DISTINCT Theatre_Name FROM theatres WHERE City_Name = %s", (self.city_var.get(),))  # Adjust this query based on your database structure
        self.theatres = [theatre[0] for theatre in self.my_cursor.fetchall()]
        self.theatre_var = tk.StringVar(frame)
        self.theatre_var.set(self.theatres[0])  # set the initial option
        self.theatre_drop = tk.OptionMenu(frame, self.theatre_var, *self.theatres)
        self.theatre_drop.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Time Slot: ").grid(row=5, column=0, padx=5, pady=5)

        # Set the time slots
        self.time_slots = ["Early Afternoon", "Evening"]
        self.time_slot_var = tk.StringVar(frame)
        self.time_slot_var.set(self.time_slots[0])  # set the initial option
        self.time_slot_drop = tk.OptionMenu(frame, self.time_slot_var, *self.time_slots)
        self.time_slot_drop.grid(row=5, column=1, padx=5, pady=5)


        ttk.Label(frame, text="Number of Tickets: ").grid(row=4, column=0, padx=5, pady=5)

        # Set the ticket count
        self.tickets = list(range(1, 11))
        self.ticket_var = tk.StringVar(frame)
        self.ticket_var.set(self.tickets[0])  # set the initial option
        self.ticket_drop = tk.OptionMenu(frame, self.ticket_var, *self.tickets)
        self.ticket_drop.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Drive-in: ").grid(row=6, column=0, padx=5, pady=5)

        # Set the drive-in options
        self.drive_in_options = ["Yes", "No"]
        self.drive_in_var = tk.StringVar(frame)
        self.drive_in_var.set(self.drive_in_options[0])  # set the initial option
        self.drive_in_drop = tk.OptionMenu(frame, self.drive_in_var, *self.drive_in_options)
        self.drive_in_drop.grid(row=6, column=1, padx=5, pady=5)

        # Button to book tickets
        self.book_button = tk.Button(frame, text="Book", command=self.create_booking_details_window)
        self.book_button.grid(row=7, column=0, padx=5, pady=5)

        # Button to go back
        self.return_button = tk.Button(frame, text="Back", command=return_callback)
        self.return_button.grid(row=7, column=1, padx=5, pady=5)
        
    def update_theatre_dropdown(self, *args):
        # Clear the current options in the theatre dropdown
        self.theatre_drop['menu'].delete(0, 'end')

        # Get the selected city from the city dropdown
        selected_city = self.city_var.get()

        # Query to fetch Theatres for the selected city
        self.my_cursor.execute("SELECT DISTINCT Theatre_Name FROM theatres WHERE City_Name = %s", (selected_city,))

        # Fetch the theatres for the selected city
        theatres = [theatre[0] for theatre in self.my_cursor.fetchall()]

        # Update the theatre dropdown with the fetched theatres
        for theatre in theatres:
            self.theatre_drop['menu'].add_command(label=theatre, command=tk._setit(self.theatre_var, theatre))

        # Set the first theatre as the default option
        if theatres:
            self.theatre_var.set(theatres[0])


    
    def create_booking_details_window(self):
        # Get the Theatre_ID based on the Theatre_Name
        self.my_cursor.execute("SELECT Theatre_ID FROM theatres WHERE Theatre_Name = %s", (self.theatre_var.get(),))
        theatre_id = self.my_cursor.fetchone()[0]

        # Calculate total price
        total_price = self.calculate_total_price(theatre_id, datetime.datetime.now(), int(self.ticket_var.get()), self.time_slot_var.get())

        # Create a new window to display booking details and total price
        newWindow = tk.Toplevel(self.root)
        BookingDetailsWindow(newWindow, self.user_id, self.show_var.get(), self.city_var.get(), self.theatre_var.get(), self.ticket_var.get(), self.drive_in_var.get(), total_price, self.time_slot_var.get())


    def calculate_total_price(self, theatre_id, booking_date, num_tickets, time_slots):
        try:
            # Get the city ID based on theatre_id
            self.my_cursor.execute("SELECT City_ID FROM theatres WHERE Theatre_ID = %s", (theatre_id,))
            fetch_result = self.my_cursor.fetchone()
            if not fetch_result:
                messagebox.showinfo("Error: Theatre ID not found in database")
                return None
            city_id = fetch_result[0]

            # Determine if it's early afternoon or evening
            show_time = 'Early_afternoon_Price' if time_slots == 'Early Afternoon' else 'Evening_Price'

            # Get the price per ticket
            self.my_cursor.execute("SELECT {} FROM price WHERE City_ID = %s".format(show_time), (city_id,))
            fetch_result = self.my_cursor.fetchone()
            if not fetch_result:
                print("Error: No price found for given City ID")
                return None
            price_per_ticket = fetch_result[0]

            # Calculate total price
            total_price = price_per_ticket * num_tickets

            return total_price

        except Exception as e:
            messagebox.showinfo("Error in calculate_total_price: ", e)
            return None



    
    def submit_booking(self):
        messagebox.showinfo(f"Creating booking with: Show: {self.show_var.get()}, City: {self.city_var.get()}, Theatre: {self.theatre_var.get()}, Tickets: {self.ticket_var.get()}")

class BookingDetailsWindow:
    def __init__(self, root, user_id, show_id, city_id, theatre_id, tickets, drive_in, total_price, time_slots):
        self.root = root
        self.root.geometry("500x400")
        self.user_id = user_id
        self.show_id = show_id
        self.city_id = city_id
        self.theatre_id = theatre_id
        self.tickets = tickets
        self.drive_in = drive_in
        self.total_price = total_price
        self.time_slots = time_slots

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="horizon",
            charset='utf8mb4'
        )
        self.my_cursor = self.mydb.cursor()
        
        frame = ttk.Frame(self.root)
        frame.pack()

        ttk.Label(frame, text="Booking Details", font=("Arial", 20)).grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(frame, text=f"User ID: {user_id}").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(frame, text=f"Show: {show_id}").grid(row=2, column=0, padx=5, pady=5)  # Updated row
        ttk.Label(frame, text=f"City: {city_id}").grid(row=3, column=0, padx=5, pady=5)  # Updated row
        ttk.Label(frame, text=f"Theatre: {theatre_id}").grid(row=4, column=0, padx=5, pady=5)  # Updated row
        ttk.Label(frame, text=f"Number of Tickets: {tickets}").grid(row=6, column=0, padx=5, pady=5)  # Updated row
        ttk.Label(frame, text=f"Drive-in: {drive_in}").grid(row=7, column=0, padx=5, pady=5)  # No need to check here, as we already converted it to 'Yes'/'No'
        ttk.Label(frame, text=f"Total Price: {total_price}").grid(row=8, column=0, padx=5, pady=5)  # Updated row

        self.submit_button = tk.Button(frame, text="Submit Booking", command=self.submit_booking)
        self.submit_button.grid(row=9, column=0, padx=5, pady=5)

        self.return_button = tk.Button(frame, text="Back", command=self.root.destroy)
        self.return_button.grid(row=9, column=1, padx=5, pady=5)

    def submit_booking(self):
        today_date = datetime.date.today()

        self.my_cursor.execute("SELECT Show_ID FROM shows WHERE Show_Name = %s", (self.show_id,))
        show_id = self.my_cursor.fetchone()[0]

        # Get the City_ID based on the City_Name
        self.my_cursor.execute("SELECT City_ID FROM city WHERE City_Name = %s", (self.city_id,))
        city_id = self.my_cursor.fetchone()[0]

        self.my_cursor.execute("SELECT Theatre_ID FROM theatres WHERE Theatre_Name = %s", (self.theatre_id,))
        theatre_id = self.my_cursor.fetchone()[0]

        # Generate a new UUID for the Booking_ID
        booking_reference = str(uuid.uuid4())
        
        self.my_cursor.execute(
            "INSERT INTO booking (Booking_Reference, User_ID, Show_ID, Theatre_ID, Total_Price, Booking_Date, Number_of_tickets, Drive_in_or_Not) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (booking_reference, self.user_id, show_id, theatre_id, self.total_price, today_date, self.tickets, self.drive_in)
        )

        self.mydb.commit()

        messagebox.showinfo(f"Booking Submitted: Booking Reference: {booking_reference}, User ID: {self.user_id}, Show ID: {show_id}, Theatre ID: {theatre_id}, Tickets: {self.tickets}, Total_price: {self.total_price}, Drive-in: {self.drive_in}")

        # After successfully inserting into the database, destroy the booking details window
        self.root.destroy()
        
class AllBookingsWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.root.geometry("800x600")  # Increase the size of the window
        self.user_id = user_id

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="horizon",
            charset='utf8mb4'
        )
        self.my_cursor = self.mydb.cursor()

        frame = ttk.Frame(self.root)
        frame.pack()

        ttk.Label(frame, text="All Bookings", font=("Arial", 20)).grid(row=0, column=0, padx=5, pady=5)

        self.my_cursor.execute("SELECT * FROM booking WHERE User_ID = %s", (self.user_id,))
        rows = self.my_cursor.fetchall()

        if rows:
            for i, row in enumerate(rows, start=1):
                ttk.Label(frame, text=f"Booking {i}:").grid(row=i, column=0, padx=5, pady=5)
                ttk.Label(frame, text=f"Booking Reference: {row[0]}").grid(row=i, column=1, padx=5, pady=5)
                ttk.Label(frame, text=f"User ID: {row[1]}").grid(row=i, column=2, padx=5, pady=5)
                ttk.Label(frame, text=f"Show ID: {row[2]}").grid(row=i, column=3, padx=5, pady=5)
                ttk.Label(frame, text=f"Theatre ID: {row[3]}").grid(row=i, column=4, padx=5, pady=5)
                ttk.Label(frame, text=f"Total Price: {row[4]}").grid(row=i, column=5, padx=5, pady=5)
                ttk.Label(frame, text=f"Booking Date: {row[5]}").grid(row=i, column=6, padx=5, pady=5)
                ttk.Label(frame, text=f"Number of Tickets: {row[6]}").grid(row=i, column=7, padx=5, pady=5)
                ttk.Label(frame, text=f"Drive-in: {row[7]}").grid(row=i, column=8, padx=5, pady=5)
        else:
            ttk.Label(frame, text="No bookings found.").grid(row=1, column=0, padx=5, pady=5)

        self.return_button = tk.Button(frame, text="Back", command=self.root.destroy)
        self.return_button.grid(row=len(rows)+1, column=0, padx=5, pady=5)
        
class CancelBookingWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.geometry("800x600")

        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.root, columns=('Booking Reference', 'Show ID', 'Theatre ID'), show='headings')
        self.tree.column('Booking Reference', width=150)
        self.tree.column('Show ID', width=100)
        self.tree.column('Theatre ID', width=100)
        self.tree.heading('Booking Reference', text='Booking Reference')
        self.tree.heading('Show ID', text='Show ID')
        self.tree.heading('Theatre ID', text='Theatre ID')
        self.tree.pack()

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="horizon",
            charset='utf8mb4'
        )

        self.my_cursor = self.mydb.cursor()
        self.my_cursor.execute("SELECT Booking_Reference, Show_ID, Theatre_ID FROM booking WHERE User_ID = %s", (self.user_id,))
        self.bookings = self.my_cursor.fetchall()

        for booking in self.bookings:
            self.tree.insert('', tk.END, values=booking)

        self.confirm_cancellation_button = tk.Button(self.root, text="Confirm Cancellation", command=self.confirm_cancellation)
        self.confirm_cancellation_button.pack()

    def confirm_cancellation(self):
        
        selected_item = self.tree.selection()[0] # get selected item
        booking_reference = self.tree.item(selected_item)["values"][0]
        self.my_cursor.execute("DELETE FROM booking WHERE Booking_Reference = %s", (booking_reference,))
        self.mydb.commit()
        messagebox.showinfo(f"Booking {booking_reference} has been cancelled.")
        self.tree.delete(selected_item)
        
class ShowAllBookingsWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id

        # Database setup
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="horizon",
            charset='utf8mb4'
        )
        self.my_cursor = self.mydb.cursor()
        
        frame = ttk.Frame(self.root)
        frame.pack()

        ttk.Label(frame, text="All Bookings", font=("Arial", 20)).grid(row=0, column=0, padx=5, pady=5)

        self.my_cursor.execute("SELECT * FROM booking WHERE User_ID = %s", (self.user_id,))
        rows = self.my_cursor.fetchall()

        if rows:
            for i, row in enumerate(rows, start=1):
                ttk.Label(frame, text=f"Booking {i}:").grid(row=i, column=0, padx=5, pady=5)
                ttk.Label(frame, text=f"Booking Reference: {row[0]}").grid(row=i, column=1, padx=5, pady=5)
                ttk.Label(frame, text=f"User ID: {row[1]}").grid(row=i, column=2, padx=5, pady=5)
                ttk.Label(frame, text=f"Show ID: {row[2]}").grid(row=i, column=3, padx=5, pady=5)
                ttk.Label(frame, text=f"Theatre ID: {row[3]}").grid(row=i, column=4, padx=5, pady=5)
                ttk.Label(frame, text=f"Total Price: {row[4]}").grid(row=i, column=5, padx=5, pady=5)
                ttk.Label(frame, text=f"Booking Date: {row[5]}").grid(row=i, column=6, padx=5, pady=5)
                ttk.Label(frame, text=f"Number of Tickets: {row[6]}").grid(row=i, column=7, padx=5, pady=5)
                ttk.Label(frame, text=f"Drive-in: {row[7]}").grid(row=i, column=8, padx=5, pady=5)
                ttk.Button(frame, text="Select", command=lambda booking_reference=row[0]: self.select_booking(booking_reference)).grid(row=i, column=9, padx=5, pady=5)
        else:
            ttk.Label(frame, text="No bookings found.").grid(row=1, column=0, padx=5, pady=5)

    def select_booking(self, booking_reference):
        newWindow = tk.Toplevel(self.root)
        self.app = UpdateBookingWindow(newWindow, self.user_id, booking_reference, self.return_to_all_bookings)

    def return_to_all_bookings(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root, self.user_id)

class UpdateBookingWindow:
    def __init__(self, root, user_id, booking_reference, return_callback):
        self.root = root
        self.user_id = user_id
        self.booking_reference = booking_reference
        self.return_callback = return_callback

        # Database setup
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="horizon",
            charset='utf8mb4'
        )
        self.my_cursor = self.mydb.cursor()

        # Fetch booking details
        self.my_cursor.execute("SELECT * FROM booking WHERE Booking_Reference = %s", (booking_reference,))
        self.booking_details = self.my_cursor.fetchone()

        frame = ttk.Frame(self.root)
        frame.pack()

        ttk.Label(frame, text="City: ").grid(row=1, column=0, padx=5, pady=5)

        # Query to fetch Cities
        self.my_cursor.execute("SELECT DISTINCT City_Name FROM city")  # Adjust this query based on your database structure
        self.cities = [city[0] for city in self.my_cursor.fetchall()]
        self.city_var = tk.StringVar(frame)
        self.city_var.set(self.cities[0])  # set the initial option
        self.city_drop = tk.OptionMenu(frame, self.city_var, *self.cities)
        self.city_drop.grid(row=1, column=1, padx=5, pady=5)
        
        # Bind the update_theatre_dropdown method to the city dropdown variable
        self.city_var.trace('w', self.update_theatre_dropdown)

        ttk.Label(frame, text="Show: ").grid(row=2, column=0, padx=5, pady=5)

        # Query to fetch Shows
        self.my_cursor.execute("SELECT DISTINCT Show_Name FROM shows")  # Adjust this query based on your database structure
        self.shows = [show[0] for show in self.my_cursor.fetchall()]
        self.show_var = tk.StringVar(frame)
        self.show_var.set(self.shows[0])  # set the initial option
        self.show_drop = tk.OptionMenu(frame, self.show_var, *self.shows)
        self.show_drop.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Theatre: ").grid(row=3, column=0, padx=5, pady=5)

        # Query to fetch Theatres
        self.my_cursor.execute("SELECT DISTINCT Theatre_Name FROM theatres WHERE City_Name = %s", (self.city_var.get(),))  # Adjust this query based on your database structure
        self.theatres = [theatre[0] for theatre in self.my_cursor.fetchall()]
        self.theatre_var = tk.StringVar(frame)
        self.theatre_var.set(self.theatres[0])  # set the initial option
        self.theatre_drop = tk.OptionMenu(frame, self.theatre_var, *self.theatres)
        self.theatre_drop.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Time Slot: ").grid(row=5, column=0, padx=5, pady=5)

        # Set the time slots
        self.time_slots = ["Early Afternoon", "Evening"]
        self.time_slot_var = tk.StringVar(frame)
        self.time_slot_var.set(self.time_slots[0])  # set the initial option
        self.time_slot_drop = tk.OptionMenu(frame, self.time_slot_var, *self.time_slots)
        self.time_slot_drop.grid(row=5, column=1, padx=5, pady=5)


        ttk.Label(frame, text="Number of Tickets: ").grid(row=4, column=0, padx=5, pady=5)

        # Set the ticket count
        self.tickets = list(range(1, 11))  # Replace this with the required ticket range
        self.ticket_var = tk.StringVar(frame)
        self.ticket_var.set(self.tickets[0])  # set the initial option
        self.ticket_drop = tk.OptionMenu(frame, self.ticket_var, *self.tickets)
        self.ticket_drop.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Drive-in: ").grid(row=6, column=0, padx=5, pady=5)

        # Set the drive-in options
        self.drive_in_options = ["Yes", "No"]
        self.drive_in_var = tk.StringVar()  # Create a StringVar
        self.drive_in_var.set(self.drive_in_options[0])  # set the initial option
        self.drive_in_drop = tk.OptionMenu(frame, self.drive_in_var, *self.drive_in_options)
        self.drive_in_drop.grid(row=6, column=1, padx=5, pady=5)

        # Confirm Update button
        self.confirm_button = tk.Button(self.root, text="Confirm Update Booking", command=self.update_booking)
        self.confirm_button.pack()
    
    def update_theatre_dropdown(self, *args):
        # Clear the current options in the theatre dropdown
        self.theatre_drop['menu'].delete(0, 'end')

        # Get the selected city from the city dropdown
        selected_city = self.city_var.get()

        # Query to fetch Theatres for the selected city
        self.my_cursor.execute("SELECT DISTINCT Theatre_Name FROM theatres WHERE City_Name = %s", (selected_city,))

        # Fetch the theatres for the selected city
        theatres = [theatre[0] for theatre in self.my_cursor.fetchall()]

        # Update the theatre dropdown with the fetched theatres
        for theatre in theatres:
            self.theatre_drop['menu'].add_command(label=theatre, command=tk._setit(self.theatre_var, theatre))

        # Set the first theatre as the default option
        if theatres:
            self.theatre_var.set(theatres[0])

    def update_booking(self):
        # Collect updated data from dropdowns
        new_show_name = self.show_var.get()
        new_theatre_name = self.theatre_var.get()
        new_city_name = self.city_var.get()
        new_num_tickets = int(self.ticket_var.get())  # Ensure this is an integer
        new_drive_in = 1 if self.drive_in_var.get() == "Yes" else 'No'
        new_time_slot = self.time_slot_var.get()

        # Fetch Show_ID
        self.my_cursor.execute("SELECT Show_ID FROM shows WHERE Show_Name = %s", (new_show_name,))
        new_show_id = self.my_cursor.fetchone()[0]

        # Fetch Theatre_ID
        self.my_cursor.execute("SELECT Theatre_ID FROM theatres WHERE Theatre_Name = %s", (new_theatre_name,))
        new_theatre_id = self.my_cursor.fetchone()[0]
        
        # Fetch City_ID
        self.my_cursor.execute("SELECT City_ID FROM city WHERE City_Name = %s", (new_city_name,))
        new_city_id = self.my_cursor.fetchone()[0]

        # Fetch ticket price based on time slot
        if new_time_slot == "Early Afternoon":
            self.my_cursor.execute("SELECT Early_afternoon_Price FROM price WHERE City_ID = %s", (new_city_id,))
        else:  # Assume Evening slot if not Early Afternoon
            self.my_cursor.execute("SELECT Evening_Price FROM price WHERE City_ID = %s", (new_city_id,))

        ticket_price = self.my_cursor.fetchone()[0]

        # Calculate total price
        new_total_price = new_num_tickets * ticket_price

        self.my_cursor.execute("""
            UPDATE booking 
            SET Show_ID = %s, Theatre_ID = %s, Number_of_tickets = %s, Drive_in_or_Not = %s, Total_Price = %s 
            WHERE Booking_Reference = %s""", 
            (new_show_id, new_theatre_id, new_num_tickets, new_drive_in, new_total_price, self.booking_reference))

        self.mydb.commit()

        self.return_callback()  # Return to the previous window

class ShowList:
    def __init__(self, root, return_callback, logout_callback, user_id, is_manager):
        self.root = root
        self.return_callback = return_callback
        self.logout_callback = logout_callback
        self.user_id = user_id
        self.is_manager = is_manager

        self.root.geometry("800x600")
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.root.geometry("800x600")
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        if self.is_manager:  # Add these buttons if the user is a manager or a staff member
            self.operation = tk.StringVar(value="add")
            
            # Create radio buttons for the user to choose the operation type
            self.add_theatre_radio = tk.Radiobutton(self.frame, text="Add Theatre", value="add", variable=self.operation)
            self.add_theatre_radio.pack(side="bottom", pady=10)
            self.remove_theatre_radio = tk.Radiobutton(self.frame, text="Remove Theatre", value="remove", variable=self.operation)
            self.remove_theatre_radio.pack(side="bottom", pady=10)
            self.update_theatre_radio = tk.Radiobutton(self.frame, text="Update Theatre", value="update", variable=self.operation)
            self.update_theatre_radio.pack(side="bottom", pady=10)
            self.execute_theatre_button = tk.Button(self.frame, text="Execute", command=self.execute_theatre_operation)
            self.execute_theatre_button.pack(side="bottom", pady=10)

            # Create radio buttons for the user to choose the operation type
            self.add_city_radio = tk.Radiobutton(self.frame, text="Add City", value="add", variable=self.operation)
            self.add_city_radio.pack(side="bottom", pady=10)
            self.remove_city_radio = tk.Radiobutton(self.frame, text="Remove City", value="remove", variable=self.operation)
            self.remove_city_radio.pack(side="bottom", pady=10)
            self.update_city_radio = tk.Radiobutton(self.frame, text="Update City", value="update", variable=self.operation)
            self.update_city_radio.pack(side="bottom", pady=10)
            self.execute_city_button = tk.Button(self.frame, text="Execute", command=self.execute_city_operation)
            self.execute_city_button.pack(side="bottom", pady=10)

        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.root, columns=('Show ID', 'Show Name', 'Description', 'Actors', 'Age Rating', 'Theatre ID', 'Theatre Name'), show='headings')
        self.tree.column('Show ID', width=60)
        self.tree.column('Show Name', width=150)
        self.tree.column('Description', width=700)
        self.tree.column('Actors', width=200)
        self.tree.column('Age Rating', width=80)
        self.tree.column('Theatre ID', width=60)
        self.tree.column('Theatre Name', width=200)
        self.tree.heading('Show ID', text='Show ID')
        self.tree.heading('Show Name', text='Show Name') 
        self.tree.heading('Description', text='Description')
        self.tree.heading('Actors', text='Actors')
        self.tree.heading('Age Rating', text='Age Rating')
        self.tree.heading('Theatre ID', text='Theatre ID')
        self.tree.heading('Theatre Name', text='Theatre Name')
        self.tree.pack()

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="horizon",
            charset='utf8mb4'
        )

        self.my_cursor = self.mydb.cursor()
        self.my_cursor.execute("SELECT Show_ID, Show_Name, Description, Actors, Age_Rating, Theatre_ID, Theatre_Name FROM shows")

        self.shows = self.my_cursor.fetchall()
        for show in self.shows:
            self.tree.insert('', tk.END, values=show)
                # General Buttons
        self.logout_button = tk.Button(self.root, text="Logout", command=return_callback)
        self.logout_button.pack()

        self.create_booking_button = tk.Button(self.root, text="Create Booking", command=self.create_booking)
        self.create_booking_button.pack()

        self.fetch_booking_button = tk.Button(self.root, text="Fetch Booking", command=self.fetch_booking)
        self.fetch_booking_button.pack()

        self.update_booking_button = tk.Button(self.root, text="Update Booking", command=self.update_booking)
        self.update_booking_button.pack()

        self.cancel_booking_button = tk.Button(self.root, text="Cancel Booking", command=self.cancel_booking)
        self.cancel_booking_button.pack()

        if self.is_manager:  # Add these buttons if the user is a manager
            self.execute_theatre_button = tk.Button(self.root, text="Manage Theatre", command=self.open_add_theatre_window)
            self.execute_theatre_button.pack()
        
            self.execute_city_button = tk.Button(self.root, text="Manage City", command=self.open_add_city_window)
            self.execute_city_button.pack()
            
            self.report_button = tk.Button(self.root, text="Generate Strategic Report", command=self.generate_report)
            self.report_button.pack()

        # Callbacks
        self.return_callback = return_callback


    # Add the function definitions for each button
    def logout(self):
        self.return_callback()
        
    def execute_theatre_operation(self):
        operation = self.operation.get()
        if operation:
            self.new_window = tk.Toplevel(self.root)
            self.app = AddTheatreWindow(self.new_window)
            self.app.execute_operation()  # Correct method call
        else:
            messagebox.showinfo("Error", "Please select an operation")
    
    def add_theatre(self):
        self.new_window = tk.Toplevel(self.root)
        AddTheatreWindow(self.new_window)
        
    def remove_theatre(self):
        self.new_window = tk.Toplevel(self.root)
        AddTheatreWindow(self.new_window)
        
    def update_theatre(self):
        self.new_window = tk.Toplevel(self.root)
        AddTheatreWindow(self.new_window)
        
    def open_add_theatre_window(self):
        newWindow = tk.Toplevel(self.root)
        self.app = AddTheatreWindow(newWindow, self.user_id)  
          
    def execute_city_operation(self):
        operation = self.operation.get()
        if operation:
            self.new_window = tk.Toplevel(self.root)
            self.app = AddCityWindow(self.new_window)
            self.app.execute_operation_city()  # Correct method call
        else:
            messagebox.showinfo("Error", "Please select an operation")
        
    def add_city(self):
        self.new_window = tk.Toplevel(self.root)
        AddCityWindow(self.new_window)
        
    def remove_city(self):
        self.new_window = tk.Toplevel(self.root)
        AddCityWindow(self.new_window)
        
    def update_city(self):
        self.new_window = tk.Toplevel(self.root)
        AddCityWindow(self.new_window)
        
    def open_add_city_window(self):
        newWindow = tk.Toplevel(self.root)
        self.app = AddCityWindow(newWindow, self.user_id)
        
    def generate_report(self):
        
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="horizon",
            charset='utf8mb4'
        )
        
        self.my_cursor = self.mydb.cursor()
        
        # Query to calculate total profit
        self.my_cursor.execute("SELECT SUM(total_price) FROM booking")
        total_profit = self.my_cursor.fetchone()[0]

        # Query to count total bookings
        self.my_cursor.execute("SELECT COUNT(*) FROM booking")
        total_bookings = self.my_cursor.fetchone()[0]

        # Query to count bookings per user
        self.my_cursor.execute("SELECT COUNT(*), user_id FROM booking GROUP BY user_id")
        bookings_per_user = self.my_cursor.fetchall()

        # Get current date and time
        current_date = datetime.datetime.now()

        # Generate report data
        report_data = f'Total profit: {total_profit}\n'
        report_data += f'Total bookings: {total_bookings}\n'
        for booking in bookings_per_user:
            report_data += f'User with ID {booking[1]} made {booking[0]} bookings\n'
        
        # Query to find the current highest ID in the report table
        self.my_cursor.execute("SELECT MAX(ID) FROM report")
        current_max_id = self.my_cursor.fetchone()[0]
        new_id = current_max_id if current_max_id else 0

        # Insert the report into the database for the manager (user_id = 1)
        insert_query = "INSERT INTO report (ID, User_ID, Creation_date_and_time, Report_Data) VALUES (%s, %s, %s, %s)"
        new_id += 1
        for booking in bookings_per_user:
            user_id = booking[1]
            if user_id == 1:  # Check if the user_id matches the manager's user_id
                self.my_cursor.execute(insert_query, (new_id, user_id, current_date, report_data))
                self.mydb.commit()
        
        # Create a new window and display the report data
        new_window = tk.Toplevel(self.root)
        new_window.title("Strategic Report")
        report_text = tk.Text(new_window, wrap='word')
        report_text.insert(tk.END, report_data)
        report_text.pack()

        # Close the connection
        self.mydb.close()

    def create_booking(self):
        newWindow = tk.Toplevel(self.root)
        self.app = BookingWindow(newWindow, self.return_to_show_list, self.logout_callback, self.user_id)

    def return_to_show_list(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root, self.return_callback, self.logout_callback, self.user_id, self.is_manager)

        
    def fetch_booking(self):
        
        self.my_cursor.execute("SELECT * FROM booking WHERE User_ID = %s", (self.user_id,))
        rows = self.my_cursor.fetchall()

        if rows:
            newWindow = tk.Toplevel(self.root)
            AllBookingsWindow(newWindow, self.user_id)  # Create one window for all bookings
        else:
            messagebox.showinfo("No bookings found for this user.")

    def update_booking(self):
        newWindow = tk.Toplevel(self.root)
        self.app = ShowAllBookingsWindow(newWindow, self.user_id)

    def cancel_booking(self):
        newWindow = tk.Toplevel(self.root)
        self.app = CancelBookingWindow(newWindow, self.user_id)

        self.my_cursor.close()
        self.mydb.close()

        # After the data is loaded, use update_idletasks to make sure all
        # widgets have had a chance to update their dimensions
        self.root.update_idletasks()
        width = self.tree.winfo_reqwidth()
        height = self.tree.winfo_reqheight()

        # Add a bit of padding to the dimensions
        width += 20
        height += 20
        self.root.geometry(f"{width}x{height}")

root = tk.Tk()
app = LoginWindow(root)
root.mainloop()
