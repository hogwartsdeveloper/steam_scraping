import requests
from bs4 import BeautifulSoup


class SteamGenreScraping:
    def __init__(self, link):
        self.link = link
