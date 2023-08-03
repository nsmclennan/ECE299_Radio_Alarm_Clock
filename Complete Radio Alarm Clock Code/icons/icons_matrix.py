"""
Module that contains all the icon matrices used in the code and the 
function to convert from txt file to matrix
"""
"""
*    Title: Icons Matrix Generation for Radio Alarm Clock
*    Author: Nicholas McLennan
*    Date: July 20, 2023
*    Code version: 1.0
"""

def convert_binary_to_matrix(img):
    """Converts a binary input text file to a matrix for drawing to display

    Args:
        img (string): path to text file

    Returns:
        list[list]: 2D matrix with binary representation ready to be drawn to display
    """
    matrix = []
    with open(img, 'r') as binary_image:
        i = 0 
        # Iterate over each line and character in each line
        for line in binary_image:
            row = []
            for character in line:
                # If the character is 1, add 1 to matrix
                if character == '1':
                    row.append(1)
                # If the character is 0, add 0 to matrix
                else:
                    row.append(0)
            # Only append row if there is information on it
            if row is not None:
                matrix.append(row)
        i += 1
    return matrix

# To print icons to screen from bianry
alarm_matrices = [convert_binary_to_matrix("icons/alarm_1.txt"),convert_binary_to_matrix("icons/alarm_2.txt"),convert_binary_to_matrix("icons/alarm_3.txt")]
volume_up = convert_binary_to_matrix("icons/volume_up.txt")
volume_down = convert_binary_to_matrix("icons/volume_down.txt")
volume_off = convert_binary_to_matrix("icons/volume_off.txt")
settings = convert_binary_to_matrix("icons/settings.txt")
back_arrow_selector = convert_binary_to_matrix("icons/back_arrow_selector.txt")
check = convert_binary_to_matrix("icons/check.txt")
high_brightness = convert_binary_to_matrix("icons/high_brightness.txt")
low_brightness = convert_binary_to_matrix("icons/low_brightness.txt")
alarm_big = convert_binary_to_matrix("icons/alarm_big.txt")
alarm_off = convert_binary_to_matrix("icons/alarm_off.txt")
star = convert_binary_to_matrix("icons/star.txt")

