import mysql.connector
import random

connection = mysql.connector.connect(
    host='127.0.1.1',
    port=3306,
    user='root',
    password='0707',
    database='table',
    autocommit=True
)

cursor = connection.cursor()

def load_airports():
    cursor.execute("SELECT ident, name, iso_country, municipality, iata_code FROM airports")
    airports = cursor.fetchall()
    return airports

class Aircraft:
    def __init__(self, name, speed, capacity, fuel):
        self.name = name
        self.speed = speed
        self.capacity = capacity
        self.fuel = fuel
        self.gold_coins = 100

    def upgrade_aircraft(self, new_speed, new_capacity):
        if self.gold_coins >= 50:
            self.speed = new_speed
            self.capacity = new_capacity
            self.gold_coins -= 50
            print(f"Aircraft upgraded! New speed: {self.speed}, New capacity: {self.capacity}")
        else:
            print("Not enough gold coins to upgrade!")

    def buy_fuel(self, amount):
        cost = amount * 5
        if self.gold_coins >= cost:
            self.fuel += amount
            self.gold_coins -= cost
            print(f"Bought {amount} units of fuel. Remaining fuel: {self.fuel}, Remaining gold coins: {self.gold_coins}")
        else:
            print("Not enough gold coins to buy fuel!")

    def fly(self, distance):
        fuel_needed = distance / 10
        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            print(f"Flew {distance} km. Remaining fuel: {self.fuel}")
            return True
        else:
            print("Not enough fuel to complete the flight!")
            return False

class Mission:
    def __init__(self, mission_type, distance, reward):
        self.mission_type = mission_type
        self.distance = distance
        self.reward = reward

    def complete_mission(self, aircraft):
        if aircraft.fly(self.distance):
            print(f"Mission {self.mission_type} completed! Earned {self.reward} gold coins.")
            aircraft.gold_coins += self.reward
        else:
            print("Mission failed! Not enough fuel.")


class Game:
    def __init__(self, player_name):
        self.player_name = player_name
        self.airports = self.load_airports_from_database()
        self.aircrafts = [
            Aircraft("Basic Plane", speed=200, capacity=100, fuel=500),
            Aircraft("Cargo Plane", speed=150, capacity=200, fuel=700),
        ]
        self.current_aircraft = None
        self.current_location = None
        self.missions = []

    def load_airports_from_database(self):
        cursor.execute("SELECT ident, name, iso_country, municipality, iata_code FROM airports")
        airports = cursor.fetchall()
        return airports

    def start_game(self):
        print(f"Welcome, {self.player_name}!")
        self.select_aircraft()
        self.select_starting_location()
        self.generate_missions()

    def select_aircraft(self):
        while True:
            try:
                print("Select an aircraft:")
                for idx, aircraft in enumerate(self.aircrafts):
                    print(f"{idx + 1}. {aircraft.name} (Speed: {aircraft.speed}, Capacity: {aircraft.capacity}, Fuel: {aircraft.fuel})")
                choice = int(input("Enter the aircraft number: ")) - 1
                if 0 <= choice < len(self.aircrafts):
                    self.current_aircraft = self.aircrafts[choice]
                    print(f"Selected aircraft: {self.current_aircraft.name}")
                    break
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Invalid input, please enter a number.")

    def select_starting_location(self):
        while True:
            try:
                print("Select your starting airport:")
                for idx, airport in enumerate(self.airports):
                    print(f"{idx + 1}. {airport[1]} (Code: {airport[0]}, City: {airport[3]}, Country: {airport[2]})")
                choice = int(input("Enter the starting airport number: ")) - 1
                if 0 <= choice < len(self.airports):
                    self.current_location = self.airports[choice]
                    print(f"Starting from: {self.current_location[1]} (Code: {self.current_location[0]}, City: {self.current_location[3]}, Country: {self.current_location[2]})")
                    break
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Invalid input, please enter a number.")

    def generate_missions(self):
        mission_types = ['Transport Passengers', 'Deliver Cargo', 'Time Trial']
        for _ in range(3):
            mission_type = random.choice(mission_types)
            distance = random.randint(100, 1000)  # Random flight distance
            reward = distance // 10  # Reward based on distance
            mission = Mission(mission_type, distance, reward)
            self.missions.append(mission)
        self.display_missions()

    def display_missions(self):
        print("Available missions:")
        for idx, mission in enumerate(self.missions):
            print(f"{idx + 1}. {mission.mission_type} - Distance: {mission.distance} km, Reward: {mission.reward} gold coins")
        self.choose_mission()

    def choose_mission(self):
        while True:
            try:
                choice = int(input("Enter the mission number: ")) - 1
                if 0 <= choice < len(self.missions):
                    selected_mission = self.missions[choice]
                    print(f"Selected mission: {selected_mission.mission_type}")
                    selected_mission.complete_mission(self.current_aircraft)
                    break
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Invalid input, please enter a number.")

    def upgrade_aircraft(self):
        print("Upgrading your aircraft...")
        self.current_aircraft.upgrade_aircraft(new_speed=300, new_capacity=150)

    def buy_fuel(self):
        while True:
            try:
                amount = int(input("Enter the amount of fuel to buy: "))
                if amount > 0:
                    self.current_aircraft.buy_fuel(amount)
                    break
                else:
                    print("The amount must be greater than 0.")
            except ValueError:
                print("Invalid input, please enter a number.")

    def save_game_to_database(self):
        cursor = connection.cursor()
        query = "INSERT INTO game (player_name, aircraft, gold_coins, location, fuel) VALUES (%s, %s, %s, %s, %s)"
        data = (self.player_name, self.current_aircraft.name, self.current_aircraft.gold_coins, self.current_location[1], self.current_aircraft.fuel)
        cursor.execute(query, data)
        connection.commit()
        print("Game progress saved.")

player_name = input("Enter your name: ")
game = Game(player_name)
game.start_game()

while True:
    action = input("Enter 'm' to start a mission, 'u' to upgrade your aircraft, 'f' to buy fuel, or 'q' to quit: ")
    if action == 'm':
        game.display_missions()
    elif action == 'u':
        game.upgrade_aircraft()
    elif action == 'f':
        game.buy_fuel()
    elif action == 'q':
        print("Exiting the game and saving progress...")
        game.save_game_to_database()
        print("Goodbye!")
        break
    else:
        print("Invalid input, please try again.")

cursor.close()
connection.close()


