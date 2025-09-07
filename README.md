# Suricata-rules-editor-Windows
A Windows Python tool to edit, add, and manage Suricata rules easily.
Suricata Tools for Windows

Features:
1. Load and save Suricata configuration settings via a settings.json file.
2. Edit existing Emerging Threat or protocol-based rules.
3. Add and manage custom rules.
4. Update network interface monitored by Suricata.
5. Supports both default and user-defined rules folders.

Prerequisites:
1. Windows operating system
2. Python 3.x installed
3. Suricata installed (optional if only editing rules)

Setup:
1. Clone the repository and place the files in a folder.
2. Ensure suricata_tool.py, settings.json, and rules.zip (optional) are present.
3. Python must be installed to run the script.

Run:
1. Launch the script.
2. Enter paths or leave blank for defaults, or edit settings.json directly to set default paths and interface (preferred).
3. Edit ET or custom rules.
4. Update the network interface. (Optional)
5. Start Suricata if installed.

The tool does not require Suricata to be installed if you are only managing rules.

