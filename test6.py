import random
import time
import os
import logging
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired
import config
from colorama import Fore, init

# Initialize colorama for colored output
init(autoreset=True)

# Set up logging
logging.basicConfig(filename="bot.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

class InstagramBot:
    def __init__(self):
        self.cl = Client()
        self.session_file = "session.json"
        self.liked_medias = []
        self.followed_users = set()
        self.elapsed_time = 0
        self.daily_like_limit = random.randint(189, 205)
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
        self.comment_list = [
            "Amazing! 🔥", "Love this! 😍", "Great post! 👏", "Incredible view! 😎", "Beautiful home! 🏡",
            "So inspiring! 🙌", "Great info! 💡", "Superb content! 🎯", "Awesome work! 🔥", "Love it! 💖"
        ]

    def login(self):
        """Logs in using session or credentials."""
        try:
            if os.path.exists(self.session_file):
                self.cl.load_settings(self.session_file)
                self.cl.login(config.username, config.password)
                self.cl.get_timeline_feed()
                print(f"{Fore.GREEN}Logged in using session!")
                return
        except LoginRequired:
            print(f"{Fore.YELLOW}Session expired. Logging in again...")
        except Exception as e:
            logger.error(f"Session error: {e}")

        try:
            self.cl.login(config.username, config.password)
            print(f"{Fore.GREEN}Logged in with username and password!")
            self.cl.dump_settings(self.session_file)
        except ChallengeRequired:
            print(f"{Fore.RED}Instagram requires verification. Complete verification manually.")
        except Exception as e:
            logger.error(f"Login failed: {e}")
            print(f"{Fore.RED}Login failed. Check logs for details.")

    def simulate_behavior(self):
        """Mimics human scrolling and engagement behavior."""
        actions = ["Scrolling feed", "Checking out a profile", "Watching stories", "Taking a break"]
        action = random.choice(actions)
        delay = random.randint(5, 20)
        print(f"{Fore.MAGENTA}{action} for {delay} seconds...")
        time.sleep(delay)
        print(f"{Fore.MAGENTA}Done.")

    def like_post(self):
        """Likes posts intelligently, avoiding spam triggers and staying within the daily limit."""
        for i in range(self.daily_like_limit):
            if random.random() < 0.3:
                self.simulate_behavior()

            post_id = self.get_post_id()
            if post_id and post_id not in self.liked_medias:
                try:
                    self.cl.media_like(post_id)
                    self.liked_medias.append(post_id)
                    print(f"{Fore.GREEN}Liked post {post_id}")
                    if random.random() < 0.2:
                        self.comment_on_post(post_id)
                    self.wait(random.randint(30, 90))
                except Exception as e:
                    logger.error(f"Error liking post: {e}")
            else:
                print(f"{Fore.YELLOW}Skipping post to maintain natural behavior.")

    def comment_on_post(self, post_id):
        """Comments on a post."""
        try:
            comment = random.choice(self.comment_list)
            self.cl.media_comment(post_id, comment)
            print(f"{Fore.BLUE}Commented on post {post_id}: {comment}")
        except Exception as e:
            logger.error(f"Error commenting: {e}")

if __name__ == "__main__":
    print(f"{Fore.BLUE}Starting Instagram Bot...")
    bot = InstagramBot()
    bot.login()
    bot.like_post()
