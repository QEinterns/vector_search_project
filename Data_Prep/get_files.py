import os

def get_files():
    path = "/Users/spatra/Desktop/Movie/Data_Prep/docs"

    # list to store files
    res = []

    # Iterate directory
    for file_path in os.listdir(path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(path, file_path)):
            # add filename to list
            res.append(os.path.join(path, file_path))
    return res[:3286] + res[3287:]

