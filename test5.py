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
        self.followed_users = set()  # Track users you have already followed
        self.elapsed_time = 0

    def wait_time(self, delay):
        messages = [
            "Taking a quick break", 
            "Pausing for a moment", 
            "Resting for a bit", 
            "Catching my breath"
        ]
        msg = random.choice(messages)
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}{msg}... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Break over, back to action!               ")

    def wait_for_api(self, delay):
        messages = [
            "Hunting for interesting posts", 
            "Searching for fresh content", 
            "Looking around for posts"
        ]
        msg = random.choice(messages)
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}{msg}... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Found some posts! Let's proceed.               ")

    def simulate_scrolling(self):
        scroll_delay = random.randint(5, 15)
        messages = [
            "Scrolling through feed", 
            "Glancing at the timeline", 
            "Browsing the posts"
        ]
        msg = random.choice(messages)
        print(f"{Fore.MAGENTA}{msg} for {scroll_delay} seconds...")
        time.sleep(scroll_delay)
        print(f"{Fore.MAGENTA}Done scrolling.")

    def simulate_view_post(self):
        view_delay = random.randint(3, 10)
        messages = [
            "Taking a closer look at a post", 
            "Viewing post details", 
            "Checking out post content"
        ]
        msg = random.choice(messages)
        print(f"{Fore.CYAN}{msg} for {view_delay} seconds...")
        time.sleep(view_delay)
        print(f"{Fore.CYAN}Finished viewing.")

    def simulate_story_view(self):
        story_delay = random.randint(5, 15)
        print(f"{Fore.CYAN}Viewing stories for {story_delay} seconds...")
        time.sleep(story_delay)
        print(f"{Fore.CYAN}Finished viewing stories.")

    def simulate_long_break(self):
        long_break = random.randint(300, 600)  # 5 to 10 minutes
        messages = [
            "Taking a long break", 
            "Stepping away for a bit", 
            "Pausing for an extended rest"
        ]
        msg = random.choice(messages)
        print(f"{Fore.RED}{msg} for {long_break // 60} minutes...")
        time.sleep(long_break)
        print(f"{Fore.RED}Long break over, resuming activity.")

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

    def auto_follow_by_hashtag(self, hashtag, amount=5):
        """
        Follow users based on a specific hashtag.
        """
        print(f"{Fore.YELLOW}Attempting to follow users who post with #{hashtag}...")
        try:
            medias = self.cl.hashtag_medias_recent(hashtag, amount=amount)
            for media in medias:
                user_id = media.user.pk
                if user_id not in self.followed_users:
                    try:
                        self.cl.user_follow(user_id)
                        self.followed_users.add(user_id)
                        print(f"{Fore.GREEN}Followed user {user_id}")
                        time.sleep(random.randint(10, 30))
                    except Exception as e:
                        print(f"{Fore.RED}Error following user {user_id}: {e}")
        except Exception as e:
            print(f"{Fore.RED}Error fetching hashtag posts for follow: {e}")

    def auto_comment(self, post_id, comment_list):
        """
        Comment on a post using a random comment from a list.
        """
        comment = random.choice(comment_list)
        try:
            self.cl.media_comment(media_id=post_id, text=comment)
            print(f"{Fore.GREEN}Commented on post {post_id} with: {comment}")
        except Exception as e:
            print(f"{Fore.RED}Error commenting on post {post_id}: {e}")

    def auto_unfollow(self):
        """
        Unfollow users who haven't followed you back.
        """
        try:
            followers = self.cl.user_followers(self.cl.user_id)
            follower_ids = set(followers.keys())
            unfollowed = 0
            for user_id in list(self.followed_users):
                if user_id not in follower_ids:
                    try:
                        self.cl.user_unfollow(user_id)
                        self.followed_users.remove(user_id)
                        print(f"{Fore.YELLOW}Unfollowed user {user_id} (not following back)")
                        unfollowed += 1
                        time.sleep(random.randint(10, 30))
                    except Exception as e:
                        print(f"{Fore.RED}Error unfollowing user {user_id}: {e}")
            print(f"{Fore.GREEN}Auto-unfollow complete. Unfollowed {unfollowed} users.")
        except Exception as e:
            print(f"{Fore.RED}Error during auto-unfollow: {e}")

    def like_post(self, amount):
        # Predefined list of human-like emoji comments for engagement
        comment_list = [
            "📸🔥😍", "❤️👌✨", "🤩👏🔥", "🙌💯🔥", "😎👌👍", 
            "👍👏😊", "🌟✨📸", "🔥💥🙌", "😍👏💖", "💯🔥😱", 
            "👌🤩🌈", "🙌✨👏", "😃💖📸", "👏😍🔥", "🔥🔥🔥", 
            "💯🙌✨", "🎉👏😍", "😍💖🔥", "🤩👏🌟", "👌🔥💯"
        ]
        for i in range(amount):
            # Simulate natural behavior with varied actions:
            if random.random() < 0.4:
                self.simulate_scrolling()
            if random.random() < 0.2:
                self.simulate_view_post()
            if random.random() < 0.1:
                self.simulate_long_break()
            if random.random() < 0.2:
                self.simulate_story_view()
            # Every 200 likes, perform an auto-unfollow check
            if i != 0 and i % 200 == 0:
                self.auto_unfollow()
            
            # Occasionally follow users from a specific hashtag to boost your followers
            if random.random() < 0.3:
                self.auto_follow_by_hashtag(random.choice(self.tags), amount=3)
            
            # 70% chance to get a post from followed users, 30% chance from hashtags
            if random.random() < 0.7:
                random_post = self.get_post_id_from_following()
            else:
                random_post = self.get_post_id_from_hashtags()

            if random_post and random_post not in self.liked_medias:
                try:
                    self.cl.media_like(media_id=random_post)
                    self.liked_medias.append(random_post)
                    
                    # 5% chance to add the post to your story after liking it.
                    if random.random() < 0.05:
                        try:
                            self.cl.media_repost_to_story(media_id=random_post)
                            print(f"{Fore.GREEN}Added post {random_post} to your story!")
                        except Exception as e:
                            print(f"{Fore.RED}Error adding post {random_post} to story: {e}")
                    
                    # Occasionally comment on the post for extra engagement
                    if random.random() < 0.3:
                        self.auto_comment(random_post, comment_list)
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
