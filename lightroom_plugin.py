import sys
import locale
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QPushButton, QLabel, QComboBox, QSpinBox
)
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import cv2
from mss import mss
from matplotlib.patches import Circle

# --- ЛОКАЛИЗАЦИЯ ---
sys_lang = locale.getdefaultlocale()[0]
is_ru = bool(sys_lang and sys_lang.startswith('ru'))

LANG = {
    "plot_panel_title": "Панель графиков" if is_ru else "Plot Panel",
    "control_panel_title": "Панель управления" if is_ru else "Control Panel",
    "select_plots": "Выберите графики:" if is_ru else "Select Plots:",
    "select_monitor": "Выберите монитор:" if is_ru else "Select Monitor:",
    "arrangement": "Расположение:" if is_ru else "Arrangement:",
    "btn_refresh": "Обновить" if is_ru else "Refresh",
    "btn_screenshot": "Захват области" if is_ru else "Take Screenshot",
    "btn_cont_start": "Непрерывный режим" if is_ru else "Continuous Mode",
    "btn_cont_stop": "Остановить режим" if is_ru else "Stop Continuous Mode",
    "arr_vertical": "Вертикально" if is_ru else "Vertical",
    "arr_horizontal": "Горизонтально" if is_ru else "Horizontal",
    "arr_2x2": "Сетка 2x2" if is_ru else "2x2",
}

class PlotPanel(QMainWindow):
    def __init__(self,control_panel=None):
        super().__init__()
        self.setWindowTitle(LANG["plot_panel_title"])
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.control_panel = control_panel
        
        self.figure = Figure(facecolor='#f0f0f0') # Светло-серый фон окна для контраста
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.axes = []
        self.sct = mss()
        
        self.monitor = self.sct.monitors[1] if len(self.sct.monitors) > 1 else self.sct.monitors[0]
        self.x, self.y, self.w, self.h = 20, 20, 400, 400 

    def set_control_panel(self, control_panel):
        self.control_panel = control_panel

    def closeEvent(self, event):
        if self.control_panel:
            self.control_panel.close()
        super().closeEvent(event)

    def update_layout(self, num_axes, arrangement):
        self.figure.clear()
        self.axes = []

        # Унификация названий макетов для разных языков
        arr_map = {
            LANG["arr_horizontal"]: "horizontal",
            "horizontal": "horizontal",
            LANG["arr_vertical"]: "vertical",
            "vertical": "vertical",
            LANG["arr_2x2"]: "2x2",
            "2x2": "2x2"
        }
        arr_type = arr_map.get(arrangement, "vertical")

        if arr_type == "horizontal" and num_axes > 0:
            for i in range(num_axes):
                ax = self.figure.add_subplot(1, num_axes, i + 1)
                self.axes.append(ax)
        elif arr_type == "vertical" and num_axes > 0:
            for i in range(num_axes):
                ax = self.figure.add_subplot(num_axes, 1, i + 1)
                self.axes.append(ax)
        elif arr_type == "2x2" and num_axes > 0:
            for i in range(num_axes):
                ax = self.figure.add_subplot(2, 2, i + 1)
                self.axes.append(ax)

        self.canvas.draw()

    def plot_data(self, plot_types):
        screenshot = np.array(self.sct.grab(self.monitor))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        roi_frame = frame[self.y:self.y + self.h, self.x:self.x + self.w]
        
        for ax, plot_type in zip(self.axes, plot_types):
            ax.clear()
            if plot_type == "Vectorscope YUV" or plot_type == "Vectorscope Color":
                self.plot_vectorscope(ax, roi_frame, plot_type)
            elif plot_type == "Waveform Luma" or plot_type == "RGB Parade" or plot_type == "Waveform RGB":
                self.plot_waveform(ax, roi_frame, plot_type)
        self.canvas.draw()

    def take_screenshot(self):
        self.sct = mss()
        self.monitor = self.sct.monitors[self.control_panel.activeScreen]

        screenshot = np.array(self.sct.grab(self.monitor))      
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        roi = cv2.selectROI(LANG["btn_screenshot"], frame, False, False)
        cv2.destroyWindow(LANG["btn_screenshot"])
        
        if roi[2] > 0 and roi[3] > 0:
            self.x, self.y, self.w, self.h = map(int, roi)
            
        if self.control_panel:
            self.control_panel.refresh_plot()
        
    def calculate_luminance_waveform(self,frame):
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, width = gray_image.shape
        waveform = np.zeros((255, width), dtype=np.uint8)
        for x in range(width):
            column = gray_image[:, x]
            hist, _ = np.histogram(column, bins=255, range=(0,256))
            normalized_hist = (hist / hist.max() * 255).astype(np.uint8) if hist.max() > 0 else hist
            for y, value in enumerate(normalized_hist):
                     waveform[254-y, x] = value
        return waveform

    def calculate_rgb_waveform(self, frame, type):
        _, width,_ = frame.shape
        frame = frame[:, :, [2, 1, 0]]
        if type == "RGB Parade":
            waveform = np.zeros((255, width * 3, 3), dtype=np.uint8)
            for x in range(width):
                for channel in range(3):
                    column = frame[:, x, channel]
                    hist, _ = np.histogram(column, bins=255, range=(0, 256))
                    normalized_hist = (hist / hist.max() * 255).astype(np.uint8) if hist.max() > 0 else hist
                    for y, value in enumerate(normalized_hist):
                        waveform[254 - y, x + channel * width, channel] = value
        elif type == "Waveform RGB":
            waveform = np.zeros((255, width, 3), dtype=np.uint8)
            for x in range(width):
                for channel in range(3):
                    column = frame[:, x, channel]
                    hist, _ = np.histogram(column, bins=255, range=(0, 256))
                    normalized_hist = (hist / hist.max() * 255).astype(np.uint8) if hist.max() > 0 else hist
                    for y, value in enumerate(normalized_hist):
                        waveform[254 - y, x, channel] = value
        return waveform

    def calculate_YUV_values(self,frame):
        yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        U = yuv[:, :, 1].flatten() / 255.0 * 2 - 1
        V = yuv[:, :, 2].flatten() / 255.0 * 2 - 1
        rgb = frame[:, :, ::-1].reshape(-1, 3) / 255.0
        return U,V, rgb

    def plot_vectorscope(self, ax, frame, type):
        U, V, rgb = self.calculate_YUV_values(frame)
        
        # Настройка профессионального вида (темные оси, цветные маркеры)
        color_points = {
            "B":  ((0.87, -0.19), '#0000FF'), # Blue
            "Mg": ((0.56, 1),     '#CC00CC'), # Magenta (чуть темнее для читаемости)
            "R":  ((-0.28, 1),    '#FF0000'), # Red
            "Yl": ((-0.87, 0.19), '#DDAA00'), # Yellow (затемненный желтый для читаемости на белом фоне)
            "G":  ((-0.56, -1),   '#00AA00'), # Green (затемненный зеленый)
            "Cy": ((0.28, -1),    '#00CCCC')  # Cyan (затемненный)
        }
        
        flesh_angle = 123
        flesh_rad = np.radians(flesh_angle)
        x_flesh, y_flesh = np.cos(flesh_rad), np.sin(flesh_rad)

        # Рисуем круги и перекрестие
        for radius in [0.5, 0.75, 1.0]:
            circle = Circle((0, 0), radius, color='#bbbbbb', fill=False, linestyle='--', linewidth=0.8)
            ax.add_artist(circle)
        ax.axhline(0, color='#bbbbbb', linestyle='-', linewidth=0.8)
        ax.axvline(0, color='#bbbbbb', linestyle='-', linewidth=0.8)

        # Рисуем линию скинтона (Оранжевую, профессиональную)
        ax.plot([0, x_flesh], [0, y_flesh], color='#FF8C00', linestyle='-', linewidth=2.0, alpha=0.9)
        ax.text(x_flesh * 0.75, y_flesh * 0.75, " Skin", fontsize=9, color='#FF8C00', fontweight='bold')

        # Расставляем цветные маркеры
        for text_label, ((u, v), hex_color) in color_points.items():
            ax.plot(u, v, 'o', color=hex_color, markersize=7)
            # Сдвигаем текст чуть дальше от центра
            ax.text(u * 1.15, v * 1.15, text_label, fontsize=11, color=hex_color, fontweight='bold', ha='center', va='center')
        
        if type == "Vectorscope YUV":
            ax.scatter(U,V, alpha=0.3, color="#555555", s=0.2) # Более плотный серый
        elif type == "Vectorscope Color":
            ax.scatter(U,V, alpha=0.5, color=rgb, s=0.3)

        ax.set_ylim((-1.1, 1.1))
        ax.set_xlim((-1.1, 1.1))
        ax.set_aspect('equal')
        ax.set_title(type, fontweight='bold')
        ax.set_facecolor('white') # Явный белый фон графика
        
    def plot_waveform(self, ax, frame, type):
        _, width, _= frame.shape
        if type == "RGB Parade":
          wave = self.calculate_rgb_waveform(frame,type)
          ax.imshow(wave, aspect='auto', extent=[0, width*3, 0, 255])
        elif type == "Waveform Luma":
          wave = self.calculate_luminance_waveform(frame)
          ax.imshow(wave, aspect='auto', extent=[0, width, 0, 255],cmap= 'gray')   
        elif type == "Waveform RGB":
          wave = self.calculate_rgb_waveform(frame, type)
          ax.imshow(wave, aspect='auto', extent=[0, width, 0, 255]) 

class ControlPanel(QMainWindow):
    def __init__(self, plot_panel):
        super().__init__()
        self.plot_panel = plot_panel
        self.plot_panel.control_panel = self

        self.setWindowTitle(LANG["control_panel_title"])
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.checkboxes = []
        self.plot_types = ["Vectorscope YUV", "Vectorscope Color", "Waveform Luma", "Waveform RGB", "RGB Parade"]
        self.checkbox_label = QLabel(LANG["select_plots"])
        self.layout.addWidget(self.checkbox_label)
        
        for plot_type in self.plot_types:
            checkbox = QCheckBox(plot_type)
            checkbox.stateChanged.connect(self.refresh_plot)
            self.checkboxes.append(checkbox)
            self.layout.addWidget(checkbox)
            
        self.monitor_label = QLabel(LANG["select_monitor"])
        self.monitor_spinner = QSpinBox()
        self.monitor_spinner.setMinimum(1)
        self.monitor_spinner.setMaximum(len(mss().monitors) - 1)
        self.monitor_spinner.setValue(1)
        self.monitor_spinner.valueChanged.connect(self.update_active_monitor)
        self.activeScreen = 1
        
        monitor_layout = QHBoxLayout()
        monitor_layout.addWidget(self.monitor_label)
        monitor_layout.addWidget(self.monitor_spinner)
        self.layout.addLayout(monitor_layout)
        
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton(LANG["btn_refresh"])
        self.continuous_mode_button = QPushButton(LANG["btn_cont_start"])
        self.screenshot_button = QPushButton(LANG["btn_screenshot"])
        button_layout.addWidget(self.screenshot_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.continuous_mode_button)      
        self.layout.addLayout(button_layout)

        self.arrangement_label = QLabel(LANG["arrangement"])
        self.arrangement_dropdown = QComboBox()
        self.arrangement_dropdown.addItems([LANG["arr_vertical"], LANG["arr_horizontal"], LANG["arr_2x2"]])
        
        arrangement_layout = QHBoxLayout()
        arrangement_layout.addWidget(self.arrangement_label)
        arrangement_layout.addWidget(self.arrangement_dropdown)
        self.layout.addLayout(arrangement_layout)

        self.refresh_button.clicked.connect(self.refresh_plot)
        self.screenshot_button.clicked.connect(self.plot_panel.take_screenshot)
        self.arrangement_dropdown.currentTextChanged.connect(self.change_arrangement)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_plot)
        self.continuous_mode_button.clicked.connect(self.toggle_continuous_mode)
        
    def closeEvent(self, event):
        if self.plot_panel:
            self.plot_panel.close()
        super().closeEvent(event)
        
    def refresh_plot(self):
        selected_plots = self.get_selected_plots()
        num_axes = len(selected_plots)
        if num_axes > 0:
            self.plot_panel.update_layout(num_axes, self.arrangement_dropdown.currentText())
            self.plot_panel.plot_data(selected_plots)

    def change_arrangement(self):
        self.refresh_plot()

    def toggle_continuous_mode(self):
        if self.timer.isActive():
            self.timer.stop()
            self.continuous_mode_button.setText(LANG["btn_cont_start"])
            self.enable_vectorscope_color_checkbox(True)
            self.refresh_button.setEnabled(True)
        else:
            self.enable_vectorscope_color_checkbox(False)
            self.refresh_button.setEnabled(False)
            self.timer.start(2000)
            self.continuous_mode_button.setText(LANG["btn_cont_stop"])

    def get_selected_plots(self):
        return [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

    def enable_vectorscope_color_checkbox(self, enable):
        for checkbox in self.checkboxes:
            if checkbox.text() == "Vectorscope Color":
                if not enable:
                    checkbox.setChecked(False)
                checkbox.setEnabled(enable)
                break

    def update_active_monitor(self, value):
        self.activeScreen = value

def main():
    app = QApplication(sys.argv)

    plot_panel = PlotPanel()
    control_panel = ControlPanel(plot_panel)
    plot_panel.set_control_panel(control_panel)
    
    screen_geometry = app.desktop().screenGeometry()
    plot_panel.setGeometry(0, 0, screen_geometry.width() // 3, screen_geometry.height())
    plot_panel.show()
    control_panel.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()