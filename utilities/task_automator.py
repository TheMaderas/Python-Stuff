"""
Utility to automate repetitive tasks like backup, cleaning, and organizing files.
"""
import os
import shutil
import time
import datetime
import glob
import zipfile
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def backup_directory(source_dir, dest_dir, zip_file=None, exclude_patterns=None):
    """
    Creates a backup of a directory.
    
    Args:
        source_dir (str): Source directory
        dest_dir (str): Destination directory
        zip_file (str): Zip file name (optional)
        exclude_patterns (list): File patterns to exclude
        
    Returns:
        str: Backup path
    """
    try:
        source_path = Path(source_dir).expanduser().resolve()
        dest_path = Path(dest_dir).expanduser().resolve()
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source directory '{source_dir}' not found")
        
        os.makedirs(dest_path, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if zip_file:
            zip_filename = zip_file if zip_file.endswith('.zip') else f"{zip_file}.zip"
            backup_path = dest_path / f"{Path(source_path).name}_{timestamp}_{zip_filename}"
            
            logger.info(f"Creating compressed backup: {backup_path}")
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                file_count = 0
                
                for root, dirs, files in os.walk(source_path):
                    if exclude_patterns:
                        dirs[:] = [d for d in dirs if not any(
                            glob.fnmatch.fnmatch(os.path.join(root, d), pattern) 
                            for pattern in exclude_patterns
                        )]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        if exclude_patterns and any(
                            glob.fnmatch.fnmatch(file_path, pattern) 
                            for pattern in exclude_patterns
                        ):
                            continue
                        
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)
                        file_count += 1
                
                logger.info(f"Backup completed: {file_count} files added to zip")
        else:
            backup_name = f"{Path(source_path).name}_{timestamp}"
            backup_path = dest_path / backup_name
            logger.info(f"Creating directory backup: {backup_path}")
            
            shutil.copytree(
                source_path, 
                backup_path, 
                ignore=shutil.ignore_patterns(*exclude_patterns) if exclude_patterns else None
            )
            
            logger.info(f"Backup completed: directory copied to {backup_path}")
        
        return str(backup_path)
    
    except Exception as e:
        logger.error(f"Error creating backup: {str(e)}")
        return None

def clean_directory(directory, pattern="*", older_than=None, dry_run=False):
    """
    Cleans files in a directory based on patterns and age.
    
    Args:
        directory (str): Directory to clean
        pattern (str): Glob pattern for files to remove
        older_than (int): Remove files older than this number of days
        dry_run (bool): If True, only simulates the operation
        
    Returns:
        tuple: (files removed, space freed)
    """
    try:
        dir_path = Path(directory).expanduser().resolve()
        
        if not dir_path.exists() or not dir_path.is_dir():
            raise FileNotFoundError(f"Directory '{directory}' not found")
        
        logger.info(f"Cleaning directory: {dir_path}")
        logger.info(f"Pattern: {pattern}, Older than: {older_than} days")
        
        files_to_delete = []
        current_time = time.time()
        
        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                if older_than is not None:
                    file_age_days = (current_time - file_path.stat().st_mtime) / (60*60*24)
                    if file_age_days < older_than:
                        continue
                
                files_to_delete.append(file_path)
        
        total_size = sum(file_path.stat().st_size for file_path in files_to_delete)
        
        if dry_run:
            logger.info(f"Simulation: {len(files_to_delete)} files would be removed")
            logger.info(f"Space that would be freed: {total_size / (1024*1024):.2f} MB")
            
            if files_to_delete:
                logger.info("Examples of files that would be removed:")
                for file in files_to_delete[:10]:
                    logger.info(f"  - {file}")
                if len(files_to_delete) > 10:
                    logger.info(f"  ... and {len(files_to_delete) - 10} more files")
        else:
            deleted_count = 0
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"Could not remove '{file_path}': {str(e)}")
            
            logger.info(f"Cleaning completed: {deleted_count} files removed")
            logger.info(f"Space freed: {total_size / (1024*1024):.2f} MB")
        
        return (len(files_to_delete), total_size)
    
    except Exception as e:
        logger.error(f"Error cleaning directory: {str(e)}")
        return (0, 0)

def organize_files(directory, rules=None):
    """
    Organizes files in a directory based on rules.
    
    Args:
        directory (str): Directory to organize
        rules (dict): Dictionary of rules {extension: destination_folder}
        
    Returns:
        int: Number of files organized
    """
    try:
        dir_path = Path(directory).expanduser().resolve()
        
        if not dir_path.exists() or not dir_path.is_dir():
            raise FileNotFoundError(f"Directory '{directory}' not found")
        
        if not rules:
            rules = {
                # Documents
                'pdf': 'Documents/PDFs',
                'doc': 'Documents/Word', 'docx': 'Documents/Word',
                'xls': 'Documents/Excel', 'xlsx': 'Documents/Excel',
                'ppt': 'Documents/PowerPoint', 'pptx': 'Documents/PowerPoint',
                'txt': 'Documents/Text',
                
                # Images
                'jpg': 'Images', 'jpeg': 'Images',
                'png': 'Images',
                'gif': 'Images',
                'bmp': 'Images',
                
                # Audio and Video
                'mp3': 'Media/Audio',
                'wav': 'Media/Audio',
                'mp4': 'Media/Video',
                'avi': 'Media/Video',
                'mkv': 'Media/Video',
                
                # Compressed files
                'zip': 'Files/Compressed',
                'rar': 'Files/Compressed',
                'tar': 'Files/Compressed',
                'gz': 'Files/Compressed',
                
                # Installers
                'exe': 'Installers',
                'msi': 'Installers',
                'dmg': 'Installers',
                
                # Code
                'py': 'Code/Python',
                'js': 'Code/JavaScript',
                'html': 'Code/Web',
                'css': 'Code/Web',
                'java': 'Code/Java',
                'c': 'Code/C',
                'cpp': 'Code/C++',
            }
        
        logger.info(f"Organizing files in: {dir_path}")
        
        organized_count = 0
        
        for file_path in dir_path.glob('*'):
            if file_path.is_file():
                extension = file_path.suffix.lower().lstrip('.')
                
                if extension in rules:
                    dest_folder = dir_path / rules[extension]
                    
                    os.makedirs(dest_folder, exist_ok=True)
                    
                    dest_path = dest_folder / file_path.name
                    
                    if dest_path.exists():
                        base_name = dest_path.stem
                        extension = dest_path.suffix
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest_path = dest_folder / f"{base_name}_{timestamp}{extension}"
                    
                    shutil.move(str(file_path), str(dest_path))
                    organized_count += 1
                    logger.debug(f"Moved: {file_path.name} -> {dest_path}")
        
        logger.info(f"Organization completed: {organized_count} files organized")
        return organized_count
    
    except Exception as e:
        logger.error(f"Error organizing files: {str(e)}")
        return 0

def main():
    while True:
        print("\n" + "="*60)
        print(" TASK AUTOMATION UTILITY ")
        print("="*60)
        print("1) Backup directory")
        print("2) Clean directory")
        print("3) Organize files by type")
        print("0) Exit")
        choice = input("Enter option number: ").strip()
        if choice == '1':
            source = input("Enter source directory: ").strip()
            dest = input("Enter destination directory: ").strip()
            zip_choice = input("Create zip backup? (y/n): ").strip().lower() == 'y'
            zip_file = None
            if zip_choice:
                zip_file = input("Enter zip filename (without .zip): ").strip()
            exclude_input = input("Exclude patterns (comma-separated, e.g., *.tmp) or leave blank: ").strip()
            exclude = [p.strip() for p in exclude_input.split(',')] if exclude_input else None
            backup_directory(source, dest, zip_file, exclude)
        elif choice == '2':
            directory = input("Enter directory to clean: ").strip()
            pattern = input("Enter file pattern to remove [default '*']: ").strip() or '*'
            older_input = input("Remove files older than days (number) or leave blank: ").strip()
            older_than = int(older_input) if older_input else None
            dry_run = input("Dry run? (y/n): ").strip().lower() == 'y'
            clean_directory(directory, pattern, older_than, dry_run)
        elif choice == '3':
            directory = input("Enter directory to organize: ").strip()
            organize_files(directory)
        elif choice == '0':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
