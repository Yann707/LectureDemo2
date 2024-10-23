'''import random
random_number = random.randint(1, 9)
number = 0
while True:
    user = int(input("Enter a number between 1 and 9: "))
    number = number + 1
    if user == random_number:
       print(f"Well done!You guessed it in {number} attempts!")
       break
    else:
        print("Wrong number!Try again")

user_input= ""
while user_input != "exit":
    user_input = input("Type something (or exit to quit): ")
    print("You typed:", user_input)

number = []

while True:
    user_input= input("Enter a number (or press Enter to quit): ")

    if user_input == "":
        break

    number.append(user_input)

if number:
    min = min(number)
    max = max(number)
    print(f"The smallest number is: {min}")
    print(f"The largest number is: {max}")
else:
    print("No numbers were entered.")

names = []

name = input("Enter the first name or quit by pressing Enter: ")
while name != "":
    names.append(name)
    name = input("Enter the next name or quit by pressing Enter: ")

print("Names list:", names)

otherNames = ["Allu", "Ninni"]
names.extend(otherNames)
print("After extending with ['Allu', 'Ninni']:", names)

###
def num(a, b):
    total = a + b
    print(f"The sum is: {total}")
    subtraction = a - b
    print(f"The subtraction is: {subtraction}")
    multiplication = a * b
    print(f"The multiplication is: {multiplication}")
    division = a / b
    print(f"The division is: {division}")
    return total, subtraction, multiplication, division

num(50,4)

###
def get_numbers():
    numbers = []
    while True:
        user_input = input("Enter a number (or type 'done' to finish): ")
        if user_input.lower() == 'done':
            break
        try:
            num = float(user_input)
            numbers.append(num)
        except ValueError:
            print("Please enter a valid number.")
    return numbers



def get_numbers():
    numbers = []
    while True:
        user = input("Enter a number (or 'Enter' to finish): ")
        if user.lower() == '':
            break
        numbers.append(float(user))
    return numbers


def main():
    numbers = get_numbers()

    if numbers:
        max_num = max(numbers)
        min_num = min(numbers)
        total_sum = sum(numbers)

        print(f"Maximum number: {max_num}")
        print(f"Minimum number: {min_num}")
        print(f"Sum of numbers: {total_sum}")
    else:
        print("No numbers were entered.")


main()
'''

import mysql.connector
import random

# MySQL Database connection
connection = mysql.connector.connect(
    host='127.0.1.1',
    port=3306,
    user='root',
    password='0707',
    database='table',  # Ensure the correct database name is used here
    autocommit=True
)

# Create a cursor to interact with the database
cursor = connection.cursor()

# Function to query data from the airports table
def load_airports():
    cursor.execute("SELECT ident, name, iso_country, municipality, iata_code FROM airports")
    airports = cursor.fetchall()  # Fetch all airport data
    return airports

# Aircraft class
class Aircraft:
    def __init__(self, name, speed, capacity, fuel):
        self.name = name
        self.speed = speed
        self.capacity = capacity
        self.fuel = fuel
        self.gold_coins = 100  # Start with 100 coins

    def upgrade_aircraft(self, new_speed, new_capacity):
        if self.gold_coins >= 50:
            self.speed = new_speed
            self.capacity = new_capacity
            self.gold_coins -= 50
            print(f"Aircraft upgraded! New speed: {self.speed}, New capacity: {self.capacity}")
        else:
            print("Not enough gold coins to upgrade!")

    def buy_fuel(self, amount):
        cost = amount * 5  # 5 coins per unit of fuel
        if self.gold_coins >= cost:
            self.fuel += amount
            self.gold_coins -= cost
            print(f"Bought {amount} units of fuel. Remaining fuel: {self.fuel}, Remaining gold coins: {self.gold_coins}")
        else:
            print("Not enough gold coins to buy fuel!")

    def fly(self, distance):
        fuel_needed = distance / 10  # 1 unit of fuel per 10 km flown
        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            print(f"Flew {distance} km. Remaining fuel: {self.fuel}")
            return True
        else:
            print("Not enough fuel to complete the flight!")
            return False

# Mission class
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

# Game class
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

    # Load airport data from the database
    def load_airports_from_database(self):
        cursor.execute("SELECT ident, name, iso_country, municipality, iata_code FROM airports")
        airports = cursor.fetchall()  # Fetch all airport data
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

# Main game loop
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

# Close the database connection
cursor.close()
connection.close()
