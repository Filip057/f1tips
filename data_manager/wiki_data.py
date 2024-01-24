import requests
from datetime import datetime
from bs4 import BeautifulSoup

from engine.models import Driver, Race



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


def get_drivers_data() -> list:
    page = requests.get(url=URL)

    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', class_="wikitable sortable",)
    
    drivers_data = []

    rows = table.find_all('tr')

    # Loop through the rows, skipping the first two as they contain headers
    for row in rows[2:-1]:
        columns = row.find_all('td')
       
        team = columns[0].text.strip()
       
        driver1_number = columns[3].find_all(string=True)[0].strip()
        driver2_number = columns[3].find_all(string=True)[1].strip()
       
        driver1_name=columns[4].find_all('a', string=True)[0].text
        driver2_name=columns[4].find_all('a', string=True)[2].text
        
        driver1 = {
            'first_name': driver1_name.split()[0],
            'last_name': driver1_name.split()[1],
            'number': driver1_number,
            'team': team,
        }
        driver2 = {
            'first_name': driver2_name.split()[0],
            'last_name': driver2_name.split()[1],
            'number': driver2_number,
            'team': team,
        }

        drivers_data.append(driver1)
        drivers_data.append(driver2)
    
    print(drivers_data)


def update_driver_model(driver_list: list):

    for driver in driver_list:
         existing_driver = Driver.objects.filter(number=driver['number'])
         if existing_driver is None:
             Driver.objects.create(
                 first_name=driver['first_name'],
                 last_name=driver['last_name'],
                 number=driver['number'],
                 team=driver['team']
             )



if __name__ == "__main__":
    # all_races = get_race_data()
    # update_race_model(races=all_races)
    driver_data= get_drivers_data()
    update_driver_model(driver_list=driver_data)