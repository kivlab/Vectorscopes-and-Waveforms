Vectorscopes

This project is a PyQt-based GUI application that provides a user-friendly interface for visualizing various plots, including vectorscopes and waveforms, using screenshots as input data. The application is designed with modularity in mind, featuring a main plot panel and a control panel for configuring the visualizations.

Features

Plot Types

Vectorscope YUV: Displays YUV color data in a vectorscope format.

Vectorscope Color: Visualizes color data in YUV space with the actual RGB values.

Waveform Luma: Displays the luminance waveform.

Waveform RGB: Shows the waveform of RGB channels.

RGB Parade: Visualizes the RGB channels side-by-side.

GUI Components

Plot Panel: Displays the plots dynamically based on user selection.

Control Panel: Allows users to:

Select plot types.

Choose the arrangement of plots (e.g., vertical, horizontal, or 2x2).

Toggle continuous mode for live updates.

Take screenshots and define Regions of Interest (ROI).

Select the active monitor for data visualization.

Continuous Mode

Automatically refreshes plots at a fixed interval for real-time updates.

Requirements

Python 3.8+

PyQt5

matplotlib

numpy

OpenCV

mss

Install dependencies using pip:

pip install PyQt5 matplotlib numpy opencv-python mss

How to Run

Clone the repository:

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

Run the application:

python main.py

Use the Control Panel to configure the plots and the Plot Panel to view the results.

Usage Instructions

Select Plots: Check the boxes in the Control Panel to choose which plots to display.

Choose Arrangement: Select the layout (Vertical, Horizontal, 2x2) from the dropdown.

Monitor Selection: Use the spinner to select the active monitor.

Screenshot & ROI:

Click Take Screenshot.

Define the Region of Interest (ROI) by selecting an area on the screen.

Continuous Mode: Toggle continuous mode for live updates.

Refresh Plots: Click Refresh to manually update the plots.

File Structure

main.py: The main application file containing the GUI logic.

Screenshots

Control Panel



Plot Panel



Contributing

Feel free to fork the repository and submit pull requests with enhancements or bug fixes. Please ensure the code is properly documented and tested.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Contact

For questions or support, please reach out to:

Name: Your Name

Email: your.email@example.com

GitHub: Your GitHub Profile

Enjoy visualizing data with the PyQt Plot Panel Application!

