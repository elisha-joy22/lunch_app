# slack_integration/slack_init.py

from slack_bolt import App
import os

# Initialize the Slack Bolt app

slack_app = App(
    token=os.environ.get("SLACK_LUNCH_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
