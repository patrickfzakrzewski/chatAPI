from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app import create_app

if __name__ == '__main__':
    APP = create_app()
    APP.run(host='0.0.0.0', port=5000)
