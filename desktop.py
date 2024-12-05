import os
import pygame
from pygame import mixer
from gtts import gTTS
from io import BytesIO
from PIL import Image
import tempfile
import time

# Initialize pygame
pygame.init()

# Set up display for full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("A for Apple to Z for Zebra")

# Get the desktop path
if os.name == 'nt':  # Windows
    desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
else:  # Linux/Mac
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 150, 200)
HOVER_COLOR = (150, 200, 250)

# Alphabet data with local file paths
alphabet_data = {
    'A': {'word': 'Apple', 'image_path': os.path.join(desktop_path, 'A.jpg')},
    'B': {'word': 'Ball', 'image_path': os.path.join(desktop_path, 'B.jpg')},
    'C': {'word': 'Cat', 'image_path': os.path.join(desktop_path, 'C.jpg')},
    'D': {'word': 'Dog', 'image_path': os.path.join(desktop_path, 'D.jpg')},
    'E': {'word': 'Elephant', 'image_path': os.path.join(desktop_path, 'E.jpg')},
    'F': {'word': 'Fish', 'image_path': os.path.join(desktop_path, 'F.jpg')},
    'G': {'word': 'Giraffe', 'image_path': os.path.join(desktop_path, 'G.jpg')},
    'H': {'word': 'Horse', 'image_path': os.path.join(desktop_path, 'H.jpg')},
    'I': {'word': 'Ice Cream', 'image_path': os.path.join(desktop_path, 'I.jpg')},
    'J': {'word': 'Jaguar', 'image_path': os.path.join(desktop_path, 'J.jpg')},
    'K': {'word': 'Kangaroo', 'image_path': os.path.join(desktop_path, 'K.jpg')},
    'L': {'word': 'Lion', 'image_path': os.path.join(desktop_path, 'L.jpg')},
    'M': {'word': 'Monkey', 'image_path': os.path.join(desktop_path, 'M.jpg')},
    'N': {'word': 'Nest', 'image_path': os.path.join(desktop_path, 'N.jpg')},
    'O': {'word': 'Owl', 'image_path': os.path.join(desktop_path, 'O.jpg')},
    'P': {'word': 'Penguin', 'image_path': os.path.join(desktop_path, 'P.jpg')},
    'Q': {'word': 'Queen', 'image_path': os.path.join(desktop_path, 'Q.jpg')},
    'R': {'word': 'Rabbit', 'image_path': os.path.join(desktop_path, 'R.jpg')},
    'S': {'word': 'Sun', 'image_path': os.path.join(desktop_path, 'S.jpg')},
    'T': {'word': 'Tiger', 'image_path': os.path.join(desktop_path, 'T.jpg')},
    'U': {'word': 'Umbrella', 'image_path': os.path.join(desktop_path, 'U.jpg')},
    'V': {'word': 'Violin', 'image_path': os.path.join(desktop_path, 'V.jpg')},
    'W': {'word': 'Whale', 'image_path': os.path.join(desktop_path, 'W.jpg')},
    'X': {'word': 'Xylophone', 'image_path': os.path.join(desktop_path, 'X.jpg')},
    'Y': {'word': 'Yacht', 'image_path': os.path.join(desktop_path, 'Y.jpg')},
    'Z': {'word': 'Zebra', 'image_path': os.path.join(desktop_path, 'Z.jpg')},
}

# Function to load image from local file
def load_image_from_file(path):
    try:
        image = pygame.image.load(path)
        return image
    except Exception as e:
        print(f"Could not load image from path {path}: {e}")
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
    image_path = alphabet_data[letter]['image_path']

    try:
        image = load_image_from_file(image_path)
        image = pygame.transform.scale(image, (400, 300))
        screen.blit(image, (screen.get_width() // 2 - 200, screen.get_height() // 2 - 150))
    except Exception as e:
        print(f"Could not load image for {letter}: {e}")

    font = pygame.font.Font(None, 74)
    text = font.render(f"{letter} for {word}", True, BLACK)
    screen.blit(text, (screen.get_width() // 2 - 100, 50))

    speak_text(f"{letter} for {word}")

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to exit full-screen mode
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            next_button.handle_event(event, next_image)
            back_button.handle_event(event, prev_image)

    pygame.time.delay(100)

pygame.quit()
