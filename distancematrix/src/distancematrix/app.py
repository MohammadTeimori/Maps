import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Define the main app class
class DistanceMatrixApp(toga.App):

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        # Set up main content box
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Origin input
        self.origin_input = toga.TextInput(placeholder='Enter origin address')
        main_box.add(toga.Box(children=[toga.Label('Origin:'), self.origin_input], style=Pack(direction=ROW, padding=5)))

        # Destinations input
        self.destinations_input = toga.TextInput(placeholder='Enter destinations, separated by commas')
        main_box.add(toga.Box(children=[toga.Label('Destinations:'), self.destinations_input], style=Pack(direction=ROW, padding=5)))

        # Submit button
        submit_button = toga.Button('Update', on_press=self.get_distances, style=Pack(padding=5))
        main_box.add(submit_button)

        # Results area
        self.results_area = toga.MultilineTextInput(readonly=True)
        main_box.add(self.results_area)

        # Add the content box to the main window
        self.main_window.content = main_box
        self.main_window.show()

    def get_distances(self, widget):
        # Get API key
        api_key = os.getenv('API_KEY')

        # Prepare API request
        origin = self.origin_input.value
        destinations = self.destinations_input.value.split(',')
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": "|".join(destinations),
            "key": api_key
        }

        # Make the request and process the response
        response = requests.get(url, params=params)
        data = response.json()

        # Display results
        results = ""
        for row in data.get('rows', []):
            for element in row.get('elements', []):
                distance = element.get('distance', {}).get('text', 'N/A')
                duration = element.get('duration', {}).get('text', 'N/A')
                results += f"Distance: {distance}; Duration: {duration}\n"
        self.results_area.value = results

# Run the app
def main():
    return DistanceMatrixApp('Distance Matrix', 'org.example.distance_matrix')

if __name__ == '__main__':
    main().main_loop()
