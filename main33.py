import random
import time
import os
from instagrapi import Client
import config
from colorama import Fore, init
from instagrapi.exceptions import LoginRequired
import logging

# Initialize colorama for colored output
init(autoreset=True)

# Set up logging
logger = logging.getLogger()

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

# Startup Message
print(f"{Fore.BLUE}Loading Instagram Bot...")
print(f"{Fore.YELLOW}Running Version 0.577V")
print(f"{Fore.RED}EXCLUSIVE MORTGAGE VERSION")
print(f"{Fore.BLUE}Welcome! {Fore.WHITE}{config.username}")

cl = login_user()

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

    def wait_time(self, delay):
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Taking a quick break... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Break over, back to action!               ")

    def simulate_scrolling(self):
        scroll_delay = random.randint(5, 15)
        print(f"{Fore.MAGENTA}Scrolling through feed for {scroll_delay} seconds...")
        time.sleep(scroll_delay)
        print(f"{Fore.MAGENTA}Done scrolling.")

    def get_post_id_from_following(self):
        try:
            following = self.cl.user_following_v1(self.cl.user_id)
            random_user_id = random.choice(following).pk
            print(f"{Fore.YELLOW}Looking up posts from someone you follow...")

            for attempt in range(3):
                try:
                    user_posts = self.cl.user_medias(random_user_id, amount=1, use_gql=False)
                    if user_posts:
                        return str(user_posts[0].model_dump()['id'])
                    else:
                        print(f"{Fore.RED}No posts found, retrying attempt {attempt + 1}/3...")
                        time.sleep(2)
                except Exception as e:
                    print(f"{Fore.RED}Fetch attempt {attempt + 1} failed: {e}")
                    time.sleep(2)

            print(f"{Fore.RED}Failed to fetch posts after 3 attempts.")
            return None

        except Exception as e:
            print(f"{Fore.RED}Error while fetching posts from followed users: {e}")
            return None

    def get_post_id_from_hashtags(self):
        try:
            print(f"{Fore.YELLOW}Exploring posts tagged with trending hashtags...")
            medias = self.cl.hashtag_medias_recent(random.choice(self.tags), amount=1)
            if medias:
                return str(medias[0].model_dump()['id'])
            else:
                print("Couldn't find any posts with that hashtag, retrying...")
                return None
        except Exception as e:
            print(f"{Fore.RED}Error fetching post via hashtag: {e}")
            return None

    def like_post(self, amount):
        daily_limit = random.randint(150, 250)
        likes_today = 0
        print(f"{Fore.CYAN}Today's like target: {daily_limit} posts.")

        for i in range(amount):
            if likes_today >= daily_limit:
                print(f"{Fore.BLUE}Reached today's like target. Exiting to stay safe.")
                break

            if random.random() < 0.2:
                self.simulate_scrolling()
                print(f"{Fore.YELLOW}Skipped liking to appear more human.")
                self.wait_time(random.randint(15, 45))
                continue

            random_post = self.get_post_id_from_following() if random.random() < 0.7 else self.get_post_id_from_hashtags()

            if random_post and random_post not in self.liked_medias:
                try:
                    self.simulate_scrolling()
                    time.sleep(random.uniform(3, 7))
                    self.cl.media_like(media_id=random_post)
                    self.liked_medias.append(random_post)
                    likes_today += 1
                    random_delay = random.choice([20, 30, 45, 60, 90, 120])
                    self.elapsed_time += random_delay
                    print(f"Total likes: {likes_today} | Time elapsed: {self.elapsed_time / 60:.2f} minutes | Next action in {random_delay} seconds")
                    self.wait_time(random_delay)
                except Exception as e:
                    print(f"{Fore.RED}Error while liking the post: {e}")
            else:
                print(f"{Fore.YELLOW}No suitable post found or already liked. Scrolling instead.")
                self.simulate_scrolling()
                self.wait_time(random.randint(15, 45))

        print(f"{Fore.GREEN}Session complete. Total likes today: {likes_today}")

try:
    bot = LikePost(cl)
    bot.like_post(207)
except Exception as e:
    print(f"{Fore.RED}A fatal error occurred: {e}")
    input("Press Enter to exit...")
