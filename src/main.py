# Import necessary modules
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# Import utility functions and optimization algorithms
from utils import parse_file, randomize_deliveries, swap_pizza_between_teams_random, evaluation_function, remove_team, new_pizzas
from hillclimbing import hill_climbing
from simulatedAnnealing import simulated_annealing
from tabusearch import tabu_search
from genetic import genetic_algorithm
from guidedlocalsearch import guided_local_search
import utils
import time

# Define the main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Even More Pizza")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet('background: #f8f7ef;')

        # Add title labels
        self.title_label = QLabel("Even", self)
        self.title_label.setStyleSheet("color: #000000; font-size: 45px; font-weight: bold; font-family: Times New Roman;")
        self.title_label.move(10, 50)
        self.title_label.setFixedWidth(300)  

        self.title_label = QLabel("More Pizza", self)
        self.title_label.setStyleSheet("color: #2e4f2c; font-size: 45px; font-weight: bold; font-family: Times New Roman;")
        self.title_label.move(10, 90)
        self.title_label.setFixedWidth(300)  

        # Add file selection widgets
        self.label_file = QLabel("Select a file:", self)
        self.label_file.setStyleSheet("color: #000000; font-size: 15px;  font-family: Times New Roman;")
        self.label_file.move(10, 150)
        self.file_combo = QComboBox(self)
        self.file_combo.addItem("Browse for a file...")
        self.file_combo.setStyleSheet("font-family: Times New Roman;")
        folder_path = "data"  
        files = os.listdir(folder_path)
        for file_name in files:
            if file_name.endswith(''):
                self.file_combo.addItem(file_name)
        self.file_combo.move(200, 145)
        self.file_combo.resize(200, 40)
        self.file_path = self.file_combo.currentIndexChanged.connect(self.select_file)

        # Add algorithm selection widgets
        self.label_file = QLabel("Select an algorithm:", self)
        self.label_file.setStyleSheet("color: #000000; font-size: 15px;  font-family: Times New Roman;")
        self.label_file.move(10, 200)
        self.label_file.resize(150, 40)
        self.algorithm_combo = QComboBox(self)
        self.algorithm_combo.addItem("")
        self.algorithm_combo.addItem("Hill Climbing")
        self.algorithm_combo.addItem("Simulated Annealing")
        self.algorithm_combo.addItem("Tabu search")
        self.algorithm_combo.addItem("Genetic algorithm")
        self.algorithm_combo.addItem("Guided Local Search")
        self.algorithm_combo.move(200, 200)
        self.algorithm_combo.resize(150, 40)
        self.algorithm_combo.currentIndexChanged.connect(self.update_algorithm_ui)        

        # Add widgets for algorithm-specific parameters
        # (Iterations, cooling option, tabu tenure, genetic population, parent selection)
        self.selection_iterations_label = QLabel("Select iterations method:", self)
        self.selection_iterations_label.move(200, 250)
        self.selection_iterations_label.resize(500, 50)
        self.selection_iterations = QComboBox(self)
        self.selection_iterations.addItem("Total of iterations")
        self.selection_iterations.addItem("Iterations without improving")
        self.selection_iterations.move(400, 260)
        self.selection_iterations_label.hide()
        self.selection_iterations.hide()
        
        self.selection_cooling_label = QLabel("Select cooling option:", self)
        self.selection_cooling_label.move(200, 250)
        self.selection_cooling_label.resize(500, 50)
        self.cooling_option = QLineEdit(self)
        self.cooling_option.setText("1") 
        self.cooling_option.move(400, 260)
        self.selection_cooling_label.hide()
        self.cooling_option.hide()

        self.tabu_tenure_label = QLabel("Select tabu tenure:", self)
        self.tabu_tenure_label.move(200, 250)
        self.tabu_tenure_label.resize(500, 50)
        self.tabu_tenure = QLineEdit(self)
        self.tabu_tenure.setText("10") 
        self.tabu_tenure.move(400, 260)
        self.tabu_tenure_label.hide()
        self.tabu_tenure.hide()
        
        self.genetic_selection_label = QLabel("Select genetic population and type of parent selection:", self)
        self.genetic_selection_label.move(200, 250)
        self.genetic_selection_label.resize(500, 50)
        self.genetic_population = QLineEdit(self)
        self.genetic_population.setText("60") 
        self.genetic_population.move(520, 260)
        self.genetic_type = QComboBox(self)
        self.genetic_type.addItem("Tournament")
        self.genetic_type.addItem("Roulette")
        self.genetic_type.move(520, 300)
        self.genetic_selection_label.hide()
        self.genetic_type.hide()
        self.genetic_population.hide()
        
        # Add widgets for specifying the number of iterations
        self.iterations_label = QLabel("Iterations:", self)
        self.iterations_label.move(10, 250)
        self.iterations_edit = QLineEdit(self)
        self.iterations_edit.setText("10") 
        self.iterations_edit.move(100, 250)
        self.iterations_edit.resize(50, 30)
        
        # Add a button to run the selected algorithm
        self.run_button = QPushButton("Run Algorithm", self)
        self.run_button.move(10, 400)
        self.run_button.clicked.connect(self.run_algorithm)
        
        # Display the final score of the algorithm
        self.algorithm_score_label = QLabel("Final score: ", self)
        self.algorithm_score_label.move(10, 300)
        self.algorithm_score_value = QLabel("", self)
        self.algorithm_score_value.move(150, 300)
        
  
    # Method to update the UI based on the selected algorithm
    def update_algorithm_ui(self, index):
        algorithm = self.algorithm_combo.currentText()
        if algorithm == "Hill Climbing":
            self.selection_iterations_label.show()
            self.selection_iterations.show()
            self.selection_cooling_label.hide()
            self.cooling_option.hide()
            self.tabu_tenure_label.hide()
            self.tabu_tenure.hide()
            self.genetic_selection_label.hide()
            self.genetic_type.hide()
            self.genetic_population.hide()
        elif algorithm == "Simulated Annealing":
            self.selection_iterations_label.hide()
            self.selection_iterations.hide()
            self.selection_cooling_label.show()
            self.cooling_option.show()
            self.tabu_tenure_label.hide()
            self.tabu_tenure.hide()
            self.genetic_population.hide()
            self.genetic_type.hide()
            self.genetic_selection_label.hide()
        elif algorithm == "Tabu search":
            self.selection_iterations_label.hide()
            self.selection_iterations.hide()
            self.selection_cooling_label.hide()
            self.cooling_option.hide()
            self.tabu_tenure_label.show()
            self.tabu_tenure.show()
            self.genetic_population.hide()
            self.genetic_type.hide()
            self.genetic_selection_label.hide()
        elif algorithm == "Genetic algorithm":
            self.selection_iterations_label.hide()
            self.selection_iterations.hide()
            self.selection_cooling_label.hide()
            self.cooling_option.hide()
            self.tabu_tenure_label.hide()
            self.tabu_tenure.hide()
            self.genetic_population.show()
            self.genetic_type.show()
            self.genetic_selection_label.show()
        elif algorithm == "Guided Local Search":
            self.selection_iterations_label.hide()
            self.selection_iterations.hide()
            self.selection_cooling_label.hide()
            self.cooling_option.hide()
            self.tabu_tenure_label.hide()
            self.tabu_tenure.hide()
            self.genetic_population.hide()
            self.genetic_type.hide()
            self.genetic_selection_label.hide()
        else:
            self.selection_iterations_label.hide()
            self.selection_iterations.hide()
            self.selection_cooling_label.hide()
            self.cooling_option.hide()
            self.tabu_tenure_label.hide()
            self.tabu_tenure.hide()
            self.genetic_population.hide()
            self.genetic_type.hide()
            self.genetic_selection_label.hide()

    # Method to select a file from the dropdown menu
    def select_file(self, index):
        if index > 0:
            file_name = self.file_combo.currentText()
            self.file_path = os.path.join("data", file_name)
            return self.file_path

    # Method to run the selected algorithm
    def run_algorithm(self):
        try:
            start_time = time.time()

            # Parse the file and get pizzas and team sizes
            self.pizzas, self.team_sizes = parse_file(self.file_path)
            algorithm = self.algorithm_combo.currentText()
            iterations_type = self.selection_iterations.currentText()
            iterations_type_bool = True
            if(iterations_type == "Total of iterations"):
                iterations_type_bool = False               
            # Execute the selected algorithm
            if algorithm == "Hill Climbing":
                solution, score = hill_climbing(self.pizzas, self.team_sizes, int(self.iterations_edit.text()), iterations_type_bool)
                solution.save_to_file("solution_output.txt")
            elif algorithm == "Simulated Annealing":
                result, score = simulated_annealing(self.pizzas, self.team_sizes, int(self.iterations_edit.text()), int(self.cooling_option.text()))
            elif algorithm == "Tabu search":
                result, score = tabu_search(self.pizzas, self.team_sizes, int(self.iterations_edit.text()), int(self.tabu_tenure.text()))
            elif algorithm == "Genetic algorithm":
                result, score = genetic_algorithm(self.pizzas, self.team_sizes, int(self.iterations_edit.text()), self.genetic_type.currentText(), int(self.genetic_population.text()))
            elif algorithm == "Guided Local Search":
                result, score = guided_local_search(self.pizzas, self.team_sizes, int(self.iterations_edit.text()))
            # Display the final score of the algorithm
            self.algorithm_score_value.setText(str(score))
            print(score)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Execution time:", execution_time, "seconds")
        except Exception as e:
            print("An error occurred:", str(e))

# Application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
