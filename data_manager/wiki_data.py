import requests
from datetime import datetime
from bs4 import BeautifulSoup



URL = "https://en.wikipedia.org/wiki/2024_Formula_One_World_Championship"


def get_race_data():
    page = requests.get(url=URL)

    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', class_="wikitable", width="650px")

    race_data = []

    # Iterate through rows and print Grand Prix name and circuit
    for row in table.find_all('tr')[1:]:  # Skip the header row
        
        columns = row.find_all(['th', 'td'])
        if len(columns) >= 4:
            round_number = columns[0].text.strip()
            grand_prix = columns[1].text.strip()
            circuit = columns[2].text.strip()
            race_date = columns[3].text.strip()

            race_data.append({
                'round_number': round_number,
                'grand_prix': grand_prix,
                'circuit': circuit,
                'race_date': datetime.strptime(race_date, "%d %B")
            })
   
    return race_data

def update_race_model(races):
    
    for race in races:
        existing_race = Race.objects.filter(grand_prix=race['grand_prix'])
        if existing_race is None:
            Race.objects.create(
                round_number=race['round_number'],
                grand_prix=race['grand_prix'],
                 circuit=race['circuit'],
                race_date=['race_date'],
            )
        else:
            # If a record exists, update its fields
            existing_race.round_number = race['round_number']
            existing_race.circuit = race['circuit']
            existing_race.race_date = race['race_date']
            existing_race.save()


def get_drivers_data():
    page = requests.get(url=URL)

    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', class_="wikitable sortable",)
    

    drivers_data = []

    rows = table.find_all('tr')

    # Loop through the rows, skipping the first two as they contain headers
    for row in rows[1:]:
        columns = row.find_all(['th', 'td'])
        
        # Handle the case where there are two names and two numbers separated by <br>
        if len(columns) == 2:
            names = columns[0].find_all('a')
            numbers = columns[1].find_all('br')
            
            # Extracting first name, last name, number, and team
            for name, number in zip(names, numbers):
                first_name, last_name = name.text.strip().split(maxsplit=1)
                number = number.next_sibling.strip()
                
                # You can extract the team information based on the specific structure of your HTML
                team = "Your code to extract team here"
                
                drivers_data.append({
                    'first_name': first_name,
                    'last_name': last_name,
                    'number': number,
                    'team': team
                })

    
    print(drivers_data)

if __name__ == "__main__":
    # all_races = get_race_data()
    # update_race_model(races=all_races)
    get_drivers_data()