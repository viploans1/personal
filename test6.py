import random
import time
import os
from datetime import datetime, timedelta
from instagrapi import Client
import config
from colorama import Fore, init
from instagrapi.exceptions import LoginRequired
import logging

# Initialize colorama for colored output
init(autoreset=True)

# Set up logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Daily Like Limit
MIN_LIKES_PER_DAY = 198
MAX_LIKES_PER_DAY = 215
likes_today = 0
reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

def login_user():
    cl = Client()
    session_file = "session.json"
    login_via_session = False
    login_via_pw = False

    if os.path.exists(session_file):
        try:
            cl.load_settings(session_file)
            cl.login(config.username, config.password)
            try:
                cl.get_timeline_feed()
                print(f"{Fore.GREEN}Logged in using session!")
                login_via_session = True
            except LoginRequired:
                print(f"{Fore.YELLOW}Session expired. Re-logging with credentials...")
                cl.set_settings({})
                cl.login(config.username, config.password)
                print(f"{Fore.GREEN}Logged in with username and password!")
        except Exception as e:
            print(f"{Fore.RED}Error loading session: {e}")

    if not login_via_session:
        try:
            print(f"{Fore.YELLOW}No valid session found. Logging in with username and password...")
            cl.login(config.username, config.password)
            print(f"{Fore.GREEN}Logged in with username and password!")
            login_via_pw = True
        except Exception as e:
            print(f"{Fore.RED}Failed to login with username and password: {e}")

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't log in with either session or password.")

    cl.dump_settings(session_file)
    print(f"{Fore.CYAN}Session saved successfully!")
    time.sleep(random.uniform(2, 5))
    return cl

class LikePost:
    def __init__(self, client):
        self.cl = client
        self.tags = [
            'Happyhomeowner', 'Firsthomeowner', 'dreamhome', 'womenwholead', 'bwofgod', 'womanofgod', 
            'jesuslovesyou', 'AVwomen', 'exprealty', 'Avrealty', 'palmdalerealestate', 'lancasterrealestate', 
            'palmdale', 'lancaster', 'firsttimebuyer', 'Realbrokerage', 'openhouse', 'coldwellbankerhartwig', 
            'santaclaritahomes', 'AVseller', 'homesweethome', 'realestategoals', 'kellerwilliams', 'Rosamond', 
            '661realestate', 'azrealtor', 'downpaymentassistance', 'AntelopeValleyRealtor', 'PalmdaleRealtor', 
            'LancasterCARealtor', 'AVRealtors', 'PalmdaleHomesForSale', 'LancasterHomesForSale'
        ]
        self.liked_medias = []
        self.elapsed_time = 0
        self.daily_like_limit = random.randint(MIN_LIKES_PER_DAY, MAX_LIKES_PER_DAY)
        print(f"{Fore.BLUE}Today's like limit: {self.daily_like_limit} likes")

    def like_post(self, amount):
        global likes_today, reset_time

        for i in range(amount):
            if datetime.now() >= reset_time:
                likes_today = 0
                reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                self.daily_like_limit = random.randint(MIN_LIKES_PER_DAY, MAX_LIKES_PER_DAY)
                print(f"{Fore.BLUE}New day's like limit: {self.daily_like_limit} likes")

            if likes_today >= self.daily_like_limit:
                print(f"{Fore.RED}Reached today's like limit! Stopping for today.")
                break

            random_post = self.get_post_id_from_hashtags()
            if random_post and random_post not in self.liked_medias:
                try:
                    self.cl.media_like(media_id=random_post)
                    self.liked_medias.append(random_post)
                    likes_today += 1
                    print(f"{Fore.GREEN}Liked post {likes_today}/{self.daily_like_limit}")

                    time.sleep(random.randint(20, 60))
                except Exception as e:
                    print(f"{Fore.RED}Error while liking the post: {e}")
            else:
                print("Skipping this post to keep things natural.")
                time.sleep(random.randint(30, 90))

try:
    cl = login_user()
    bot = LikePost(cl)
    bot.like_post(600)
except Exception as e:
    print(f"{Fore.RED}A fatal error occurred: {e}")
    input("Press Enter to exit...")
