# CubeSat CG Calculator

A Python-based tool for calculating the **Center of Gravity (CG)** of a CubeSat, featuring a Tkinter GUI, interactive components, and multi-language support. This project is designed to help aerospace and academic enthusiasts, engineers, or students quickly assess the CG position of CubeSat components while adhering to minimal and maximal distance constraints between internal modules.

---

## Table of Contents
1. [Overview](#overview)  
2. [Key Features](#key-features)  
3. [Installation & Requirements](#installation--requirements)  
4. [Usage](#usage)  
5. [Project Structure](#project-structure)  
6. [Contribution Guidelines](#contribution-guidelines)  
7. [Contact](#contact)  
8. [License](#license)

---

## Overview

**CubeSat CG Calculator** provides an interactive way to:
- Configure component masses, thicknesses, and positions.
- Enforce distance constraints among internal hardware (e.g., PL, EPS, OBC, RAD).
- Validate external components like solar panels, antennas, and chassis positions.
- Dynamically switch interface languages (Portuguese/English).
- Save or load configurations (JSON) for quick reference.
- Automatically compute a valid arrangement whose overall CG falls within a desired range.

> **Note**: This project was created by [Tomás Oliveira](https://github.com/tomasoliveirz), a Software Developer and Informatics & Computer Engineering student, to demonstrate the use of Python, Tkinter, and JSON-based configuration handling in a small engineering utility.

Since there are no available images or screenshots, feel free to clone, run the GUI, and explore its features on your own environment.

---

## Key Features

- **Interactive Graphical Interface**  
  Built with Tkinter, featuring a clear layout for component input and CG results.

- **Multi-language Support**  
  Easily toggle between Portuguese and English labels, messages, and button texts.

- **Dynamic Constraints**  
  Define minimum and maximum distances between components to simulate real CubeSat constraints.

- **JSON-Based Configuration**  
  Save and load settings to a JSON file, enabling quick reconfiguration without re-entering all data.

- **Exhaustive Calculation**  
  Iterates over permissible permutations and heights of internal components to find the best valid CG alignment.

---

## Installation & Requirements

1. **Python 3.7+**  
   Make sure you have a recent version of Python installed.

2. **Dependencies**  
   - **Tkinter**: Typically included with most Python distributions.  
   - **NumPy**: For vector/matrix operations.  
   - **json** (standard library)  
   - **itertools** (standard library)  

   If NumPy is not present, the script will attempt to install it (unless your environment is externally managed).

3. **Operating System**  
   - Works on Windows, macOS, or Linux environments with Python 3.x.

### Steps

```bash
# 1) Clone the repository
git clone https://github.com/tomasoliveirz/cubesat-cg-calculator.git

# 2) Navigate into the project directory
cd cubesat-cg-calculator

# 3) Run the Python script
python3 satelite_gui.py
```

---

## Usage

Once launched, the GUI will open with two main tabs:

1. **Main Tab**  
   - Enter masses and thicknesses for internal CubeSat modules (PL, EPS, OBC, RAD).  
   - Specify external components like solar panels, antenna, and chassis, including mass and CG height.  
   - Define the desired CG range.  
   - Set minimal and maximal distance constraints for pairs of components.  
   - Click **Calculate CG** to find a configuration that fits your constraints. Results will appear in the text area.

2. **Settings Tab**  
   - Change the application language (Portuguese/English).  
   - Load or save configuration files (in JSON).  

### Example Flow

1. **Enter** your CubeSat modules’ mass, thickness, and external component parameters.  
2. **Set** any distance constraints (min/max) between pairs if needed.  
3. **Provide** the desired CG range.  
4. **Press** the **Calculate CG** button to run.  
5. **View** the result in the text area: if a valid arrangement is found, the best configuration is shown, otherwise, a message indicates no configuration met the criteria.

---

## Project Structure

```
cubesat-cg-calculator/
  ├── satelite_gui.py        # Main Python script with Tkinter GUI and logic
  ├── README.md              # Project README (this file)
  ├── ...
  └── config.json            # Example config file (optional, can be created/saved)
```

---

## Contribution Guidelines

Contributions are welcome! If you find bugs, improvements, or would like to add new features:

1. **Fork** the repository.  
2. **Create** a new branch (`git checkout -b feature/awesome-improvement`).  
3. **Commit** your changes (`git commit -m "Add awesome improvement"`).  
4. **Push** to your branch (`git push origin feature/awesome-improvement`).  
5. **Open** a Pull Request.  

Please maintain a clear commit history and follow best practices for Python code (PEP 8 style).

---

## Contact

**Author**: [Tomás Oliveira](https://github.com/tomasoliveirz)   
**LinkedIn**: [linkedin.com/tomasoliveirz](https://www.linkedin.com/in/tom%C3%A1s-oliveira-52966422b/)  

Tomás is currently a **Software Developer** and **Informatics & Computer Engineering** student at **FEUP** (University of Porto).  
Feel free to reach out for any questions, suggestions, or collaboration ideas related to this project—or tech in general!

---

## License

You are free to use, modify, and distribute it in both commercial and non-commercial projects, but please attribute the original author where appropriate.

---

Thank you for checking out **CubeSat CG Calculator**! We hope it proves valuable for your academic or hobbyist CubeSat endeavors. If you have any suggestions or issues, don’t hesitate to create an issue or reach out directly. Safe experimenting and best of luck on your projects!
