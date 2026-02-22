# TV Launcher
A custom-built, full-screen media launcher for Linux, designed to provide a lean-back, TV-like experience. This application allows you to easily access streaming platforms, installed applications, and local multimedia files using simple keyboard navigation, making it perfect for your Home Theater PC (HTPC).

## Features
Integrated Streaming Hub: Launch popular streaming services like Netflix, YouTube, and HBO Max directly in a full-screen in new window.

<img width="1680" height="1050" alt="image" src="https://github.com/user-attachments/assets/b23871e6-cab0-40b4-ba09-33c8957136a6" />

Built-in Media Player: Play your local video and audio files from specified directories with a powerful, integrated VLC-based player.

<img width="1680" height="1050" alt="image" src="https://github.com/user-attachments/assets/88ef951f-441a-4f92-bed2-abaedbbff977" />

Automatic App Discovery: The launcher automatically scans your system for installed applications and displays them in a clean, scrollable list.

Remote-Friendly Navigation: Control the entire interface with just a few keys, ideal for use with a wireless keyboard or a universal remote programmed with keyboard shortcuts.

System Power Management: Directly sleep, restart, or shut down your computer from within the app.

<img width="282" height="338" alt="image" src="https://github.com/user-attachments/assets/ecfeeef9-2cbc-45e7-a2ad-f6ccd3400079" />


Customizable Experience: Change the time display format and timezone to suit your preferences via a simple settings menu.

<img width="679" height="90" alt="image" src="https://github.com/user-attachments/assets/db05ec94-627e-4132-9427-812e9bf33c3d" />


## Installation
The TV Launcher is provided as a single, pre-compiled executable file for Linux.

Download the latest release: Go to the Releases section of this repository and download the executable file for your system (e.g., tv-launcher-1.0-1.x86_64.rpm) and install via your app menager.
Next run this command to give the application permission to run
```Bash
bash
```
```Bash
sudo chmod +x /usr/bin/tv-launcher
```

Install the [VLC media player](https://www.videolan.org/vlc/#download)

install python-qtpy to use the built-in update feature

To run aplication please insert in terminall:

```Bash
bash
```
```Bash
sudo tv-launcher
```


## Configuration
The launcher saves its settings to a file in your home directory, which you can edit to customize the experience or in the program. The configuration file is located at ~/.streaming_launcher_config.json.

```JSON
JSON
```
```JSON

{
    "time_format": "%H:%M | %d.%m.%Y",
    "timezone": "Europe/Warsaw",
    "theme": {
        "background": "#747474",
        "foreground": "white",
        "button_bg": "#636363",
        "button_active": "#333333"
    }
}
```

## Controls
The app is designed for simple, remote-friendly navigation.

```Bash
		  Key		            -	           Action
   ____________________________________________________________________________
  	Arrow Keys (Up/Down)  	-	Change between sections (platforms, apps, media).
	_____________________________________________________________________________
	 Arrow Keys (Left/Right)	-	Move selection within the current section.
	_____________________________________________________________________________
   Enter			            	-	Launch the selected item.
	_____________________________________________________________________________
	 Esc			               	-	Exit the media player or the application.
	_____________________________________________________________________________
	 Page Up/Down	           	-	Scroll through the app and media lists.
	_____________________________________________________________________________
```

Contributing
If you find a bug or have a suggestion, please open an issue. All contributions are welcome!

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License. See the [LICENSE](https://github.com/Kubixonon/tv-launcher-for-linux/blob/main/LICENSE) file for details.
