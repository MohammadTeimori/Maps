import tkinter as tk
from tkinter import ttk
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')

def get_distance_matrix(origin, destinations):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": "|".join(destinations),
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

def update_tree():
    origin = origin_entry.get()
    destinations = destinations_entry.get().split(',')
    data = get_distance_matrix(origin, destinations)
    for i in tree.get_children():
        tree.delete(i)
    for i, element in enumerate(data['rows'][0]['elements']):
        destination = data['destination_addresses'][i]
        distance = element['distance']['text']
        duration = element['duration']['text']
        tree.insert('', 'end', values=(destination, distance, duration))

root = tk.Tk()
root.title("Distance Matrix")

origin_label = tk.Label(root, text="Origin:")
origin_label.pack()

origin_entry = tk.Entry(root)
origin_entry.pack()

destinations_label = tk.Label(root, text="Destinations (comma-separated):")
destinations_label.pack()

destinations_entry = tk.Entry(root)
destinations_entry.pack()

update_button = tk.Button(root, text="Update", command=update_tree)
update_button.pack()

tree = ttk.Treeview(root, columns=('Destination', 'Distance', 'Duration'), show='headings')
tree.heading('Destination', text='Destination')
tree.heading('Distance', text='Distance')
tree.heading('Duration', text='Duration')
tree.pack()

root.mainloop()
