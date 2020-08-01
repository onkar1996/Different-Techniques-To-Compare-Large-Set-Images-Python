# example_averagehash.py

# Import dependencies
from PIL import Image
import imagehash

# Create the Hash Object of the first image
HDBatmanHash = imagehash.phash(Image.open('1574758796105.gif'))
print('Batman HD Picture: ' + str(HDBatmanHash))

# Create the Hash Object of the second image
SDBatmanHash = imagehash.phash(Image.open('1574758802470.gif'))
print('Batman HD Picture: ' + str(SDBatmanHash))

# Compare hashes to determine whether the pictures are the same or not
if(HDBatmanHash == SDBatmanHash):
    print("The pictures are perceptually the same !" + str(HDBatmanHash - SDBatmanHash))
else:
    print("The pictures are different, distance: " + str(HDBatmanHash - SDBatmanHash))
