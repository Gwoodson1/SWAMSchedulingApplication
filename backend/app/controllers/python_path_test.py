import sys
import os

your_directory = os.path.abspath('/Users/benjamin/Documents/SWAM Application/SWAMSchedulingApplication/backend/app/controllers/test_files/')  # Replace with the path to your module

if your_directory in sys.path:
    print(f"{your_directory} is in the Python path")
else:
    print(f"{your_directory} is NOT in the Python path")
