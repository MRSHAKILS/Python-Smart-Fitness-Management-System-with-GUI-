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