import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from ipconfig import ip


class HistoricalDataAnalysis:
    def __init__(self, user_id):
        self.user_id = user_id
        self.image_index = 0

    def retrieve_stress_level_data(self):
        # Define the URL of the PHP backend API
        url = "http://"+ip+"/fsia/retrieve_stress_level.php"

        # Prepare the request data (user_id)
        data = {"user_id": self.user_id}

        try:
            # Send a POST request to the backend API
            response = requests.post(url, data=data)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                stress_data = response.json()

                # Convert data to pandas DataFrame
                dates = pd.to_datetime(stress_data['dates'])
                stress_levels = pd.to_numeric(stress_data['stress_levels'])  # Convert to numeric format
                emotions = stress_data['emotions']
                image_data = stress_data['image_data']

                return dates, stress_levels, emotions, image_data
            else:
                print("Failed to retrieve stress level data from the backend.")
                return None, None, None, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None, None, None

    def plot_stress_level_chart(self):
        # Retrieve stress level data
        dates, stress_levels, emotions, image_data = self.retrieve_stress_level_data()

        if dates is not None and stress_levels is not None:
            # Create a new Tkinter window
            chart_window = tk.Tk()
            chart_window.title("Stress Level Chart")

            # Create a Figure and a Canvas
            fig, ax = plt.subplots(figsize=(10, 7))
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()

            # Plot the stress level chart
            ax.plot(dates, stress_levels, marker='', linestyle='-', label='Stress Level')

            # Assign colors to different emotions
            emotion_colors = {
                'Happy': 'green',
                'Neutral': 'green',
                'Surprise': 'orange',
                'Sad': 'orange',
                'Disgust': 'orange',
                'Angry': 'red',
                'Fear': 'red'
            }

            # Keep track of which emotions have been added to the legend
            legend_entries = set()

            # Plot emotions as scatter points with different marker styles, colors, and sizes
            for i, (date, emotion) in enumerate(zip(dates, emotions)):
                if emotion not in legend_entries:
                    # Add emotion to the legend only if it hasn't been added before
                    ax.scatter([], [], color=emotion_colors[emotion], label=emotion)
                    legend_entries.add(emotion)

                marker = 'o' if emotion in ['Happy', 'Neutral'] else 'o'
                color = emotion_colors.get(emotion, 'purple')
                size = 50

                ax.scatter(date, stress_levels[i], color=color, marker=marker, s=size)

                # Add emotion labels above each plot point
                ax.text(date, stress_levels[i] + 0.05, emotion, ha='center', va='bottom', color=color)
                # Add stress level values above each plot point
                ax.text(date, stress_levels[i] - 0.05, f'{stress_levels[i]:.4f}', ha='center', va='top')

            ax.set_title('User Stress Level Change Over 30 Days')
            ax.set_xlabel('Date')
            ax.set_ylabel('Stress Level')
            ax.set_xticks(dates)
            ax.xaxis.set_tick_params(rotation=45)
            ax.set_ylim(min(stress_levels) - 0.1, max(stress_levels) + 0.1)  # Dynamic y-axis limits
            ax.grid(True)
            ax.legend()

            # Add a button to select date and view image
            select_button = tk.Button(chart_window, text="Select Date", command=lambda: self.select_date(dates, image_data))
            select_button.pack(side=tk.BOTTOM)

            # Pack the canvas into the window
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Show the window
            chart_window.mainloop()
        else:
            messagebox.showinfo("No Data", "No data available to plot the chart.")

    def select_date(self, dates, image_data):
        # Create a new window for image selection
        select_window = tk.Toplevel()
        select_window.title("Select Date")

        # Create a listbox to display dates
        date_listbox = tk.Listbox(select_window)
        date_listbox.pack()

        # Add dates to the listbox
        for date in dates:
            date_listbox.insert(tk.END, date.strftime('%Y-%m-%d'))

        # Add a button to view selected image
        view_button = tk.Button(select_window, text="View Image", command=lambda: self.view_image(date_listbox.get(tk.ACTIVE), dates, image_data))
        view_button.pack()

    def view_image(self, selected_date, dates, image_data):
        # Find the index of the selected date
        index = [i for i, date in enumerate(dates) if date.strftime('%Y-%m-%d') == selected_date]

        if index:
            # Create a new window for image display
            image_window = tk.Toplevel()
            image_window.title("Selected Image")

            # Load the selected image
            image_path = image_data[index[0]]  # Assuming image_data is a list of image paths
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)

            # Display the image
            label = tk.Label(image_window, image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
            label.pack()
        else:
            messagebox.showinfo("No Image", "No image available for the selected date.")


if __name__ == "__main__":
    import sys

    # Retrieve user ID from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python historical_data_analysis.py <user_id>")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print("Error: User ID must be an integer.")
        sys.exit(1)

    # Create an instance of HistoricalDataAnalysis with the provided user ID and plot the stress level chart
    analyzer = HistoricalDataAnalysis(user_id)
    analyzer.plot_stress_level_chart()
