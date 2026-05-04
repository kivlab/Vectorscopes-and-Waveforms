# Vectorscopes and Waveforms 

If you are looking for a quick solution to plot various vector scopes and waveforms, feel free to download this repository. I have created an easy-to-use and very basic user interface to display additional information about your image. If you are used to working with vectorscopes (for example, from Premiere Pro) and you are missing them in Lightroom Desktop or Capture One, this may be a great workaround for you. 

Simply select a region of your screen, and you can see the respective scopes (YUV, YUV with RGB color) or waveforms (Luminance, RGB, RGB Parade). You can either manually refresh after you make changes or work in continuous mode where everything updates automatically in real-time. 

**Disclaimer:**
At this stage, this has only been a "weekend project" for me, and it basically fulfills all my needs. I may add new features sometime, but for now, I just want to use it as is. Feel free to contribute and improve the project. It should be available for the photography community and everybody who finds these features useful in their editing workflow.

---

## Download / Executable (Windows)
You can find a pre-compiled Windows executable (`.exe`) in the **[Releases](../../releases)** section of this repository. This is the easiest way to use the tool and is recommended for everyone who does not want to install Python, edit the files, or build from source.

---

## Features

### GUI Components & Enhancements
- **Multi-Monitor Support**: Seamlessly define your Region of Interest (ROI) across any connected monitor.
- **ROI Overlay Frame**: Displays a transparent, click-through border over your selected area, so you always know exactly what part of the screen is being analyzed.
- **Always on Top**: Pin the control panel above your editing software (Lightroom, Photoshop, etc.) for uninterrupted monitoring.
- **Control Panel**: Allows users to select plot types, choose the arrangement of plots (e.g., vertical, horizontal, or 2x2), and toggle live updates.

### Plot Types
- **Vectorscope YUV**: Displays YUV color data in a standard vectorscope format.
- **Vectorscope Color**: Visualizes data in YUV space but pixels are displayed in their actual RGB colors. *(Note: Takes longer to generate and is therefore disabled in continuous mode).*
- **Waveform Luma**: Displays the luminance waveform.
- **Waveform RGB**: Shows the waveform of RGB channels.
- **RGB Parade**: Visualizes the RGB channels side-by-side.

### Continuous Mode
- Automatically refreshes plots at a fixed interval for real-time live updates.

---

## Installation (For Developers)

To run the Python script from source, you need Python 3.8+ installed on your system. 

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip` and the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## Building the Executable (`.exe`)

If you want to modify the code and compile your own standalone Windows executable, you can easily do so using `PyInstaller`.

1. Ensure all project dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
3. Build the executable (the `--noconsole` flag hides the background command prompt, and `--onefile` bundles everything into a single `.exe`):
   ```bash
   pyinstaller --noconsole --onefile lightroom_gui.py
   ```
4. Once the build is complete, you will find your compiled executable inside the newly generated `dist` folder.

---

## Usage Instructions

1. **Screenshot & ROI**:
   - Click **Take Screenshot**.
   - Define the Region of Interest (ROI) by clicking and dragging over the desired area on any monitor. A red overlay frame will appear to highlight your selection.
2. **Choose Arrangement**: Select the layout (Vertical, Horizontal, 2x2) from the dropdown.
3. **Select Plots**: Check the boxes in the Control Panel to choose which plots to display.
4. **Always on Top**: Toggle the checkbox to keep the scopes floating above your editor.
5. **Continuous Mode**: Toggle continuous mode for real-time live updates.
6. **Refresh Plots**: Click **Refresh** to manually update the plots if continuous mode is off.

---

## File Structure

- **`lightroom_gui.py`**: The main application file containing the GUI and plotting logic.
- **`requirements.txt`**: List of all Python dependencies required to run or build the app.

---

## Contributing

Feel free to fork the repository and submit pull requests with enhancements or bug fixes. Please ensure the code is properly documented and tested.

---

### Acknowledgments & Recent Enhancements

This project is a modified fork of the original [Vectorscopes and Waveforms](https://github.com/JulianOstertag/Vectorscopes-and-Waveforms) repository created by **Julian Ostertag**. The following modifications and stability improvements were introduced to this version by **Nikolay Ivanov**:

- **Refined Vectorscope Design:** The visual appearance and layout of the vectorscope plots have been updated for better clarity and readability.
- **Russian Localization:** Implemented full Russian language support for the user interface.
- **Stability Fixes:** Resolved a critical application crash that previously occurred if a user interacted with the plot selection checkboxes prior to defining a Region of Interest (ROI) via the "Take Screenshot" button.