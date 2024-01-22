import requests
from datetime import datetime
from bs4 import BeautifulSoup

from engine.models import Race

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

if __name__ == "__main__":
    all_races = get_race_data()
    update_race_model(races=all_races)