from waitress import serve
from hms_project.wsgi import application
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

if __name__ == "__main__":
    print("Serving on http://0.0.0.0:8000 (accessible on your Local IP)")
    serve(application, host='0.0.0.0', port=8000)
