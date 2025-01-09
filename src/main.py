import os
import shutil

# Import the function for generating the page
from copystatic import copy_files_recursive
from page_generator import generate_pages_recursive # Replace with the actual module where generate_page is defined

# Directories
dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "template.html"

def main():
    # Step 1: Delete the public directory
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    # Step 2: Copy static files to the public directory
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # Step 3: Generate pages for every markdown file in the content directory
    print("Generating pages from content directory...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

    print("Site generated successfully!")
if __name__ == "__main__":
    main()