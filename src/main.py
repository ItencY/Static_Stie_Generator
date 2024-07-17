import os
import shutil
from copy_static import copy_files_recursive

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"

def main():
    print("Delete public directory")
    if os.path.exists(DIR_PATH_PUBLIC):
        shutil.rmtree(DIR_PATH_PUBLIC)
    
    print("Copying static files to public directory")
    copy_files_recursive(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    

main()