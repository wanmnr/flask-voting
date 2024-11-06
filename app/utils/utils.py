# app/utils.py
from datetime import datetime

def get_context_processors():
    def utility_processor():
        return {
            'now': datetime.now()
        }
    return utility_processor