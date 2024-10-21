import os
import atproto
import requests

def scrape_user_tweets(username: str, num_tweets=10, mock: bool = False) -> list[dict]:
    print(f'\nProfile Posts of {username}:\n\n')

    client = atproto.Client()
    client.login(os.environ.get('BLUESKY_USERNAME'),os.environ.get('BLUESKY_PASSWORD'))

    profile_feed = client.get_author_feed(actor=username, limit=num_tweets)

    bsky_list = []

    for feed_view in profile_feed.feed:
        bsky_dict = {}

        bsky_dict["time_posted"] = feed_view.post.indexed_at
        bsky_dict["text"] = feed_view.post.record.text
        post_id = feed_view.post.uri.split('/')[-1]
        bsky_dict["url"] = f"https://bsky.app/profile/{username}/post/{post_id}"

        bsky_list.append(bsky_dict)

    return bsky_list

if __name__ == "__main__":
    #input_handle = 'jeffgerstmann.com'
    input_handle ='pkrugman.bsky.social'
    output = scrape_user_tweets(username=input_handle)

    print(output)