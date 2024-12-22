import os
import shutil

TEMPLATES_DIR = "./Templates"

def copy_template(template_name, project_name):
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(template_path):
        print(f"Template '{template_name}' does not exist.")
        return
    
    # Copy the template to a new project directory
    shutil.copytree(template_path, project_name)
    print(f"✅ Project '{project_name}' created using template '{template_name}'")

if __name__ == "__main__":
    print("Available Templates:")
    templates = os.listdir(TEMPLATES_DIR)
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template}")
    
    choice = int(input("Enter the number for the template you want to use: "))
    project_name = input("Enter the name of your new project: ")

    chosen_template = templates[choice - 1]
    copy_template(chosen_template, project_name)
