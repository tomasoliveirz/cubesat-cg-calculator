#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
PROGRAM TO CALCULATE THE CENTER OF GRAVITY (CG) OF A CUBESAT
WITH AN INTERACTIVE TKINTER GUI (IMPROVED VERSION)
--------------------------------------------------------------------------------
Author: github.com/tomasoliveirz
Date  : 2024-12-30

This program exemplifies a professional tool to calculate the
Center of Gravity (CG) of a CubeSat, with checking of minimum and
maximum distances between components, including:

  - Interactive GUI with two tabs (Main and Settings).
  - Multiple language support (Portuguese and English) with dynamic switching.
  - Functions to save and load settings (JSON file).
  - Visualization of the best configuration results (CG within the range).
  - Individual adjustment of masses, thicknesses, and distance constraints
    between pairs of components.
  - Definition of the desired CG range, and other extras.

Requirements:
-------------
  - Python 3.x
  - tk/tkinter (native in Python)
  - itertools (native)
  - numpy (installed via pip or package manager)
  - json (native)
  - subprocess, sys, os (native)

Usage:
------
  python3 satelite_gui.py
===============================================================================
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fdlg
import json
import sys
import subprocess
import os
import itertools

# ---------------------------------------------------------------------
# 1) Auxiliary function to install numpy if possible
# ---------------------------------------------------------------------
def install_numpy_if_possible():
    """
    Tries to install NumPy via pip, unless the environment is
    externally managed (PEP 668). In that case, it shows a warning
    to install via apt-get or use a venv/conda.
    """
    externally_managed = False
    try:
        import sysconfig
        scheme_path = sysconfig.get_paths()["platlib"]  # e.g. /usr/lib/python3.X/site-packages
        marker_file = os.path.join(os.path.dirname(scheme_path), "EXTERNALLY-MANAGED")
        if os.path.exists(marker_file):
            externally_managed = True
    except:
        pass

    if externally_managed:
        print("This Python is externally managed (PEP 668).")
        print("Please install NumPy via your package manager, e.g.:")
        print("    sudo apt-get install python3-numpy")
        print("Or use a virtualenv/conda environment.")
        return

    print("Attempting to install 'numpy' in the current Python environment...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
        print("NumPy successfully installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing 'numpy': {e}")
        print("Try using --user, creating a venv, or install via apt-get/conda.")
        sys.exit(1)


# ---------------------------------------------------------------------
# 2) Translations (PT and EN)
# ---------------------------------------------------------------------
LANG_TEXTS = {
    "pt": {
        "title": "Calculadora de CG para CubeSat",
        "tab_main": "Principal",
        "tab_settings": "Configurações",
        "btn_calculate": "Calcular CG",
        "lbl_components_int": "Componentes Internos (Massas/Espessuras)",
        "lbl_components_ext": "Componentes Externos",
        "lbl_range": "Faixa de CG Desejada",
        "lbl_distances": "Distâncias entre Pares (Mínima e Máxima)",
        "lbl_mass": "Massa (g):",
        "lbl_thickness": "Espessura (mm):",
        "lbl_mass_pl": "Massa PL (g):",
        "lbl_thk_pl": "Esp. PL (mm):",
        "lbl_mass_eps": "Massa EPS (g):",
        "lbl_thk_eps": "Esp. EPS (mm):",
        "lbl_mass_obc": "Massa OBC (g):",
        "lbl_thk_obc": "Esp. OBC (mm):",
        "lbl_mass_rad": "Massa RAD (g):",
        "lbl_thk_rad": "Esp. RAD (mm):",
        "lbl_mass_solar": "Massa Painel Solar (g):",
        "lbl_height_solar": "Altura CG Painel (mm):",
        "lbl_mass_antenna": "Massa Antena (g):",
        "lbl_height_antenna": "Altura CG Antena (mm):",
        "lbl_mass_chassis": "Massa Chassi (g):",
        "lbl_height_chassis": "Altura CG Chassi (mm):",
        "lbl_total_height": "Altura Total CubeSat (mm):",
        "lbl_min_cg": "CG mínimo (mm):",
        "lbl_max_cg": "CG máximo (mm):",
        "lbl_dist": "Distância {A} - {B}:",
        "lbl_min": "Mín:",
        "lbl_max": "Máx:",
        "res_no_numpy": "Numpy não encontrado. Tente rodar o script novamente.\n",
        "res_error": "Erro ao ler parâmetros e executar cálculo: ",
        "res_best_config": "\nMelhor configuração encontrada!\n",
        "res_comp_height": "  {name} -> Altura do centro: {height:.2f} mm\n",
        "res_cg": "Centro de Gravidade (CG): {val:.2f} mm (dentro da faixa desejada)\n\n",
        "res_no_config": "\nNão foi encontrada configuração válida dentro da faixa de CG desejada.\n\n",
        "res_error_iteration": "Erro durante a geração e teste de configurações: ",
        "lbl_language": "Idioma:",
        "lbl_load_config": "Carregar Config.",
        "lbl_save_config": "Salvar Config.",
        "msg_config_loaded": "Configurações carregadas com sucesso!\n",
        "msg_config_saved": "Configurações salvas com sucesso!\n",
        "default_config_name": "config.json"
    },
    "en": {
        "title": "CubeSat CG Calculator",
        "tab_main": "Main",
        "tab_settings": "Settings",
        "btn_calculate": "Calculate CG",
        "lbl_components_int": "Internal Components (Mass/Thickness)",
        "lbl_components_ext": "External Components",
        "lbl_range": "Desired CG Range",
        "lbl_distances": "Distances Between Pairs (Min & Max)",
        "lbl_mass": "Mass (g):",
        "lbl_thickness": "Thickness (mm):",
        "lbl_mass_pl": "PL Mass (g):",
        "lbl_thk_pl": "PL Thick (mm):",
        "lbl_mass_eps": "EPS Mass (g):",
        "lbl_thk_eps": "EPS Thick (mm):",
        "lbl_mass_obc": "OBC Mass (g):",
        "lbl_thk_obc": "OBC Thick (mm):",
        "lbl_mass_rad": "RAD Mass (g):",
        "lbl_thk_rad": "RAD Thick (mm):",
        "lbl_mass_solar": "Solar Panel Mass (g):",
        "lbl_height_solar": "Solar Panel CG Height (mm):",
        "lbl_mass_antenna": "Antenna Mass (g):",
        "lbl_height_antenna": "Antenna CG Height (mm):",
        "lbl_mass_chassis": "Chassis Mass (g):",
        "lbl_height_chassis": "Chassis CG Height (mm):",
        "lbl_total_height": "CubeSat Total Height (mm):",
        "lbl_min_cg": "Min CG (mm):",
        "lbl_max_cg": "Max CG (mm):",
        "lbl_dist": "Distance {A} - {B}:",
        "lbl_min": "Min:",
        "lbl_max": "Max:",
        "res_no_numpy": "Numpy not found. Please rerun the script.\n",
        "res_error": "Error reading parameters or executing calculation: ",
        "res_best_config": "\nBest configuration found!\n",
        "res_comp_height": "  {name} -> Center height: {height:.2f} mm\n",
        "res_cg": "Center of Gravity (CG): {val:.2f} mm (within target range)\n\n",
        "res_no_config": "\nNo valid configuration found within the desired CG range.\n\n",
        "res_error_iteration": "Error during generation/testing of configurations: ",
        "lbl_language": "Language:",
        "lbl_load_config": "Load Config",
        "lbl_save_config": "Save Config",
        "msg_config_loaded": "Configuration successfully loaded!\n",
        "msg_config_saved": "Configuration successfully saved!\n",
        "default_config_name": "config.json"
    }
}


# ---------------------------------------------------------------------
# 3) Main application class
# ---------------------------------------------------------------------
class SateliteApp:
    """
    Main application class, containing all GUI elements and the CG calculation logic.
    """

    def __init__(self, master):
        """
        Class constructor. Responsible for creating the interface and initializing variables.
        """
        self.master = master
        
        # Default language
        self.current_lang = "en"

        # Configure TTK Style for a more "professional" look
        self.style = ttk.Style(self.master)
        # Try to use one of the available themes ('clam', 'vista', 'alt', etc.)
        try:
            self.style.theme_use('clam')
        except:
            pass
        # Customize fonts and frame sizes
        self.style.configure('TLabelFrame', font=('Arial', 11, 'bold'), padding=10)
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)
        self.style.configure('TEntry', padding=5)

        # Set window title (language-dependent)
        self.master.title(self.tr("title"))
        # Set window size
        self.master.geometry("1600x500")
        self.master.resizable(True, True)

        # ------------------------------------------------------------
        # 1) Definition of component names (internal)
        # ------------------------------------------------------------
        # Indices: 0->PL, 1->EPS, 2->OBC, 3->RAD
        self.component_names = ['PL', 'EPS', 'OBC', 'RAD']
        self.component_indices = {'PL': 0, 'EPS': 1, 'OBC': 2, 'RAD': 3}

        # Pairs of components to avoid duplication (X, Y) with X < Y
        self.component_pairs = [
            ('PL', 'EPS'),
            ('PL', 'OBC'),
            ('PL', 'RAD'),
            ('EPS', 'OBC'),
            ('EPS', 'RAD'),
            ('OBC', 'RAD')
        ]

        # ------------------------------------------------------------
        # 2) Input variables (mass, thickness, etc.)
        # ------------------------------------------------------------
        self.var_mass_pl = tk.DoubleVar(value=100.0)
        self.var_mass_eps = tk.DoubleVar(value=300.0)
        self.var_mass_obc = tk.DoubleVar(value=100.0)
        self.var_mass_rad = tk.DoubleVar(value=100.0)

        self.var_thk_pl = tk.DoubleVar(value=20.0)
        self.var_thk_eps = tk.DoubleVar(value=20.0)
        self.var_thk_obc = tk.DoubleVar(value=15.0)
        self.var_thk_rad = tk.DoubleVar(value=15.0)

        # External components
        self.var_solar_mass = tk.DoubleVar(value=57.0)
        self.var_solar_height = tk.DoubleVar(value=105.0)
        self.var_antenna_mass = tk.DoubleVar(value=90.0)
        self.var_antenna_height = tk.DoubleVar(value=105.0)

        # Chassis
        self.var_chassis_mass = tk.DoubleVar(value=120.0)
        self.var_chassis_height = tk.DoubleVar(value=48.0)

        # Total height
        self.var_total_height = tk.DoubleVar(value=98.0)

        # ------------------------------------------------------------
        # 3) Desired CG range
        # ------------------------------------------------------------
        self.var_target_min = tk.DoubleVar(value=40.0)
        self.var_target_max = tk.DoubleVar(value=60.0)

        # ------------------------------------------------------------
        # 4) Minimum and maximum distances between pairs
        # ------------------------------------------------------------
        self.min_dist_vars = {}
        self.max_dist_vars = {}
        for pair in self.component_pairs:
            self.min_dist_vars[pair] = tk.DoubleVar(value=0.0)
            self.max_dist_vars[pair] = tk.DoubleVar(value=9999.0)

        # ------------------------------------------------------------
        # 5) Creating Notebook tabs (Main and Settings)
        # ------------------------------------------------------------
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # --- Main Tab ---
        self.tab_main = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_main, text=self.tr("tab_main"))

        # --- Settings Tab ---
        self.tab_settings = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_settings, text=self.tr("tab_settings"))

        # Build the interface inside each tab
        self._build_tab_main()
        self._build_tab_settings()

    # -------------------------------------------------------------------------
    # Translation function
    # -------------------------------------------------------------------------
    def tr(self, key):
        """
        Returns the translation for a given key, according to the current language.
        """
        if key in LANG_TEXTS[self.current_lang]:
            return LANG_TEXTS[self.current_lang][key]
        else:
            # If the key does not exist, return the key itself
            return key

    def set_language(self, lang):
        """
        Changes the application language (pt or en) and updates labels.
        """
        self.current_lang = lang
        self.master.title(self.tr("title"))
        # Update tab texts
        self.notebook.tab(self.tab_main, text=self.tr("tab_main"))
        self.notebook.tab(self.tab_settings, text=self.tr("tab_settings"))
        # Update all label texts in the main tab
        self._update_tab_main_texts()
        # Update all label texts in the settings tab
        self._update_tab_settings_texts()

    # -------------------------------------------------------------------------
    # Main tab construction
    # -------------------------------------------------------------------------
    def _build_tab_main(self):
        """
        Creates the main interface (data input + calculate button + results text area).
        """
        # Top frame in the main tab
        self.frame_main_top = ttk.Frame(self.tab_main)
        self.frame_main_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Subdivision of the main top frame
        # 1) Frame for internal components
        self.frame_comp_int = ttk.LabelFrame(self.frame_main_top, text=self.tr("lbl_components_int"))
        self.frame_comp_int.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 2) Frame for external components
        self.frame_comp_ext = ttk.LabelFrame(self.frame_main_top, text=self.tr("lbl_components_ext"))
        self.frame_comp_ext.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 3) Frame for CG range
        self.frame_cg_range = ttk.LabelFrame(self.frame_main_top, text=self.tr("lbl_range"))
        self.frame_cg_range.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 4) Frame for distances
        self.frame_dists = ttk.LabelFrame(self.frame_main_top, text=self.tr("lbl_distances"))
        self.frame_dists.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 5) Bottom frame for calculate button and results
        self.frame_main_bottom = ttk.Frame(self.tab_main)
        self.frame_main_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Fill each frame
        self._fill_frame_comp_int()
        self._fill_frame_comp_ext()
        self._fill_frame_cg_range()
        self._fill_frame_distances()

        # Calculate button
        self.btn_calcular = ttk.Button(
            self.frame_main_bottom, 
            text=self.tr("btn_calculate"), 
            command=self._on_calcular
        )
        self.btn_calcular.pack(side=tk.LEFT, padx=5, pady=5)

        # Results TextArea
        self.text_result = tk.Text(self.frame_main_bottom, height=20, width=100)
        self.text_result.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_result.configure(state=tk.DISABLED)

    def _fill_frame_comp_int(self):
        """
        Creates and stores references to the labels and entries for internal components
        so we can update them dynamically when switching language.
        """
        row = 0
        self.lbl_mass_pl = ttk.Label(self.frame_comp_int, text=self.tr("lbl_mass_pl"))
        self.lbl_mass_pl.grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.frame_comp_int, textvariable=self.var_mass_pl, width=10).grid(row=row, column=1)

        self.lbl_thk_pl = ttk.Label(self.frame_comp_int, text=self.tr("lbl_thk_pl"))
        self.lbl_thk_pl.grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.frame_comp_int, textvariable=self.var_thk_pl, width=10).grid(row=row, column=3)

        row += 1
        self.lbl_mass_eps = ttk.Label(self.frame_comp_int, text=self.tr("lbl_mass_eps"))
        self.lbl_mass_eps.grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.frame_comp_int, textvariable=self.var_mass_eps, width=10).grid(row=row, column=1)

        self.lbl_thk_eps = ttk.Label(self.frame_comp_int, text=self.tr("lbl_thk_eps"))
        self.lbl_thk_eps.grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.frame_comp_int, textvariable=self.var_thk_eps, width=10).grid(row=row, column=3)

        row += 1
        self.lbl_mass_obc = ttk.Label(self.frame_comp_int, text=self.tr("lbl_mass_obc"))
        self.lbl_mass_obc.grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.frame_comp_int, textvariable=self.var_mass_obc, width=10).grid(row=row, column=1)

        self.lbl_thk_obc = ttk.Label(self.frame_comp_int, text=self.tr("lbl_thk_obc"))
        self.lbl_thk_obc.grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.frame_comp_int, textvariable=self.var_thk_obc, width=10).grid(row=row, column=3)

        row += 1
        self.lbl_mass_rad = ttk.Label(self.frame_comp_int, text=self.tr("lbl_mass_rad"))
        self.lbl_mass_rad.grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.frame_comp_int, textvariable=self.var_mass_rad, width=10).grid(row=row, column=1)

        self.lbl_thk_rad = ttk.Label(self.frame_comp_int, text=self.tr("lbl_thk_rad"))
        self.lbl_thk_rad.grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.frame_comp_int, textvariable=self.var_thk_rad, width=10).grid(row=row, column=3)

    def _fill_frame_comp_ext(self):
        """
        Creates and stores references to the labels and entries for external components
        so we can update them dynamically when switching language.
        """
        row = 0
        self.lbl_mass_solar = ttk.Label(self.frame_comp_ext, text=self.tr("lbl_mass_solar"))
        self.lbl_mass_solar.grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.frame_comp_ext, textvariable=self.var_solar_mass, width=10).grid(row=row, column=1)

        self.lbl_height_solar = ttk.Label(self.frame_comp_ext, text=self.tr("lbl_height_solar"))
        self.lbl_height_solar.grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.frame_comp_ext, textvariable=self.var_solar_height, width=10).grid(row=row, column=3)

        row += 1
        self.lbl_mass_antenna = ttk.Label(self.frame_comp_ext, text=self.tr("lbl_mass_antenna"))
        self.lbl_mass_antenna.grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.frame_comp_ext, textvariable=self.var_antenna_mass, width=10).grid(row=row, column=1)

        self.lbl_height_antenna = ttk.Label(self.frame_comp_ext, text=self.tr("lbl_height_antenna"))
        self.lbl_height_antenna.grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.frame_comp_ext, textvariable=self.var_antenna_height, width=10).grid(row=row, column=3)

        row += 1
        self.lbl_mass_chassis = ttk.Label(self.frame_comp_ext, text=self.tr("lbl_mass_chassis"))
        self.lbl_mass_chassis.grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.frame_comp_ext, textvariable=self.var_chassis_mass, width=10).grid(row=row, column=1)

        self.lbl_height_chassis = ttk.Label(self.frame_comp_ext, text=self.tr("lbl_height_chassis"))
        self.lbl_height_chassis.grid(row=row, column=2, sticky=tk.W)
        ttk.Entry(self.frame_comp_ext, textvariable=self.var_chassis_height, width=10).grid(row=row, column=3)

        row += 1
        self.lbl_total_height = ttk.Label(self.frame_comp_ext, text=self.tr("lbl_total_height"))
        self.lbl_total_height.grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(self.frame_comp_ext, textvariable=self.var_total_height, width=10).grid(row=row, column=1)

    def _fill_frame_cg_range(self):
        """
        Creates and stores references for CG range inputs.
        """
        ttk.Label(self.frame_cg_range, text=self.tr("lbl_min_cg")).grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.frame_cg_range, textvariable=self.var_target_min, width=10).grid(row=0, column=1)

        ttk.Label(self.frame_cg_range, text=self.tr("lbl_max_cg")).grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self.frame_cg_range, textvariable=self.var_target_max, width=10).grid(row=1, column=1)

    def _fill_frame_distances(self):
        """
        Creates and stores references for minimum and maximum distance inputs.
        """
        row_idx = 0
        for pair in self.component_pairs:
            A, B = pair
            label_text = self.tr("lbl_dist").format(A=A, B=B)
            ttk.Label(self.frame_dists, text=label_text).grid(row=row_idx, column=0, sticky=tk.W, padx=5, pady=2)

            ttk.Label(self.frame_dists, text=self.tr("lbl_min")).grid(row=row_idx, column=1, sticky=tk.E)
            ttk.Entry(self.frame_dists, textvariable=self.min_dist_vars[pair], width=6).grid(row=row_idx, column=2, sticky=tk.W)

            ttk.Label(self.frame_dists, text=self.tr("lbl_max")).grid(row=row_idx, column=3, sticky=tk.E)
            ttk.Entry(self.frame_dists, textvariable=self.max_dist_vars[pair], width=6).grid(row=row_idx, column=4, sticky=tk.W)

            row_idx += 1

    def _update_tab_main_texts(self):
        """
        Updates the label text in the main tab according to the current language.
        """
        # Update LabelFrames
        self.frame_comp_int.config(text=self.tr("lbl_components_int"))
        self.frame_comp_ext.config(text=self.tr("lbl_components_ext"))
        self.frame_cg_range.config(text=self.tr("lbl_range"))
        self.frame_dists.config(text=self.tr("lbl_distances"))
        self.btn_calcular.config(text=self.tr("btn_calculate"))

        # Update individual Labels for Internal Components
        self.lbl_mass_pl.config(text=self.tr("lbl_mass_pl"))
        self.lbl_thk_pl.config(text=self.tr("lbl_thk_pl"))
        self.lbl_mass_eps.config(text=self.tr("lbl_mass_eps"))
        self.lbl_thk_eps.config(text=self.tr("lbl_thk_eps"))
        self.lbl_mass_obc.config(text=self.tr("lbl_mass_obc"))
        self.lbl_thk_obc.config(text=self.tr("lbl_thk_obc"))
        self.lbl_mass_rad.config(text=self.tr("lbl_mass_rad"))
        self.lbl_thk_rad.config(text=self.tr("lbl_thk_rad"))

        # Update individual Labels for External Components
        self.lbl_mass_solar.config(text=self.tr("lbl_mass_solar"))
        self.lbl_height_solar.config(text=self.tr("lbl_height_solar"))
        self.lbl_mass_antenna.config(text=self.tr("lbl_mass_antenna"))
        self.lbl_height_antenna.config(text=self.tr("lbl_height_antenna"))
        self.lbl_mass_chassis.config(text=self.tr("lbl_mass_chassis"))
        self.lbl_height_chassis.config(text=self.tr("lbl_height_chassis"))
        self.lbl_total_height.config(text=self.tr("lbl_total_height"))

        # For distances, we re-check each pair's label, but it's simpler to rebuild
        # or rely on the dynamic text (the format with A, B doesn't require storing a label).
        # In a more elaborate approach, we'd store references to these labels as well.

    # -------------------------------------------------------------------------
    # Settings tab construction
    # -------------------------------------------------------------------------
    def _build_tab_settings(self):
        """
        Creates the interface in the Settings tab: language switch, save/load config, etc.
        """
        # Language frame
        frame_lang = ttk.LabelFrame(self.tab_settings, text=self.tr("tab_settings"))
        frame_lang.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Language selector
        ttk.Label(frame_lang, text=self.tr("lbl_language")).pack(side=tk.LEFT, padx=5)
        self.cmb_language = ttk.Combobox(frame_lang, values=["pt", "en"], width=5)
        self.cmb_language.set(self.current_lang)
        self.cmb_language.pack(side=tk.LEFT, padx=5)

        self.btn_apply_lang = ttk.Button(frame_lang, text="OK", command=self._on_apply_lang)
        self.btn_apply_lang.pack(side=tk.LEFT, padx=5)

        # Frame for save/load config
        frame_config = ttk.LabelFrame(self.tab_settings)
        frame_config.config(text=self.tr("tab_settings"))
        frame_config.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.btn_load_config = ttk.Button(frame_config, text=self.tr("lbl_load_config"), command=self._on_load_config)
        self.btn_load_config.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_save_config = ttk.Button(frame_config, text=self.tr("lbl_save_config"), command=self._on_save_config)
        self.btn_save_config.pack(side=tk.LEFT, padx=5, pady=5)

    def _update_tab_settings_texts(self):
        """
        Updates text in the Settings tab when changing language.
        """
        # Update the LabelFrames in the settings tab
        for f in self.tab_settings.winfo_children():
            if isinstance(f, ttk.LabelFrame):
                f.config(text=self.tr("tab_settings"))
                for child in f.winfo_children():
                    if isinstance(child, ttk.Label):
                        if child.cget("text") in [
                            LANG_TEXTS["pt"]["lbl_language"], 
                            LANG_TEXTS["en"]["lbl_language"]
                        ]:
                            child.config(text=self.tr("lbl_language"))
                    if isinstance(child, ttk.Button):
                        txt = child.cget("text")
                        if txt in [LANG_TEXTS["pt"]["lbl_load_config"], LANG_TEXTS["en"]["lbl_load_config"]]:
                            child.config(text=self.tr("lbl_load_config"))
                        elif txt in [LANG_TEXTS["pt"]["lbl_save_config"], LANG_TEXTS["en"]["lbl_save_config"]]:
                            child.config(text=self.tr("lbl_save_config"))

    def _on_apply_lang(self):
        """
        Called when user clicks "OK" to change the language.
        """
        new_lang = self.cmb_language.get()
        if new_lang in ("pt", "en"):
            self.set_language(new_lang)

    # -------------------------------------------------------------------------
    # Save and Load Configurations (JSON)
    # -------------------------------------------------------------------------
    def _on_save_config(self):
        """
        Saves current variables to a JSON file.
        """
        filename = fdlg.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=self.tr("default_config_name")
        )
        if not filename:
            return
        cfg = self._export_config()
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
            self._append_texto(self.tr("msg_config_saved"))
        except Exception as e:
            self._append_texto(f"{self.tr('res_error')}{str(e)}\n")

    def _on_load_config(self):
        """
        Loads configurations from a JSON file and applies them.
        """
        filename = fdlg.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            self._import_config(cfg)
            self._append_texto(self.tr("msg_config_loaded"))
        except Exception as e:
            self._append_texto(f"{self.tr('res_error')}{str(e)}\n")

    def _export_config(self):
        """
        Returns a dictionary with all current application data (masses, etc.).
        """
        data = {
            "mass_pl": self.var_mass_pl.get(),
            "mass_eps": self.var_mass_eps.get(),
            "mass_obc": self.var_mass_obc.get(),
            "mass_rad": self.var_mass_rad.get(),
            "thk_pl": self.var_thk_pl.get(),
            "thk_eps": self.var_thk_eps.get(),
            "thk_obc": self.var_thk_obc.get(),
            "thk_rad": self.var_thk_rad.get(),
            "solar_mass": self.var_solar_mass.get(),
            "solar_height": self.var_solar_height.get(),
            "antenna_mass": self.var_antenna_mass.get(),
            "antenna_height": self.var_antenna_height.get(),
            "chassis_mass": self.var_chassis_mass.get(),
            "chassis_height": self.var_chassis_height.get(),
            "total_height": self.var_total_height.get(),
            "target_min": self.var_target_min.get(),
            "target_max": self.var_target_max.get(),
            "min_dists": {},
            "max_dists": {}
        }
        for pair in self.component_pairs:
            data["min_dists"][pair[0] + "_" + pair[1]] = self.min_dist_vars[pair].get()
            data["max_dists"][pair[0] + "_" + pair[1]] = self.max_dist_vars[pair].get()
        data["language"] = self.current_lang
        return data

    def _import_config(self, cfg):
        """
        Applies the settings from a dictionary to the current state.
        """
        self.var_mass_pl.set(cfg.get("mass_pl", 100.0))
        self.var_mass_eps.set(cfg.get("mass_eps", 300.0))
        self.var_mass_obc.set(cfg.get("mass_obc", 100.0))
        self.var_mass_rad.set(cfg.get("mass_rad", 100.0))

        self.var_thk_pl.set(cfg.get("thk_pl", 20.0))
        self.var_thk_eps.set(cfg.get("thk_eps", 20.0))
        self.var_thk_obc.set(cfg.get("thk_obc", 15.0))
        self.var_thk_rad.set(cfg.get("thk_rad", 15.0))

        self.var_solar_mass.set(cfg.get("solar_mass", 57.0))
        self.var_solar_height.set(cfg.get("solar_height", 105.0))
        self.var_antenna_mass.set(cfg.get("antenna_mass", 90.0))
        self.var_antenna_height.set(cfg.get("antenna_height", 105.0))

        self.var_chassis_mass.set(cfg.get("chassis_mass", 120.0))
        self.var_chassis_height.set(cfg.get("chassis_height", 48.0))

        self.var_total_height.set(cfg.get("total_height", 98.0))

        self.var_target_min.set(cfg.get("target_min", 40.0))
        self.var_target_max.set(cfg.get("target_max", 60.0))

        # Distance constraints
        min_dists = cfg.get("min_dists", {})
        max_dists = cfg.get("max_dists", {})
        for pair in self.component_pairs:
            key = pair[0] + "_" + pair[1]
            if key in min_dists:
                self.min_dist_vars[pair].set(min_dists[key])
            if key in max_dists:
                self.max_dist_vars[pair].set(max_dists[key])

        # Language
        if "language" in cfg:
            self.set_language(cfg["language"])

    # -------------------------------------------------------------------------
    # Calculation
    # -------------------------------------------------------------------------
    def _on_calcular(self):
        """
        Called when the user clicks "Calcular CG" / "Calculate CG".
        Reads field values, builds the distance matrices, and invokes the logic.
        """
        self._limpar_texto()

        # Try to import numpy now
        try:
            import numpy as np
        except ImportError:
            self._append_texto(self.tr("res_no_numpy"))
            return

        try:
            # 1) Get masses and thicknesses
            masses = np.array([
                self.var_mass_pl.get(),
                self.var_mass_eps.get(),
                self.var_mass_obc.get(),
                self.var_mass_rad.get()
            ], dtype=float)

            thicknesses = np.array([
                self.var_thk_pl.get(),
                self.var_thk_eps.get(),
                self.var_thk_obc.get(),
                self.var_thk_rad.get()
            ], dtype=float)

            # 2) Get external component values
            solar_panel_mass = self.var_solar_mass.get()
            solar_panel_height = self.var_solar_height.get()
            antenna_mass = self.var_antenna_mass.get()
            antenna_height = self.var_antenna_height.get()
            chassis_mass = self.var_chassis_mass.get()
            chassis_height = self.var_chassis_height.get()
            total_height = self.var_total_height.get()

            # 3) Target CG range
            target_range = (
                self.var_target_min.get(),
                self.var_target_max.get()
            )

            # 4) Build min/max distance matrices
            min_distance_matrix = self._build_distance_matrix(self.min_dist_vars, np)
            max_distance_matrix = self._build_distance_matrix(self.max_dist_vars, np)

            # 5) Execute calculation
            result = self._executar_calculo(
                masses, thicknesses,
                solar_panel_mass, solar_panel_height,
                antenna_mass, antenna_height,
                chassis_mass, chassis_height,
                total_height,
                target_range,
                min_distance_matrix, max_distance_matrix,
                np
            )

            self._append_texto(result)

        except Exception as e:
            self._append_texto(f"{self.tr('res_error')}{str(e)}\n")

    def _build_distance_matrix(self, dist_vars_dict, np):
        """
        Dynamically builds a 4x4 matrix (for the 4 components).
        """
        size = len(self.component_names)  # 4
        matrix = np.zeros((size, size), dtype=float)

        for i in range(size):
            matrix[i][i] = 0.0

        for pair, var_value in dist_vars_dict.items():
            A, B = pair
            dist_val = var_value.get()
            iA = self.component_indices[A]
            iB = self.component_indices[B]
            matrix[iA][iB] = dist_val
            matrix[iB][iA] = dist_val

        return matrix

    def _executar_calculo(self,
                          masses, thicknesses,
                          solar_panel_mass, solar_panel_height,
                          antenna_mass, antenna_height,
                          chassis_mass, chassis_height,
                          total_height,
                          target_range,
                          min_distance_matrix,
                          max_distance_matrix,
                          np):
        """
        Exhaustively searches for the best configuration
        that provides the lowest CG within the target range.
        """
        best_cg = float('inf')
        best_heights = None

        heights = np.zeros(len(masses), dtype=float)
        # Fix PL at the bottom
        heights[0] = thicknesses[0] / 2.0
        # Fix RAD at the top
        heights[3] = total_height - (thicknesses[3] / 2.0)

        # The movable components
        movable_indices = [1, 2]  # EPS, OBC

        try:
            for perm in itertools.permutations(movable_indices):
                min_altura_1 = int(thicknesses[perm[0]] / 2)
                max_altura_1 = int(heights[3] - thicknesses[3] / 2 - thicknesses[perm[0]] / 2)

                for height1 in range(min_altura_1, max_altura_1 + 1):
                    heights[perm[0]] = float(height1)

                    min_altura_2 = int(
                        height1
                        + thicknesses[perm[0]] / 2
                        + thicknesses[perm[1]] / 2
                        + min_distance_matrix[perm[0]][perm[1]]
                        - thicknesses[perm[1]] / 2
                    )
                    max_altura_2 = int(heights[3] - thicknesses[3] / 2 - thicknesses[perm[1]] / 2)

                    for height2 in range(min_altura_2, max_altura_2 + 1):
                        heights[perm[1]] = float(height2)

                        # Check if distance constraints are satisfied
                        if not self.verifica_distancias_minmax(
                            heights, thicknesses,
                            min_distance_matrix,
                            max_distance_matrix
                        ):
                            continue

                        # Calculate CG
                        cg_val = self.calcula_cg(
                            heights, masses,
                            solar_panel_height, solar_panel_mass,
                            antenna_height, antenna_mass,
                            chassis_height, chassis_mass
                        )
                        if cg_val is None:
                            continue

                        # If CG is within range and is the best so far, store
                        if target_range[0] <= cg_val <= target_range[1] and cg_val < best_cg:
                            best_cg = cg_val
                            best_heights = heights.copy()

            if best_heights is not None:
                res = self.tr("res_best_config")
                for i, name in enumerate(self.component_names):
                    res += self.tr("res_comp_height").format(name=name, height=best_heights[i])
                res += self.tr("res_cg").format(val=best_cg)
            else:
                res = self.tr("res_no_config")

            return res

        except Exception as e:
            return f"{self.tr('res_error_iteration')}{str(e)}\n"

    @staticmethod
    def calcula_cg(heights, masses,
                   solar_panel_height, solar_panel_mass,
                   antenna_height, antenna_mass,
                   chassis_height, chassis_mass):
        """
        Calculates the Center of Gravity (CG) based on the central heights of internal components,
        including the contributions of the solar panel, antenna, and chassis.
        """
        try:
            total_mass = sum(masses) + solar_panel_mass + antenna_mass + chassis_mass
            soma_momentos = (
                sum(heights * masses)
                + (solar_panel_height * solar_panel_mass)
                + (antenna_height * antenna_mass)
                + (chassis_height * chassis_mass)
            )
            return soma_momentos / total_mass
        except:
            return None

    @staticmethod
    def verifica_distancias_minmax(heights, thicknesses, min_distance_matrix, max_distance_matrix):
        """
        Checks if all distances between component edges respect the min/max distance matrices.
        """
        n = len(heights)
        edges = {}
        for i in range(n):
            edges[i] = (
                heights[i] - thicknesses[i] / 2.0,
                heights[i] + thicknesses[i] / 2.0
            )
        for i in range(n):
            for j in range(i + 1, n):
                if heights[i] <= heights[j]:
                    lower, higher = i, j
                else:
                    lower, higher = j, i

                dist_entre_bordas = edges[higher][0] - edges[lower][1]

                if dist_entre_bordas < min_distance_matrix[lower][higher]:
                    return False
                if dist_entre_bordas > max_distance_matrix[lower][higher]:
                    return False
        return True

    # -------------------------------------------------------------------------
    # Helper functions for the results text
    # -------------------------------------------------------------------------
    def _limpar_texto(self):
        self.text_result.configure(state=tk.NORMAL)
        self.text_result.delete("1.0", tk.END)
        self.text_result.configure(state=tk.DISABLED)

    def _append_texto(self, texto):
        self.text_result.configure(state=tk.NORMAL)
        self.text_result.insert(tk.END, texto)
        self.text_result.configure(state=tk.DISABLED)


# ---------------------------------------------------------------------
# 4) main
# ---------------------------------------------------------------------
def main():
    # Try importing numpy; if it fails, install if possible
    try:
        import numpy  # noqa
        print("NumPy is already installed. Continuing...")
    except ImportError:
        install_numpy_if_possible()
        try:
            import numpy  # noqa
            print("NumPy imported successfully after installation.")
        except ImportError:
            print("Failed to import 'numpy' even after attempted installation.")
            sys.exit(1)

    print("Starting application...")
    root = tk.Tk()
    app = SateliteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
