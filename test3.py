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
    """
    Logs in to Instagram, creating a session if it doesn't exist or is invalid.
    """
    cl = Client()
    session_file = "session.json"
    login_via_session = False
    login_via_pw = False

    if os.path.exists(session_file):
        try:
            cl.load_settings(session_file)
            cl.login(config.username, config.password)
            # Check if the session is still valid
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

    # Save the new session
    cl.dump_settings(session_file)
    print(f"{Fore.CYAN}Session saved successfully!")
    # Introduce a human-like pause before continuing
    time.sleep(random.uniform(2, 5))
    return cl

# Display a loading message when starting the bot
print(f"{Fore.BLUE}Loading Instagram Bot...")
print(f"{Fore.YELLOW}Running Version 0.577V")
print(f"{Fore.RED}EXCLUSIVE MORTGAGE VERSION")
print(f"{Fore.BLUE}Welcome! {Fore.WHITE}{config.username}")

# Log in using the function
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
            'LancasterCARealtor', 'AVRealtors', 'PalmdaleHomesForSale', 'LancasterHomesForSale', 
            'AntelopeValleyRealEstate', 'PalmdaleRealEstate', 'LancasterCARealEstate', 'AntelopeValleyLiving', 
            'PalmdaleLiving', 'LancasterCALiving', 'AVLuxuryHomes', 'AVNewHomes', 'AVHomeLoans', 'AntelopeValleyMortgage', 
            'PalmdaleMortgageLender', 'LancasterCAMortgage', 'HomeBuyingMadeEasy', 'RealtorNetworking', 
            'RealtorMarketing', 'RealEstateGrowth', 'AVInvestors', 'FirstTimeHomeBuyerAV', 'HomeBuyersPalmdale', 
            'BuySellInvestAV', 'RealtorsOfInstagram', 'CaliforniaRealtors', 'RealEstateLife', 'RealtorGoals', 
            'RealtorSuccess', 'RealEstateMarketing', 'RealEstateInvesting', 'HouseHunting', 'JustListed', 
            'HomeOwnerLife', 'MyFirstHome', 'ForeverHome', 'DreamHomeGoals', 'HomeSweetHome', 'HouseToHome', 
            'NewHomeJourney', 'HomeOwnersUnite', 'FirstTimeBuyerTips', 'HomeBuying101', 'MortgageMadeEasy', 
            'HomeLoanExperts', 'HomeBuyingProcess', 'HomeLoanHelp', 'HomeFinance', 'SellingYourHome', 'ReadyToSell', 
            'TimeToMove', 'HouseForSaleNow', 'ListYourHome', 'SellYourHomeFast', 'BestTimeToSell', 
            'AntelopeValleyHomes', 'PalmdaleLiving', 'LancasterLiving', 'MoveToAV', 'AVHomesForSale', 
            'LiveInPalmdale', 'LiveInLancaster', 'BuyAHomeInAV', 'LuxuryHomesAV', 'AVInvestmentProperties', 
            'CaliforniaLuxuryHomes', 'RealEstateInvestorAV', 'RealtorLife', 'HomeBuyingMadeSimple', 
            'DreamHomeLoading', 'RealtorSuccessStories', 'HelpingHomeowners', 'HouseHunters'
        ]
        self.liked_medias = []
        self.elapsed_time = 0

    def wait_time(self, delay):
        # Human-like countdown with varied messaging
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Taking a quick break... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Break over, back to action!               ")

    def wait_for_api(self, delay):
        # Countdown before fetching posts with natural messages
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Hunting for interesting posts... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Found some posts! Let's proceed.               ")

    def simulate_scrolling(self):
        # Simulate a human scrolling through their feed
        scroll_delay = random.randint(5, 15)
        print(f"{Fore.MAGENTA}Scrolling through feed for {scroll_delay} seconds...")
        time.sleep(scroll_delay)
        print(f"{Fore.MAGENTA}Done scrolling.")

    def get_post_id_from_following(self):
        try:
            following = self.cl.user_following_v1(self.cl.user_id)
            random_user_id = random.choice(following).pk
            print(f"{Fore.YELLOW}Looking up posts from someone you follow...")
            self.wait_for_api(random.randint(10, 30))
            # Use user_medias_v1 to bypass the GraphQL issue
            user_posts = self.cl.user_medias_v1(random_user_id, amount=1)
            if user_posts:
                media_dict = user_posts[0].model_dump()
                print(f"{Fore.GREEN}Found a post from a followed user!")
                return str(media_dict['id'])
            else:
                print(f"{Fore.RED}No posts available from this user, trying another...")
                return None
        except Exception as e:
            print(f"{Fore.RED}Error while fetching posts from followed users: {e}")
            return None

    def get_post_id_from_hashtags(self):
        try:
            print(f"{Fore.YELLOW}Exploring posts tagged with trending hashtags...")
            medias = self.cl.hashtag_medias_recent(random.choice(self.tags), amount=1)
            if medias:
                media_dict = medias[0].model_dump()
                print(f"{Fore.GREEN}Discovered a post from hashtag search!")
                return str(media_dict['id'])
            else:
                print("Couldn't find any posts with that hashtag, retrying...")
                return None
        except Exception as e:
            print(f"{Fore.RED}Error fetching post via hashtag: {e}")
            return None

    def like_post(self, amount):
        for i in range(amount):
            # With a 40% chance, simulate scrolling to mimic organic browsing behavior
            if random.random() < 0.4:
                self.simulate_scrolling()

            # 70% chance to get a post from followed users, 30% chance from hashtags
            if random.random() < 0.7:
                random_post = self.get_post_id_from_following()
            else:
                random_post = self.get_post_id_from_hashtags()

            if random_post and random_post not in self.liked_medias:
                try:
                    self.cl.media_like(media_id=random_post)
                    self.liked_medias.append(random_post)
                    random_delay = random.randint(20, 60)
                    self.elapsed_time += random_delay
                    print(f"Total likes: {len(self.liked_medias)} | Time elapsed: {self.elapsed_time / 60:.2f} minutes | Pausing for {random_delay} seconds")
                    self.wait_time(random_delay)
                except Exception as e:
                    print(f"{Fore.RED}Error while liking the post: {e}")
            else:
                print("Skipping this post to keep things natural.")

try:
    bot = LikePost(cl)
    bot.like_post(600)
except Exception as e:
    print(f"{Fore.RED}A fatal error occurred: {e}")
    input("Press Enter to exit...")
