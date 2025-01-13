# Vectorscopes
If you are looking for quick solution to plot various vector scopes and waveforms feel free to download this repository. I have created a easy to use and very basic user interface to display additional information about your image. If you are used to working with vectorscopes for example from Premiere Pro and you are missing them in Lightroom for example, this may be a "good enough" workaround for you. Simply screenshot the image and you can see the respective scopes (YUV, YUV but with RGB color) or waveforms (Luminance, RGB, RGB Parade). You can either manually refresh after you made some changes or work in teh continous mode where everything refreshes automatically. At this stage this has only been a "weekend project" for me and it basically fullfills all my needs. 

I may add new features sometime, but for now I just want to use it as is. Feel free to contribute and improve the project. It should be available for the photography community and everybody who finds these features useful in their editing workflow. 
If it has been helpful for you and you think it may be worth a dollor or more, I am happy to accept donations. 

---

## Features

### Plot Types
- **Vectorscope YUV**: Displays YUV color data in a vectorscope format.
- **Vectorscope Color**: Visualizes color data in YUV space with the actual RGB values.
- **Waveform Luma**: Displays the luminance waveform.
- **Waveform RGB**: Shows the waveform of RGB channels.
- **RGB Parade**: Visualizes the RGB channels side-by-side.

### GUI Components
- **Plot Panel**: Displays the plots dynamically based on user selection.
- **Control Panel**: Allows users to:
  - Select plot types.
  - Choose the arrangement of plots (e.g., vertical, horizontal, or 2x2).
  - Toggle continuous mode for live updates.
  - Take screenshots and define Regions of Interest (ROI).
  - Select the active monitor for data visualization.

### Continuous Mode
- Automatically refreshes plots at a fixed interval for real-time updates.

---

## Requirements

- Python 3.8+
- PyQt5
- matplotlib
- numpy
- OpenCV
- mss

Install dependencies using pip:

```bash
pip install PyQt5 matplotlib numpy opencv-python mss
```

```bash
pip install -r requirements.txt
```
---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Use the **Control Panel** to configure the plots and the **Plot Panel** to view the results.

---

## Usage Instructions
1. **Screenshot & ROI**:
   - Click **Take Screenshot**.
   - Define the Region of Interest (ROI) by selecting an area on the screen.
2. **Choose Arrangement**: Select the layout (Vertical, Horizontal, 2x2) from the dropdown.
3. **Monitor Selection**: Use the spinner to select the active monitor.
4. **Select Plots**: Check the boxes in the Control Panel to choose which plots to display.
5. **Continuous Mode**: Toggle continuous mode for live updates.
6. **Refresh Plots**: Click **Refresh** to manually update the plots.

---

## File Structure

- **lightroom_guin.py**: The main application file containing the GUI logic.

---

## Contributing

Feel free to fork the repository and submit pull requests with enhancements or bug fixes. Please ensure the code is properly documented and tested.

---

## Contact

For questions or support, please reach out to:

- Name: Julian Ostertag
- Email: julianostertag@aol.de

---
