#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, Menu, simpledialog, filedialog
import os
import subprocess
import datetime
import webview
import sys
import json
import pytz
from PIL import Image, ImageTk

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
            # Use VLC for playback
            self.process = subprocess.Popen(
                ['vlc', '--fullscreen', self.current_file],
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
                'button_active': '#333333'
            }
        }

        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass

        return default_config

    def save_config(self):
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except:
            pass

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
            'app': self.create_icon("#888888")
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
        self.root.configure(bg=self.config['theme']['background'])
        self.root.attributes('-fullscreen', True)

        # Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Style configuration
        bg = self.config['theme']['background']
        fg = self.config['theme']['foreground']
        btn_bg = self.config['theme']['button_bg']
        btn_active = self.config['theme']['button_active']

        self.style.configure('Dark.TFrame', background=bg)
        self.style.configure('Dark.TButton',
                            foreground=fg,
                            background=btn_bg,
                            bordercolor='#333333',
                            lightcolor='#333333',
                            darkcolor='#333333',
                            padding=10,
                            font=('Arial', 12))
        self.style.map('Dark.TButton',
                      background=[('active', btn_active)],
                      foreground=[('active', fg)])
        self.style.configure('Selected.TButton', background=btn_active)

        # Main container
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=50, pady=20)

        # Platforms section
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
                font=('Arial', 14, 'bold' if i == 0 else 'normal'),
                fg='white',
                bg=platform["color"],
                activeforeground='white',
                activebackground="#747474",
                borderwidth=0,
                padx=20,
                pady=10,
                image=platform["icon"],
                compound='left',
                command=lambda url=platform["url"]: self.launch_platform(url)
            )
            btn.pack(side='left', padx=15)
            self.platform_buttons.append(btn)

        # "Apps" section
        self.apps_label_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.apps_label_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(
            self.apps_label_frame,
            text="Applications",
            font=('Arial', 16, 'bold'),
            foreground='white',
            background=bg
        ).pack(side='left')

        self.apps_container = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.apps_container.pack(fill='x', pady=(0, 40))

        self.apps_frame = ttk.Frame(self.apps_container, style='Dark.TFrame')
        self.apps_frame.pack()

        self.app_buttons = []

        # Multimedia section
        self.movies_label_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.movies_label_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(
            self.movies_label_frame,
            text="Multimedia",
            font=('Arial', 16, 'bold'),
            foreground='white',
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

        self.clock_label = ttk.Label(
            self.bottom_frame,
            font=('Arial', 14),
            foreground='white',
            background=bg
        )
        self.clock_label.pack(side='left')

        ttk.Button(
            self.bottom_frame,
            text="Settings",
            style='Dark.TButton',
            command=self.show_settings
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

    def show_settings(self):
        """Shows the settings menu"""
        menu = Menu(self.root, tearoff=0, bg='#333333', fg='white')

        # Clock settings
        time_menu = Menu(menu, tearoff=0, bg='#333333', fg='white')
        time_menu.add_command(label="Time format", command=self.change_time_format)
        time_menu.add_command(label="Timezone", command=self.change_timezone)
        menu.add_cascade(label="Clock", menu=time_menu)

        menu.add_separator()
        menu.add_command(label="Close", command=lambda: None)

        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def change_time_format(self):
        new_format = simpledialog.askstring(
            "Time format",
            "Enter the time display format (e.g., %H:%M):\n\nAvailable formats:\n%H - hour (24h)\n%I - hour (12h)\n%M - minutes\n%S - seconds\n%p - AM/PM\n%d - day\n%m - month\n%Y - year",
            parent=self.root,
            initialvalue=self.config['time_format']
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
            initialvalue=self.config['timezone']
        )

        if zone and zone in zones:
            self.config['timezone'] = zone
            self.save_config()
        elif zone:
            messagebox.showerror("Error", "Unknown timezone")

    def update_clock(self):
        """Updates the displayed time"""
        try:
            tz = pytz.timezone(self.config['timezone'])
            now = datetime.datetime.now(tz)
            time_str = now.strftime(self.config['time_format'])
            self.clock_label.config(text=time_str)
        except:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M | %d.%m.%Y  ""TV Launcher")
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
        self.update_apps_display()

    def update_apps_display(self):
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
        self.media_files = []
        media_dirs = [
            os.path.expanduser('~/wideo'),
            os.path.expanduser('~/Wideo'),
            os.path.expanduser('~/Videos'),
            '/wideo'
        ]

        for media_dir in media_dirs:
            if os.path.exists(media_dir):
                for root, dirs, files in os.walk(media_dir):
                    for file in files:
                        if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                            self.media_files.append({
                                "name": os.path.splitext(file)[0],
                                "path": os.path.join(root, file),
                                "icon": self.icons['mp4']
                            })
                        elif file.lower().endswith(('.mp3', '.flac', '.wav')):
                            self.media_files.append({
                                "name": os.path.splitext(file)[0],
                                "path": os.path.join(root, file),
                                "icon": self.icons['mp3']
                            })

        if not self.media_files:
            self.media_files = [
                {"name": "The Witcher", "path": "", "icon": self.icons['mp4']},
                {"name": "Stranger Things", "path": "", "icon": self.icons['mp4']},
                {"name": "The Mandalorian", "path": "", "icon": self.icons['mp4']},
                {"name": "House of the Dragon", "path": "", "icon": self.icons['mp4']},
                {"name": "Peaky Blinders", "path": "", "icon": self.icons['mp4']},
                {"name": "Breaking Bad", "path": "", "icon": self.icons['mp4']}
            ]

        self.update_movies_display()

    def update_movies_display(self):
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
        if media.get("path"):
            if not self.media_player or not tk.Toplevel.winfo_exists(self.media_player.player_window):
                self.media_player = MediaPlayer(self.root, self.on_media_player_close)
            self.media_player.open_file(media["path"])
        else:
            messagebox.showinfo("Selected", f"Playing: {media['name']}")

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
            max_index = min(self.visible_apps, len(self.all_apps)) - 1
        elif self.selected_section == 2:
            max_index = min(self.visible_movies, len(self.media_files)) - 1

        new_index = self.selected_index + direction
        if 0 <= new_index <= max_index:
            self.selected_index = new_index
            self.update_selection()
        elif direction > 0 and self.selected_section == 1 and (self.apps_offset + self.visible_apps) < len(self.all_apps):
            self.apps_offset += 1
            self.update_apps_display()
            self.update_selection()
        elif direction < 0 and self.selected_section == 1 and self.apps_offset > 0:
            self.apps_offset -= 1
            self.update_apps_display()
            self.update_selection()
        elif direction > 0 and self.selected_section == 2 and (self.movies_offset + self.visible_movies) < len(self.media_files):
            self.movies_offset += 1
            self.update_movies_display()
            self.update_selection()
        elif direction < 0 and self.selected_section == 2 and self.movies_offset > 0:
            self.movies_offset -= 1
            self.update_movies_display()
            self.update_selection()

    def scroll_up(self):
        if self.selected_section == 1 and self.apps_offset > 0:
            self.apps_offset -= 1
            self.update_apps_display()
            self.update_selection()
        elif self.selected_section == 2 and self.movies_offset > 0:
            self.movies_offset -= 1
            self.update_movies_display()
            self.update_selection()

    def scroll_down(self):
        if self.selected_section == 1 and (self.apps_offset + self.visible_apps) < len(self.all_apps):
            self.apps_offset += 1
            self.update_apps_display()
            self.update_selection()
        elif self.selected_section == 2 and (self.movies_offset + self.visible_movies) < len(self.media_files):
            self.movies_offset += 1
            self.update_movies_display()
            self.update_selection()

    def update_selection(self):
        for btn in self.platform_buttons:
            btn.config(bg=self.platforms[self.platform_buttons.index(btn)]["color"], font=('Arial', 14, 'normal'))

        for btn in self.app_buttons:
            btn.config(style='Dark.TButton')

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
