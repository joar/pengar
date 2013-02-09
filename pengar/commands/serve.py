from pengar.www import app

import config
import logging

def main():
    app.run(
        port=config.PORT)
