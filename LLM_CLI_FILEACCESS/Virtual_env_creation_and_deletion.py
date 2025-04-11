import venv
import subprocess as subprocess
import os
import shutil
import time

choice = input("Do you want to create or remove a virtual environment? (c/r): ")
if choice == "r":
    if os.path.exists(".venv"):
        print("Removing virtual environment...")
        #
        time.sleep(2)  # Optional: Wait for 2 seconds before removing
        # Remove the virtual environment
        shutil.rmtree(".venv")
    else:
        print("No virtual environment found to remove.")
        exit()
elif choice == "c":
    if os.path.exists(".venv"):
        print("Virtual environment already exists.")
        exit()
    else:
        print("Creating virtual environment...")
        venv.create(".venv", with_pip=True)  # Create the virtual environment

    print("windows, mac, linux")
    OS = input("Operating System: ").strip().lower()

    # Path to the main script
    main_script = r"enter_complete_path_here\main_code.py"

    if OS == "windows":
        requirements_file = r"enter_full_file_path_here\requirements.txt"
        print("Installing dependencies...")
        subprocess.run(["pip", "install", "-r", requirements_file], shell=True)
        subprocess.run(["pip", "install", "groq"], shell=True)
        python_executable = os.path.join(".venv", "Scripts", "python.exe")
        try:
            subprocess.run([python_executable, main_script])
        except exception as e:
            print(f"Error running the script: {e}")
            exit()

    elif OS == "mac":
        python_executable = os.path.join(".venv", "bin", "python3")
        subprocess.run([python_executable, main_script])
    elif OS == "linux":
        python_executable = os.path.join(".venv", "bin", "python")
        subprocess.run([python_executable, main_script])
    else:
        print("Unsupported operating system.")
        exit()