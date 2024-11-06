import tkinter as tk
from tkinter import messagebox
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
import os

# API Key for OpenCage Geocoding
key = "93238961916b43289773c2d3d793ce26"

def get_location():
    number = entry.get()
    try:
        check_number = phonenumbers.parse(number)
        number_location = geocoder.description_for_number(check_number, "en")
        service_provider = carrier.name_for_number(check_number, "en")

        if number_location:
            lbl_location.config(text=f"Location: {number_location}")
            lbl_carrier.config(text=f"Carrier: {service_provider}")
            get_coordinates(number_location)
        else:
            messagebox.showerror("Error", "Could not find location for this number.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_coordinates(location):
    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(location)

    if results:
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        create_map(lat, lng, location)
    else:
        messagebox.showerror("Error", "Could not find coordinates for this location.")

def create_map(lat, lng, location):
    map_location = folium.Map(location=[lat, lng], zoom_start=9)
    folium.Marker([lat, lng], popup=location).add_to(map_location)
    map_location.save("mylocation.html")
    messagebox.showinfo("Success", "Map has been created! Open 'mylocation.html' to view.")

# GUI Setup
root = tk.Tk()
root.title("Phone Number Locator")
root.geometry("400x300")

# Input Field
tk.Label(root, text="Enter Phone Number:").pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Buttons
btn_get_location = tk.Button(root, text="Get Location", command=get_location)
btn_get_location.pack(pady=10)

# Labels for output
lbl_location = tk.Label(root, text="Location: ")
lbl_location.pack(pady=5)

lbl_carrier = tk.Label(root, text="Carrier: ")
lbl_carrier.pack(pady=5)

# Start the GUI
root.mainloop()