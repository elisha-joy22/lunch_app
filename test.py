from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Function to superimpose profile picture onto another image
def superimpose_images(background_url, profile_pic_url, text):
    # Download background image
    response_bg = requests.get(background_url)
    bg_image = Image.open(BytesIO(response_bg.content))

    # Download profile picture
    response_profile = requests.get(profile_pic_url)
    profile_pic = Image.open(BytesIO(response_profile.content))
    # Resize profile picture to fit within the background image
    profile_pic = profile_pic.resize((100, 100))  # Adjust size as needed

    # Superimpose profile picture onto background image at top-left corner
    bg_image.paste(profile_pic, (0, 0))  # Adjust position as needed


    # Define text properties
    font = ImageFont.load_default()
    text_color = "white"
    text_position = (bg_image.width-340, bg_image.height-455)

    # Draw filled rectangle as background for text
    draw = ImageDraw.Draw(bg_image)
    rect_start = (text_position[0]-10, text_position[1]-3)
    rect_end = (text_position[0] + 70, text_position[1] + 15) 
    draw.rectangle([rect_start, rect_end], fill="black")

    # Draw text on top of the filled rectangle
    draw.text(text_position, text, fill=text_color, font=font)

    # Save the superimposed image
    bg_image.save("superimposed_image.jpg")
    print("superimposed image created successfully!!")
    return "super"

# URLs of the background image and profile picture
background_url = "https://picsum.photos/id/1/350/550"
profile_pic_url = "https://avatars.slack-edge.com/2023-04-03/5046848306597_ccb54a0b69ea4f096630_192.jpg"
text_to_display = "21-08-2024"  

superimpose_images(background_url,profile_pic_url,text_to_display)