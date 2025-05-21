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
        
         new_member = Member(name, age, membership_type, goals)
        self.controller.members.append(new_member)
        self.controller.save_members()
        self.refresh()
        messagebox.showinfo("Success", f"Member '{name}' created successfully!")

    def update_member(self):
        if not self.selected_member:
            messagebox.showerror("Selection Error", "No member selected to update.")
            return

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

        self.selected_member.update(name, age, membership_type, goals)
        self.controller.save_members()
        self.refresh()
        messagebox.showinfo("Success", f"Member '{name}' updated successfully!")

        def delete_member(self):
        if not self.selected_member:
            messagebox.showerror("Selection Error", "No member selected to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete member '{self.selected_member.name}'?")
        if confirm:
            self.controller.members.remove(self.selected_member)
            self.controller.save_members()
            self.refresh()
            messagebox.showinfo("Deleted", "Member deleted successfully.")

            # Workout Tracking Screen
class WorkoutTrackingScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_member = None
        self.selected_workout_index = None

        left_frame = ttk.Frame(self, padding=10)
        left_frame.pack(side="left", fill="y")

        ttk.Label(left_frame, text="Members", font=("Helvetica", 16)).pack(pady=5)
        self.member_listbox = tk.Listbox(left_frame, height=20, width=30)
        self.member_listbox.pack()
        self.member_listbox.bind("<<ListboxSelect>>", self.on_member_select)

        ttk.Label(left_frame, text="Workouts", font=("Helvetica", 16)).pack(pady=10)
        self.workout_listbox = tk.Listbox(left_frame, height=20, width=30)
        self.workout_listbox.pack()
        self.workout_listbox.bind("<<ListboxSelect>>", self.on_workout_select)

        right_frame = ttk.Frame(self, padding=10)
        right_frame.pack(side="right", fill="both", expand=True)

        ttk.Label(right_frame, text="Log/Edit Workout", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(right_frame, text="Exercise Type:").grid(row=1, column=0, sticky="e")
        self.exercise_entry = ttk.Entry(right_frame, width=40)
        self.exercise_entry.grid(row=1, column=1, pady=5)

        ttk.Label(right_frame, text="Duration (minutes):").grid(row=2, column=0, sticky="e")
        self.duration_entry = ttk.Entry(right_frame, width=40)
        self.duration_entry.grid(row=2, column=1, pady=5)

        ttk.Label(right_frame, text="Calories Burned:").grid(row=3, column=0, sticky="e")
        self.calories_entry = ttk.Entry(right_frame, width=40)
        self.calories_entry.grid(row=3, column=1, pady=5)

        ttk.Label(right_frame, text="Notes:").grid(row=4, column=0, sticky="e")
        self.notes_entry = ttk.Entry(right_frame, width=40)
        self.notes_entry.grid(row=4, column=1, pady=5)

        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Add Workout", command=self.add_workout).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update Workout", command=self.update_workout).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Workout", command=self.delete_workout).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_workout_form).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).grid(row=0, column=4, padx=5)

        self.refresh()

        def refresh(self):
        self.populate_member_list()
        self.clear_workout_form()
        self.selected_member = None
        self.selected_workout_index = None

    def populate_member_list(self):
        self.member_listbox.delete(0, tk.END)
        for m in self.controller.members:
            self.member_listbox.insert(tk.END, f"{m.name} ({m.membership_type})")

    def populate_workout_list(self):
        self.workout_listbox.delete(0, tk.END)
        if self.selected_member:
            for i, workout in enumerate(self.selected_member.workouts):
                etype = workout.get("exercise_type", "N/A")
                date = workout.get("date", "N/A")
                self.workout_listbox.insert(tk.END, f"{i+1}. {etype} on {date}")

    def on_member_select(self, event):
        if not self.member_listbox.curselection():
            return
        index = self.member_listbox.curselection()[0]
        self.selected_member = self.controller.members[index]
        self.populate_workout_list()
        self.clear_workout_form()

    def on_workout_select(self, event):
        if not self.workout_listbox.curselection():
            return
        index = self.workout_listbox.curselection()[0]
        self.selected_workout_index = index
        workout = self.selected_member.workouts[index]
        self.load_workout_to_form(workout)

    def load_workout_to_form(self, workout):
        self.exercise_entry.delete(0, tk.END)
        self.exercise_entry.insert(0, workout.get("exercise_type", ""))

        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, str(workout.get("duration", "")))

        self.calories_entry.delete(0, tk.END)
        self.calories_entry.insert(0, str(workout.get("calories_burned", "")))

        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, workout.get("notes", ""))

    def clear_workout_form(self):
        self.selected_workout_index = None
        self.exercise_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        self.workout_listbox.selection_clear(0, tk.END)

    def add_workout(self):
        if not self.selected_member:
            messagebox.showerror("No User Selected", "Please select a member first.")
            return
        etype = self.exercise_entry.get().strip()
        duration = self.duration_entry.get().strip()
        calories = self.calories_entry.get().strip()
        notes = self.notes_entry.get().strip()

         if not etype or not duration or not calories:
            messagebox.showerror("Input Error", "Exercise Type, Duration, and Calories are required.")
            return
        try:
            duration = float(duration)
            calories = float(calories)
            if duration <= 0 or calories <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Duration and Calories must be positive numbers.")
            return

        workout = {
            "exercise_type": etype,
            "duration": duration,
            "calories_burned": calories,
            "notes": notes,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.selected_member.workouts.append(workout)
        self.controller.save_members()
        self.populate_workout_list()
        messagebox.showinfo("Success", "Workout added successfully.")
        self.clear_workout_form()

    def update_workout(self):
        if self.selected_workout_index is None:
            messagebox.showerror("No Workout Selected", "Please select a workout to update.")
            return
        if not self.selected_member:
            messagebox.showerror("No User Selected", "Please select a member first.")
            return

        etype = self.exercise_entry.get().strip()
        duration = self.duration_entry.get().strip()
        calories = self.calories_entry.get().strip()
        notes = self.notes_entry.get().strip()

         if not etype or not duration or not calories:
            messagebox.showerror("Input Error", "Exercise Type, Duration, and Calories are required.")
            return
        try:
            duration = float(duration)
            calories = float(calories)
            if duration <= 0 or calories <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Duration and Calories must be positive numbers.")
            return

        workout = self.selected_member.workouts[self.selected_workout_index]
        workout["exercise_type"] = etype
        workout["duration"] = duration
        workout["calories_burned"] = calories
        workout["notes"] = notes
        workout["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.controller.save_members()
        self.populate_workout_list()
        messagebox.showinfo("Success", "Workout updated successfully.")
        self.clear_workout_form()

         def delete_workout(self):
        if self.selected_workout_index is None:
            messagebox.showerror("No Workout Selected", "Please select a workout to delete.")
            return
        if not self.selected_member:
            messagebox.showerror("No User Selected", "Please select a member first.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this workout?")
        if confirm:
            del self.selected_member.workouts[self.selected_workout_index]
            self.controller.save_members()
            self.populate_workout_list()
            messagebox.showinfo("Deleted", "Workout deleted successfully.")
            self.clear_workout_form()

            # Goal Tracking Screen
class GoalTrackingScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_member = None

        left_frame = ttk.Frame(self, padding=10)
        left_frame.pack(side="left", fill="y")

        ttk.Label(left_frame, text="Members", font=("Helvetica", 16)).pack(pady=5)
        self.member_listbox = tk.Listbox(left_frame, height=30, width=30)
        self.member_listbox.pack()
        self.member_listbox.bind("<<ListboxSelect>>", self.on_member_select)

        right_frame = ttk.Frame(self, padding=10)
        right_frame.pack(side="right", fill="both", expand=True)

        ttk.Label(right_frame, text="Set Fitness Goals", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(right_frame, text="Calories to Burn:").grid(row=1, column=0, sticky="e")
        self.calories_goal_entry = ttk.Entry(right_frame, width=40)
        self.calories_goal_entry.grid(row=1, column=1, pady=5)

        ttk.Label(right_frame, text="Distance to Run (km):").grid(row=2, column=0, sticky="e")
        self.distance_goal_entry = ttk.Entry(right_frame, width=40)
        self.distance_goal_entry.grid(row=2, column=1, pady=5)

        ttk.Label(right_frame, text="Weight to Lift (kg):").grid(row=3, column=0, sticky="e")
        self.weight_goal_entry = ttk.Entry(right_frame, width=40)
        self.weight_goal_entry.grid(row=3, column=1, pady=5)

        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Set Goals", command=self.set_goals).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="View Progress", command=self.view_progress).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).grid(row=0, column=3, padx=5)

        self.progress_label = ttk.Label(right_frame, text="", font=("Helvetica", 14))
        self.progress_label.grid(row=5, column=0, columnspan=2)

        self.refresh()

    def refresh(self):
        self.populate_member_list()
        self.clear_form()
        self.selected_member = None

    def populate_member_list(self):
        self.member_listbox.delete(0, tk.END)
        for m in self.controller.members:
            self.member_listbox.insert(tk.END, f"{m.name} ({m.membership_type})")

    def on_member_select(self, event):
        if not self.member_listbox.curselection():
            return
        index = self.member_listbox.curselection()[0]
        self.selected_member = self.controller.members[index]
        self.load_goals()

    def load_goals(self):
        goals = self.selected_member.goals
        self.calories_goal_entry.delete(0, tk.END)
        self.distance_goal_entry.delete(0, tk.END)
        self.weight_goal_entry.delete(0, tk.END)

        self.calories_goal_entry.insert(0, goals.get("calories_to_burn", ""))
        self.distance_goal_entry.insert(0, goals.get("distance_to_run", ""))
        self.weight_goal_entry.insert(0, goals.get("weight_to_lift", ""))

    def set_goals(self):
        if not self.selected_member:
            messagebox.showerror("No User Selected", "Please select a member first.")
            return

        calories = self.calories_goal_entry.get().strip()
        distance = self.distance_goal_entry.get().strip()
        weight = self.weight_goal_entry.get().strip()

        try:
            calories_val = float(calories) if calories else 0
            distance_val = float(distance) if distance else 0
            weight_val = float(weight) if weight else 0
            if calories_val < 0 or distance_val < 0 or weight_val < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Goals must be non-negative numbers.")
            return

        self.selected_member.goals = {
            "calories_to_burn": calories_val,
            "distance_to_run": distance_val,
            "weight_to_lift": weight_val,
        }
        self.controller.save_members()
        messagebox.showinfo("Success", "Goals set successfully.")

    def view_progress(self):
        if not self.selected_member:
            messagebox.showerror("No User Selected", "Please select a member first.")
            return
        goals = self.selected_member.goals
        workouts = self.selected_member.workouts

        if not goals:
            self.progress_label.config(text="No goals set yet.")
            return
        
                # Calculate progress
        total_calories = sum(w.get("calories_burned", 0) for w in workouts)
        total_distance = sum(w.get("distance", 0) for w in workouts)  # distance optional
        # Weight lifting progress not tracked directly here, show as N/A

        progress_text = f"Calories burned: {total_calories} / {goals.get('calories_to_burn', 0)}\n"
        progress_text += f"Distance run: {total_distance} km / {goals.get('distance_to_run', 0)} km\n"
        progress_text += f"Weight to lift goal: {goals.get('weight_to_lift', 'N/A')} kg\n"

        self.progress_label.config(text=progress_text)

    def clear_form(self):
        self.calories_goal_entry.delete(0, tk.END)
        self.distance_goal_entry.delete(0, tk.END)
        self.weight_goal_entry.delete(0, tk.END)
        self.progress_label.config(text="")
        self.member_listbox.selection_clear(0, tk.END)
        self.selected_member = None

        # Nutrition Tracking Screen
class NutritionTrackingScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_member = None
        self.selected_meal_index = None

        left_frame = ttk.Frame(self, padding=10)
        left_frame.pack(side="left", fill="y")

        ttk.Label(left_frame, text="Members", font=("Helvetica", 16)).pack(pady=5)
        self.member_listbox = tk.Listbox(left_frame, height=20, width=30)
        self.member_listbox.pack()
        self.member_listbox.bind("<<ListboxSelect>>", self.on_member_select)

        ttk.Label(left_frame, text="Meals", font=("Helvetica", 16)).pack(pady=10)
        self.meal_listbox = tk.Listbox(left_frame, height=20, width=30)
        self.meal_listbox.pack()
        self.meal_listbox.bind("<<ListboxSelect>>", self.on_meal_select)

        right_frame = ttk.Frame(self, padding=10)
        right_frame.pack(side="right", fill="both", expand=True)

        ttk.Label(right_frame, text="Log/Edit Meal", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(right_frame, text="Meal Type:").grid(row=1, column=0, sticky="e")
        self.meal_type_combo = ttk.Combobox(right_frame, values=["Breakfast", "Lunch", "Dinner", "Snack"], state="readonly")
        self.meal_type_combo.grid(row=1, column=1, pady=5)

        ttk.Label(right_frame, text="Calories:").grid(row=2, column=0, sticky="e")
        self.calories_entry = ttk.Entry(right_frame, width=40)
        self.calories_entry.grid(row=2, column=1, pady=5)

        ttk.Label(right_frame, text="Proteins (g):").grid(row=3, column=0, sticky="e")
        self.protein_entry = ttk.Entry(right_frame, width=40)
        self.protein_entry.grid(row=3, column=1, pady=5)

        ttk.Label(right_frame, text="Carbs (g):").grid(row=4, column=0, sticky="e")
        self.carbs_entry = ttk.Entry(right_frame, width=40)
        self.carbs_entry.grid(row=4, column=1, pady=5)

        ttk.Label(right_frame, text="Fats (g):").grid(row=5, column=0, sticky="e")
        self.fats_entry = ttk.Entry(right_frame, width=40)
        self.fats_entry.grid(row=5, column=1, pady=5)

        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Add Meal", command=self.add_meal).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update Meal", command=self.update_meal).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Meal", command=self.delete_meal).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_meal_form).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).grid(row=0, column=4, padx=5)

        self.refresh()

    def refresh(self):
        self.populate_member_list()
        self.clear_meal_form()
        self.selected_member = None
        self.selected_meal_index = None

    def populate_member_list(self):
        self.member_listbox.delete(0, tk.END)
        for m in self.controller.members:
            self.member_listbox.insert(tk.END, f"{m.name} ({m.membership_type})")

    def populate_meal_list(self):
        self.meal_listbox.delete(0, tk.END)
        if self.selected_member:
            for i, meal in enumerate(self.selected_member.meals):
                mtype = meal.get("meal_type", "N/A")
                date = meal.get("date", "N/A")
                self.meal_listbox.insert(tk.END, f"{i+1}. {mtype} on {date}")

    def on_member_select(self, event):
        if not self.member_listbox.curselection():
            return
        index = self.member_listbox.curselection()[0]
        self.selected_member = self.controller.members[index]
        self.populate_meal_list()
        self.clear_meal_form()

    def on_meal_select(self, event):
        if not self.meal_listbox.curselection():
            return
        index = self.meal_listbox.curselection()[0]
        self.selected_meal_index = index
        meal = self.selected_member.meals[index]
        self.load_meal_to_form(meal)

    def load_meal_to_form(self, meal):
        self.meal_type_combo.set(meal.get("meal_type", ""))
        self.calories_entry.delete(0, tk.END)
        self.calories_entry.insert(0, str(meal.get("calories", "")))
        self.protein_entry.delete(0, tk.END)
        self.protein_entry.insert(0, str(meal.get("protein", "")))
        self.carbs_entry.delete(0, tk.END)
        self.carbs_entry.insert(0, str(meal.get("carbs", "")))
        self.fats_entry.delete(0, tk.END)
        self.fats_entry.insert(0, str(meal.get("fats", "")))

    def clear_meal_form(self):
        self.selected_meal_index = None
        self.meal_type_combo.set('')
        self.calories_entry.delete(0, tk.END)
        self.protein_entry.delete(0, tk.END)
        self.carbs_entry.delete(0, tk.END)
        self.fats_entry.delete(0, tk.END)
        self.meal_listbox.selection_clear(0, tk.END)

    def add_meal(self):
        if not self.selected_member:
            messagebox.showerror("No User Selected", "Please select a member first.")
            return
        mtype = self.meal_type_combo.get()
        calories = self.calories_entry.get().strip()
        protein = self.protein_entry.get().strip()
        carbs = self.carbs_entry.get().strip()
        fats = self.fats_entry.get().strip()

        if not mtype or not calories:
            messagebox.showerror("Input Error", "Meal Type and Calories are required.")
            return

        try:
            calories_val = float(calories)
            protein_val = float(protein) if protein else 0
            carbs_val = float(carbs) if carbs else 0
            fats_val = float(fats) if fats else 0
            if calories_val < 0 or protein_val < 0 or carbs_val < 0 or fats_val < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Nutritional values must be non-negative numbers.")
            return

        meal = {
            "meal_type": mtype,
            "calories": calories_val,
            "protein": protein_val,
            "carbs": carbs_val,
            "fats": fats_val,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.selected_member.meals.append(meal)
        self.controller.save_members()
        self.populate_meal_list()
        messagebox.showinfo("Success", "Meal added successfully.")
        self.clear_meal_form()

    def update_meal(self):
        if self.selected_meal_index is None:
            messagebox.showerror("No Meal Selected", "Please select a meal to update.")
            return
        if not self.selected_member:
            messagebox.showerror("No User Selected", "Please select a member first.")
            return
        mtype = self.meal_type_combo.get()
        calories = self.calories_entry.get().strip()
        protein = self.protein_entry.get().strip()
        carbs = self.carbs_entry.get().strip()
        fats = self.fats_entry.get().strip()

        if not mtype or not calories:
            messagebox.showerror("Input Error", "Meal Type and Calories are required.")
            return

        try:
            calories_val = float(calories)
            protein_val = float(protein) if protein else 0
            carbs_val = float(carbs) if carbs else 0
            fats_val = float(fats) if fats else 0
            if calories_val < 0 or protein_val < 0 or carbs_val < 0 or fats_val < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Nutritional values must be non-negative numbers.")
            return

        meal = self.selected_member.meals[self.selected_meal_index]
        meal["meal_type"] = mtype
        meal["calories"] = calories_val
        meal["protein"] = protein_val
        meal["carbs"] = carbs_val
        meal["fats"] = fats_val
        meal["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.controller.save_members()
        self.populate_meal_list()
        messagebox.showinfo("Success", "Meal updated successfully.")
        self.clear_meal_form()

    def delete_meal(self):
        if self.selected_meal_index is None:
            messagebox.showerror("No Meal Selected", "Please select a meal to delete.")
            return
        if not self.selected_member:
            messagebox.showerror("No User Selected", "Please select a member first.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this meal?")
        if confirm:
            del self.selected_member.meals[self.selected_meal_index]
            self.controller.save_members()
            self.populate_meal_list()
            messagebox.showinfo("Deleted", "Meal deleted successfully.")
            self.clear_meal_form()








