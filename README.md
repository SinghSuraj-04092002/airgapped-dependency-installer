# Offline Dependency Installation for Python Projects

This repository provides a simple method to download Python dependencies from an internet-connected machine and install them on an offline machine. This is particularly useful for client production environments where internet access is restricted.

## Features
- Downloads all required dependencies and their sub-dependencies.
- Includes essential build tools like `setuptools`, `wheel`, and `pip`.
- Supports downloading packages in both `wheel` and `source` format.
- Handles errors and retries package downloads individually if needed.

## Setup & Usage

### Step 1: Generate the Requirements File
Run the following command on your internet-connected machine to create a `requirements.txt` file listing all dependencies of your project:

```bash
pip freeze > requirements.txt
```

### Step 2: Download Dependencies
Use the provided script to download all required packages and store them in a `wheels` directory:

```bash
python download_depend.py requirements.txt ./wheels
```

This script will:
- Check if `requirements.txt` exists.
- Download all specified packages and their dependencies.
- Include common build dependencies like setuptools, wheel, and exceptiongroup
- Check for any additional dependencies that might be needed
- Handle both wheel and source distributions
- Store them in the `wheels` directory.

### Step 3: Transfer the Wheels Directory
Copy the `wheels` directory and the `requirements.txt` file to the offline machine via USB, network transfer, or any other secure method.

### Step 4: Install Dependencies Offline
On the offline machine, run the following command to install all downloaded dependencies:

```bash
pip install --no-index --find-links=./wheels --no-deps -r requirements.txt
```

This will install all required packages without accessing the internet.

## Notes
- Ensure you are using the same Python version on both machines.
- If a package fails to download, check the error messages and manually download the required files.

## License
This project is released under the MIT License.

