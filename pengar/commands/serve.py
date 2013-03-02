from pengar.www import app

import config
import logging

def main():
    # Enable logging for others than pengar.*
    logging.getLogger().setLevel(logging.INFO)

    app.run(
        port=config.PORT)
