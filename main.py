from io import BytesIO
import random
import requests
from pexelsapi.pexels import Pexels
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from myConstants import *
import time
from env import *

# tags = "coding|tech|mathematics|developer|inspirational"



pexel = Pexels(PEXELS_KEY)

def generate_path():
    """
    Generate a unique path for a quote image based on timestamp.

    Returns:
        str: The path of the generated quote image.
    """
    timestamp = int(time.time())
    return f"/tmp/quote_{timestamp}.jpg"
 
def get_quote(tags) -> str:
    """
    Retrieves a quote from the QUOTE_API based on the provided tags.

    Args:
        tags (str): A string of tags to filter the quote by, separated by |.

    Returns:
        str: The content of the retrieved quote.
    """
        
    
    URL = QUOTE_API + "?tags=" + tags
    data = requests.get(URL).json()

    if (len(data) == 0):
        # If no quotes are found, trying default tags: 
        print("No quotes found. Trying default tags...")
        URL = QUOTE_API + "?tags=" + "Inspirational|Motivation|Life|Happy"

        data = requests.get(URL).json()
        
    quote = data[0].get("content")
    return quote


def get_random_photo(img_queries):
    photos_dict = pexel.search_photos(random.choice(img_queries),
                                      size="small",
                                      per_page=NUMBER_OF_IMAGES)

    # If no enough photos matching the query are found, run again with default tags
    if not photos_dict.get("photos") or (len(photos_dict.get("photos")) < NUMBER_OF_IMAGES):
        return get_random_photo(["Life", "Health", "Tech", "Goal", "Physics"])

    photo_index = random.randint(0, NUMBER_OF_IMAGES - 1)
    random_photo = photos_dict.get("photos")[photo_index]
    return random_photo


def get_image_from_url(image_url):
    image_response = requests.get(image_url)
    image_data = BytesIO(image_response.content)
    image = Image.open(image_data)
    brightness_controller = ImageEnhance.Brightness(image)
    image = brightness_controller.enhance(0.3)  #30%
    return image

   
def process_image(image, text, text_x, text_y, file_path):
    d = d1 = ImageDraw.Draw(image)

    font = ImageFont.truetype("BebasNeue-Regular.ttf", 60)
    d1.multiline_text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    image.save(file_path)


def create_image(interests):
    """
    Generates a new image with a random photo and a quote.
    
    Args:
        interests (str): A single string of topics or interests separated by comma.
        
    Returns:
        str: The file path of the generated image.
    """
    img_queries = interests.split(",") #creating a list from the interests 
    photo = get_random_photo(img_queries)

    image_url = photo.get("src").get("portrait")
    image_width = photo.get("width")
    image_height = photo.get("height")
    image = get_image_from_url(image_url)

    quote_tags = interests.replace(",", "|") #replacing comma with |
    quote = get_quote(tags=quote_tags)
    words = quote.split()

    index = 4
    for i in range(0, len(words)):
        words.insert(index, "\n")
        index += 4

    quote = " " + " ".join(words)
    
    path = generate_path()
    
    process_image(image, quote, 20, 200, file_path=path)

    return path
   
