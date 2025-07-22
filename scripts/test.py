# Set up Django environment
import os
import sys
import django

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
django.setup()

from apps.controllers.submit_score_controller import DestinationController
from apps.db_manager.models import User


def list_destinations():
    data = {
        "action": "validate_destination",
        "clues": [
            "Home to a giant clock tower that tourists love taking pictures of.",
            "This city has a famous river running through it called the Thames.",
        ],
        "user_answer": "Paris",
    }
    x = DestinationController(data)
    x()
    print(x.result)


if __name__ == "__main__":
    list_destinations()
