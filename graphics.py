import os, pygame

imgext = ["png", "jpeg", "jpg", "jpe", "jfif", "bmp", "gif", "dip", "tiff", "tif", "heic"]

def load_image(filename=None):
    if not filename == None:
        if "." in filename[-4:-2]:
            try:
                return pygame.image.load(os.path.join(filename)).convert_alpha()
            except FileNotFoundError:
                print(f"The file {filename} was not found, please double check to make sure that the file exists.")
        else:
            raise Exception(f"file string {filename} is invalid.")
    else:
        raise TypeError("You forgot to supply a filename for the image")
