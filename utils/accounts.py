from accounts.models import CustomUser


def update_or_create_user(user):
    try:
        print('inside update_or_create user')
        returned_user = CustomUser.objects.update_or_create(
                                                slack_id=user.get('slack_id'),                                        #returns boolean true if new obj created
                                                defaults=user
                        )[0]
    except CustomUser.DoesNotExist:
        print ("{'error':'User creation falied!!'}")
    
    return returned_user



def create_user_info(user_info_response):
    user_info = {
                    "slack_id" : user_info_response.get("https://slack.com/user_id"),
                    "email" : user_info_response.get("email"),
                    "name" : user_info_response.get("name"),
                    "picture_url": user_info_response.get("https://slack.com/user_image_48")
                }        
    return user_info