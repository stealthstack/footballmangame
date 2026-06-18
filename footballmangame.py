import os
import random

CITY_NAMES = [
    "Tacoma", "Sacramento", "Charleston", "Fayetteville", "Pueblo", "Roswell",
    "Huntsville", "Tucson", "Gulfport", "Columbus", "Dover", "Missoula",
    "Buffalo", "Laredo", "Fresno", "Portland", "San Antonio", "San Diego",
    "Austin", "Albaquerque", "Louisville", "Boise", "Richmond", "Omaha",
    "Freemont", "Tulsa", "Wichita", "Mesa", "El Paso", "Bakersfield",
    "Aurora", "Colorado Springs", "Honolulu", "Santa Ana", "Corpus Christi",
    "Riverside", "Stockton", "Anchorage", "Henderson", "Greensboro",
    "Plano", "Lincoln", "Toledo", "Irvine", "Jersey City", "Durham",
    "Madison", "Scottsdale", "Reno", "Norfolk", "Chesapeake", "Garland",
    "Napa Valley", "Navarre", "Destin", "Lubbock",
]

ANIMAL_OBJECT_NAMES = [
    "Sound", "Arachnids", "Heights", "Blackout", "Dogs", "Storm",
    "Snakes", "Ocean", "Wilds", "Mirrors", "Whales", "Zoom",
    "Sharks", "Spectres", "Reapers", "Devils", "Wildcats", "Strays",
    "Jesters", "Tyrants",
]

PLAYER_NAMES = [
    "Oliver", "Tree", "Tom", "Julio", "Aaron", "Patrick", "Derrick",
    "Travis", "Michael", "Tyreek", "Dalvin", "Stefon", "Alvin", "George",
    "Josh", "Justin", "Jordan", "Jaylen", "Kevin", "Kyrie", "Kyle", "Karl",
    "Kobe", "Jamin", "James", "Jason", "DeAndre", "Jay", "Colby", "Cole",
    "Cody", "Cameron", "Cam", "Clay", "Chris", "Chase", "Chad", "Blake",
    "Brad", "Bradley", "Brett", "Bryce", "Bryan", "Bryant", "Bryson",
    "Alex", "Carl", "Carlos", "Carlton", "Eric", "Eddie", "Edward",
    "Dean", "Darius", "Darren", "Darrell", "Darryl", "Darion", "Darwin",
    "Felix", "Frank", "Frankie", "Freddie", "Fred", "Fredrick", "Freddy",
    "Greg", "Gregory", "Garrett", "George", "Gerald", "Harry", "Henry",
    "Hank", "Henrik", "Isaac", "Isaiah", "Jack", "Jake", "Jamal", "Jamison",
    "Larry", "Loyd", "Louis", "Louie", "Mark", "Marcus", "Marco",
    "Marshall", "Mason", "Michael", "Mitchell", "Mitchel", "Mitch", "Mike",
    "Nate", "Nathan", "Nathaniel", "Nicholas", "Oscar", "Omar", "Otis",
    "Owen", "Pat", "Randy", "Randall", "Scott", "Sean", "Shawn", "Steve",
    "Steven", "Terry", "Tim", "Timothy", "Tyler", "Ty", "Tyrone", "Ulysses",
    "Victor", "Vincent", "William", "Wilson", "Wesley", "Wes", "Walker",
    "Xavier", "Xander", "Zach", "Zack", "Zane", "Zackary", "Christian",
]

# Global variables
cut_players = []
drafted_players = []
free_agent_pool = []
worst_teams_after_8_games = []

INITIAL_FREE_AGENTS = 5
POSITION_COUNTS = {"QB": 1, "RB": 1, "WR": 2, "DL": 2, "Safety": 1, "Kicker": 1}

# Define ANSI color codes for traits
TRAIT_COLORS = {
    "Problematic": "\033[91m",      # Red
    "Hometown Hero": "\033[92m",    # Green
    "Challenger": "\033[92m",       # Green
    "Optimist": "\033[92m",         # Green
    "Star Player": "\033[94m",      # Light Blue
    "Medalist": "\033[94m",         # Light Blue
    "Team Captain": "\033[94m",     # Light Blue
    "Hall of Fame": "\033[38;5;208m",  # Orange
    "Reformed": "\033[93m",         # Yellow
}

GREEN_TRAITS = {"Hometown Hero", "Challenger", "Optimist"}
LIGHT_BLUE_TRAITS = {"Star Player", "Medalist", "Team Captain"}
RED_TRAITS = {"Problematic"}
ORANGE_TRAITS = {"Hall of Fame"}
YELLOW_TRAITS = {"Reformed"}

TRAIT_DESCRIPTIONS = {
    "Problematic": "This player has been cut from a team and may pose issues.",
    "Hometown Hero": "This player shined brightly in a highlight and gains a bonus when playing at home.",
    "Challenger": "This player shined brightly in a highlight and gains a bonus when playing away.",
    "Star Player": "This player was a star in the championship game.",
    "Medalist": "This player gains bonus points based on medals.",
    "Optimist": "This player keeps a positive mindset, enhancing performance overall.",
    "Team Captain": "The team leader who provides consistent bonuses.",
    "Hall of Fame": "A legendary player who has reached the pinnacle of excellence.",
    "Reformed": "Once a liability, now a cornerstone. This player turned it around.",
}

TRAIT_SCORE_MODIFIERS = {
    "Problematic": -5,
    "Hometown Hero": 10,
    "Challenger": 15,
    "Optimist": 5,
    "Star Player": 10,
    "Team Captain": 5,
    "Hall of Fame": 20,
    "Reformed": 10,
}

POSITIVE_TRAITS = ["Hometown Hero", "Challenger"]

def reset_color():
    return "\033[0m"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def ansi_color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def generate_random_color(used_colors):
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color not in used_colors:
            used_colors.add(color)
            return color

class Player:
    def __init__(self, position, first_name, last_name, score=70):
        self.original_position = position
        self.position = position
        self.first_name = first_name
        self.last_name = last_name
        self.score = max(score or 70, 1)  # Ensure score is never None or 0
        self.player_name = f"{self.first_name} {self.last_name}"
        self.temp_retrieved = False
        self.gold_medals = 0
        self.silver_medals = 0
        self.traits = {}
        self.home = False
        self.nfl_team = None
        self.hof_news_shown = False
        self.started_season = False
        
    def update_position(self, new_position):
        """Handle position changes and trait management"""
        if new_position != self.original_position:
            if "Reformed" in self.traits:
                self.traits.pop("Reformed")
            if "Problematic" not in self.traits:
                self.add_trait("Problematic")
        self.position = new_position
  
    def add_trait(self, trait_name):
        """Add a trait to the player with its predefined modifier"""
        if trait_name in TRAIT_SCORE_MODIFIERS:
            self.traits[trait_name] = TRAIT_SCORE_MODIFIERS[trait_name]
        else:
            self.traits[trait_name] = 0
    
    def calculate_medalist_bonus(self):
        """Calculate bonus points from medals"""
        return (self.gold_medals * 5) + (self.silver_medals * 2)
        
    def get_effective_score(self):
        """Calculate the player's effective score including all bonuses"""
        effective_score = self.score
        
        for trait, bonus in self.traits.items():
            if trait == "Medalist":
                effective_score += self.calculate_medalist_bonus()
            elif trait == "Hometown Hero":
                if self.home:
                    effective_score += bonus
            elif trait == "Challenger":
                if not self.home:
                    effective_score += bonus
            else:  # All other traits including Problematic
                effective_score += bonus
                
        return max(effective_score, 1)  # Ensure score never goes below 1

    def __str__(self):
        medals = ""
        if self.gold_medals > 0:
            medals += f"{self.gold_medals}x🥇 "
        if self.silver_medals > 0:
            medals += f"{self.silver_medals}x🥈"
        
        effective_score = self.get_effective_score()
        bonus_str = ""
        net_bonus = effective_score - self.score
        trait_strs = []
        
        # Process each trait in consistent order
        for trait in sorted(self.traits.keys()):
            if trait in TRAIT_COLORS:
                trait_strs.append(f"{TRAIT_COLORS[trait]}{trait}{reset_color()}")
            else:
                trait_strs.append(trait)
        
        # Show net bonus only if non-zero
        if net_bonus != 0:
            bonus_color = TRAIT_COLORS["Hometown Hero"] if net_bonus > 0 else TRAIT_COLORS["Problematic"]
            bonus_str = f" {bonus_color}{'+' if net_bonus > 0 else ''}{net_bonus}{reset_color()}"
        
        traits_display = " ".join(trait_strs)
        
        return f"{self.player_name} ({effective_score}{bonus_str}) {medals.strip()} {traits_display}"

class Team:
    def __init__(self, name, color, home=False):
        self.name = name
        self.color = color
        self.players = []
        self.home = home
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.games_played = 0
        self.trophies = []
        self.coach_name = generate_coach_name()
        self.current_streak = 0
        self.playoff_bubble_shown = False
        self.playoff_secured_shown = False
        self.rebrand_immunity = False
        self.historic_wins = 0
        self.historic_losses = 0
        self.historic_ties = 0
        self.historic_games_played = 0
        self.first_place_seasons = []
        self.second_place_seasons = []

    def add_first_place(self, season_number):
        self.first_place_seasons.append(season_number)

    def add_second_place(self, season_number):
        self.second_place_seasons.append(season_number)

    def get_place_badges(self):
        badges = ""
        if self.first_place_seasons:
            recent_first = self.first_place_seasons[-1]
            total_firsts = len(self.first_place_seasons)
            badges += f" 🥇 (S{recent_first}, #:{total_firsts})"
        if self.second_place_seasons:
            recent_second = self.second_place_seasons[-1]
            total_seconds = len(self.second_place_seasons)
            badges += f" 🥈 (S{recent_second}, #:{total_seconds})"
        return badges

    def add_player(self, player):
        if player not in self.players:  # Prevent duplicates
            self.players.append(player)

    def get_total_score(self):
        total_score = 0
        for player in self.players:
            effective_score = player.get_effective_score()
            total_score += effective_score
        return total_score

    def display_team(self):
        home_away = "Home" if self.home else "Away"
        print(f"{home_away} - {self}:")
        for player in self.players:
            print(f"{player.position}: {str(player)}")
        print(f"Team Score: {self.get_total_score()}")

    def display_record(self):
        print(f"Record: Wins: {self.wins}, Losses: {self.losses}, Ties: {self.ties}, Games Played: {self.games_played}")
        print(f"Historic Record: Wins: {self.historic_wins}, Losses: {self.historic_losses}, Ties: {self.historic_ties}, Games Played: {self.historic_games_played}")

    def __str__(self):
        color_code = ansi_color(*self.color)
        reset_code = reset_color()
        return f"{color_code}{self.name}{reset_code}{self.get_place_badges()}"
    def get_team_captain(self):
        """Get the current team captain, if any"""
        for player in self.players:
            if "Team Captain" in player.traits:
                return player
        return None

    def get_spokesperson_info(self):
        """Returns (name, title) — 50/50 between captain and coach when both exist."""
        captain = self.get_team_captain()
        if captain and random.random() < 0.5:
            return captain.player_name, "Team Captain"
        return self.coach_name, "Coach"

    def assign_team_captain(self, new_captain):
        """Assign team captain role to a player"""
        # Remove captain from current captain if exists
        current_captain = self.get_team_captain()
        if current_captain and current_captain != new_captain:
            if "Team Captain" in current_captain.traits:
                del current_captain.traits["Team Captain"]
    
        # Assign to new captain
        new_captain.add_trait("Team Captain")
        print(f"🎖️ {new_captain.player_name} has been named Team Captain of {self.name}!")
        
    def award_trophy(self, trophy_name):
        self.trophies.append(trophy_name)
        print(f"{self.name} has been awarded the {trophy_name}!")

# Utility functions
def generate_coach_name():
    return f"{random.choice(PLAYER_NAMES)} {random.choice(PLAYER_NAMES)}"

def generate_random_name(team):
    attempts = 0
    while attempts < 100:
        first_name = random.choice(PLAYER_NAMES)
        last_name = random.choice(PLAYER_NAMES)
        player_name = f"{first_name} {last_name}"
        if not any(player.player_name == player_name for player in team.players):
            return player_name
        attempts += 1
    # Fallback: add random number to ensure uniqueness
    first_name = random.choice(PLAYER_NAMES)
    last_name = random.choice(PLAYER_NAMES)
    return f"{first_name} {last_name} {random.randint(1000, 9999)}"

def add_random_player_to_team(team, position):
    player_name = generate_random_name(team)
    first_name, last_name = player_name.split(None, 1)  # Handle names with numbers
    score = random.randint(65, 75)  # Changed from 60-85 to 65-75
    new_player = Player(position, first_name, last_name, score)
    return new_player

def generate_initial_free_agents():
    """Create initial random players for free agent pool"""
    global free_agent_pool
    free_agent_pool.clear()  # Clear existing pool
    for _ in range(INITIAL_FREE_AGENTS):
        position = random.choice(["QB", "RB", "WR", "DL", "Safety", "Kicker"])
        first_name = random.choice(PLAYER_NAMES)
        last_name = random.choice(PLAYER_NAMES)
        score = random.randint(65, 75)
        player = Player(position, first_name, last_name, score)
        free_agent_pool.append(player)

def display_free_agents():
    """Show available free agents with stats"""
    if not free_agent_pool:
        print("No free agents available currently.")
        return
    
    print("\nFree Agent Pool:")
    print("{:<5} {:<20} {:<10} {:<10} {:<15}".format(
        "#", "Name", "Position", "Score", "Traits"))
    
    for i, player in enumerate(free_agent_pool, 1):
        traits = ", ".join(player.traits.keys()) if player.traits else "None"
        print("{:<5} {:<20} {:<10} {:<10} {:<15}".format(
            i, player.player_name, player.position, 
            player.get_effective_score(), traits))

def sign_free_agent(team, preferred_position=None):
    """Allow user to manually sign a free agent"""
    if not free_agent_pool:
        print("No free agents available to sign.")
        return False
    
    display_free_agents()
    print(f"\nWhich free agent would you like to sign for {team.name}?")
    print(f"Enter number (1-{len(free_agent_pool)}) or 0 to cancel")

    while True:
        raw = input("> ").strip()
        if raw == "":
            print("Please enter a number or 0 to cancel.")
            continue
        if not raw.isdigit():
            print("Please enter a valid number.")
            continue

        choice = int(raw) - 1
        if choice == -1:
            return False

        if 0 <= choice < len(free_agent_pool):
            player = free_agent_pool[choice]

            # If no preferred position, ask user
            if not preferred_position:
                print(f"\nSign {player.player_name} (Original: {player.original_position})")
                print("Assign to position:")
                valid_positions = ["QB", "RB", "WR", "DL", "Safety", "Kicker"]
                for i, pos in enumerate(valid_positions, 1):
                    print(f"{i}. {pos}")

                while True:
                    pos_raw = input("> ").strip()
                    if not pos_raw.isdigit():
                        print("Please enter the number of the position.")
                        continue
                    pos_choice = int(pos_raw) - 1
                    if 0 <= pos_choice < len(valid_positions):
                        new_position = valid_positions[pos_choice]
                        break
                    else:
                        print("Invalid position choice. Try again.")
            else:
                new_position = preferred_position

            # If position is under its expected headcount, fill the vacancy
            position_players = [p for p in team.players if p.position == new_position]
            expected = POSITION_COUNTS.get(new_position, 1)
            if len(position_players) < expected:
                player.update_position(new_position)
                team.add_player(player)
                free_agent_pool.remove(player)
                print(f"Signed {player.player_name} as {new_position} (filling vacant slot)!")
                return True

            # Otherwise find the worst player at this position to replace
            worst_player = min(position_players, key=lambda p: p.get_effective_score())

            print(f"\nThis will replace {worst_player.player_name} (Score: {worst_player.get_effective_score()})")

            while True:
                confirm = input("Confirm signing? (y/n): ").strip().lower()
                if confirm in ("y", "n"):
                    break
                print("Please enter 'y' or 'n'.")

            if confirm == 'y':
                # Cut existing player (who becomes new free agent)
                team.players.remove(worst_player)
                worst_player.add_trait("Problematic")
                free_agent_pool.append(worst_player)

                # Add new player
                player.update_position(new_position)
                team.add_player(player)
                free_agent_pool.remove(player)

                print(f"Signed {player.player_name} as {new_position}!")
                if new_position != player.original_position:
                    print("⚠️ Player gained Problematic trait (-5) for playing out of position")
                return True
            else:
                print("Signing cancelled.")
                return False
        else:
            print(f"Invalid selection. Enter a number between 1 and {len(free_agent_pool)}, or 0 to cancel.")
            continue

def cut_player_interactive(team):
    """Allow user to manually cut a player"""
    global free_agent_pool
    
    if not team.players:
        print("No players to cut!")
        return
        
    print("\nCurrent Roster:")
    team.display_team()
    print("\nSelect player to cut:")
    
    for i, player in enumerate(team.players, 1):
        print(f"{i}. {player}")

    while True:
        raw = input("Enter number (0 to cancel): ").strip()
        if raw == "":
            print("Please enter a number or 0 to cancel.")
            continue
        if not raw.isdigit():
            print("Please enter a valid number.")
            continue

        choice = int(raw)
        if choice == 0:
            print("Cut cancelled.")
            return
        if 1 <= choice <= len(team.players):
            player = team.players[choice - 1]
            print(f"\nCutting {player.player_name}...")
            team.players.remove(player)
            player.add_trait("Problematic")
            free_agent_pool.append(player)  # Add to free agent pool
            print(f"{player.player_name} has been cut and added to free agents")
            return
        else:
            print(f"Invalid selection. Enter 1-{len(team.players)} or 0 to cancel.")
            continue

def create_random_team(existing_team_names, used_city_names, used_mascot_names, used_colors):
    max_attempts = 100
    attempts = 0
    
    while attempts < max_attempts:
        city_name = random.choice(CITY_NAMES)
        animal_object_name = random.choice(ANIMAL_OBJECT_NAMES)
        team_name = f"{city_name} {animal_object_name}"

        if (city_name not in used_city_names and 
            animal_object_name not in used_mascot_names and 
            team_name not in existing_team_names):
            
            existing_team_names.add(team_name)
            used_city_names.add(city_name)
            used_mascot_names.add(animal_object_name)
            break
        attempts += 1
    else:
        # Fallback: create team with number suffix
        city_name = random.choice(CITY_NAMES)
        animal_object_name = random.choice(ANIMAL_OBJECT_NAMES)
        team_name = f"{city_name} {animal_object_name} {random.randint(1, 999)}"

    team_color = generate_random_color(used_colors)
    team = Team(team_name, team_color)
    
    # Create roster
    for position, count in [("QB", 1), ("RB", 1), ("WR", 2), ("DL", 2), ("Safety", 1), ("Kicker", 1)]:
        for _ in range(count):
            player_name = generate_random_name(team)
            first_name, last_name = player_name.split(None, 1)
            team.add_player(Player(position, first_name, last_name, random.randint(70, 95)))
    
    return team

def generate_teams(num_teams=16):
    teams = []
    existing_team_names = set()
    used_city_names = set()
    used_mascot_names = set()
    used_colors = set()
    
    while len(teams) < num_teams:
        team = create_random_team(existing_team_names, used_city_names, used_mascot_names, used_colors)
        teams.append(team)
    
    return teams

def generate_round_robin_schedule(teams):
    if len(teams) != 16:
        raise ValueError("The number of teams must be 16")
    
    schedule = []
    teams_copy = teams.copy()
    num_teams = len(teams_copy)
    
    for round_num in range(num_teams - 1):
        round_matchups = []
        for i in range(num_teams // 2):
            team1 = teams_copy[i]
            team2 = teams_copy[num_teams - 1 - i]
            round_matchups.append((team1, team2))
        
        # Rotate teams for the next round while keeping the first team in place
        teams_copy = [teams_copy[0]] + [teams_copy[-1]] + teams_copy[1:-1]
        schedule.append(round_matchups)
    
    return schedule

def calculate_win_probability(my_score, opp_score, my_team_is_home):
    """Exact probability based on roll ranges: home 51-150, away 1-100."""
    G = (opp_score - my_score) - 50 if my_team_is_home else (opp_score - my_score) + 50
    if G >= 99:
        return 0.0
    if G >= 0:
        return (99 - G) * (100 - G) / 20000.0
    G_prime = -G - 1
    if G_prime >= 99:
        return 1.0
    return 1.0 - (99 - G_prime) * (100 - G_prime) / 20000.0

def simulate_game(home_team, away_team, must_have_winner=False):
    """Simulate a game between two teams"""
    # Set home/away status
    home_team.home = True
    away_team.home = False

    # Set home attribute for players
    for player in home_team.players:
        player.home = True
    for player in away_team.players:
        player.home = False

    max_attempts = 100
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        home_roll = random.randint(1, 100) + 50  # Home team advantage
        away_roll = random.randint(1, 100)
        home_total = home_roll + home_team.get_total_score()
        away_total = away_roll + away_team.get_total_score()

        if home_total > away_total:
            home_team.wins += 1
            away_team.losses += 1
            home_team.games_played += 1
            away_team.games_played += 1
            home_team.current_streak = home_team.current_streak + 1 if home_team.current_streak > 0 else 1
            away_team.current_streak = away_team.current_streak - 1 if away_team.current_streak < 0 else -1
            return home_team, away_team
        elif home_total < away_total:
            away_team.wins += 1
            home_team.losses += 1
            home_team.games_played += 1
            away_team.games_played += 1
            away_team.current_streak = away_team.current_streak + 1 if away_team.current_streak > 0 else 1
            home_team.current_streak = home_team.current_streak - 1 if home_team.current_streak < 0 else -1
            return away_team, home_team
        elif not must_have_winner:
            home_team.games_played += 1
            away_team.games_played += 1
            home_team.ties += 1
            away_team.ties += 1
            home_team.current_streak = 0
            away_team.current_streak = 0
            return None, None

    # If we reach max attempts and must have winner, pick winner based on team score
    home_team.games_played += 1
    away_team.games_played += 1

    if home_team.get_total_score() >= away_team.get_total_score():
        home_team.wins += 1
        away_team.losses += 1
        home_team.current_streak = home_team.current_streak + 1 if home_team.current_streak > 0 else 1
        away_team.current_streak = away_team.current_streak - 1 if away_team.current_streak < 0 else -1
        return home_team, away_team
    else:
        away_team.wins += 1
        home_team.losses += 1
        away_team.current_streak = away_team.current_streak + 1 if away_team.current_streak > 0 else 1
        home_team.current_streak = home_team.current_streak - 1 if home_team.current_streak < 0 else -1
        return away_team, home_team

def generate_highlight(winner_team, loser_team, is_championship=False, show_improvements=False):
    if not loser_team or not winner_team.players:
        return "The game ended in a tie!", None, None, None
        
    highlight_templates = [
        "{player} of the {winner_team} threw a 50-yard touchdown pass against {loser_team}!",
        "{player} of the {winner_team} rushed for 100+ yards against {loser_team}!",
        "{player} of the {winner_team} caught the ball and scored against {loser_team}!",
        "{player} of the {winner_team} made a touchdown against {loser_team}!",
        "{player} of the {winner_team} scored a field goal against {loser_team}!",
        "{player} of the {winner_team} sacked the Quarterback of {loser_team}!",
        "{player} of the {winner_team} intercepted the ball against {loser_team}!",
    ]

    chosen_template = random.choice(highlight_templates)
    chosen_player = random.choice(winner_team.players)
    
    highlight = chosen_template.format(
        player=chosen_player.player_name,
        winner_team=str(winner_team),
        loser_team=str(loser_team)
    )
    
    # Store initial state
    initial_score = chosen_player.score
    initial_traits = set(chosen_player.traits.keys())
    
    # Increase player score
    score_increase = random.randint(10, 20) if is_championship else random.randint(1, 3)
    chosen_player.score += score_increase

    # Check what traits the player already has
    has_green_trait = any(trait in GREEN_TRAITS for trait in chosen_player.traits)
    has_light_blue_trait = any(trait in LIGHT_BLUE_TRAITS for trait in chosen_player.traits)
    has_orange_trait = any(trait in ORANGE_TRAITS for trait in chosen_player.traits)
    has_red_trait = any(trait in RED_TRAITS for trait in chosen_player.traits)
    
    new_trait_added = None
    
    # Championship game special logic for Hall of Fame
    if is_championship and has_light_blue_trait and not has_orange_trait:
        chosen_player.add_trait("Hall of Fame")
        new_trait_added = "Hall of Fame"
    # First priority: Add green trait if player doesn't have one
    elif not has_green_trait:
        new_trait = random.choice(list(GREEN_TRAITS))
        chosen_player.add_trait(new_trait)
        new_trait_added = new_trait
    # Second priority: If player has green trait but no light blue trait, consider Team Captain
    elif has_green_trait and not has_light_blue_trait:
        current_captain = winner_team.get_team_captain()
        # Only assign Team Captain if no one else on team has it
        if not current_captain:
            winner_team.assign_team_captain(chosen_player)
            new_trait_added = "Team Captain"
    
    # Return highlight and improvement details
    return highlight, chosen_player, score_increase, new_trait_added

def display_player_improvements(player, score_increase, new_trait):
    """Display player improvements to the human player"""
    print(f"\n{'='*50}")
    print(f"🌟 PLAYER IMPROVEMENT 🌟")
    print(f"{'='*50}")
    print(f"Player: {player.player_name}")
    print(f"Score increased by +{score_increase} (Now: {player.score})")
    
    if new_trait:
        trait_color = TRAIT_COLORS.get(new_trait, "")
        trait_description = TRAIT_DESCRIPTIONS.get(new_trait, "No description available.")
        print(f"🎯 New Trait Gained: {trait_color}{new_trait}{reset_color()}")
        print(f"   {trait_description}")
    else:
        print("No new traits gained this time.")
    
    print(f"{'='*50}")

def simulate_round(teams, round_matchups):
    """Simulate all games in a round"""
    for team1, team2 in round_matchups:
        if team1 is None or team2 is None:
            continue
            
        # Set home/away status
        team1.home = True
        team2.home = False

        winner, loser = simulate_game(team1, team2, must_have_winner=False)
        if winner:
            highlight, player, score_increase, new_trait = generate_highlight(winner, loser, show_improvements=False)
            print(f"Highlight: {highlight}")
            
def draft_player(player, team):
    """Draft a player to NFL"""
    global drafted_players
    
    if player not in drafted_players:
        drafted_players.append(player)
    
    # Check if this player was team captain
    was_captain = "Team Captain" in player.traits
    
    nfl_teams = [
        "Patriots", "Cowboys", "Packers", "Seahawks", "49ers", "Giants",
        "Bears", "Dolphins", "Broncos", "Chiefs", "Rams", "Raiders",
        "Steelers", "Vikings", "Ravens", "Bills"
    ]
    
    drafted_team = random.choice(nfl_teams)
    player.nfl_team = drafted_team
    player.temp_retrieved = False
    print(f"{player.position} {str(player)} of the {team.name} has been drafted to the NFL team {drafted_team}!")
    
    # If the drafted player was team captain, announce vacancy
    if was_captain:
        print(f"🎖️ The Team Captain role is now vacant on {team.name}!")

def free_agent_draft(teams):
    """Handle free agent draft after first match - uses consolidated logic"""
    any_players_to_draft = False
    
    for team in teams:
        # Use same threshold as main draft system (125)
        players_to_draft = [player for player in team.players if player.score >= 115]

        if players_to_draft:
            any_players_to_draft = True

        for player in players_to_draft:
            draft_player(player, team)
            team.players.remove(player)

            # Add replacement player with consistent scoring
            replacement_position = player.position
            new_player = add_random_player_to_team(team, replacement_position)
            team.add_player(new_player)
            print(f"New player {new_player.player_name} has joined the {team} from the local beer league as a {new_player.position}!")

    if not any_players_to_draft:
        print("Skipping Free Agent Draft - no players eligible.")

def draft_players_if_applicable(teams, silent=False):
    """Handle player drafting and replacements - CONSOLIDATED VERSION"""
    global drafted_players, free_agent_pool

    human_team = teams[0]
    signings = []  # (drafted_player, new_player, team)

    for team in teams:
        players_to_draft = [player for player in team.players if player.score >= 125]

        for player in players_to_draft:
            draft_player(player, team)
            team.players.remove(player)
            replacement_position = player.position

            # Human-controlled team
            if team == human_team and not silent:
                print(f"\n🚨 EMERGENCY SIGNING: {player.player_name} was drafted to the NFL!")
                print(f"Position needing replacement: {replacement_position}")

                while True:
                    choice = input("\nSign a free agent? (y/n): ").strip().lower()
                    if choice in ("y", "n"):
                        break
                    print("Please enter 'y' or 'n'.")

                if choice == 'y':
                    before = set(p.player_name for p in team.players)
                    if sign_free_agent(team, replacement_position):
                        new_player = next((p for p in team.players if p.player_name not in before), None)
                        signings.append((player, new_player, team))
                        continue

                new_player = add_random_player_to_team(team, replacement_position)
                team.add_player(new_player)
                if not silent:
                    print(f"Auto-signed beer league player {new_player.player_name} (Score: {new_player.score})")
                signings.append((player, new_player, team))

            # AI teams (or silent mode for any team)
            else:
                new_player = add_random_player_to_team(team, replacement_position)
                team.add_player(new_player)
                if not silent:
                    print(f"New player {new_player.player_name} has joined the {team} from the local beer league as a {new_player.position}!")
                signings.append((player, new_player, team))

    return signings

def calculate_league_standings(teams):
    """Display current league standings"""
    # Sort by wins (desc), losses (asc), ties (desc) for a clear ranking
    standings = sorted(teams, key=lambda team: (-team.wins, team.losses, -team.ties))
    print("\nLeague Standings:")
    for i, team in enumerate(standings, 1):
        print(f"{i}. {team}: Wins: {team.wins}, Losses: {team.losses}, Ties: {team.ties}")

def view_team_records(teams):
    print("\nTeam Records:")
    for i, team in enumerate(teams, start=1):
        print(
            f"{i}. {team} - Wins: {team.wins}, Losses: {team.losses}, Ties: {team.ties}"
        )
    prompt = f"\nEnter the number of the team you want to see the current players of (1-{len(teams)}) or 0 to return to the menu: "
    while True:
        choice = input(prompt).strip()
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue
        num = int(choice)
        if num == 0:
            print("\nReturning to the menu...\n")
            break
        if 1 <= num <= len(teams):
            team_index = num - 1
            team = teams[team_index]
            print(f"\nCurrent players of {team.name}:")
            team.display_team()
            break
        print(f"Please enter a number between 0 and {len(teams)}.")

    input("\nPress Enter to return to the menu...")

def get_top_teams(teams, num_top_teams=8):
    """Get top teams for playoffs"""
    # Reuse the same explicit sorting used in standings
    standings = sorted(teams, key=lambda team: (-
                                                team.wins, team.losses, -team.ties))
    return standings[:num_top_teams]

def knockout_round(teams, round_name):
    """Simulate knockout round"""
    next_round_teams = []
    round_matchups = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]

    print(f"\n{'━' * 52}")
    print(f"  🏈  {round_name.upper()}")
    print(f"{'━' * 52}")
    for i, (team1, team2) in enumerate(round_matchups):
        print(f"  Match {i + 1}:  {team1}  vs  {team2}")
    input(f"\n  Press Enter to simulate {round_name}...")
    print()

    for i, (team1, team2) in enumerate(round_matchups):
        winner, loser = simulate_game(team1, team2, must_have_winner=True)
        next_round_teams.append(winner)

        if not winner:
            raise RuntimeError("Failed to determine a winner in a knockout match.")

        print(f"  Match {i + 1}:  {team1}  vs  {team2}  ➜  {winner} advances!")
        highlight, player, score_increase, new_trait = generate_highlight(winner, loser, show_improvements=False)
        print(f"  📺  {highlight}")

    print(f"\n{'━' * 52}")
    print("  Advancing:")
    for team in next_round_teams:
        print(f"    ✔  {team}")
    print(f"{'━' * 52}")
    input("\n  Press Enter to continue...")

    return next_round_teams


def championship_match(team1, team2, season_number):
    print(f"\n{'━' * 52}")
    print(f"  🏆  SEASON {season_number} CHAMPIONSHIP")
    print(f"{'━' * 52}")
    print(f"\n  {team1}  vs  {team2}")
    input("\n  Press Enter to simulate the Championship...")
    winner, loser = simulate_game(team1, team2, must_have_winner=True)
    print(f"\n  ➜  {winner} are your Season {season_number} Champions!")
    print(f"{'━' * 52}")
    trophy_name = f"Season {season_number} Trophy"
    winner.award_trophy(trophy_name)
    winner.add_first_place(season_number)
    if loser:
        loser.add_second_place(season_number)

    # Award gold medal to each player in the winning team
    for player in winner.players:
        player.gold_medals += 1

    # Award silver medal to each player in the runner-up team
    if loser:
        for player in loser.players:
            player.silver_medals += 1
            
    # Randomly choose a player to assign traits based on what they already have
    chosen_player = random.choice(winner.players)
    
    # Check what traits the player already has
    has_light_blue_trait = any(trait in LIGHT_BLUE_TRAITS for trait in chosen_player.traits)
    has_orange_trait = any(trait in ORANGE_TRAITS for trait in chosen_player.traits)
    
    # Priority order: Orange (Hall of Fame) > Light Blue > no trait assignment
    if has_light_blue_trait and not has_orange_trait:
        # Player has light blue trait but no orange - add Hall of Fame
        chosen_player.add_trait("Hall of Fame")
        print(f"🏆 {chosen_player.player_name} has been inducted into the Hall of Fame!")
    elif not has_light_blue_trait:
        # Player doesn't have light blue trait - add one
        if random.choice([True, False]):
            chosen_player.add_trait("Star Player")
        else:
            chosen_player.add_trait("Medalist")

    highlight, player, score_increase, new_trait = generate_highlight(winner, loser, is_championship=True, show_improvements=False)
    print(f"\n  📺  {highlight}")
    return winner

def reset_teams_for_new_season(teams):
    for team in teams:
        # Update historic stats
        team.historic_wins += team.wins
        team.historic_losses += team.losses
        team.historic_ties += team.ties
        team.historic_games_played += team.games_played

        # Reset current season stats
        team.wins = 0
        team.losses = 0
        team.ties = 0
        team.games_played = 0
        team.current_streak = 0
        team.playoff_bubble_shown = False
        team.playoff_secured_shown = False
        for player in team.players:
            player.started_season = True


def identify_worst_teams(teams, num_worst_teams=2):
    return sorted(teams, key=lambda team: (team.wins, team.losses, team.ties))[:num_worst_teams]

worst_teams_after_8_games = []

def improve_low_ranked_teams(teams, all_drafted_players, num_low_teams=2):
    low_ranked_teams = sorted(teams, key=lambda team: (team.wins, team.losses, team.ties))[:num_low_teams]
    for team in low_ranked_teams:
        print(f"\nImproving team: {team.name}")
        print(f"Initial team state:")
        team.display_team()
        # Cut the worst player and replace them according to the new rules
        cut_and_replace_player(team)
        # Remove temporary players at the end of the season
        remove_temporary_players([team])
        print(f"Final team state:")
        team.display_team()
        print(f"Improvement complete for team: {team.name}")
    print(f"Improved {len(low_ranked_teams)} low-ranked teams.")

def cut_and_replace_player(team):
    global cut_players, free_agent_pool
    if not team.players:
        return
    # Identify and cut the worst player
    worst_player = min(team.players, key=lambda p: (1 if p.traits else 0, p.score))
    print(f"Cutting worst player {worst_player.player_name} from {team.name}")
    team.players.remove(worst_player)
    
    worst_player.started_season = False
    if "Reformed" in worst_player.traits:
        worst_player.traits.pop("Reformed")
    if "Problematic" not in worst_player.traits:
        worst_player.add_trait("Problematic")
    
    # Add cut player to free agent pool instead of just cut_players list
    free_agent_pool.append(worst_player)
    cut_players.append((worst_player, team.name))  # Keep for tracking purposes
    
    # Find a replacement player, specifying the position of the cut player
    replacement_player, position = find_replacement_player(team, worst_player.position)
    if not replacement_player:
        # If no replacement found, add a new beer league player with the same position
        replacement_player = add_random_player_to_team(team, position=worst_player.position)
        print(f"Adding a new beer league player {replacement_player.player_name} to {team.name} as {replacement_player.position}")
    else:
        # Update replacement player to take the position of the cut player or a suitable position
        replacement_player.started_season = False
        replacement_player.update_position(position)
        print(f"Adding cut/drafted player {replacement_player.player_name} to {team.name} as {replacement_player.position}")
    team.add_player(replacement_player)

def find_replacement_player(team, desired_position=None):
    global drafted_players, free_agent_pool
    # Try to add a cut player who hasn't been on the team yet
    for player, original_team in list(cut_players):
        if team.name != original_team:
            cut_players.remove((player, original_team))
            # Remove from free agent pool if they're being signed
            if player in free_agent_pool:
                free_agent_pool.remove(player)
            return player, desired_position or player.position
    
    # Try to retrieve an NFL drafted player
    for player in list(drafted_players):
        drafted_players.remove(player)
        return player, desired_position or player.position
    
    return None, None

def human_team_improvement(team):
    print(f"\nYour team ({team.name}) can make improvements:")
    while True:
        print("\n1. Cut player")
        print("2. Sign free agent")
        print("3. View roster")
        print("4. Done improving")
        
        choice = input("Choose action: ").strip()
        if choice not in {"1", "2", "3", "4"}:
            print("Invalid choice. Enter 1-4.")
            continue

        if choice == "1":
            cut_player_interactive(team)
        elif choice == "2":
            sign_free_agent(team)
        elif choice == "3":
            team.display_team()
        elif choice == "4":
            break

def reassign_team_city(team, teams):
    old_name = team.name

    existing_team_names = set(t.name for t in teams)
    used_city_names = set(t.name.split()[0] for t in teams)
    used_mascot_names = set(t.name.split()[1] for t in teams)
    used_colors = set(t.color for t in teams)

    new_team = create_random_team(existing_team_names, used_city_names, used_mascot_names, used_colors)

    team.name = new_team.name
    team.color = new_team.color
    team.coach_name = generate_coach_name()
    team.current_streak = 0
    team.first_place_seasons = []
    team.second_place_seasons = []
    team.trophies = []

    return old_name, team

def add_player_to_position(team, player):
    possible_positions = ["QB", "RB", "WR", "DL", "Safety", "Kicker"]
    existing_positions = [p.position for p in team.players]

    # A restored player should keep the same position
    team.add_player(player)
    
def remove_temporary_players(teams):
    for team in teams:
        temp_players = [player for player in team.players if player.temp_retrieved]
        for player in temp_players:
            team.players.remove(player)
            drafted_players.append(player)  # Return player to the drafted players pool
            player.temp_retrieved = False  # Reset the temp_retrieved flag
            print(f"Removed temporary NFL player {player.player_name} from {team.name}. They return to the {player.nfl_team}.")

def management_menu(team, teams):  # Add teams parameter
    while True:
        print("\nTeam Management:")
        print("1. View free agent pool")
        print("2. Sign free agent")
        print("3. View team roster")
        print("4. View league standings")
        print("5. Return to main")
        
        choice = input("> ").strip()
        if choice not in {"1", "2", "3", "4", "5"}:
            print("Invalid choice. Enter 1-5.")
            continue

        if choice == "1":
            display_free_agents()
            input("\nPress Enter to continue...")
        elif choice == "2":
            sign_free_agent(team)
        elif choice == "3":
            team.display_team()
            input("\nPress Enter to continue...")
        elif choice == "4":
            calculate_league_standings(teams)
            input("\nPress Enter to continue...")
        elif choice == "5":
            break

NEWS_QUOTES = {
    "win_streak": [
        "We're not surprised. We've been putting in the work.",
        "The league is starting to notice us. Good.",
        "Keep your heads down and keep winning. That's all.",
        "This team has something special. I can feel it.",
        "We take it one game at a time. Always have.",
    ],
    "loss_streak": [
        "We're going to turn this around. I believe in this team.",
        "It's been tough, but nobody's quitting in that locker room.",
        "We need to look at ourselves in the mirror. Starting with me.",
        "Tough times never last. Only tough people last.",
        "This is where champions are made — in the hard moments.",
    ],
    "player_draft_watch": [
        "I'm just focused on helping this team win right now.",
        "That's not something I'm thinking about. My guys need me.",
        "I let my play do the talking.",
        "One game at a time. That's all I can control.",
        "There's still work to do here. That comes first.",
    ],
    "player_draft_imminent": [
        "I've worked my whole life for an opportunity like this.",
        "Whatever happens, I'll always love this city.",
        "It's hard not to think about it. I won't lie.",
        "This team gave me everything. I owe them a championship run first.",
        "I just want to leave it all on the field while I'm still here.",
    ],
    "hall_of_fame": [
        "Legends don't retire. They just move on.",
        "I've been around a long time. Players like this don't come around often.",
        "Buy a ticket and watch closely. You're seeing history.",
        "There are no words. Just gratitude.",
    ],
    "emergency_signing": [
        "It happened fast. But we're ready.",
        "Big shoes to fill. We're up for the challenge.",
        "We wish him well. Now we move on.",
        "The door closes, another opens. That's this league.",
        "Nobody panics in that locker room. We have a plan.",
    ],
    "rebrand": [
        "New city, new energy, same hunger.",
        "The name changes. The work ethic doesn't.",
        "This city deserves a winner. We're going to give them one.",
        "Fresh start. That's all this is.",
        "We're not running from anything. We're running toward something.",
    ],
    "playoff_push": [
        "We need every point from here on out.",
        "Every game is a playoff game now.",
        "The math is still in our favor. Barely.",
        "We didn't come this far to go home early.",
    ],
    "playoff_secured": [
        "We earned our spot. Now we go take something.",
        "Playoffs were the floor, not the ceiling.",
        "We're not done. We're just getting started.",
        "The real season starts now.",
    ],
}

def generate_news_headlines(teams, round_counter, season_number, rebrands=None, signings=None):
    priority = []
    used_teams = set()

    # 1. Rebrands — unconditional
    if rebrands:
        for old_name, team in rebrands:
            quote = random.choice(NEWS_QUOTES["rebrand"])
            priority.append((
                f"🏙️  BREAKING: The {old_name} have relocated! Welcome the {team}.",
                quote, team.coach_name, "Coach", team.name
            ))
            used_teams.add(team.name)

    standings = sorted(teams, key=lambda t: (-t.wins, t.losses, -t.ties))
    rank_map = {team: i + 1 for i, team in enumerate(standings)}

    # 2. Secured playoff spots — always shown unless emergency signings are happening
    if round_counter == 13:
        for team in teams:
            rank = rank_map[team]
            if rank <= 6 and team.playoff_bubble_shown and not team.playoff_secured_shown:
                if not signings:
                    spokesperson, title = team.get_spokesperson_info()
                    quote = random.choice(NEWS_QUOTES["playoff_secured"])
                    priority.append((
                        f"✅ {team} has secured their playoff spot!",
                        quote, spokesperson, title, team.name
                    ))
                    team.playoff_secured_shown = True
                    used_teams.add(team.name)
                # If signings exist, leave playoff_secured_shown=False so it fires next round

    # 3. Emergency signings
    if signings:
        for drafted, replacement, team in signings:
            quote = random.choice(NEWS_QUOTES["emergency_signing"])
            rep_str = f"{replacement.player_name} ({replacement.score})" if replacement else "a beer league pickup"
            priority.append((
                f"📋 {drafted.position} {str(drafted)} has been called up to the {drafted.nfl_team}! {team} signs {rep_str}.",
                quote, team.coach_name, "Coach", team.name
            ))
            used_teams.add(team.name)

    candidates = []

    # Only the single biggest win streak and loss streak earn a headline
    streak_teams = [t for t in teams if t.current_streak >= 5]
    if streak_teams:
        best = max(streak_teams, key=lambda t: t.current_streak)
        spokesperson, title = best.get_spokesperson_info()
        candidates.append((
            f"🔥 The {best} are on a {best.current_streak}-game winning streak!",
            random.choice(NEWS_QUOTES["win_streak"]), spokesperson, title, best.name
        ))
        used_teams.add(best.name)

    skid_teams = [t for t in teams if t.current_streak <= -3]
    if skid_teams:
        worst = min(skid_teams, key=lambda t: t.current_streak)
        spokesperson, title = worst.get_spokesperson_info()
        candidates.append((
            f"📉 The {worst} have dropped {abs(worst.current_streak)} straight.",
            random.choice(NEWS_QUOTES["loss_streak"]), spokesperson, title, worst.name
        ))
        used_teams.add(worst.name)

    for team in teams:
        if team.name in used_teams:
            continue
        spokesperson, title = team.get_spokesperson_info()

        for player in team.players:
            if player.score >= 120 and random.random() < 0.5:
                quote = random.choice(NEWS_QUOTES["player_draft_imminent"])
                candidates.append((
                    f"🚨 DRAFT ALERT: {player.player_name} ({player.score}) could be gone any day now.",
                    quote, player.player_name, player.position, team.name
                ))
                used_teams.add(team.name)
                break
            elif 115 <= player.score < 120 and random.random() < 0.3:
                quote = random.choice(NEWS_QUOTES["player_draft_watch"])
                candidates.append((
                    f"👀 DRAFT WATCH: {player.player_name} ({player.score}) is turning heads across the league.",
                    quote, player.player_name, player.position, team.name
                ))
                used_teams.add(team.name)
                break

        if team.name not in used_teams:
            rank = rank_map[team]
            if 7 <= rank <= 9 and not team.playoff_bubble_shown and team.wins < 10 and 8 <= round_counter <= 13:
                quote = random.choice(NEWS_QUOTES["playoff_push"])
                candidates.append((
                    f"⚔️  {team} sitting at #{rank} — right on the playoff cutoff.",
                    quote, spokesperson, title, team.name
                ))
                team.playoff_bubble_shown = True
                used_teams.add(team.name)

        if team.name not in used_teams:
            for player in team.players:
                if "Hall of Fame" in player.traits and not player.hof_news_shown:
                    quote = random.choice(NEWS_QUOTES["hall_of_fame"])
                    candidates.append((
                        f"🏛️  {player.position} {str(player)} walks among legends — inducted into the League Hall of Fame.",
                        quote, team.coach_name, "Coach", team.name
                    ))
                    player.hof_news_shown = True
                    used_teams.add(team.name)
                    break

    random.shuffle(candidates)
    remaining = max(0, 3 - len(priority))
    return priority + candidates[:remaining]

def display_news(teams, round_counter, season_number, rebrands=None, signings=None):
    headlines = generate_news_headlines(teams, round_counter, season_number, rebrands, signings)
    if not headlines:
        return
    print(f"\n{'━' * 52}")
    if len(headlines) > 3:
        print(f"  📰  EXTRA! EXTRA! — Season {season_number}, Round {round_counter + 1}")
    else:
        print(f"  📰  LEAGUE NEWS — Season {season_number}, Round {round_counter + 1}")
    print(f"{'━' * 52}")
    for headline, quote, spokesperson, title, team_name in headlines:
        print(f"\n  {headline}")
        print(f'  "{quote}"')
        attribution = f"{title} {spokesperson}" if title else spokesperson
        print(f"  — {attribution}, {team_name}")
    print(f"{'━' * 52}")

def main():
    global teams, drafted_players, free_agent_pool
    free_agent_pool = []
    season_number = 1
    teams = generate_teams()
    for team in teams:
        for player in team.players:
            player.started_season = True
    drafted_players = []
    generate_initial_free_agents()
    all_drafted_players = []
    worst_teams_previous_season = []
    while True:
        print(f"\nWelcome to Season {season_number}!")
        if season_number > 1:
            reset_teams_for_new_season(teams)  # Reset teams' stats for the new season
        my_team = teams[0]  # Assign the first team as the user's team
        schedule = generate_round_robin_schedule(list(teams))  # Create a schedule
        round_counter = 0
        all_drafted_players = []

        halfway_point = len(schedule) // 2  # Determine halfway point

        while round_counter < len(schedule):
            clear_console()
            round_matchups = schedule[round_counter]
            # Find the user's match if present
            user_matches = [(team1, team2) for team1, team2 in round_matchups if my_team in (team1, team2)]
            if user_matches:
                user_match = user_matches[0]
                user_opponent = user_match[1] if user_match[0] == my_team else user_match[0]
            else:
                # If user's team isn't scheduled this round (shouldn't happen in round-robin),
                # just simulate the round and continue to next iteration
                simulate_round(teams, round_matchups)
                round_counter += 1
                continue

            # Properly set home and away
            if random.choice([True, False]):
                home_team = my_team
                away_team = user_opponent
            else:
                home_team = user_opponent
                away_team = my_team

            home_team.home = True
            away_team.home = False

            # Ensure player's home status is updated correctly
            for player in home_team.players:
                player.home = True
            for player in away_team.players:
                player.home = False

            print(f"My Team ({my_team.name}):")
            my_team.display_team()
            my_team.display_record()

            print(f"\nOpponent Team ({user_opponent.name}):")
            user_opponent.display_team()
            user_opponent.display_record()

            my_team_is_home = (home_team == my_team)
            win_pct = calculate_win_probability(
                my_team.get_total_score(),
                user_opponent.get_total_score(),
                my_team_is_home
            )
            print(f"\nWin probability: {win_pct * 100:.1f}%")
            input("Press Enter to start the game...")

            # Simulate the user's game specifically and update the records
            winner, loser = simulate_game(home_team, away_team)

            if winner:
                print(f"Game result: {winner.name} wins!")
                highlight, improved_player, score_increase, new_trait = generate_highlight(winner, loser, show_improvements=True)
                print(f"Highlight: {highlight}")
                
                # Show player improvements if the human team won
                if winner == my_team and improved_player:
                    display_player_improvements(improved_player, score_increase, new_trait)
                    input("Press Enter to continue...")
            else:
                print("The game ended in a tie!")

            # Remove the user's match from round matchups to avoid simulating it again
            round_matchups.remove(user_match)
            simulate_round(teams, round_matchups)

            calculate_league_standings(teams)

            signings = draft_players_if_applicable(teams)

            all_drafted_players.extend(player for player in drafted_players if player not in all_drafted_players)  # Ensure no duplicates

            # Call free agent draft after the first match of the season
            if round_counter == 0:
                print("Calling free agent draft after the first match.")
                free_agent_draft(teams)

            if season_number > 1 and round_counter == 8:
                print("\nImproving low-ranked teams in the halfway mark of the season...")
                improve_low_ranked_teams(teams, all_drafted_players)
                worst_teams_after_8_games = identify_worst_teams(teams)

            rebrands = []
            if season_number > 2 and round_counter == 14:
                current_worst_teams = identify_worst_teams(teams, num_worst_teams=2)
                for team in current_worst_teams:
                    if team in worst_teams_previous_season:
                        old_name, rebranded_team = reassign_team_city(team, teams)
                        rebrands.append((old_name, rebranded_team))
                        rebranded_team.rebrand_immunity = True
                        worst_teams_previous_season.remove(team)

            display_news(teams, round_counter, season_number, rebrands, signings)

            round_counter += 1

            # Post-match menu: loop until the user chooses to play the next match or quit.
            while True:
                print("\nWhat would you like to do next?")
                print("1. Play next match")
                print("2. Team management")
                print("3. View team records")
                print("4. Quit")

                choice = input("Enter your choice (1-4): ").strip()
                # Treat empty input (pressing Enter) as 'Play next match' for fast advance
                if choice == "" or choice == "1":
                    # Proceed to the next match
                    break
                elif choice == "2":
                    management_menu(my_team, teams)
                    # After management, return to this menu
                    continue
                elif choice == "3":
                    view_team_records(teams)
                    # After viewing records, return to this menu
                    continue
                elif choice == "4":
                    print("Thanks for playing!")
                    return
                else:
                    print("Invalid choice. Please enter 1-4.")

        # Post-season code (this should be outside the round_counter loop but inside the season loop)
        remove_temporary_players(teams)

        top_teams = get_top_teams(teams)
        all_drafted_players.extend(player for player in drafted_players if player not in all_drafted_players)

        print(f"\n{'━' * 52}")
        print(f"  End of Regular Season — Playoff Bracket")
        print(f"{'━' * 52}")
        for i, team in enumerate(top_teams):
            print(f"  {i + 1}.  {team}")
        print(f"{'━' * 52}")
        input("\n  Press Enter to begin the Playoffs...")

        semifinal_teams = knockout_round(top_teams, "Quarterfinals")
        final_teams = knockout_round(semifinal_teams, "Semifinals")
        champion = championship_match(final_teams[0], final_teams[1], season_number)

        draft_players_if_applicable(teams, silent=True)

        for team in teams:
            for player in list(team.players):
                if "Problematic" in player.traits and player.started_season:
                    player.traits.pop("Problematic")
                    player.add_trait("Reformed")
                    yellow = TRAIT_COLORS["Reformed"]
                    print(f"\n  {yellow}✨ {player.player_name} has Reformed after a full season with {team}.{reset_color()}")

        eligible = [t for t in teams if not t.rebrand_immunity]
        worst_teams_previous_season = identify_worst_teams(eligible, num_worst_teams=2)
        for team in teams:
            team.rebrand_immunity = False

        input("\n  Press Enter to continue to the next season...")
        season_number += 1

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Game crashed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
