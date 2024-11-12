import pygame
from gtts import gTTS
import requests
from io import BytesIO
from PIL import Image
import os
import tempfile
import time

# Initialize pygame
pygame.init()

# Set up display for full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("A for Apple to Z for Zebra")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 150, 200)
HOVER_COLOR = (150, 200, 250)

# Alphabet data with words and image URLs (currently set to the first two letters for testing)
alphabet_data = {
    'A': {'word': 'Apple', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg'},
    'B': {'word': 'Ball', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png'},
    'C': {'word': 'Cat', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg'},
    'D': {'word': 'Dog', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Golde33443.jpg'},
    'E': {'word': 'Elephant', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/e/e1/Elephant_in_Ampara_%282022%29.jpg'},
    'F': {'word': 'Fish', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/1/17/Goldfish3.jpg'},
    'G': {'word': 'Giraffe', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/9f/Giraffe_standing.jpg'},
    'H': {'word': 'Horse', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/4d/Horse_at_paddock.jpg'},
    'I': {'word': 'Ice Cream', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6f/Ice_cream_cone.jpg'},
    'J': {'word': 'Jaguar', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/4c/Jaguar_head_shot.jpg'},
    'K': {'word': 'Kangaroo', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/0/0f/Kangaroo_Australia_01.jpg'},
    'L': {'word': 'Lion', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/73/Lion_waiting_in_Namibia.jpg'},
    'M': {'word': 'Monkey', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/21/Monkey_face.jpg'},
    'N': {'word': 'Nest', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/48/Bird_nest.jpg'},
    'O': {'word': 'Owl', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/e/ec/Great_Horned_Owl%2C_Bubo_virginianus.jpg'},
    'P': {'word': 'Penguin', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Emperor_Penguin_manuel_ANTARCTIQUE.jpg'},
    'Q': {'word': 'Queen', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Playing_card_heart_Q.svg'},
    'R': {'word': 'Rabbit', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/0/0b/Rabbit_in_montana.jpg'},
    'S': {'word': 'Sun', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/c/c3/Solar_prominence_from_STEREO_spacecraft.jpg'},
    'T': {'word': 'Tiger', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/5/56/Tiger.50.jpg'},
    'U': {'word': 'Umbrella', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Umbrella_with_Mount_Mayon.jpg'},
    'V': {'word': 'Violin', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/5/58/Violin_VL100.jpg'},
    'W': {'word': 'Whale', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Humpback_whale_NOAA.jpg'},
    'X': {'word': 'Xylophone', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Wooden_xylophone.jpg'},
    'Y': {'word': 'Yacht', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Yacht%2C_French_Riviera.jpg'},
    'Z': {'word': 'Zebra', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Zebra_Botswana_edit02.jpg'}
}


# Download and convert image from URL
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # Check if the response contains an image
        if 'image' not in response.headers['Content-Type']:
            print(f"URL does not contain an image: {url}")
            return None

        # Load the image using PIL
        image = Image.open(BytesIO(response.content))
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    except Exception as e:
        print(f"Could not load image from URL {url}: {e}")
        return None


# Function to speak the text
def speak_text(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
        temp_audio_file_path = temp_audio_file.name
        tts = gTTS(text=text, lang='en')
        tts.save(temp_audio_file_path)

    pygame.mixer.music.load(temp_audio_file_path)
    pygame.mixer.music.set_volume(1.0)  # Set volume to maximum
    pygame.mixer.music.play()

    # Wait until the playback is finished
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)

    pygame.mixer.music.unload()
    os.remove(temp_audio_file_path)  # Clean up the temp file after playback

# Button class for navigation


class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = BUTTON_COLOR
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_event(self, event, callback):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered():
            callback()

# Navigation functions


def next_image():
    global current_index
    if current_index < len(alphabet_keys) - 1:
        current_index += 1
        update_display()
    else:
        speak_text("No more letters")


def prev_image():
    global current_index
    if current_index > 0:
        current_index -= 1
        update_display()

# Update display with the current image and text


def update_display():
    screen.fill(WHITE)
    letter = alphabet_keys[current_index]
    word = alphabet_data[letter]['word']
    image_url = alphabet_data[letter]['image_url']

    # Load and display the image
    try:
        image = load_image_from_url(image_url)
        image = pygame.transform.scale(image, (400, 300))
        screen.blit(image, (screen.get_width() // 2 -
                    200, screen.get_height() // 2 - 150))
    except Exception as e:
        print(f"Could not load image for {letter}: {e}")

    # Display the text
    font = pygame.font.Font(None, 74)
    text = font.render(f"{letter} for {word}", True, BLACK)
    screen.blit(text, (screen.get_width() // 2 - 100, 50))

    # Play the audio for the current letter and word
    speak_text(f"{letter} for {word}")

    # Draw navigation buttons
    for button in [next_button, back_button]:
        button.color = HOVER_COLOR if button.is_hovered() else BUTTON_COLOR
        button.draw(screen)

    pygame.display.flip()


# Set up navigation buttons
next_button = Button("Next", (1200, 650), (150, 70))
back_button = Button("Back", (100, 650), (150, 70))

# Main loop
running = True
alphabet_keys = list(alphabet_data.keys())
current_index = 0
update_display()  # Initial display

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to exit full-screen mode
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check button clicks
            next_button.handle_event(event, next_image)
            back_button.handle_event(event, prev_image)

    pygame.time.delay(100)

pygame.quit()
