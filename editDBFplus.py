###
### editDBFplus.py
### Autores: Javier Garcia and Elisangela Cristina Mendes
###
import dbf
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_dbf_files():
    """Finds .dbf files using os.listdir instead of glob."""
    # List everything in current directory
    all_entries = os.listdir('.')
    # Filter for files ending in .dbf (case-insensitive)
    dbf_files = [f for f in all_entries if f.lower().endswith('.dbf')]
    return dbf_files

def select_file():
    """Prompts the user to choose a DBF file from the directory."""
    files = get_dbf_files()
    
    if not files:
        print("No .dbf files found in the current folder.")
        return None

    while True:
        clear_screen()
        print("--- Available VFP6 DBF Files ---")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        print("-" * 32)
        
        choice = input("Select a file number (or 'Q' to quit): ").strip().upper()
        
        if choice == 'Q':
            return None
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                return files[idx]
        
        input("Invalid selection. Press Enter to try again.")

def edit_dbf_terminal(file_path):
    try:
        # Open the VFP6 table
        table = dbf.Table(file_path)
        table.open(mode=dbf.READ_WRITE)
        
        if len(table) == 0:
            print(f"\n{file_path} is empty. Adding a blank record...")
            with table:
                table.append({})
        
        record = table[0]

        while True:
            clear_screen()
            print(f"--- Editing File: {file_path} ---")
            print("Type a Line # (1-20), 'B' for file list, or 'Q' to quit.")
            print("-" * 60)

            # Display the 20 lines
            for i in range(1, 21):
                field_name = f"line{i}"
                try:
                    # Fetching field value
                    content = getattr(record, field_name).strip()
                    print(f"{i:2d}: {content}")
                except AttributeError:
                    print(f"{i:2d}: [Field '{field_name}' not found]")

            print("-" * 60)
            choice = input("\nCommand: ").strip().upper()

            if choice == 'Q':
                table.close()
                return False
            
            if choice == 'B':
                table.close()
                return True
            
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= 20:
                    field_to_edit = f"line{idx}"
                    new_val = input(f"New text for {field_to_edit} (79 char max): ")
                    
                    # Update the record with FoxPro-style locking
                    with record:
                        try:
                            setattr(record, field_to_edit, new_val[:79])
                        except AttributeError:
                            input(f"Error: Field '{field_to_edit}' does not exist.")
                else:
                    input("Number must be between 1 and 20. Press Enter.")
            else:
                input("Invalid input. Press Enter.")

    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to return to menu...")
        return True

if __name__ == "__main__":
    while True:
        selected_file = select_file()
        if not selected_file:
            print("Exiting.")
            break
        
        should_continue = edit_dbf_terminal(selected_file)
        if not should_continue:
            print("Exiting.")
            break