import os.path
import pickle
import random

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Credentials:

    def get_token(self):
        credentials = None

        # token.pickle stores the user's credentials from previously successful logins
        if os.path.exists("token.pickle"):
            print("Loading credentials from file...")
            with open("token.pickle", "rb") as token:
                credentials = pickle.load(token)


        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print("Refreshing Access token...")
                credentials.refresh(Request())
            else:
                print("Fetching new tokens...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secrets.json",
                    scopes=["https://www.googleapis.com/auth/youtube.readonly"]
                )
                flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
                credentials = flow.credentials

                with open("token.pickle", "wb") as f:
                    print("Saving New credentials to file...")
                    pickle.dump(credentials, f)

        return credentials

    def get_api_key(self):
        return "AIzaSyBywJQPr7ii0OKbrBnCLgkC_SK-3BBdsRU"


class UserComments:
    def __init__(self, api_key, video_id):
        self.video_id = video_id
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def grab_and_process_comments(self, response):
        comments_dict = {}
        items = response.get("items")
        if not items:
            print("Sorry, no comments for this video")
        else:
            for comment_info in items:
                comment = comment_info.get("snippet").get("topLevelComment").get("snippet").get("textDisplay")
                author_name = comment_info.get("snippet").get("topLevelComment").get("snippet").get("authorDisplayName")
                author_channel = comment_info.get("snippet").get("topLevelComment").get("snippet").get(
                    "authorChannelUrl")
                comments_dict[author_name] = (comment, author_channel)

        return comments_dict


    def make_comments_request(self, next_page_token=None):
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=self.video_id,
            maxResults=100,
            order="relevance",
            pageToken=next_page_token
        )
        response = request.execute()
        next_page_token = response.get("nextPageToken")

        return response, next_page_token


    def get_comments_by_video_id(self):
        total_comments = {}
        response, next_page_token = self.make_comments_request()

        while True:
            total_comments.update(self.grab_and_process_comments(response))
            if not next_page_token:
                break

            response, next_page_token = self.make_comments_request(next_page_token)

        return total_comments


class ChannelSubscriptions:

    def __init__(self, credentials, channel_id="UCe6sH8zuzfo2YMUd9F0Brwg"):
        self.channel_id = channel_id
        self.credentials = credentials
        self.youtube = build("youtube", "v3", credentials=self.credentials)

    def grab_and_process_subscribers(self, response):
        sub_dict = {}
        items = response.get("items")
        if not items:
            print("Sorry, you have no subscribers")
        else:
            for sub_info in items:
                subscriber_name = sub_info.get("subscriberSnippet").get("title")
                subscriber_channel = f"https://www.youtube.com/channel/{sub_info.get('subscriberSnippet').get('channelId')}"
                sub_dict[subscriber_name] = subscriber_channel

        return sub_dict

    def make_subscriptions_request(self, next_page_token=None):
        request = self.youtube.subscriptions().list(
            part="subscriberSnippet",
            mySubscribers=True,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        next_page_token = response.get("nextPageToken")

        return response, next_page_token

    def get_all_subscribers(self):
        total_subscribers = {}
        response, next_page_token = self.make_subscriptions_request()

        while True:
            total_subscribers.update(self.grab_and_process_subscribers(response))
            if not next_page_token:
                break

            response, next_page_token = self.make_subscriptions_request(next_page_token)

        return total_subscribers


def print_all_subscribers(subs: dict):
    for name, url in subs.items():
        print(f"{name}:\t\t{url}")
    print("")
    print("")


def print_all_comments(comments: dict):
    for name, info in comments.items():
        print(f"{name}:\t\t{info[0]} --->>> {info[1]}")

    print("")
    print("")


if __name__ == "__main__":

    #TODO Take into account keyword to filter comments

    # Set video id
    video_id="biSOwmA0tLg"

    # Init Credentials
    credentials = Credentials()

    # Get all subscribers
    subscriptions = ChannelSubscriptions(credentials.get_token())
    subscriptions_dict = subscriptions.get_all_subscribers()

    # print_all_subscribers(subscriptions_dict)

    comments = UserComments(credentials.get_api_key(), video_id)
    comments_dict = comments.get_comments_by_video_id()

    # print_all_comments(comments_dict)

    subs_set = set(subscriptions_dict.keys())
    comments_set = set(comments_dict.keys())

    intersection_list = list(subs_set.intersection(comments_set))

    # print(f"result is: {intersection_list}")

    winner = random.choice(intersection_list)

    print("\n======================================================\n")
    print(f"And the winner is... {winner}")
    print("\n======================================================\n")
    print(f"The prize for comment: {comments_dict.get(winner)[0]}")
    print("\n======================================================\n")