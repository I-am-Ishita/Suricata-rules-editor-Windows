print("This is suricata_tool.py being executed")

import json
import os
import re

# -------------------- Paths --------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where suricata_tool.py is
except NameError:
    BASE_DIR = os.getcwd()
DEFAULT_RULES_DIR = os.path.join(BASE_DIR, "rules")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# Ensure default rules folder exists
if not os.path.exists(DEFAULT_RULES_DIR):
    os.makedirs(DEFAULT_RULES_DIR)

# -------------------- Settings Functions --------------------
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "suricata_path": "",
            "config_path": "",
            "rules_folder": DEFAULT_RULES_DIR,
            "interface": ""
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(default_settings, f, indent=4)
        return default_settings
    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)
    print("Settings saved successfully!")

def update_interface(settings):
    original_interface = settings.get('interface', '')
    print("Current network interface:", original_interface)
    new_interface = input("Enter new interface path (or leave blank): ").strip()
    if new_interface:
        settings['interface'] = new_interface
        save_settings(settings)
        restore = input("Do you want to restore the original interface now? (yes/no): ").strip()
        if restore.lower() == 'yes':
            settings['interface'] = original_interface
            save_settings(settings)
    else:
        print("No changes made.")

# -------------------- Rule Functions --------------------
def edit_rule_file(filepath):
    if not os.path.exists(filepath):
        open(filepath, 'w').close()

    with open(filepath, 'r') as f:
        lines = f.readlines()

    print("\n--- Current Rules (Full File) ---")
    for i, line in enumerate(lines, 1):
        print(f"{i}: {line.strip()}")

    choice = input("\nDo you want to edit an existing line or append a new line? (Press Enter to skip): ").strip().lower()

    if choice == "edit":
        line_no = int(input("Enter line number to edit: ").strip())
        if not (1 <= line_no <= len(lines)):
            print("Invalid line number.")
            return

        original_line = lines[line_no - 1].rstrip('\n')
        print(f"\nSelected Line {line_no}: {original_line}")

        while True:
            print("\nWhat do you want to edit?")
            print("1. Message (msg)")
            print("2. Content (content)")
            print("3. Class type (classtype)")
            print("4. Keypad value (sid)")
            print("5. Revision (rev)")
            print("6. Any other update (replace full line)")
            print("7. Finish editing this line")
            option = input("Enter option number: ").strip()

            if option == "1":
                match = re.search(r'msg\s*:\s*"(.*?)"', original_line)
                old = match.group(1) if match else ""
                new_val = input(f"Current msg: {old}\nEnter new msg: ")
                if match:
                    original_line = original_line.replace(f'msg:"{old}"', f'msg:"{new_val}"')
                else:
                    original_line += f' msg:"{new_val}";'
            elif option == "2":
                match = re.search(r'content\s*:\s*"(.*?)"', original_line)
                old = match.group(1) if match else ""
                new_val = input(f"Current content: {old}\nEnter new content: ")
                if match:
                    original_line = original_line.replace(f'content:"{old}"', f'content:"{new_val}"')
                else:
                    original_line += f' content:"{new_val}";'
            elif option == "3":
                match = re.search(r'classtype\s*:\s*(.*?);', original_line)
                old = match.group(1) if match else ""
                new_val = input(f"Current classtype: {old}\nEnter new classtype: ")
                if match:
                    original_line = original_line.replace(f'classtype:{old}', f'classtype:{new_val}')
                else:
                    original_line += f' classtype:{new_val};'
            elif option == "4":
                match = re.search(r'sid\s*:\s*(\d+);', original_line)
                old = match.group(1) if match else ""
                new_val = input(f"Current sid: {old}\nEnter new sid: ")
                if match:
                    original_line = original_line.replace(f'sid:{old}', f'sid:{new_val}')
                else:
                    original_line += f' sid:{new_val};'
            elif option == "5":
                match = re.search(r'rev\s*:\s*(\d+);', original_line)
                old = match.group(1) if match else ""
                new_val = input(f"Current rev: {old}\nEnter new rev: ")
                if match:
                    original_line = original_line.replace(f'rev:{old}', f'rev:{new_val}')
                else:
                    original_line += f' rev:{new_val};'
            elif option == "6":
                new_val = input("Enter new full line: ")
                original_line = new_val
            elif option == "7":
                break
            else:
                print("Invalid option. Try again.")

        confirm = input(f"\nFinal Updated Line:\n{original_line}\nSave this change? (yes/no): ").strip().lower()
        if confirm == "yes":
            lines[line_no - 1] = original_line + "\n"
            with open(filepath, 'w') as f:
                f.writelines(lines)
            print("Line updated successfully!")

    elif choice == "append":
        append_type = input(
            "Do you want to:\n"
            "1. Append a whole new rule\n"
            "2. Append extra option to last rule\n"
            "3. Erase the last rule\n"
            "Enter 1, 2 or 3: "
        ).strip()

        if append_type == "1":
            new_rule = input("Enter new rule to append: ").strip()
            if new_rule:
                with open(filepath, 'a') as f:
                    f.write(new_rule + "\n")
                print("New rule appended successfully!")

        elif append_type == "2":
            if not lines:
                print("No existing rules to append to!")
                return
            last_rule = lines[-1].rstrip("\n")
            print(f"Last rule:\n{last_rule}")
            extra_part = input("Enter the extra option to append (e.g., content:\"test\";): ").strip()
            if extra_part:
                updated_rule = last_rule.rstrip(";") + " " + extra_part + ";"
                lines[-1] = updated_rule + "\n"
                with open(filepath, 'w') as f:
                    f.writelines(lines)
                print("Extra option appended to last rule successfully!")

        elif append_type == "3":
            if not lines:
                print("No rules to erase!")
                return
            print(f"Last rule being erased:\n{lines[-1].strip()}")
            confirm = input("Are you sure you want to erase this rule? (yes/no): ").strip().lower()
            if confirm == "yes":
                lines = lines[:-1]  # remove last rule
                with open(filepath, 'w') as f:
                    f.writelines(lines)
                print("Last rule erased successfully!")
            else:
                print("Erase cancelled.")

    else:
        print("No changes made.")

def select_rule_to_edit(settings):
    print("\nChoose what you want to edit:")
    print("1. Edit existing ET rules")
    print("2. Edit/add custom rules")
    choice = input("Enter 1 or 2: ").strip()

    rules_folder = settings.get("rules_folder", DEFAULT_RULES_DIR)
    if choice == "1":
        categories = {
            "Protocol-based rules": [
                "dhcp-events.rules", "dns-events.rules", "ftp-events.rules", "http-events.rules",
                "http2-events.rules", "kerberos-events.rules", "mqtt-events.rules", "nfs-events.rules",
                "ntp-events.rules", "rfb-events.rules", "smb-events.rules", "smtp-events.rules",
                "ssh-events.rules", "stream-events.rules", "tls-events.rules"
            ],
            "Emerging Threat rules": [
                "botcc.rules", "botcc.portgrouped.rules", "ciarmy.rules", "compromised.rules", "drop.rules",
                "dshield.rules", "emerging-activex.rules", "emerging-adware_pup.rules", "emerging-attack_response.rules",
                "emerging-chat.rules", "emerging-coinminer.rules", "emerging-current_events.rules", "emerging-dns.rules",
                "emerging-dos.rules", "emerging-exploit.rules", "emerging-ftp.rules", "emerging-games.rules",
                "emerging-icmp.rules", "emerging-imap.rules", "emerging-inappropriate.rules", "emerging-info.rules",
                "emerging-ja3.rules", "emerging-malware.rules", "emerging-misc.rules", "emerging-mobile_malware.rules",
                "emerging-netbios.rules", "emerging-phishing.rules", "emerging-p2p.rules", "emerging-pop3.rules",
                "emerging-rpc.rules", "emerging-scada.rules", "emerging-scan.rules", "emerging-shellcode.rules",
                "emerging-smtp.rules", "emerging-snmp.rules", "emerging-sql.rules", "emerging-telnet.rules",
                "emerging-tftp.rules", "emerging-user_agents.rules", "emerging-voip.rules", "emerging-web_client.rules",
                "emerging-web_server.rules", "emerging-web_specific_apps.rules", "emerging-worm.rules", "tor.rules"
            ]
        }
    elif choice == "2":
        categories = {"Custom rules": ["custom.rules"]}
    else:
        print("Invalid choice")
        return

    print("\nAvailable Categories:")
    category_list = list(categories.keys())
    for idx, cat in enumerate(category_list, 1):
        print(f"{idx}. {cat}")

    cat_choice = int(input("Enter category number: ").strip()) - 1
    if not (0 <= cat_choice < len(category_list)):
        print("Invalid choice")
        return

    selected_category = category_list[cat_choice]
    files = categories[selected_category]

    print(f"\n{selected_category}:")
    for idx, f in enumerate(files, 1):
        print(f"{idx}. {f}")

    file_choice = int(input("Enter rule number to edit: ").strip()) - 1
    if not (0 <= file_choice < len(files)):
        print("Invalid choice")
        return

    selected_file = os.path.join(rules_folder, files[file_choice])
    edit_rule_file(selected_file)

# -------------------- Main --------------------
def main():
    settings = load_settings()

    # Prompt user to enter/update all paths
    settings["suricata_path"] = input("Enter Suricata executable path (or leave blank): ").strip() or settings.get('suricata_path','')
    settings["config_path"] = input("Enter Suricata config path (or leave blank): ").strip() or settings.get('config_path','')
    settings["rules_folder"] = input("Enter Suricata rules folder path (or leave blank): ").strip() or settings.get('rules_folder', DEFAULT_RULES_DIR)
    save_settings(settings)

    # Option to edit rules
    edit_choice = input("\nDo you want to edit rules? (yes/no): ").strip().lower()
    if edit_choice == 'yes':
        select_rule_to_edit(settings)

    # Option to update network interface
    update_choice = input("\nDo you want to update the network interface? (yes/no): ").strip().lower()
    if update_choice == 'yes':
        update_interface(settings)

# -------------------- Execute --------------------
if __name__ == "__main__":
    main()
