import numpy # Needed for standard deviation/coefficient calculations
import csv # Needed for processing CSV file into 2D matrix
import math # Needed for some math functions
import os # Needed for file path check

def find_correction_angle(binary_image):
    """
    Given a CSV file name in the existing directory, returns the correction
    angle of an image.

    ex. find_correction_angle("rotated.csv")

    This function uses linear regression of the points making up the left
    side of the rectangle to determine the slope. It returns the inverse
    tangent of the reciprocal of the slope, which is the desired correction
    angle.

    Args:
        (str) binary_image: the name of the CSV file.
    Returns:
        (int) The correction angle of the image.
    """

    # Convert CSV file to 2D matrix with image data
    try:
        img_data = list(csv.reader(open(binary_image), delimiter = ','))
    except FileNotFoundError:
        # Incorrect file name error scenario
        print("This file doesn't exist!")
        return 0

    # Empty image scenario
    if img_data is None:
        return 0

    x_coordinates = []
    y_coordinates = []

    row_len = len(img_data)
    col_len = len(img_data[0])

    # Keeps track of the previous column index while traversing image data
    prev_col_index = col_len

    # Flag for checking whether we are on the left side of the rectangle
    is_left_side = True

    # Iterate through image data rows
    # Skip the 0th index since that row isn't part of the data in the CSV file
    for i in range(1, row_len):

        # Break if we aren't traversing on the left side anymore
        if not is_left_side:
            break

        # Iterate through image data columns
        for j in range(col_len):

            # Retrieve the coordinates of the first '1' on each row
            if img_data[i][j] == '1':

                # Check whether we still are on the left side of the rectangle
                if (j > prev_col_index):
                    is_left_side = False
                else:
                    x_coordinates.append(i)
                    y_coordinates.append(j)
                    prev_col_index = j

                break

    if not x_coordinates or not y_coordinates:
        return 0

    # Calculate the standard deviation of both x and y coordinates
    x_std_dev = numpy.std(x_coordinates)
    y_std_dev = numpy.std(y_coordinates)

    # Edge case for already corrected image (no deviation in the y-coordinates)
    if y_std_dev == 0:
        return 0

    # Pearson correlation coefficient (r) calculation for linear regression
    correlation_coeff = numpy.corrcoef(x_coordinates, y_coordinates)[0][1]

    # LINEAR REGRESSION FORMULA: Slope = r * (SDy / SDx)
    slope = correlation_coeff * (y_std_dev / x_std_dev)

    # The angle we are looking for is the arctan of the reciprocal of the slope
    correction_angle = round(math.degrees(math.atan(1 / slope)))

    return correction_angle

def main():
    print(find_correction_angle("rotated.csv"))
    print(find_correction_angle("test0.csv"))
    print(find_correction_angle("test.csv"))

if __name__ == '__main__':
    main()
