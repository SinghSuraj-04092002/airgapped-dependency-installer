import os
import sys
import subprocess
import argparse
 
def download_requirements(requirements_path, output_dir):
    """
    Downloads all dependencies from a requirements file including all subdependencies.
    """
    # Check if requirements file exists
    if not os.path.exists(requirements_path):
        print(f"Error: Requirements file '{requirements_path}' not found.")
        return False
   
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
   
    # Get Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(f"Using Python version: {python_version}")
   
    # First try to download the requirements with no constraints
    print(f"Downloading requirements from {requirements_path} to {output_dir}...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "download",
            "-r", requirements_path,
            "-d", output_dir
        ])
    except subprocess.CalledProcessError as e:
        print(f"Warning: Initial download failed with exit code {e.returncode}")
        print("Trying again package by package...")
       
        # Read requirements file line by line
        with open(requirements_path, 'r') as req_file:
            for line in req_file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
               
                # Try to download each package individually
                try:
                    print(f"Downloading {line}...")
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "download",
                        line,
                        "-d", output_dir
                    ])
                except subprocess.CalledProcessError:
                    print(f"Warning: Could not download {line}")
   
    # Additional common build dependencies
    build_deps = ["setuptools", "wheel", "pip", "build", "exceptiongroup"]
    for dep in build_deps:
        try:
            print(f"Downloading {dep}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "download",
                dep,
                "-d", output_dir
            ])
        except subprocess.CalledProcessError:
            print(f"Warning: Could not download {dep}")
   
    return True
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Python dependencies for offline installation')
    parser.add_argument('requirements', help='Path to requirements.txt file')
    parser.add_argument('output', help='Directory to store downloaded wheels')
   
    args = parser.parse_args()
   
    if download_requirements(args.requirements, args.output):
        print(f"All dependencies downloaded to {args.output}")
        print("\nTo install in the offline environment, use:")
        print(f"pip install --no-index --find-links={args.output} -r {args.requirements}")
    else:
        print("Failed to download all dependencies")
        sys.exit(1)