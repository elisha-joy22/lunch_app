from slack_sdk.errors import SlackApiError


def post_content(app,channel_id,text,blocks=None):
    try:
        response = app.client.chat_postMessage(
            channel=channel_id,
            text=text,
            blocks=blocks
        )
        return response
    except SlackApiError as e:
        print(f"Error posting content: {e.response['error']}")