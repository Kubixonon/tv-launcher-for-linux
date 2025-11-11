#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, Menu, simpledialog, filedialog, colorchooser
import os
import subprocess
import datetime
import webview
import qtpy
import sys
import json
import pytz
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
import requests
import tempfile
import shutil

# --- Słownik Tłumaczeń (Translations) ---
DEFAULT_TRANSLATIONS = {
    'en': {
        'app_title': "Streaming Launcher",
        'vlc_player': "VLC Player",
        'vlc_playing': "Playing:",
        'back': "Back",
        'error': "Error",
        'vlc_not_found': "VLC not found. Install it with 'sudo apt install vlc'",
        'could_not_play': "Could not play file:",
        'warning': "Warning",
        'vlc_playback_warning': "VLC not found. File playback may not work.\nInstall with: (e.g., sudo apt-get install vlc)",
        'applications': "Applications",
        'multimedia': "Multimedia",
        'settings': "Settings",
        'shutdown': "Shutdown",
        'confirm': "Confirm",
        'reset_theme_confirm': "Reset theme to default?",
        'success': "Success",
        'bg_color_changed': "Background color changed! Restart the app to see changes.",
        'accent_color_changed': "Accent color changed! Restart the app to see changes.",
        'change_font': "Change Font",
        'font_family': "Font Family:",
        'font_size': "Font Size:",
        'apply': "Apply",
        'font_changed': "Font changed! Restart the app to see changes.",
        'theme_reset': "Theme reset! Restart the app to see changes.",
        'select_bg_image': "Select background image",
        'image_files': "Image files",
        'bg_image_set': "Background image set! Restart the app to see changes.",
        'bg_image_removed': "Background image removed! Restart the app to see changes.",
        'bg_brightness': "Background Brightness",
        'enter_brightness': "Enter brightness value (0.1 - 2.0):",
        'brightness_saved': "Brightness setting saved! Restart the app to see changes.",
        'bg_blur': "Background Blur",
        'enter_blur': "Enter blur radius (0-20):",
        'blur_saved': "Blur setting saved! Restart the app to see changes.",
        'setting_updated': "Setting updated! Restart the app to see changes.",
        'button_style': "Button Style",
        'rounded': "Rounded",
        'square': "Square",
        'modern': "Modern",
        'style_changed': "Button style changed! Restart the app to see changes.",
        'change_video_folder': "Change Video Folder",
        'select_video_folder': "Select video folder",
        'folder_changed': "Video folder changed to:",
        'rescan_media': "Rescan Media",
        'rescan_complete': "Media library rescanned!",
        'theme': "Theme",
        'change_bg_color': "Change Background Color",
        'change_accent_color': "Change Accent Color",
        'reset_theme': "Reset Theme",
        'background': "Background",
        'set_bg_image': "Set Background Image",
        'remove_bg_image': "Remove Background Image",
        'bg_brightness_opt': "Background Brightness",
        'bg_blur_opt': "Background Blur",
        'layout': "Layout",
        'toggle_clock': "Toggle Clock",
        'toggle_apps': "Toggle Apps",
        'toggle_movies': "Toggle Movies",
        'media': "Media",
        'update_app': "Update App",
        'close': "Close",
        'downloading_update': "Downloading update...",
        'installing_update': "Installing update...",
        'update_complete': "Update completed! The app will restart.",
        'download_failed': "Download failed:",
        'time_format': "Time format",
        'enter_time_format': "Enter the time display format (e.g., %H:%M):",
        'invalid_format': "Invalid time format",
        'timezone': "Timezone",
        'enter_timezone': "Enter the timezone (e.g., Europe/London):",
        'unknown_timezone': "Unknown timezone",
        'sleep': "Sleep",
        'restart': "Restart",
        'shutdown_pc': "Shutdown PC",
        'restart_launcher': "Restart launcher",
        'exit_launcher': "Exit launcher",
        'sleep_confirm': "Are you sure you want to put the system to sleep?",
        'restart_confirm': "Are you sure you want to restart the system?",
        'shutdown_confirm': "Are you sure you want to shut down the system?",
        'could_not_launch_app': "Could not launch application:",
        'file_not_found': "File not found:",
        'no_videos_found': "No videos found",
        'add_videos': "Add videos to video folder",
        'select_multimedia_file': "Select a multimedia file",
        'multimedia_files': "Multimedia files",
        'launch_discover_error': "plasma-discover not found. Install with: sudo apt install plasma-discover",
        'change_language': "Change Language",
        'language_setting': "Language",
        'choose_language': "Choose Language",
        'language_changed': "Language changed to %s! Restart the app to see changes.",
        'download_language': "Download Language from GitHub",
        'enter_language_code': "Enter the language code to download (e.g., pl, de):",
        'language_download_fail': "Error downloading language file %s. Check if it exists in the repository.",
        'language_load_fail': "Error loading downloaded language file.",
        'language_download_success': "Language %s downloaded and loaded! Restart the app to see changes.",
    }
}
# Folder, gdzie będą zapisywane pobrane pliki językowe
LANG_DIR = os.path.expanduser('~/.tv_launcher_lang')


class MediaPlayer:
    # Zmodyfikowano __init__ aby przyjmował funkcję tłumaczenia (tr_func)
    def __init__(self, root, on_back_callback, tr_func):
        self.root = root
        self.on_back_callback = on_back_callback
        self.tr = tr_func # Przypisanie funkcji tłumaczącej
        self.setup_ui()

    def setup_ui(self):
        self.player_window = tk.Toplevel(self.root)
        self.player_window.title(self.tr('vlc_player')) # Użycie tłumaczenia
        self.player_window.attributes('-fullscreen', True)
        self.player_window.configure(bg='black')

        # Bind Escape to leave
        self.player_window.bind('<Escape>', lambda e: self.on_back())

        # player controls
        self.control_frame = ttk.Frame(self.player_window, style='Dark.TFrame')
        self.control_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(
            self.control_frame,
            text=self.tr('back'), # Użycie tłumaczenia
            style='Dark.TButton',
            command=self.on_back
        ).pack(side='left', padx=5)

        self.status_label = ttk.Label(
            self.control_frame,
            text=self.tr('vlc_player'), # Użycie tłumaczenia
            font=('Arial', 12),
            foreground='white',
            background='#222222'
        )
        self.status_label.pack(side='left', padx=10, expand=True)

        self.current_file = None
        self.process = None

    def on_back(self):
        self.stop_playback()
        self.player_window.destroy()
        self.on_back_callback()

    def open_file(self, file_path):
        if file_path:
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.status_label.config(text=f"{self.tr('vlc_playing')} {filename}") # Użycie tłumaczenia
            self.start_playback()

    def start_playback(self):
        if not self.current_file:
            return

        try:
            # Use VLC for playback with fullscreen
            self.process = subprocess.Popen(
                ['vlc', '--fullscreen', '--play-and-exit', self.current_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            messagebox.showerror(self.tr('error'), self.tr('vlc_not_found')) # Użycie tłumaczenia
        except Exception as e:
            messagebox.showerror(self.tr('error'), f"{self.tr('could_not_play')} {str(e)}") # Użycie tłumaczenia

    def stop_playback(self):
        if self.process:
            self.process.terminate()
            self.process = None

class StreamingLauncher:
    CONFIG_FILE = os.path.expanduser('~/.streaming_launcher_config.json')
    GITHUB_REPO = "Kubixonon/tv-launcher-for-linux"  # Główny kod
    GITHUB_LANG_REPO = "Kubixonon/tv-launcher-language"
    LANG_FILE_FORMAT = "lang_%s.json"

    def __init__(self, root):
        self.root = root
        self.selected_section = 0
        self.selected_index = 0
        self.apps_offset = 0
        self.movies_offset = 0
        self.visible_apps = 8
        self.visible_movies = 8
        self.media_player = None
        self.icons = {}
        self.custom_background = None
        self.translations = {} # Słownik na załadowane tłumaczenia

        # Initialize lists to avoid AttributeError
        self.platform_buttons = []
        self.app_buttons = []
        self.movie_buttons = []

        # Load configuration
        self.config = self.load_config()
        self.load_translations() # Nowa metoda ładowania tłumaczeń
        self.check_dependencies
        self.load_icons()
        self.setup_ui()
        self.setup_keyboard_controls()
        self.update_clock()
        self.load_apps()
        self.load_media()

    # --- METODY DO OBSŁUGI JĘZYKA ---

    def tr(self, key):
        """Pobiera przetłumaczony tekst na podstawie klucza"""
        lang = self.config.get('language', 'en') # Domyślnie 'en'

        # 1. Sprawdź aktualny język
        if lang in self.translations and key in self.translations[lang]:
            return self.translations[lang][key]
        # 2. Fallback na domyślny 'en'
        if 'en' in self.translations and key in self.translations['en']:
            return self.translations['en'][key]
        # 3. Fallback na sam klucz
        return key

    def load_translations(self):
        """Ładuje wbudowane i pobrane tłumaczenia"""
        # Wczytaj domyślne (angielskie)
        self.translations = DEFAULT_TRANSLATIONS.copy()

        # Upewnij się, że katalog językowy istnieje
        os.makedirs(LANG_DIR, exist_ok=True)

        # Wczytaj pobrane języki z lokalnego folderu
        for filename in os.listdir(LANG_DIR):
            if filename.startswith('lang_') and filename.endswith('.json'):
                lang_code = filename[5:-5]
                try:
                    with open(os.path.join(LANG_DIR, filename), 'r', encoding='utf-8') as f:
                        downloaded_lang = json.load(f)
                        self.translations[lang_code] = downloaded_lang
                except Exception as e:
                    print(f"Błąd wczytywania pobranego języka {lang_code}: {e}")

    def download_and_load_language(self, lang_code):
        """Pobiera plik językowy z GitHub i zapisuje go lokalnie"""
        raw_url = f"https://raw.githubusercontent.com/{self.GITHUB_LANG_REPO}/main/{self.LANG_FILE_FORMAT % lang_code}"
        lang_filename = self.LANG_FILE_FORMAT % lang_code
        local_path = os.path.join(LANG_DIR, lang_filename)

        try:
            response = requests.get(raw_url, timeout=30)
            if response.status_code != 200:
                messagebox.showerror(self.tr('error'), self.tr('language_download_fail') % lang_code)
                return False

            # Zapisz plik
            with open(local_path, 'w', encoding='utf-8') as f:
                # Użyj response.json() do zapisu, co zapewni, że to poprawny JSON
                json.dump(response.json(), f, indent=4, ensure_ascii=False)

            # Wczytaj do aplikacji
            self.translations[lang_code] = response.json()

            messagebox.showinfo(self.tr('success'), self.tr('language_download_success') % lang_code)
            return True

        except requests.exceptions.Timeout:
            messagebox.showerror(self.tr('error'), f"Timeout: {self.tr('language_download_fail') % lang_code}")
            return False
        except Exception as e:
            messagebox.showerror(self.tr('error'), f"{self.tr('language_load_fail')} {str(e)}")
            return False

    def change_language(self):
        """Okno dialogowe do zmiany lub pobierania języka"""

        lang_window = tk.Toplevel(self.root)
        lang_window.title(self.tr('choose_language'))
        lang_window.geometry("350x250")
        lang_window.transient(self.root)
        lang_window.grab_set()

        ttk.Label(lang_window, text=self.tr('language_setting')).pack(pady=5)

        # Lista dostępnych języków (wbudowane + pobrane)
        available_langs = sorted(list(self.translations.keys()))

        lang_var = tk.StringVar(value=self.config.get('language', 'en'))
        lang_combo = ttk.Combobox(lang_window, textvariable=lang_var, values=available_langs)
        lang_combo.pack(pady=5)

        def apply_language():
            selected_lang = lang_var.get()
            if selected_lang in self.translations:
                self.config['language'] = selected_lang
                self.save_config()
                lang_window.destroy()
                messagebox.showinfo(self.tr('success'), self.tr('language_changed') % selected_lang)
            else:
                messagebox.showerror(self.tr('error'), "Unknown language code.")

        def download_language_prompt():
            code = simpledialog.askstring(
                self.tr('download_language'),
                self.tr('enter_language_code'),
                parent=lang_window
            )
            if code and code not in self.translations:
                lang_window.grab_release() # Zwolnij grab, aby pobieranie działało
                lang_window.destroy()

                if self.download_and_load_language(code):
                    self.config['language'] = code # Ustawia nowo pobrany jako aktywny
                    self.save_config()
                    self.restart_application() # Wymagany restart, aby UI w pełni się odświeżył

        ttk.Button(lang_window, text=self.tr('apply'), command=apply_language).pack(pady=10)

        ttk.Separator(lang_window, orient='horizontal').pack(fill='x', padx=10, pady=5)

        # Zakładka do pobierania języków z GitHub
        ttk.Button(lang_window, text=self.tr('download_language'), command=download_language_prompt).pack(pady=5)

    def create_language_menu(self, parent_menu):
        """Tworzy podmenu do zmiany języka dla show_settings"""
        lang_menu = Menu(parent_menu, tearoff=0, bg='#333333', fg='white')
        lang_menu.add_command(label=self.tr('choose_language'), command=self.change_language)
        return lang_menu

    # --- KONIEC METOD DO OBSŁUGI JĘZYKA ---

    def load_config(self):
        default_config = {
            'language': 'en', # <--- Domyślny język ustawiony na EN
            'time_format': "%H:%M | %d.%m.%Y        TV Launcher",
            'timezone': 'Europe/London',
            'theme': {
                'background': "#747474",
                'foreground': 'white',
                'button_bg': "#636363",
                'button_active': '#333333',
                'accent_color': '#FF5500',
                'font_family': 'Arial',
                'font_size': 12
            },
            'github_repo': self.GITHUB_REPO,
            'customization': {
                'background_image': '',
                'background_blur': 0,
                'background_brightness': 1.0,
                'show_clock': True,
                'show_apps': True,
                'show_movies': True,
                'animation_effects': True,
                'button_style': 'rounded'
            },
            'media_settings': {
                'video_folder': os.path.expanduser('~/Videos'),
                'auto_play': True,
                'default_player': 'vlc'
            }
        }

        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    loaded_config = json.load(f)
                    # Ensure all keys exist by merging with default config
                    self.merge_configs(loaded_config, default_config)
                    loaded_config['github_repo'] = self.GITHUB_REPO
                    return loaded_config
        except Exception as e:
            print(f"Error loading config: {e}")

        return default_config

    def merge_configs(self, loaded_config, default_config):
        """Recursively merge loaded config with default config"""
        for key, value in default_config.items():
            if key not in loaded_config:
                loaded_config[key] = value
            elif isinstance(value, dict) and isinstance(loaded_config[key], dict):
                self.merge_configs(loaded_config[key], value)

    def save_config(self):
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def load_icons(self):
        # Basic icons (in reality, they should be loaded from files)
        self.icons = {
            'netflix': self.create_icon("#E50914"),
            'youtube': self.create_icon("#FF0000"),
            'prime': self.create_icon("#00A8E1"),
            'disnay': self.create_icon("#1A6565"),
            'hbo': self.create_icon("#2C0181"),
            'discover': self.create_icon("#3DAEE9"),
            'media': self.create_icon("#FFA500"),
            'mp3': self.create_icon("#1DB954"),
            'mp4': self.create_icon("#FF5500"),
            'app': self.create_icon("#888888"),
            'update': self.create_icon("#4CAF50"),
            'settings': self.create_icon("#9C27B0"),
            'customize': self.create_icon("#E91E63")
        }

    def create_icon(self, color, size=32):
        """Creates a simple icon (in reality, should be loaded from files)"""
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((0, 0, size-1, size-1), fill=color)
            return ImageTk.PhotoImage(img)
        except:
            return None
            
    def check_dependencies(self):
        # Check if VLC is installed
        self.has_vlc = self.check_command('vlc --version')
        if not self.has_vlc:
            messagebox.showwarning(
                self.tr('warning'), # Użycie tłumaczenia
                self.tr('vlc_playback_warning') # Użycie tłumaczenia
            )

    def check_command(self, cmd):
        try:
            subprocess.run(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except:
            return False

    def setup_ui(self):
        self.root.title(self.tr('app_title')) # Użycie tłumaczenia
        self.root.geometry("1280x720")
        
        # Apply background first
        self.apply_background()
        
        self.root.attributes('-fullscreen', True)

        # Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Style configuration - use get() with default values for safety
        bg = self.config['theme'].get('background', "#747474")
        fg = self.config['theme'].get('foreground', 'white')
        btn_bg = self.config['theme'].get('button_bg', "#636363")
        btn_active = self.config['theme'].get('button_active', '#333333')
        accent = self.config['theme'].get('accent_color', '#FF5500')
        font_family = self.config['theme'].get('font_family', 'Arial')
        font_size = self.config['theme'].get('font_size', 12)

        self.style.configure('Dark.TFrame', background=bg)
        self.style.configure('Dark.TButton',
                            foreground=fg,
                            background=btn_bg,
                            bordercolor='#333333',
                            lightcolor='#333333',
                            darkcolor='#333333',
                            padding=10,
                            font=(font_family, font_size))
        self.style.map('Dark.TButton',
                      background=[('active', btn_active)],
                      foreground=[('active', fg)])
        self.style.configure('Selected.TButton', background=accent)
        self.style.configure('Accent.TButton', background=accent, foreground='white')
        self.style.configure('Title.TLabel', font=(font_family, 18, 'bold'), foreground=accent)

        # Main container with some transparency for background
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=50, pady=20)

        # Platforms section
        if self.config['customization'].get('show_apps', True):
            self.platforms_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
            self.platforms_frame.pack(fill='x', pady=(0, 40))

            self.platforms = [
                {"name": "NETFLIX", "url": "https://www.netflix.com", "color": "#E50914", "icon": self.icons['netflix']},
                {"name": "YouTube", "url": "https://www.youtube.com/tv", "color": "#FF0000", "icon": self.icons['youtube']},
                {"name": "Hbo Max", "url": "https://www.hbomax.com", "color": "#2C0181", "icon": self.icons['hbo']},
                {"name": "Prime Video", "url": "https://www.primevideo.com", "color": "#00A8E1", "icon": self.icons['prime']},
                {"name": "Disnay+", "url": "https://www.disneyplus.com", "color": "#1A6565", "icon": self.icons['disnay']},
                {"name": self.tr("applications"), "url": "plasma-discover", "color": "#3DAEE9", "icon": self.icons['discover']},
                {"name": self.tr("vlc_player"), "url": "media_player", "color": "#FFA500", "icon": self.icons['media']}
            ]

            self.platform_buttons = []
            for i, platform in enumerate(self.platforms):
                btn = tk.Button(
                    self.platforms_frame,
                    text=f"  {platform['name']}",
                    font=(font_family, 14, 'bold' if i == 0 else 'normal'),
                    fg='white',
                    bg=platform["color"],
                    activeforeground='white',
                    activebackground=accent,
                    borderwidth=0,
                    padx=20,
                    pady=10,
                    image=platform["icon"],
                    compound='left',
                    command=lambda url=platform["url"]: self.launch_platform(url)
                )
                # Apply button style
                button_style = self.config['customization'].get('button_style', 'rounded')
                if button_style == 'rounded':
                    btn.config(relief='flat', bd=0, highlightthickness=0)
                elif button_style == 'modern':
                    btn.config(relief='raised', bd=2)
                
                btn.pack(side='left', padx=15)
                self.platform_buttons.append(btn)

        # "Apps" section
        if self.config['customization'].get('show_apps', True):
            self.apps_label_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
            self.apps_label_frame.pack(fill='x', pady=(0, 10))

            ttk.Label(
                self.apps_label_frame,
                text=self.tr('applications'), # Użycie tłumaczenia
                style='Title.TLabel',
                background=bg
            ).pack(side='left')

            self.apps_container = ttk.Frame(self.main_frame, style='Dark.TFrame')
            self.apps_container.pack(fill='x', pady=(0, 40))

            self.apps_frame = ttk.Frame(self.apps_container, style='Dark.TFrame')
            self.apps_frame.pack()

            self.app_buttons = []

        # Multimedia section
        if self.config['customization'].get('show_movies', True):
            self.movies_label_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
            self.movies_label_frame.pack(fill='x', pady=(0, 10))

            ttk.Label(
                self.movies_label_frame,
                text=self.tr('multimedia'), # Użycie tłumaczenia
                style='Title.TLabel',
                background=bg
            ).pack(side='left')

            self.movies_container = ttk.Frame(self.main_frame, style='Dark.TFrame')
            self.movies_container.pack(fill='both', expand=True)

            self.movies_frame = ttk.Frame(self.movies_container, style='Dark.TFrame')
            self.movies_frame.pack()

            self.movie_buttons = []

        # Bottom panel
        self.bottom_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.bottom_frame.pack(side='bottom', fill='x', padx=10, pady=5)

        if self.config['customization'].get('show_clock', True):
            self.clock_label = ttk.Label(
                self.bottom_frame,
                font=(font_family, 14),
                foreground=fg,
                background=bg
            )
            self.clock_label.pack(side='left')

        ttk.Button(
            self.bottom_frame,
            text=self.tr('settings'), # Użycie tłumaczenia
            style='Dark.TButton',
            image=self.icons['settings'],
            compound='left',
            command=self.show_settings
        ).pack(side='left', padx=10)

        ttk.Button(
            self.bottom_frame,
            text=self.tr('shutdown'), # Użycie tłumaczenia
            style='Dark.TButton',
            command=self.show_power_menu
        ).pack(side='right', padx=10)

        # Select the first button
        self.selected_section = 0
        self.selected_index = 0
        self.update_selection()

    def apply_background(self):
        """Apply custom background image or color"""
        bg_image_path = self.config['customization'].get('background_image', '')
        
        if bg_image_path and os.path.exists(bg_image_path):
            try:
                # Load and process background image
                bg_image = Image.open(bg_image_path)
                bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
                
                # Apply brightness
                brightness = self.config['customization'].get('background_brightness', 1.0)
                if brightness != 1.0:
                    enhancer = ImageEnhance.Brightness(bg_image)
                    bg_image = enhancer.enhance(brightness)
                
                # Apply blur if specified
                blur_radius = self.config['customization'].get('background_blur', 0)
                if blur_radius > 0:
                    bg_image = bg_image.filter(ImageFilter.GaussianBlur(blur_radius))
                
                self.background_photo = ImageTk.PhotoImage(bg_image)
                
                # Create background label
                self.background_label = tk.Label(self.root, image=self.background_photo)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.background_label.lower()  # Move to background
                
            except Exception as e:
                print(f"Error loading background image: {e}")
                # Fallback to color background
                self.root.configure(bg=self.config['theme'].get('background', "#747474"))
        else:
            # Use color background
            self.root.configure(bg=self.config['theme'].get('background', "#747474"))

    def show_settings(self):
        """Shows the settings menu"""
        menu = Menu(self.root, tearoff=0, bg='#333333', fg='white')

        # Język
        menu.add_cascade(label=self.tr('language_setting'), menu=self.create_language_menu(menu))

        # Clock settings
        time_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        time_menu.add_command(label=self.tr('time_format'), command=self.change_time_format)
        time_menu.add_command(label=self.tr('timezone'), command=self.change_timezone)
        menu.add_cascade(label=self.tr('time_format'), menu=time_menu)

        # Theme submenu
        theme_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        theme_menu.add_command(label=self.tr('change_bg_color'), command=self.change_background_color)
        theme_menu.add_command(label=self.tr('change_accent_color'), command=self.change_accent_color)
        theme_menu.add_command(label=self.tr('change_font'), command=self.change_font)
        theme_menu.add_separator()
        theme_menu.add_command(label=self.tr('reset_theme'), command=self.reset_theme)
        menu.add_cascade(label=self.tr('theme'), menu=theme_menu)
        
        # Background submenu
        bg_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        bg_menu.add_command(label=self.tr('set_bg_image'), command=self.set_background_image)
        bg_menu.add_command(label=self.tr('remove_bg_image'), command=self.remove_background_image)
        bg_menu.add_command(label=self.tr('bg_brightness_opt'), command=self.set_background_brightness)
        bg_menu.add_command(label=self.tr('bg_blur_opt'), command=self.set_background_blur)
        menu.add_cascade(label=self.tr('background'), menu=bg_menu)
        
        # Layout submenu
        layout_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        layout_menu.add_command(label=self.tr('toggle_clock'), command=lambda: self.toggle_setting('show_clock'))
        layout_menu.add_command(label=self.tr('toggle_apps'), command=lambda: self.toggle_setting('show_apps'))
        layout_menu.add_command(label=self.tr('toggle_movies'), command=lambda: self.toggle_setting('show_movies'))
        layout_menu.add_separator()
        layout_menu.add_command(label=self.tr('button_style'), command=self.change_button_style)
        menu.add_cascade(label=self.tr('layout'), menu=layout_menu)
        
        # Media submenu
        media_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        media_menu.add_command(label=self.tr('change_video_folder'), command=self.change_video_folder)
        media_menu.add_command(label=self.tr('rescan_media'), command=self.rescan_media)
        menu.add_cascade(label=self.tr('media'), menu=media_menu)
        
        menu.add_separator()
        menu.add_command(label=self.tr('update_app'), command=self.simple_update)
        menu.add_separator()
        menu.add_command(label=self.tr('close'), command=lambda: None)

        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def change_background_color(self):
        """Change background color"""
        color = colorchooser.askcolor(
            title=self.tr('change_bg_color'), # Użycie tłumaczenia
            initialcolor=self.config['theme'].get('background', "#747474")
        )
        if color[1]:
            self.config['theme']['background'] = color[1]
            self.save_config()
            messagebox.showinfo(self.tr('success'), self.tr('bg_color_changed')) # Użycie tłumaczenia

    def change_accent_color(self):
        """Change accent color"""
        color = colorchooser.askcolor(
            title=self.tr('change_accent_color'), # Użycie tłumaczenia
            initialcolor=self.config['theme'].get('accent_color', '#FF5500')
        )
        if color[1]:
            self.config['theme']['accent_color'] = color[1]
            self.save_config()
            messagebox.showinfo(self.tr('success'), self.tr('accent_color_changed')) # Użycie tłumaczenia

    def change_font(self):
        """Change font family and size"""
        font_window = tk.Toplevel(self.root)
        font_window.title(self.tr('change_font')) # Użycie tłumaczenia
        font_window.geometry("300x200")
        font_window.transient(self.root)
        font_window.grab_set()
        
        ttk.Label(font_window, text=self.tr('font_family')).pack(pady=5) # Użycie tłumaczenia
        font_family_var = tk.StringVar(value=self.config['theme'].get('font_family', 'Arial'))
        font_family_combo = ttk.Combobox(font_window, textvariable=font_family_var, 
                                       values=['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana'])
        font_family_combo.pack(pady=5)
        
        ttk.Label(font_window, text=self.tr('font_size')).pack(pady=5) # Użycie tłumaczenia
        font_size_var = tk.StringVar(value=str(self.config['theme'].get('font_size', 12)))
        font_size_combo = ttk.Combobox(font_window, textvariable=font_size_var, 
                                     values=['10', '12', '14', '16', '18', '20'])
        font_size_combo.pack(pady=5)
        
        def apply_font():
            self.config['theme']['font_family'] = font_family_var.get()
            self.config['theme']['font_size'] = int(font_size_var.get())
            self.save_config()
            font_window.destroy()
            messagebox.showinfo(self.tr('success'), self.tr('font_changed')) # Użycie tłumaczenia
        
        ttk.Button(font_window, text=self.tr('apply'), command=apply_font).pack(pady=10) # Użycie tłumaczenia

    def reset_theme(self):
        """Reset theme to default"""
        if messagebox.askyesno(self.tr('confirm'), self.tr('reset_theme_confirm')): # Użycie tłumaczenia
            default_theme = {
                'background': "#747474",
                'foreground': 'white',
                'button_bg': "#636363",
                'button_active': '#333333',
                'accent_color': '#FF5500',
                'font_family': 'Arial',
                'font_size': 12
            }
            self.config['theme'] = default_theme
            self.config['customization']['background_image'] = ''
            self.save_config()
            messagebox.showinfo(self.tr('success'), self.tr('theme_reset')) # Użycie tłumaczenia

    def set_background_image(self):
        """Set custom background image"""
        file_path = filedialog.askopenfilename(
            title=self.tr('select_bg_image'), # Użycie tłumaczenia
            filetypes=(
                (self.tr('image_files'), "*.jpg *.jpeg *.png *.bmp *.gif"), # Użycie tłumaczenia
                ("All files", "*.*")
            )
        )
        if file_path:
            self.config['customization']['background_image'] = file_path
            self.save_config()
            messagebox.showinfo(self.tr('success'), self.tr('bg_image_set')) # Użycie tłumaczenia

    def remove_background_image(self):
        """Remove background image"""
        self.config['customization']['background_image'] = ''
        self.save_config()
        messagebox.showinfo(self.tr('success'), self.tr('bg_image_removed')) # Użycie tłumaczenia

    def set_background_brightness(self):
        """Set background brightness"""
        brightness = simpledialog.askfloat(
            self.tr('bg_brightness'), # Użycie tłumaczenia
            self.tr('enter_brightness'), # Użycie tłumaczenia
            initialvalue=self.config['customization'].get('background_brightness', 1.0),
            minvalue=0.1,
            maxvalue=2.0
        )
        if brightness:
            self.config['customization']['background_brightness'] = brightness
            self.save_config()
            messagebox.showinfo(self.tr('success'), self.tr('brightness_saved')) # Użycie tłumaczenia

    def set_background_blur(self):
        """Set background blur"""
        blur = simpledialog.askinteger(
            self.tr('bg_blur'), # Użycie tłumaczenia
            self.tr('enter_blur'), # Użycie tłumaczenia
            initialvalue=self.config['customization'].get('background_blur', 0),
            minvalue=0,
            maxvalue=20
        )
        if blur is not None:
            self.config['customization']['background_blur'] = blur
            self.save_config()
            messagebox.showinfo(self.tr('success'), self.tr('blur_saved')) # Użycie tłumaczenia

    def toggle_setting(self, setting):
        """Toggle boolean settings"""
        self.config['customization'][setting] = not self.config['customization'].get(setting, True)
        self.save_config()
        messagebox.showinfo(self.tr('success'), self.tr('setting_updated')) # Użycie tłumaczenia

    def change_button_style(self):
        """Change button style"""
        style_window = tk.Toplevel(self.root)
        style_window.title(self.tr('button_style')) # Użycie tłumaczenia
        style_window.geometry("250x150")
        style_window.transient(self.root)
        style_window.grab_set()
        
        style_var = tk.StringVar(value=self.config['customization'].get('button_style', 'rounded'))
        
        ttk.Radiobutton(style_window, text=self.tr('rounded'), variable=style_var, value="rounded").pack(pady=5) # Użycie tłumaczenia
        ttk.Radiobutton(style_window, text=self.tr('square'), variable=style_var, value="square").pack(pady=5) # Użycie tłumaczenia
        ttk.Radiobutton(style_window, text=self.tr('modern'), variable=style_var, value="modern").pack(pady=5) # Użycie tłumaczenia
        
        def apply_style():
            self.config['customization']['button_style'] = style_var.get()
            self.save_config()
            style_window.destroy()
            messagebox.showinfo(self.tr('success'), self.tr('style_changed')) # Użycie tłumaczenia
        
        ttk.Button(style_window, text=self.tr('apply'), command=apply_style).pack(pady=10) # Użycie tłumaczenia

    def change_video_folder(self):
        """Change video folder location"""
        folder = filedialog.askdirectory(title=self.tr('select_video_folder')) # Użycie tłumaczenia
        if folder:
            self.config['media_settings']['video_folder'] = folder
            self.save_config()
            self.load_media()  # Reload media with new folder
            messagebox.showinfo(self.tr('success'), f"{self.tr('folder_changed')} {folder}") # Użycie tłumaczenia

    def rescan_media(self):
        """Rescan media files"""
        self.load_media()
        messagebox.showinfo(self.tr('success'), self.tr('rescan_complete')) # Użycie tłumaczenia


    def simple_update(self):
        """Prosta aktualizacja - pobiera plik z GitHub i zamienia obecny"""
        try:
            # URL do surowego pliku na GitHub
            raw_url = f"https://raw.githubusercontent.com/{self.GITHUB_REPO}/main/smarttv.py" # Zakładamy, że plik ma nazwę smarttv.py
            
            if hasattr(self, 'clock_label'):
                self.clock_label.config(text=self.tr('downloading_update')) # Użycie tłumaczenia
            self.root.update()
            
            # Pobierz plik
            response = requests.get(raw_url, timeout=30)
            if response.status_code != 200:
                messagebox.showerror(self.tr('error'), f"{self.tr('download_failed')} {response.status_code}") # Użycie tłumaczenia
                self.update_clock()
                return
            
            # Zapisz do pliku tymczasowego
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py')
            temp_file.write(response.text)
            temp_file.close()
            
            if hasattr(self, 'clock_label'):
                self.clock_label.config(text=self.tr('installing_update')) # Użycie tłumaczenia
            self.root.update()
            
            # Skopiuj do obecnego pliku
            current_file = __file__  # Obecny plik
            shutil.copy2(temp_file.name, current_file)
            
            # Usuń plik tymczasowy
            os.unlink(temp_file.name)
            
            messagebox.showinfo(self.tr('success'), self.tr('update_complete')) # Użycie tłumaczenia
            self.restart_application()
            
        except Exception as e:
            messagebox.showerror(self.tr('error'), f"{self.tr('download_failed')} {str(e)}") # Użycie tłumaczenia
            self.update_clock()

    def restart_application(self):
        """Restartuje aplikację"""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def change_time_format(self):
        new_format = simpledialog.askstring(
            self.tr('time_format'), # Użycie tłumaczenia
            self.tr('enter_time_format'), # Użycie tłumaczenia
            parent=self.root,
            initialvalue=self.config.get('time_format', "%H:%M | %d.%m.%Y        TV Launcher")
        )

        if new_format:
            try:
                # Check if format is valid
                datetime.datetime.now().strftime(new_format)
                self.config['time_format'] = new_format
                self.save_config()
            except:
                messagebox.showerror(self.tr('error'), self.tr('invalid_format')) # Użycie tłumaczenia

    def change_timezone(self):
        zones = pytz.all_timezones
        zone = simpledialog.askstring(
            self.tr('timezone'), # Użycie tłumaczenia
            self.tr('enter_timezone'), # Użycie tłumaczenia
            parent=self.root,
            initialvalue=self.config.get('timezone', 'Europe/London')
        )

        if zone and zone in zones:
            self.config['timezone'] = zone
            self.save_config()
        elif zone:
            messagebox.showerror(self.tr('error'), self.tr('unknown_timezone')) # Użycie tłumaczenia

    def update_clock(self):
        """Updates the displayed time"""
        try:
            tz = pytz.timezone(self.config.get('timezone', 'Europe/London'))
            now = datetime.datetime.now(tz)
            time_str = now.strftime(self.config.get('time_format', "%H:%M | %d.%m.%Y  TV Launcher"))
            if hasattr(self, 'clock_label'):
                self.clock_label.config(text=time_str)
        except:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M | %d.%m.%Y  TV Launcher")
            if hasattr(self, 'clock_label'):
                self.clock_label.config(text=time_str)

        self.root.after(1000, self.update_clock)

    def show_power_menu(self):
        """Displays the power menu"""
        menu = Menu(self.root, tearoff=0, bg='#333333', fg='white')
        menu.add_command(label=self.tr('sleep'), command=self.sleep_pc) # Użycie tłumaczenia
        menu.add_command(label=self.tr('restart'), command=self.restart_pc) # Użycie tłumaczenia
        menu.add_command(label=self.tr('shutdown_pc'), command=self.shutdown_pc) # Użycie tłumaczenia
        menu.add_separator()
        menu.add_command(label=self.tr('restart_launcher'), command=self.restart_application) # Użycie tłumaczenia
        menu.add_command(label=self.tr('exit_launcher'), command=self.root.destroy) # Użycie tłumaczenia
        menu.add_separator()
        menu.add_command(label=self.tr('close'), command=lambda: None) # Użycie tłumaczenia
        menu.add_separator()

        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def sleep_pc(self):
        """Puts the computer to sleep"""
        if messagebox.askyesno(self.tr('sleep'), self.tr('sleep_confirm')): # Użycie tłumaczenia
            os.system("systemctl suspend")

    def restart_pc(self):
        """Restarts the computer"""
        if messagebox.askyesno(self.tr('restart'), self.tr('restart_confirm')): # Użycie tłumaczenia
            os.system("systemctl reboot")

    def shutdown_pc(self):
        """Shuts down the computer"""
        if messagebox.askyesno(self.tr('shutdown_pc'), self.tr('shutdown_confirm')): # Użycie tłumaczenia
            os.system("systemctl poweroff")

    def load_apps(self):
        app_dirs = [
            '/usr/share/applications',
            os.path.expanduser('~/.local/share/applications')
        ]

        self.all_apps = []
        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                for file in os.listdir(app_dir):
                    if file.endswith('.desktop'):
                        try:
                            with open(os.path.join(app_dir, file), 'r', encoding='utf-8') as f:
                                content = f.read()
                                if 'NoDisplay=true' not in content and 'Hidden=true' not in content:
                                    name = None
                                    exec_line = None
                                    icon_name = None
                                    for line in content.split('\n'):
                                        if line.startswith('Name='):
                                            name = line.split('=')[1]
                                        elif line.startswith('Exec='):
                                            exec_line = line.split('=')[1]
                                            exec_line = exec_line.split('%')[0].strip()
                                            if exec_line.startswith('"') and exec_line.endswith('"'):
                                                exec_line = exec_line[1:-1]
                                        elif line.startswith('Icon='):
                                            icon_name = line.split('=')[1]

                                    if name and exec_line:
                                        self.all_apps.append({
                                            "name": name,
                                            "exec": exec_line,
                                            "file": os.path.join(app_dir, file),
                                            "icon": self.icons['app']  # Placeholder icon
                                        })
                        except Exception as e:
                            print(f"Error loading {file}: {str(e)}")
                            continue

        self.all_apps.sort(key=lambda x: x["name"])
        if hasattr(self, 'apps_frame'):
            self.update_apps_display()


    def update_apps_display(self):
        if not hasattr(self, 'apps_frame'):
            return
            
        for widget in self.apps_frame.winfo_children():
            widget.destroy()

        self.app_buttons = []

        apps_to_show = self.all_apps[self.apps_offset:self.apps_offset + self.visible_apps]

        for i, app in enumerate(apps_to_show):
            btn = ttk.Button(
                self.apps_frame,
                text=f"  {app['name']}",
                style='Dark.TButton',
                image=app.get('icon', self.icons['app']),
                compound='left',
                command=lambda a=app: self.launch_app(a)
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5, sticky='ew')
            self.app_buttons.append(btn)

    def launch_app(self, app):
        try:
            try:
                subprocess.Popen(["gtk-launch", os.path.basename(app["file"])])
                return
            except:
                pass

            try:
                subprocess.Popen(['bash', '-c', app["exec"]])
                return
            except Exception as e:
                print(f"Error launching: {str(e)}")

            try:
                subprocess.Popen(["xdg-open", app["file"]])
                return
            except:
                pass

            messagebox.showerror(self.tr('error'), f"{self.tr('could_not_launch_app')} {app['name']}") # Użycie tłumaczenia
        except Exception as e:
            messagebox.showerror(self.tr('error'), f"{self.tr('could_not_launch_app')} {str(e)}") # Użycie tłumaczenia

    def load_media(self):
        """Wczytuje filmy z folderu wideo"""
        self.media_files = []
        
        # Sprawdź różne możliwe lokalizacje folderu Wideo
        video_dirs = [
            self.config['media_settings'].get('video_folder', os.path.expanduser('~/Videos')),
            os.path.expanduser('~/Videos'),
            os.path.expanduser('~/videos')
        ]
        
        found_videos = False
        
        for video_dir in video_dirs:
            if os.path.exists(video_dir) and os.path.isdir(video_dir):
                print(f"Searching for videos in: {video_dir}")
                found_videos = self.scan_video_directory(video_dir)
                if found_videos:
                    break
        
        if not found_videos:
            # Jeśli nie znaleziono żadnych filmów, pokaż przykładowe
            self.media_files = [
                {"name": self.tr('no_videos_found'), "path": "", "icon": self.icons['mp4']}, # Użycie tłumaczenia
                {"name": self.tr('add_videos'), "path": "", "icon": self.icons['mp4']} # Użycie tłumaczenia
            ]
        
        if hasattr(self, 'movies_frame'):
            self.update_movies_display()

    def scan_video_directory(self, directory):
        """Skanuje katalog w poszukiwaniu filmów"""
        video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'}
        found_files = False
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext in video_extensions:
                        file_path = os.path.join(root, file)
                        file_name = os.path.splitext(file)[0]
                        
                        self.media_files.append({
                            "name": file_name,
                            "path": file_path,
                            "icon": self.icons['mp4']
                        })
                        found_files = True
                        print(f"Found video: {file_name}")
            
            # Sortuj alfabetycznie
            self.media_files.sort(key=lambda x: x["name"])
            
        except Exception as e:
            print(f"Error scanning directory {directory}: {str(e)}")
        
        return found_files


    def update_movies_display(self):
        if not hasattr(self, 'movies_frame'):
            return
            
        for widget in self.movies_frame.winfo_children():
            widget.destroy()

        self.movie_buttons = []

        movies_to_show = self.media_files[self.movies_offset:self.movies_offset + self.visible_movies]

        for i, media in enumerate(movies_to_show):
            btn = ttk.Button(
                self.movies_frame,
                text=f"  {media['name']}",
                style='Dark.TButton',
                image=media.get('icon', self.icons['mp4']),
                compound='left',
                command=lambda m=media: self.select_movie(m)
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5, sticky='ew')
            self.movie_buttons.append(btn)

    def select_movie(self, media):
        """Odtwarza wybrany film w VLC na fullscreen"""
        if media.get("path") and os.path.exists(media["path"]):
            if not self.media_player or not tk.Toplevel.winfo_exists(self.media_player.player_window):
                # Przekazanie self.tr
                self.media_player = MediaPlayer(self.root, self.on_media_player_close, self.tr)
            self.media_player.open_file(media["path"])
        elif media.get("path"):
            messagebox.showerror(self.tr('error'), f"{self.tr('file_not_found')} {media['path']}") # Użycie tłumaczenia
        else:
            messagebox.showinfo("Info", media['name'])

    def on_media_player_close(self):
        """Callback triggered after the player closes"""
        self.media_player = None
        self.root.focus_force()

    def launch_platform(self, url):
        if url == "plasma-discover":
            self.launch_discover()
        elif url == "media_player":
            if not self.media_player or not tk.Toplevel.winfo_exists(self.media_player.player_window):
                # Przekazanie self.tr
                self.media_player = MediaPlayer(self.root, self.on_media_player_close, self.tr)
                # Open file dialog
                file_path = filedialog.askopenfilename(
                    title=self.tr('select_multimedia_file'), # Użycie tłumaczenia
                    filetypes=(
                        (self.tr('multimedia_files'), "*.mp4 *.avi *.mkv *.mov *.mp3 *.flac *.wav"), # Użycie tłumaczenia
                        ("All files", "*.*")
                    )
                )
                if file_path:
                    self.media_player.open_file(file_path)
            else:
                self.media_player.player_window.lift()
        elif url:
            try:
                window = webview.create_window(
                    'Streaming',
                    url,
                    width=1280,
                    height=720,
                    fullscreen=True,
                    frameless=False
                )
                webview.start()
            except Exception as e:
                messagebox.showerror(self.tr('error'), f"{self.tr('could_not_launch_app')}: {str(e)}") # Użycie tłumaczenia

    def launch_discover(self):
        try:
            # Use plasma-discover instead of discover
            subprocess.Popen(['plasma-discover'])
        except FileNotFoundError:
            messagebox.showerror(self.tr('error'), self.tr('launch_discover_error')) # Użycie tłumaczenia
        except Exception as e:
            messagebox.showerror(self.tr('error'), f"{self.tr('could_not_launch_app')}: {str(e)}") # Użycie tłumaczenia

    def setup_keyboard_controls(self):
        self.root.bind('<Left>', lambda e: self.move_selection(-1))
        self.root.bind('<Right>', lambda e: self.move_selection(1))
        self.root.bind('<Up>', lambda e: self.move_section(-1))
        self.root.bind('<Down>', lambda e: self.move_section(1))
        self.root.bind('<Return>', lambda e: self.press_selected())
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.bind('<Prior>', lambda e: self.scroll_up())  # Page Up
        self.root.bind('<Next>', lambda e: self.scroll_down())  # Page Down

    def move_section(self, direction):
        new_section = self.selected_section + direction
        if 0 <= new_section <= 2:  # 0-platforms, 1-apps, 2-movies
            self.selected_section = new_section
            self.selected_index = 0
            self.update_selection()

    def move_selection(self, direction):
        max_index = 0
        if self.selected_section == 0:
            max_index = len(self.platform_buttons) - 1
        elif self.selected_section == 1:
            if hasattr(self, 'app_buttons'):
                max_index = min(self.visible_apps, len(self.all_apps)) - 1
            else:
                max_index = 0
        elif self.selected_section == 2:
            if hasattr(self, 'movie_buttons'):
                max_index = min(self.visible_movies, len(self.media_files)) - 1
            else:
                max_index = 0

        new_index = self.selected_index + direction
        if 0 <= new_index <= max_index:
            self.selected_index = new_index
            self.update_selection()
        elif direction > 0 and self.selected_section == 1 and (self.apps_offset + self.visible_apps) < len(self.all_apps):
            self.apps_offset += 1
            if hasattr(self, 'apps_frame'):
                self.update_apps_display()
            self.update_selection()
        elif direction < 0 and self.selected_section == 1 and self.apps_offset > 0:
            self.apps_offset -= 1
            if hasattr(self, 'apps_frame'):
                self.update_apps_display()
            self.update_selection()
        elif direction > 0 and self.selected_section == 2 and (self.movies_offset + self.visible_movies) < len(self.media_files):
            self.movies_offset += 1
            if hasattr(self, 'movies_frame'):
                self.update_movies_display()
            self.update_selection()
        elif direction < 0 and self.selected_section == 2 and self.movies_offset > 0:
            self.movies_offset -= 1
            if hasattr(self, 'movies_frame'):
                self.update_movies_display()
            self.update_selection()

    def scroll_up(self):
        if self.selected_section == 1 and self.apps_offset > 0:
            self.apps_offset -= 1
            if hasattr(self, 'apps_frame'):
                self.update_apps_display()
            self.update_selection()
        elif self.selected_section == 2 and self.movies_offset > 0:
            self.movies_offset -= 1
            if hasattr(self, 'movies_frame'):
                self.update_movies_display()
            self.update_selection()

    def scroll_down(self):
        if self.selected_section == 1 and (self.apps_offset + self.visible_apps) < len(self.all_apps):
            self.apps_offset += 1
            if hasattr(self, 'apps_frame'):
                self.update_apps_display()
            self.update_selection()
        elif self.selected_section == 2 and (self.movies_offset + self.visible_movies) < len(self.media_files):
            self.movies_offset += 1
            if hasattr(self, 'movies_frame'):
                self.update_movies_display()
            self.update_selection()

    def update_selection(self):
        # Platform buttons
        for btn in self.platform_buttons:
            # Użycie oryginalnych kolorów dla nieaktywnych
            index = self.platform_buttons.index(btn)
            btn.config(bg=self.platforms[index]["color"], font=('Arial', 14, 'normal'), fg='white')

        # App buttons
        for btn in self.app_buttons:
            btn.config(style='Dark.TButton')

        # Movie buttons
        for btn in self.movie_buttons:
            btn.config(style='Dark.TButton')

        if self.selected_section == 0 and self.platform_buttons:
            # Akcentowanie przycisku platformy
            self.platform_buttons[self.selected_index].config(bg='white', fg='black')
            self.platform_buttons[self.selected_index].focus_set()
        elif self.selected_section == 1 and self.app_buttons:
            self.app_buttons[self.selected_index].config(style='Selected.TButton')
            self.app_buttons[self.selected_index].focus_set()
        elif self.selected_section == 2 and self.movie_buttons:
            self.movie_buttons[self.selected_index].config(style='Selected.TButton')
            self.movie_buttons[self.selected_index].focus_set()

    def press_selected(self):
        if self.selected_section == 0 and self.platform_buttons:
            self.platform_buttons[self.selected_index].invoke()
        elif self.selected_section == 1 and self.app_buttons:
            self.app_buttons[self.selected_index].invoke()
        elif self.selected_section == 2 and self.movie_buttons:
            self.movie_buttons[self.selected_index].invoke()

if __name__ == "__main__":
    root = tk.Tk()

    # Create button styles
    style = ttk.Style()
    # Zostawiamy styl Selected.TButton, ale kolor będzie brany z config.accent_color
    style.configure('Selected.TButton', background='#FF5500') 

    app = StreamingLauncher(root)
    root.mainloop()
