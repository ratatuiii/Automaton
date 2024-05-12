import random

class Day:
    def __init__(self, minutes=1440):
        self.minutes = minutes

    def update_minutes(self, minutes):
        self.minutes -= minutes

    def display_time(self):
        hours = (1440 - self.minutes) // 60
        minutes = (1440 - self.minutes) % 60
        return f"{hours:02d}:{minutes:02d}"


class State:
    def __init__(self):
        self.energy = 0
        self.mood = 0
        self.food = 80
        self.sleep_deposit = 0
        self.name = "Sleeping"
        self.day = Day()

    def update_markers(self, activity):
        if activity == "Sleeping":
            self.mood += 10
            self.food -= 10
            self.sleep_deposit += 10
            self.day.update_minutes(60)
        elif activity == "Meal Preparation":
            self.food += 20
            self.energy -= 5
            self.sleep_deposit -= 5
            self.day.update_minutes(30)
        elif activity == "Eating":
            self.mood += 10
            self.food += 30
            self.energy += 5
            self.sleep_deposit -= 5
            self.day.update_minutes(30)
        elif activity == "Washing dishes":
            self.mood += 5
            self.food -= 5
            self.energy -= 10
            self.sleep_deposit -= 5
            self.day.update_minutes(15)
        elif activity == "Work":
            self.mood -= 5
            self.food -= 10
            self.energy -= 15
            self.day.update_minutes(60)
        elif activity == "Walk":
            self.mood += 10
            self.food -= 10
            self.energy -= 10
            self.sleep_deposit -= 5
            self.day.update_minutes(30)
        elif activity == "Housekeeping":
            self.mood -= 5
            self.food -= 10
            self.energy -= 10
            self.sleep_deposit -= 5
            self.day.update_minutes(30)
        elif activity == "Relaxing":
            self.mood += 15
            self.food -= 5
            self.energy += 50
            self.sleep_deposit -= 5
            self.day.update_minutes(30)
        elif activity == "Conversation":
            self.mood += 5
            self.food -= 5
            self.energy -= 5
            self.day.update_minutes(30)
        elif activity == "Bed-to-toilet":
            self.energy -= 5
            self.food -= 5
            self.sleep_deposit -= 5
            self.day.update_minutes(15)

    def get_valid_transitions(self):
        if self.sleep_deposit < 80 and self.name == "Sleeping":
            return ["Sleeping"]

        if self.sleep_deposit < 1 and self.name != "Sleeping":
            return ["Sleeping"]

        if self.food <= 10 and self.name != "Meal Preparation":
            return ["Meal Preparation"]

        if self.energy < 10:
            return ["Relaxing"]

        valid_transitions = {
            "Sleeping": ["Bed-to-toilet"],
            "Bed-to-toilet": ["Meal Preparation", "Walk", "Work"],
            "Conversation": ["Relaxing", "Walk", "Eating", "Housekeeping"],
            "Meal Preparation": ["Eating"],
            "Eating": ["Washing dishes", "Relaxing", "Work"],
            "Washing dishes": ["Relaxing", "Work"],
            "Work": ["Relaxing", "Walk", "Conversation"],
            "Walk": ["Relaxing", "Conversation"],
            "Housekeeping": ["Relaxing"],
            "Relaxing": ["Work", "Walk", "Housekeeping", "Conversation"]
        }
        return valid_transitions[self.name]


class FSM:
    def __init__(self):
        self.state = State()

    def transition(self, next_activity):
        if next_activity in self.state.get_valid_transitions():
            self.info(next_activity)
            self.state.update_markers(next_activity)
            self.state.name = next_activity
        else:
            print(f"Invalid transition from {self.state.name} to {next_activity}")

    def handle_random_event(self):
        import random
        random_event = random.choice(["Call", "Headache", "Bad news"])
        print(f"Random event: {random_event}")

        if random_event == "Call":
            if "Conversation" in self.state.get_valid_transitions() and self.state.name != "Work":
                self.transition("Conversation")
        elif random_event == "Headache":
            if self.state.mood > 30:
                if "Relaxing" in self.state.get_valid_transitions():
                    self.transition("Relaxing")
            else:
                if "Sleeping" in self.state.get_valid_transitions():
                    self.transition("Sleeping")
        elif random_event == "Bad news":
            if self.state.mood > 70:
                if "Walk" in self.state.get_valid_transitions():
                    self.transition("Walk")
            else:
                if "Relaxing" in self.state.get_valid_transitions():
                    self.transition("Relaxing")

    def info(self, next_activity):
        print("-----------------")
        print(f"Transitioning from {self.state.name} to {next_activity}")
        print(f"Energy {self.state.energy}")
        print(f"Mood {self.state.mood}")
        print(f"Food {self.state.food}")
        print(f"Sleep_deposit: {self.state.sleep_deposit}")
        print(f"Current time: {self.state.day.display_time()}")

    def run(self):
        while self.state.day.minutes > 0:
            self.handle_random_event()
            valid_transitions = self.state.get_valid_transitions()
            random_activity = random.choice(valid_transitions)
            self.transition(random_activity)


if __name__ == "__main__":
    state_machine = FSM()
    state_machine.run()
