import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import uuid
import json

# Backend Classes
class Member:
    def __init__(self, name, age, membership_type, fitness_goals):
        self.member_id = str(uuid.uuid4())[:8]
        self.name = name
        self.age = age
        self.membership_type = membership_type
        self.fitness_goals = fitness_goals
        self.progress_data = []
        self.workouts = []
        self.meals = []
        self.goals = {}

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "age": self.age,
            "membership_type": self.membership_type,
            "fitness_goals": self.fitness_goals,
            "progress_data": self.progress_data,
            "workouts": self.workouts,
            "meals": self.meals,
            "goals": self.goals,
        }
    
    def update(self, name, age, membership_type, fitness_goals):
        self.name = name
        self.age = age
        self.membership_type = membership_type
        self.fitness_goals = fitness_goals

class Trainer:
    # Placeholder for future extension, not used in GUI yet
    pass

class FitnessClass:
    # Placeholder for future extension, not used in GUI yet
    pass

class Transaction:
    # Placeholder for future extension, not used in GUI yet
    pass


# Main Application Controller
class SFMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Fitness Management System (SFMS)")
        self.geometry("1000x650")

        self.members = []
        self.load_members()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainMenu, UserManagementScreen, WorkoutTrackingScreen, GoalTrackingScreen,
                  NutritionTrackingScreen, ReportsScreen):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if hasattr(frame, "refresh"):  # call refresh method if exists
            frame.refresh()

    def save_members(self):
        try:
            data = [m.to_dict() for m in self.members]
            with open("sfms_members_data.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save members: {e}")

    def load_members(self):
        try:
            with open("sfms_members_data.json", "r") as f:
                data = json.load(f)
                for mdata in data:
                    member = Member(
                        mdata["name"],
                        mdata["age"],
                        mdata["membership_type"],
                        mdata["fitness_goals"],
                    )
                    member.member_id = mdata["member_id"]
                    member.progress_data = mdata.get("progress_data", [])
                    member.workouts = mdata.get("workouts", [])
                    member.meals = mdata.get("meals", [])
                    member.goals = mdata.get("goals", {})
                    self.members.append(member)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load members: {e}")

            # Main Menu Screen
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Smart Fitness Management System", font=("Helvetica", 24)).pack(pady=40)

        buttons = [
            ("User Management", UserManagementScreen),
            ("Workout Tracking", WorkoutTrackingScreen),
            ("Goal Tracking", GoalTrackingScreen),
            ("Nutrition Tracking", NutritionTrackingScreen),
            ("Reports & Analytics", ReportsScreen),
        ]

        for label, screen in buttons:
            ttk.Button(self, text=label, width=30, command=lambda s=screen: controller.show_frame(s)).pack(pady=12)


            # User Management Screen
class UserManagementScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_member = None

        # Layout
        left_frame = ttk.Frame(self, padding=10)
        left_frame.pack(side="left", fill="y")

        ttk.Label(left_frame, text="Members", font=("Helvetica", 16)).pack(pady=5)

        self.member_listbox = tk.Listbox(left_frame, height=25, width=35)
        self.member_listbox.pack()
        self.member_listbox.bind("<<ListboxSelect>>", self.on_member_select)

        right_frame = ttk.Frame(self, padding=10)
        right_frame.pack(side="right", fill="both", expand=True)

        ttk.Label(right_frame, text="Member Details", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(right_frame, text="Name:").grid(row=1, column=0, sticky="e")
        self.name_entry = ttk.Entry(right_frame, width=40)
        self.name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(right_frame, text="Age:").grid(row=2, column=0, sticky="e")
        self.age_entry = ttk.Entry(right_frame, width=40)
        self.age_entry.grid(row=2, column=1, pady=5)

        ttk.Label(right_frame, text="Membership Type:").grid(row=3, column=0, sticky="e")
        self.membership_var = tk.StringVar()
        self.membership_combo = ttk.Combobox(right_frame, textvariable=self.membership_var,
                                             values=["Basic", "Premium", "VIP"], state="readonly")
        self.membership_combo.grid(row=3, column=1, pady=5)

        ttk.Label(right_frame, text="Fitness Goals:").grid(row=4, column=0, sticky="e")
        self.goals_entry = ttk.Entry(right_frame, width=40)
        self.goals_entry.grid(row=4, column=1, pady=5)

        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Create New Member", command=self.create_member).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update Member", command=self.update_member).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Member", command=self.delete_member).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).grid(row=0, column=4, padx=5)

        ttk.Label(right_frame, text="Progress History", font=("Helvetica", 14)).grid(row=6, column=0, columnspan=2, pady=10)
        self.progress_text = tk.Text(right_frame, height=10, width=70, state="disabled")
        self.progress_text.grid(row=7, column=0, columnspan=2)

        self.refresh()

         def refresh(self):
        self.populate_member_list()
        self.clear_form()

    def populate_member_list(self):
        self.member_listbox.delete(0, tk.END)
        for m in self.controller.members:
            self.member_listbox.insert(tk.END, f"{m.name} ({m.membership_type})")

    def on_member_select(self, event):
        if not self.member_listbox.curselection():
            return
        index = self.member_listbox.curselection()[0]
        self.selected_member = self.controller.members[index]
        self.load_member_to_form(self.selected_member)

    def load_member_to_form(self, member):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, member.name)

        self.age_entry.delete(0, tk.END)
        self.age_entry.insert(0, str(member.age))

        self.membership_var.set(member.membership_type)
        self.goals_entry.delete(0, tk.END)
        self.goals_entry.insert(0, member.fitness_goals)

        self.progress_text.config(state="normal")
        self.progress_text.delete("1.0", tk.END)
        if member.progress_data:
            for i, entry in enumerate(member.progress_data, 1):
                self.progress_text.insert(tk.END, f"Entry {i} - Date: {entry.get('date', 'N/A')}\n")
                for k, v in entry.items():
                    if k != "date":
                        self.progress_text.insert(tk.END, f"  {k}: {v}\n")
                self.progress_text.insert(tk.END, "\n")
        else:
            self.progress_text.insert(tk.END, "No progress data recorded yet.\n")
        self.progress_text.config(state="disabled")

    def clear_form(self):
        self.selected_member = None
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.membership_var.set('')
        self.goals_entry.delete(0, tk.END)
        self.progress_text.config(state="normal")
        self.progress_text.delete("1.0", tk.END)
        self.progress_text.config(state="disabled")
        self.member_listbox.selection_clear(0, tk.END)

    def create_member(self):
        name = self.name_entry.get().strip()
        age_text = self.age_entry.get().strip()
        membership_type = self.membership_var.get()
        goals = self.goals_entry.get().strip()

        if not name or not age_text or not membership_type or not goals:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Age must be a positive integer.")
            return


