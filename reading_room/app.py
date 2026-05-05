import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing_speed import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
