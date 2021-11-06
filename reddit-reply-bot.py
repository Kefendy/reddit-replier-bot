#!/usr/bin/env python3

import praw
import random
import config

class Bot:

    def __init__(
            self,
            client_id,
            client_secret,
            username,
            password,
            user_agent,
            path_to_quotes,
            subreddit_name,
            trigger
        ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.user_agent = user_agent
        self.path_to_quotes = path_to_quotes
        self.subreddit_name = subreddit_name
        self.trigger = trigger.lower()

        with open(self.path_to_quotes) as f:
            self.quotes = [q.lower() for q in f.read().split('\n') if q]

        self.number_quotes = len(self.quotes)

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            username=self.username,
            password=self.password
        )

        self.subreddit = self.reddit.subreddit(self.subreddit_name)

        self.reset_buffer()

    def reset_buffer(self):
        self.used_quotes = []
        self.unused_quotes = list(range(self.number_quotes))

    def get_quotes(self):
        return self.quotes 

    def contains_trigger(self, comment):
        return self.trigger in str(comment.body).lower()

    def get_random_quote(self, comment):
        if not self.unused_quotes:
            self.reset_buffer()
 
        random_int = random.choice(self.unused_quotes)
        random_quote = self.quotes[random_int]

        author = '/u/' + str(comment.author)
        random_quote = random_quote.replace('!USERNAME', author)

        self.unused_quotes.remove(random_int)
        self.used_quotes.append(random_int)

        return random_quote

    def welcome_message(self):
        print('Posting as /u/' + self.username, 'on /r/' + self.subreddit_name)
        print('Trigger word is', self.trigger)
        print('Use <Ctrl> + c to exit')

    def start_stream(self):
        self.welcome_message()
        for comment in self.subreddit.stream.comments():
            trigger_status = self.contains_trigger(comment)
            same_author = str(comment.author).lower == config.username.lower()

            if trigger_status and not same_author:
                random_quote = self.get_random_quote(comment)
                comment.reply(random_quote)

def main():
    bot = Bot(
        client_id = config.client_id,
        client_secret = config.client_secret, 
        username = config.username, 
        password = config.password, 
        user_agent = config.user_agent, 
        path_to_quotes = config.path_to_quotes,
        subreddit_name = config.subreddit_name,
        trigger = config.trigger
    )

    bot.start_stream()

if __name__ == '__main__':
    main()
