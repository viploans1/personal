
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
logging.basicConfig(filename='bot_errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def login_user():
    """Logs in to Instagram, handling session management."""
    cl = Client()
    session_file = "session.json"
    
    if os.path.exists(session_file):
        try:
            cl.load_settings(session_file)
            cl.login(config.username, config.password)
            cl.get_timeline_feed()
            print(f"{Fore.GREEN}Logged in using session!")
        except LoginRequired:
            print(f"{Fore.YELLOW}Session expired. Re-logging...")
            cl.set_settings({})
        except Exception as e:
            print(f"{Fore.RED}Error loading session: {e}")
            logging.error(f"Session error: {e}")

    if not cl.user_id:
        try:
            print(f"{Fore.YELLOW}Logging in with credentials...")
            cl.login(config.username, config.password)
            print(f"{Fore.GREEN}Logged in successfully!")
        except ChallengeRequired:
            print(f"{Fore.RED}Instagram requires manual verification!")
            logging.error("Login challenge required. Manual verification needed.")
            exit()
        except Exception as e:
            print(f"{Fore.RED}Login failed: {e}")
            logging.error(f"Login failed: {e}")
            exit()
    
    cl.dump_settings(session_file)
    print(f"{Fore.CYAN}Session saved successfully!")
    time.sleep(random.uniform(2, 5))
    return cl

# Proxy support (Optional)
# cl.set_proxy('http://yourproxy:port')

print(f"{Fore.BLUE}Starting Instagram Bot...")
cl = login_user()

class InstaBot:
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
        self.comment_messages = ["Awesome post! 👏", "Great content! 👍", "Love this! 🙌"]
        self.daily_like_limit = 300  # New daily limit
        self.like_count = 0
        
    def get_post_from_hashtags(self):
        try:
            selected_tag = random.choice(self.tags)
            print(f"{Fore.YELLOW}Searching posts from #{selected_tag}...")
            medias = self.cl.hashtag_medias_recent(selected_tag, amount=1)
            return str(medias[0].id) if medias else None
        except Exception as e:
            logging.error(f"Error fetching post via hashtag: {e}")
            return None
    
    def interact_with_post(self, media_id):
        if self.like_count >= self.daily_like_limit:
            print(f"{Fore.RED}Daily like limit reached! Stopping bot.")
            return False
        
        try:
            self.cl.media_like(media_id)
            print(f"{Fore.GREEN}Liked post: {media_id}")
            self.like_count += 1
            if random.random() < 0.3:
                comment = random.choice(self.comment_messages)
                self.cl.media_comment(media_id, comment)
                print(f"{Fore.CYAN}Commented: {comment}")
            return True
        except Exception as e:
            logging.error(f"Error interacting with post {media_id}: {e}")
            return False
    
    def wait_time(self, delay):
        print(f"{Fore.YELLOW}Waiting {delay}s...")
        time.sleep(delay)
    
    def run(self, amount):
        for _ in range(amount):
            post_id = self.get_post_from_hashtags()
            if post_id and post_id not in self.liked_medias:
                if self.interact_with_post(post_id):
                    self.liked_medias.append(post_id)
                    self.wait_time(random.randint(20, 60))
                else:
                    print(f"{Fore.RED}Skipping post due to error.")
            else:
                print(f"{Fore.YELLOW}Skipping duplicate or unavailable post.")

try:
    bot = InstaBot(cl)
    bot.run(50)
except Exception as e:
    logging.error(f"Fatal error: {e}")
    print(f"{Fore.RED}A fatal error occurred: {e}")
