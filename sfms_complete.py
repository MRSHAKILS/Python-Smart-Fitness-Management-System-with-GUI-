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
