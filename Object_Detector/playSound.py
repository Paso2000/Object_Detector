import pygame
import os

def playSound():
    """
    Initializes the Pygame mixer and plays a sound file.

    This function sets up the Pygame mixer module and loads a specified audio file
    from the project directory. Once loaded, it begins playback of the audio file.

    The sound file is expected to be located in a 'sound' directory within the
    project root directory. The audio file should be in a compatible format, 
    such as MP3.

    Returns:
    - None: The function does not return any value. It plays the sound in the background.
    """
    pygame.mixer.init()  # Initialize the Pygame mixer
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # Get the project root directory
    sound_path = os.path.join(PROJECT_ROOT, 'sound/alarm.mp3')  # Construct the full path to the sound file
    pygame.mixer.music.load(sound_path)  # Load the sound file
    pygame.mixer.music.play(-1)  # Play the sound in loop


def stop_sound():
    """
    Stops any currently playing sound.

    This function initializes the Pygame mixer (if not already initialized)
    and stops the playback of the currently loaded audio. If no sound is playing,
    this function will have no effect.

    Returns:
    - None: The function does not return any value. It simply stops the audio playback.
    """
    pygame.mixer.init()  # Initialize the Pygame mixer
    pygame.mixer.music.stop()  # Stop the currently playing music