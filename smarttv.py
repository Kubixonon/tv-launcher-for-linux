#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, Menu, simpledialog, filedialog, colorchooser
import os
import subprocess
import datetime
import webview
import sys
import json
import pytz
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
import requests
import tempfile
import shutil

class MediaPlayer:
    def __init__(self, root, on_back_callback):
        self.root = root
        self.on_back_callback = on_back_callback
        self.setup_ui()

    def setup_ui(self):
        self.player_window = tk.Toplevel(self.root)
        self.player_window.title("VLC Player")
        self.player_window.attributes('-fullscreen', True)
        self.player_window.configure(bg='black')

        # Bind Escape to leave
        self.player_window.bind('<Escape>', lambda e: self.on_back())

        # player controls
        self.control_frame = ttk.Frame(self.player_window, style='Dark.TFrame')
        self.control_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(
            self.control_frame,
            text="Back",
            style='Dark.TButton',
            command=self.on_back
        ).pack(side='left', padx=5)

        self.status_label = ttk.Label(
            self.control_frame,
            text="VLC Player",
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
            self.status_label.config(text=f"Playing: {filename}")
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
            messagebox.showerror("Error", "VLC not found. Install it with 'sudo apt install vlc'")
        except Exception as e:
            messagebox.showerror("Error", f"Could not play file: {str(e)}")

    def stop_playback(self):
        if self.process:
            self.process.terminate()
            self.process = None

class StreamingLauncher:
    CONFIG_FILE = os.path.expanduser('~/.streaming_launcher_config.json')
    # ZASZYTE REPOZYTORIUM GITHUB
    GITHUB_REPO = "Kubixonon/tv-launcher-for-linux"  # Format: username/reponame

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

        # Initialize lists to avoid AttributeError
        self.platform_buttons = []
        self.app_buttons = []
        self.movie_buttons = []

        # Load configuration
        self.config = self.load_config()
        self.check_dependencies()
        self.load_icons()
        self.setup_ui()
        self.setup_keyboard_controls()
        self.update_clock()
        self.load_apps()
        self.load_media()

    def load_config(self):
        default_config = {
            'time_format': "%H:%M | %d.%m.%Y        TV Launcher",
            'timezone': 'Europe/Warsaw',
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
                'video_folder': '/Wideo',
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
                "Warning",
                "VLC not found. File playback may not work.\n"
                "Install with: sudo apt install vlc"
            )

    def check_command(self, cmd):
        try:
            subprocess.run(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except:
            return False

    def setup_ui(self):
        self.root.title("Streaming Launcher")
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
                {"name": "Discover", "url": "plasma-discover", "color": "#3DAEE9", "icon": self.icons['discover']},
                {"name": "Media Player", "url": "media_player", "color": "#FFA500", "icon": self.icons['media']}
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
                text="Applications",
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
                text="Multimedia",
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
            text="Settings",
            style='Dark.TButton',
            image=self.icons['settings'],
            compound='left',
            command=self.show_settings
        ).pack(side='left', padx=10)

        # Dodaj przycisk customizacji
        ttk.Button(
            self.bottom_frame,
            text="Customize",
            style='Dark.TButton',
            image=self.icons['customize'],
            compound='left',
            command=self.show_customization_menu
        ).pack(side='left', padx=10)

        # Dodaj przycisk aktualizacji
        ttk.Button(
            self.bottom_frame,
            text="Update",
            style='Dark.TButton',
            image=self.icons['update'],
            compound='left',
            command=self.simple_update
        ).pack(side='left', padx=10)

        ttk.Button(
            self.bottom_frame,
            text="Shutdown",
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

    def show_customization_menu(self):
        """Show customization options"""
        menu = Menu(self.root, tearoff=0, bg='#333333', fg='white')
        
        # Theme submenu
        theme_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        theme_menu.add_command(label="Change Background Color", command=self.change_background_color)
        theme_menu.add_command(label="Change Accent Color", command=self.change_accent_color)
        theme_menu.add_command(label="Change Font", command=self.change_font)
        theme_menu.add_separator()
        theme_menu.add_command(label="Reset Theme", command=self.reset_theme)
        menu.add_cascade(label="Theme", menu=theme_menu)
        
        # Background submenu
        bg_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        #bg_menu.add_command(label="Set Background Image", command=self.set_background_image)
        #bg_menu.add_command(label="Remove Background Image", command=self.remove_background_image)
        bg_menu.add_command(label="Background Brightness", command=self.set_background_brightness)
        bg_menu.add_command(label="Background Blur", command=self.set_background_blur)
        menu.add_cascade(label="Background", menu=bg_menu)
        
        # Layout submenu
        layout_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        layout_menu.add_command(label="Toggle Clock", command=lambda: self.toggle_setting('show_clock'))
        layout_menu.add_command(label="Toggle Apps", command=lambda: self.toggle_setting('show_apps'))
        layout_menu.add_command(label="Toggle Movies", command=lambda: self.toggle_setting('show_movies'))
        layout_menu.add_separator()
        layout_menu.add_command(label="Button Style", command=self.change_button_style)
        menu.add_cascade(label="Layout", menu=layout_menu)
        
        # Media submenu
        media_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        media_menu.add_command(label="Change Video Folder", command=self.change_video_folder)
        media_menu.add_command(label="Rescan Media", command=self.rescan_media)
        menu.add_cascade(label="Media", menu=media_menu)
        
        menu.add_separator()
        menu.add_command(label="Close", command=lambda: None)

        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def change_background_color(self):
        """Change background color"""
        color = colorchooser.askcolor(
            title="Choose background color",
            initialcolor=self.config['theme'].get('background', "#747474")
        )
        if color[1]:
            self.config['theme']['background'] = color[1]
            self.save_config()
            messagebox.showinfo("Success", "Background color changed! Restart the app to see changes.")

    def change_accent_color(self):
        """Change accent color"""
        color = colorchooser.askcolor(
            title="Choose accent color",
            initialcolor=self.config['theme'].get('accent_color', '#FF5500')
        )
        if color[1]:
            self.config['theme']['accent_color'] = color[1]
            self.save_config()
            messagebox.showinfo("Success", "Accent color changed! Restart the app to see changes.")

    def change_font(self):
        """Change font family and size"""
        font_window = tk.Toplevel(self.root)
        font_window.title("Change Font")
        font_window.geometry("300x200")
        font_window.transient(self.root)
        font_window.grab_set()
        
        ttk.Label(font_window, text="Font Family:").pack(pady=5)
        font_family_var = tk.StringVar(value=self.config['theme'].get('font_family', 'Arial'))
        font_family_combo = ttk.Combobox(font_window, textvariable=font_family_var, 
                                       values=['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana'])
        font_family_combo.pack(pady=5)
        
        ttk.Label(font_window, text="Font Size:").pack(pady=5)
        font_size_var = tk.StringVar(value=str(self.config['theme'].get('font_size', 12)))
        font_size_combo = ttk.Combobox(font_window, textvariable=font_size_var, 
                                     values=['10', '12', '14', '16', '18', '20'])
        font_size_combo.pack(pady=5)
        
        def apply_font():
            self.config['theme']['font_family'] = font_family_var.get()
            self.config['theme']['font_size'] = int(font_size_var.get())
            self.save_config()
            font_window.destroy()
            messagebox.showinfo("Success", "Font changed! Restart the app to see changes.")
        
        ttk.Button(font_window, text="Apply", command=apply_font).pack(pady=10)

    def reset_theme(self):
        """Reset theme to default"""
        if messagebox.askyesno("Confirm", "Reset theme to default?"):
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
            messagebox.showinfo("Success", "Theme reset! Restart the app to see changes.")

    def set_background_image(self):
        """Set custom background image"""
        file_path = filedialog.askopenfilename(
            title="Select background image",
            filetypes=(
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            )
        )
        if file_path:
            self.config['customization']['background_image'] = file_path
            self.save_config()
            messagebox.showinfo("Success", "Background image set! Restart the app to see changes.")

    def remove_background_image(self):
        """Remove background image"""
        self.config['customization']['background_image'] = ''
        self.save_config()
        messagebox.showinfo("Success", "Background image removed! Restart the app to see changes.")

    def set_background_brightness(self):
        """Set background brightness"""
        brightness = simpledialog.askfloat(
            "Background Brightness",
            "Enter brightness value (0.1 - 2.0):",
            initialvalue=self.config['customization'].get('background_brightness', 1.0),
            minvalue=0.1,
            maxvalue=2.0
        )
        if brightness:
            self.config['customization']['background_brightness'] = brightness
            self.save_config()
            messagebox.showinfo("Success", "Brightness setting saved! Restart the app to see changes.")

    def set_background_blur(self):
        """Set background blur"""
        blur = simpledialog.askinteger(
            "Background Blur",
            "Enter blur radius (0-20):",
            initialvalue=self.config['customization'].get('background_blur', 0),
            minvalue=0,
            maxvalue=20
        )
        if blur is not None:
            self.config['customization']['background_blur'] = blur
            self.save_config()
            messagebox.showinfo("Success", "Blur setting saved! Restart the app to see changes.")

    def toggle_setting(self, setting):
        """Toggle boolean settings"""
        self.config['customization'][setting] = not self.config['customization'].get(setting, True)
        self.save_config()
        messagebox.showinfo("Success", f"Setting updated! Restart the app to see changes.")

    def change_button_style(self):
        """Change button style"""
        style_window = tk.Toplevel(self.root)
        style_window.title("Button Style")
        style_window.geometry("250x150")
        style_window.transient(self.root)
        style_window.grab_set()
        
        style_var = tk.StringVar(value=self.config['customization'].get('button_style', 'rounded'))
        
        ttk.Radiobutton(style_window, text="Rounded", variable=style_var, value="rounded").pack(pady=5)
        ttk.Radiobutton(style_window, text="Square", variable=style_var, value="square").pack(pady=5)
        ttk.Radiobutton(style_window, text="Modern", variable=style_var, value="modern").pack(pady=5)
        
        def apply_style():
            self.config['customization']['button_style'] = style_var.get()
            self.save_config()
            style_window.destroy()
            messagebox.showinfo("Success", "Button style changed! Restart the app to see changes.")
        
        ttk.Button(style_window, text="Apply", command=apply_style).pack(pady=10)

    def change_video_folder(self):
        """Change video folder location"""
        folder = filedialog.askdirectory(title="Select video folder")
        if folder:
            self.config['media_settings']['video_folder'] = folder
            self.save_config()
            self.load_media()  # Reload media with new folder
            messagebox.showinfo("Success", f"Video folder changed to: {folder}")

    def rescan_media(self):
        """Rescan media files"""
        self.load_media()
        messagebox.showinfo("Success", "Media library rescanned!")

    def show_settings(self):
        """Shows the settings menu"""
        menu = Menu(self.root, tearoff=0, bg='#333333', fg='white')

        # Clock settings
        time_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        time_menu.add_command(label="Time format", command=self.change_time_format)
        time_menu.add_command(label="Timezone", command=self.change_timezone)
        menu.add_cascade(label="Clock", menu=time_menu)

        menu.add_separator()
        menu.add_command(label="Update App", command=self.simple_update)
        menu.add_command(label="Close", command=lambda: None)

        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def simple_update(self):
        """Prosta aktualizacja - pobiera plik z GitHub i zamienia obecny"""
        try:
            # URL do surowego pliku na GitHub
            raw_url = f"https://raw.githubusercontent.com/{self.GITHUB_REPO}/main/launcherpy"
            
            if hasattr(self, 'clock_label'):
                self.clock_label.config(text="Downloading update...")
            self.root.update()
            
            # Pobierz plik
            response = requests.get(raw_url, timeout=30)
            if response.status_code != 200:
                messagebox.showerror("Error", f"Download failed: {response.status_code}")
                self.update_clock()
                return
            
            # Zapisz do pliku tymczasowego
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py')
            temp_file.write(response.text)
            temp_file.close()
            
            if hasattr(self, 'clock_label'):
                self.clock_label.config(text="Installing update...")
            self.root.update()
            
            # Skopiuj do obecnego pliku
            current_file = __file__  # Obecny plik
            shutil.copy2(temp_file.name, current_file)
            
            # Usuń plik tymczasowy
            os.unlink(temp_file.name)
            
            messagebox.showinfo("Success", "Update completed! The app will restart.")
            self.restart_application()
            
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")
            self.update_clock()

    def restart_application(self):
        """Restartuje aplikację"""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def change_time_format(self):
        new_format = simpledialog.askstring(
            "Time format",
            "Enter the time display format (e.g., %H:%M):\n\nAvailable formats:\n%H - hour (24h)\n%I - hour (12h)\n%M - minutes\n%S - seconds\n%p - AM/PM\n%d - day\n%m - month\n%Y - year",
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
                messagebox.showerror("Error", "Invalid time format")

    def change_timezone(self):
        zones = pytz.all_timezones
        zone = simpledialog.askstring(
            "Timezone",
            "Enter the timezone (e.g., Europe/Warsaw):",
            parent=self.root,
            initialvalue=self.config.get('timezone', 'Europe/Warsaw')
        )

        if zone and zone in zones:
            self.config['timezone'] = zone
            self.save_config()
        elif zone:
            messagebox.showerror("Error", "Unknown timezone")

    def update_clock(self):
        """Updates the displayed time"""
        try:
            tz = pytz.timezone(self.config.get('timezone', 'Europe/Warsaw'))
            now = datetime.datetime.now(tz)
            time_str = now.strftime(self.config.get('time_format', "%H:%M | %d.%m.%Y        TV Launcher"))
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
        menu.add_command(label="Sleep", command=self.sleep_pc)
        menu.add_command(label="Restart", command=self.restart_pc)
        menu.add_command(label="Shutdown", command=self.shutdown_pc)
        menu.add_separator()
        menu.add_command(label="Exit launcher", command=self.root.destroy)
        menu.add_command(label="Close menu", command=lambda: None)

        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def sleep_pc(self):
        """Puts the computer to sleep"""
        if messagebox.askyesno("Sleep", "Are you sure you want to put the system to sleep?"):
            os.system("systemctl suspend")

    def restart_pc(self):
        """Restarts the computer"""
        if messagebox.askyesno("Restart", "Are you sure you want to restart the system?"):
            os.system("systemctl reboot")

    def shutdown_pc(self):
        """Shuts down the computer"""
        if messagebox.askyesno("Shutdown", "Are you sure you want to shut down the system?"):
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

            messagebox.showerror("Error", f"Could not launch application: {app['name']}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch application: {str(e)}")

    def load_media(self):
        """Wczytuje prawdziwe filmy z folderu /Wideo/"""
        self.media_files = []
        
        # Sprawdź różne możliwe lokalizacje folderu Wideo
        video_dirs = [
            self.config['media_settings'].get('video_folder', '/Wideo'),
            '/Wideo',
            '/wideo',
            os.path.expanduser('~/Wideo'),
            os.path.expanduser('~/wideo'),
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
                {"name": "No videos found", "path": "", "icon": self.icons['mp4']},
                {"name": "Add videos to video folder", "path": "", "icon": self.icons['mp4']}
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
                self.media_player = MediaPlayer(self.root, self.on_media_player_close)
            self.media_player.open_file(media["path"])
        elif media.get("path"):
            messagebox.showerror("Error", f"File not found: {media['path']}")
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
                self.media_player = MediaPlayer(self.root, self.on_media_player_close)
                # Open file dialog
                file_path = filedialog.askopenfilename(
                    title="Select a multimedia file",
                    filetypes=(
                        ("Multimedia files", "*.mp4 *.avi *.mkv *.mov *.mp3 *.flac *.wav"),
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
                messagebox.showerror("Error", f"Could not launch: {str(e)}")

    def launch_discover(self):
        try:
            # Use plasma-discover instead of discover
            subprocess.Popen(['plasma-discover'])
        except FileNotFoundError:
            messagebox.showerror("Error", "plasma-discover not found. Install with: sudo apt install plasma-discover")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch Discover: {str(e)}")

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
            btn.config(bg=self.platforms[self.platform_buttons.index(btn)]["color"], font=('Arial', 14, 'normal'))

        # App buttons
        for btn in self.app_buttons:
            btn.config(style='Dark.TButton')

        # Movie buttons
        for btn in self.movie_buttons:
            btn.config(style='Dark.TButton')

        if self.selected_section == 0 and self.platform_buttons:
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
    style.configure('Selected.TButton', background='#555555')

    app = StreamingLauncher(root)
    root.mainloop()