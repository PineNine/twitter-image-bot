# "pip install tweepy" if not working
import tweepy
import tweepy.errors
import os
import my_keys as k # separate python file containing keys

# thing thing thing access to twitter api?
client = tweepy.Client(k.bearer_token, k.api_key, k.api_secret, k.access_token, k.access_secret)
auth = tweepy.OAuth1UserHandler(k.api_key, k.api_secret, k.access_token, k.access_secret)
api = tweepy.API(auth)

# src: not yet uploaded folder
# dest: uploaded media
CWD = os.getcwd()
SRC = os.path.join(CWD, "FOLDER_NAME")
DEST = os.path.join(CWD, "FOLDER_NAME")

# moves file after uploading files
def move_files(files):
    for i in files:
        # move file to DEST folder 
        try:
            src_path = os.path.join(SRC, i)
            dest_path = os.path.join(DEST, i)
            os.rename(src_path, dest_path)
        except FileExistsError:
            print(f"{i}: FILE NOT MOVED, file already exist in folder")
            continue

# grabs media id and return them as a list
def get_ids(files):
    id_list = []
    for i in files:
        file_path = os.path.join(SRC, i)
        media_id = api.media_upload(filename=file_path).media_id_string

        # add id and corresponding file as a list
        id_list.append(media_id)
    return id_list

# uploads the images
def upload(all_files):
    
    for i in range(0, len(all_files), 4):
        id_list = get_ids(all_files[i:i+4])

        try:
            client.create_tweet(media_ids=id_list)
        except tweepy.errors.TooManyRequests:
            print("POST LIMIT REACHED, try again tomorrow")
            break
        
        move_files(all_files[i:i+4])
        print(i, "uploaded files: ", all_files[i:i+4])

# grabs all files names in folder
all_files = os.listdir(SRC)

# function to upload images
upload(all_files)