"""
Script used for manual classification of images. The script loads the images in the 'dataset' folder and then display
a GUI to label these images.

Input:
    - '-categories': List of categories to label these images into (i.e -categories Cat Dog Tiger)
    - '-keys': List of keyboard key to label the images into their respective category (i.e -keys c d t)
            Can also takes directional arrow as keys with 'Left', 'Right', 'Up', 'Down'

Examples:
    python label_images.py -categories Dog Cat -keys Left Right
    python label_images.py -categories Dog Cat Tiger -keys d c t
"""

import matplotlib
import os
import glob2 as glob
from PIL import ImageTk
import tkinter as tk  # Used for GUI
import argparse

matplotlib.use("TkAgg") # For compatibility purpose


class Window:
    """
        Class used to instantiate a manual labeling GUI. When created, the class load the different images and
        wait for keyboard input to label the images and change the displayed image.
    """
    def __init__(self, window, dict_cat):
        """
            Initialization of the Window class
        :param window: tkinter window
        :param dict_cat: dictionary where the keys are the keyboard touch to press and the values the corresponding
        categories
        """
        self.filenames = glob.glob('dataset/*')
        self.number_of_images = len(self.filenames)
        self.categories = dict_cat

        # Size of the window
        self.width = 700
        self.height = 600

        # Create a canvas inside the window to plot the images
        self.cv = tk.Canvas(window, width=self.width, height=self.height)
        self.cv.pack(side='top', fill='both', expand='yes')

        # Load all images using the tkinter library to plot them inside the window
        # Currently all images must be loaded at the beginning of the script
        # TODO: Find a way to load the images progressively instead of all at once
        self.all_images = [ImageTk.PhotoImage(file=self.filenames[j]) for j in range(self.number_of_images)]

        # Display the first image inside the canvas
        self.image_id = self.cv.create_image(0, 0, image=self.all_images[0], anchor='nw')

        # Increment used for navigating through the list of images
        self.i = 0

        # Iterate over the dictionary to bind the keyboard pressing events to the function that change the images
        for key, value in self.categories.items():
            window.bind('<'+key+'>', self.key_touch)

        # Use the space key when the classification is neither of the categories
        window.bind('<space>', self.key_touch)



    def key_touch(self, event):
        """
            Function triggered by a keyboard event. Depending on the key pressed, the function move the current
            image into its respective category and change the image.
        :param event: Keyboard press event
        """

        self.test_if_image_exist()

        # Get the pressed key and its respective category
        key = event.keysym
        if key == 'space': # Other category
            os.rename(self.filenames[self.i], "Other/" + os.path.basename(self.filenames[self.i]))
        else:
            category = self.categories[key]
            # Move the image to its respective category folder
            os.rename(self.filenames[self.i], category + "/" + os.path.basename(self.filenames[self.i]))

        # Display the next image on the window
        self.cv.delete(self.image_id)
        self.image_id = self.cv.create_image(0, 0, image=self.all_images[self.i+1], anchor='nw')
        # Increase the increment to get the next image
        self.i = self.i + 1

    def test_if_image_exist(self):
        """
            Function used to test if there is still images in the folder to label.
            If not raise an exception.
        """
        if self.i == len(self.filenames)-1:
            self.cv.delete(self.image_id)
            raise Exception('No image to be labeled')

    def write_button_choice(self):
        """
            Function used to write the keyboard keys for each class on the canva
        """
        # Define the text to be displayed
        txt = "Button press: \n \n"
        # Iterate over the dictionary to display the category and its respective key on the window
        for key, value in self.categories.items():
            txt += value + ': ' + key + '\n'
        txt += 'Space: Other'
        # Display the text on the canva
        self.cv.create_text(600, 200, fill="black", font="Times 20 bold", text=txt)


def manual_classification(args):
    """
        Main function. This function runs the script by declaring the tkinter window.
    :param args: Script arguments containing the categories and the keys to be pressed
    """

    if not os.path.isdir("dataset"):
        raise Exception('Dataset folder not found')

    # Declare the GUI window
    window = tk.Tk()
    window.title('Manual Image Classification')

    # Construct a dictionary from the list of categories and keyboard keys passed as arguments
    try:
        categories = dict(zip(args.keys,args.categories))
    except Exception:
        raise Exception('Error in arguments input')

    # Declare the Window Class to create the canvas
    W = Window(window, categories)
    # Display the possibles key input
    W.write_button_choice()

    # Create a folder for each category if not already done
    for key, value in categories.items():
        if not os.path.isdir(value):
            os.makedirs(value)
    if not os.path.isdir("Other"):
        os.makedirs("Other")

    # Display the window
    window.mainloop()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # categories argument, takes a variable number of category to label the images into
    parser.add_argument("-categories",dest='categories', nargs='*', type=str)
    # keyboard keys argument, takes the different key stroke that must be pressed for each category
    parser.add_argument("-keys", dest='keys', nargs='*', type=str)

    args = parser.parse_args()

    manual_classification(args)