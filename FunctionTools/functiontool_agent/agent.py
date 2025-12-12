# agent.py

import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

load_dotenv()


# Define the function for creating a file

def create_file(filename: str) -> str:
   """
   Creates a new, empty file with the specified name in the current directory.
  
   Args:
       filename: The name of the file to create (e.g., 'educosys.txt').
      
   Returns:
       A success or error message confirming the file status.
   """
   try:
       if os.path.exists(filename):
           return f"Error: File '{filename}' already exists. No action taken."
       else:
           with open(filename, "w") as f:
               pass
           return f"Successfully created empty file: '{os.path.abspath(filename)}'."
  
   except Exception as e:
       return f"Error creating file '{filename}': {e}"


file_tool_instance = FunctionTool(func=create_file)


# Define the function for creating a folder

def create_folder(folder_name: str) -> str:
   """
   Creates a new folder in the current directory.


   Args:
       folder_name: Name of the folder to create.


   Returns:
       A message confirming success or describing the error.
   """
   try:
       if os.path.exists(folder_name):
           return f"Error: Folder '{folder_name}' already exists. No action taken."
       else:
           os.makedirs(folder_name)
           return f"Successfully created folder: '{os.path.abspath(folder_name)}'."
   except Exception as e:
       return f"Error creating folder '{folder_name}': {e}"


folder_tool_instance = FunctionTool(func=create_folder)

# Define the function for deleting a file

def delete_file(filename: str) -> str:
   """
   Deletes a file from the current directory.


   Args:
       filename: The name of the file to delete.


   Returns:
       A message confirming success or describing the error.
   """
   try:
       if not os.path.isfile(filename):
           return f"Error: File '{filename}' does not exist."
      
       os.remove(filename)
       return f"Successfully deleted file: '{os.path.abspath(filename)}'."
  
   except Exception as e:
       return f"Error deleting file '{filename}': {e}"


delete_file_tool_instance = FunctionTool(func=delete_file)


# Define the function for deleting a folder

def delete_folder(folder_name: str) -> str:
   """
   Deletes a folder from the current directory (only if it is empty).


   Args:
       folder_name: The folder to delete.


   Returns:
       A message confirming success or describing the error.
   """
   try:
       if not os.path.isdir(folder_name):
           return f"Error: Folder '{folder_name}' does not exist."
      
       os.rmdir(folder_name)  # Only deletes empty folders
       return f"Successfully deleted folder: '{os.path.abspath(folder_name)}'."
  
   except Exception as e:
       return f"Error deleting folder '{folder_name}': {e}"


delete_folder_tool_instance = FunctionTool(func=delete_folder)

# Define the function for listing all files and folders in the current directory

def list_all_files() -> str:
   """
   Lists all files and folders in the current directory.


   Returns:
       A formatted string containing all entries or an error message.
   """
   try:
       items = os.listdir(".")
      
       if not items:
           return "The current directory is empty."


       result = "Contents of current directory:\n"
       for name in items:
           path = os.path.abspath(name)
           if os.path.isdir(name):
               result += f"[DIR]  {path}\n"
           else:
               result += f"[FILE] {path}\n"
      
       return result.strip()
  
   except Exception as e:
       return f"Error listing directory contents: {e}"


list_files_tool_instance = FunctionTool(func=list_all_files)


# root_agent = Agent(
#    model='gemini-2.5-flash',
#    name='root_agent',
#    description='A helpful assistant for user questions, with file creation capability.',
#    instruction=(
#        'You are a file management assistant. When asked to create a new file, '
#        'you MUST use the "create_file" tool and provide the exact filename as an argument.'
#         'You are also a folder management assistant. When asked to create a new folder, '
#        'you MUST use the "create_folder" tool and provide the exact foldername as an argument.'
#         'You are also a delete folder management assistant. When asked to delete a folder, '
#        'you MUST use the "delete_folder" tool and provide the exact foldername as an argument.'
#    ),
#    tools=[file_tool_instance, folder_tool_instance, delete_folder_tool_instance]
# )

root_agent = Agent(
   model=LiteLlm(model="openai/gpt-4o"),
   name="gpt_agent",
   description='A helpful assistant for user questions, with file creation capability.',
   instruction=(
       'You are a file management assistant. When asked to create a new file, '
       'you MUST use the "create_file" tool and provide the exact filename as an argument.'
        'You are also a folder management assistant. When asked to create a new folder, '
       'you MUST use the "create_folder" tool and provide the exact foldername as an argument.'
        'You are also a delete file management assistant. When asked to delete a file, '
       'you MUST use the "delete_file" tool and provide the exact filename as an argument.'
        'You are also a delete folder management assistant. When asked to delete a folder, '
       'you MUST use the "delete_folder" tool and provide the exact foldername as an argument.'
       'You are also a directory listing assistant. When asked to list all the files and folders '
       'inside the current working directory, you MUST use the "list_all_files" tool and '
       'call it with no arguments.'
       
   ),
   tools=[file_tool_instance, folder_tool_instance, delete_file_tool_instance, delete_folder_tool_instance, list_files_tool_instance]
)