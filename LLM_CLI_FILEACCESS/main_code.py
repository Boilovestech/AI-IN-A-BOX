import os
import shutil
import subprocess as subproccess
from groq import Groq
from dotenv import load_dotenv
import logging as lg
from datetime import datetime
from colorlog import ColoredFormatter
from file_serialisation import structure_to_use, read_file_contents
import time 


#----------------------------#

# Log filename with timestamp
log_filename = f"LLM_actions_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Create a logger
logger = lg.getLogger()
logger.setLevel(lg.DEBUG)

# File handler for saving logs to a file
file_handler = lg.FileHandler(log_filename)
file_handler.setLevel(lg.DEBUG)
file_formatter = lg.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Console handler for colored logs
console_handler = lg.StreamHandler()
console_handler.setLevel(lg.DEBUG)
color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'blue,bg_white,bold',
        'WARNING': 'yellow',
        'ERROR': 'red,bg_white',
        'CRITICAL': 'white,bg_red,bold',
    }
)
console_handler.setFormatter(color_formatter)
logger.addHandler(console_handler)
#----------------------------#

load_dotenv()
delay = 30 #seconds

payload = ""
deleted_files = set()

# Create the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Set the system prompt
system_prompt = {
    "role": "system",
    "content":
    f"""Give short answers.
    More instructions are in--'read.txt' file.
    [DO NOT GIVE ANYTHINGELSE OTHER THAN THE COMMANDS IN YOUR RESPONSES]
    -Mention paths using '\\' insted of '\' .
    -to see the file hirarchy--->'Action:List',
    -to see the content of the file--->'Action:Read <filepath>',
    -never do this 'Action:Read <filename>'(without path),insted do this 'Action:Read <filepath>'.
    -to see the content of the directory--->'Action:seeDir <directory_path>',
    -To end the loop say 'Q123'(do after u r done with the what u want),
    -to delete any file/folder->say 'Action:Delete <filepath>'.
    -to create new files(only txt,csv,json,md)->Action:New <filenamewithtype>
    -to write to a file->'Action:WriteToEx <filepath> <content>'. 
    -to run a python file->'Action:Run <filepath>'.
    !First look at the file structure using 'Action:List' command!"""
}

# Initialize the chat history
chat_history = [system_prompt]
messeges = {"role": "user", "content": payload}
chat_history.append(messeges)
#----------------------------#
json_str = structure_to_use()

# Define the trash folder path
trash_folder = "LLM_CLI_FILEACCESS_trash"

# Ensure the trash folder exists
if not os.path.exists(trash_folder):
    os.makedirs(trash_folder)

#---------------LOOP---------------#

while True:
    chat_history.append({"role": "user", "content": str(payload)})
    response = client.chat.completions.create(model="llama3-70b-8192",
                                              messages=chat_history,
                                              max_tokens=100,
                                              temperature=1.2)

    assistant_msg = str(response.choices[0].message.content)
    logger.info("Assistant: %s", assistant_msg)

    # Append response to history
    chat_history.append({
        "role": "assistant",
        "content": assistant_msg
    })

    if "Q123" in assistant_msg:
        logger.info("Exiting the program.")
        break

    # Add a cooldown to avoid rate limits
    time.sleep(delay)  # Wait before the next request
#---------------------------------#
    if "Action:WriteToEx" in response.choices[0].message.content:
        try:
            # Extract the command parts
            command_parts = response.choices[0].message.content.split("Action:WriteToEx ", 1)
            if len(command_parts) > 1:
                # Split the filepath and content
                filepath_and_content = command_parts[1].strip().split(" ", 1)
                if len(filepath_and_content) == 2:
                    filename = filepath_and_content[0].strip()  # Extract the file path
                    whattowrite = filepath_and_content[1].strip()  # Extract the content to write

                    # Write the content to the specified file
                    with open(filename, 'w') as file:
                        file.write(whattowrite)
                    logger.info("File %s created and written successfully.", filename)
                else:
                    logger.error("Invalid command format. Missing content to write.")
            else:
                logger.error("Invalid command format. Missing filepath and content.")
        except Exception as e:
            logger.critical("Critical Error: %s", e)
#---------------------------------#
    if "Action:New" in response.choices[0].message.content:
        try:
            # Extract the filename from the response
            filename = response.choices[0].message.content.split("Action:New ")[1].strip()
            # Create a new file with the specified filename
            with open(filename, 'w') as new_file:
                new_file.write("")
            print(f"File {filename} created successfully.")
            logger.info("System: %s", system_prompt)
            logger.info("Chat History: %s", chat_history)
            logger.info("Assistant: %s", assistant_msg)
            logger.info("User: %s", payload)
        except Exception as e:
            logger.critical("CRITICAL ERROR: %s", e)
#---------------------------------#
    elif "Action:Delete" in response.choices[0].message.content:
        try:
            # Extract the filename from the response
            filename = response.choices[0].message.content.split("Action:Delete ")[1].strip()
            if filename in deleted_files:
                print(f"File {filename} has already been deleted.")
            else:
                # Check if the file exists
                if os.path.exists(filename):
                    # Move the file to the trash folder
                    trash_path = os.path.join(trash_folder, os.path.basename(filename))
                    shutil.move(filename, trash_path)
                    print(f"File {filename} moved to trash at {trash_path}.")
                    deleted_files.add(filename)
                else:
                    print(f"File {filename} does not exist.")
                    deleted_files.add(filename)
            logger.info("System: %s", system_prompt)
            logger.info("Chat History: %s", chat_history)
            logger.info("Assistant: %s", assistant_msg)
            logger.info("User: %s", payload)
        except Exception as e:
            logger.critical("CRITICAL ERROR: %s", e)
#---------------------------------#
    elif "Action:Read" in assistant_msg:
        command_parts = assistant_msg.split("Action:Read ")
        if len(command_parts) > 1 and os.path.exists(command_parts[1].strip()):
            filename = command_parts[1].strip()
            try:
                # Read the contents of the file
                file_contents = read_file_contents(filename)
                # Append the file contents to the payload variable
                payload = file_contents
                logger.info("System: %s", system_prompt)
                logger.info("Chat History: %s", chat_history)
                logger.info("Assistant: %s", assistant_msg)
                logger.info("User: %s", payload)
            except Exception as e:
                logger.critical("CRITICAL ERROR: %s", e)

        else:
            print("Invalid or non-existent file path.")
            logger.error("Invalid or non-existent file path: %s", assistant_msg)
#---------------------------------#
    elif "Action:List" in response.choices[0].message.content:
        try:
            json_str = structure_to_use()
            payload = json_str
            logger.info("Viewed file hierarchy: %s", json_str)
        except Exception as e:
            logger.error("Error: %s", e)
            payload = "Error reading file hierarchy"
#---------------------------------#
    elif "Action:seeDir" in response.choices[0].message.content:
        try:
            # Extract the directory path from the response
            directory_path = response.choices[0].message.content.split("Action:seeDir ")[1].strip()
            # List the contents of the directory
            dir_contents = str(os.listdir(directory_path))
            payload = dir_contents
        except Exception as e:
            logger.error("Error: %s", e)
            payload = "[Error reading directory]"
#---------------------------------#
    elif "Action:Run" in response.choices[0].message.content:
        try:
            # Extract the command from the response
            command = response.choices[0].message.content.split("Action:Run ")[1].strip()
            if ".py" in command:
                subproccess.run(["python", command],check=True)
            else:
                lg.info("File is not a Python file.")
                payload = "[File is not a Python file.]"
            lg.warning(f"Python file: {command} was excecuted by the AI.")
            payload = ["Command executed successfully"]
        except Exception as e:
            lg.critical("CRITICAL ERROR: %s", e)
            payload = "[Error executing command]"
#---------------------------------#







