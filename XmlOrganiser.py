###################################
# This code is used in order to clean-up a dataset gathered from twitter API
# Each user must have a threshold of tweets of his own and a number of photos
# Truth file is the ground truth file
#
# October 2018
###################################

import xml.etree.ElementTree as ET
import os
import shutil
from tqdm import tqdm

path_to_xmls = "C:\\Users\\polat\\Desktop\\turkish_tweets\\text"
path_to_photos = "C:\\Users\\polat\\Desktop\\turkish_tweets\\photo"

path_to_problematic_users = "C:\\Users\\polat\\Desktop\\unuseful"

truth_path = os.path.join(path_to_xmls,"truth.txt")

threshold_of_tweets = 100
threshold_of_photos = 10
threshold_of_total_tweets = 100


truth_file = open(truth_path,"r", encoding="utf8")
lines = truth_file.readlines()
truth_file.close()

truth_file = open(truth_path,"w", encoding="utf8")

thrash_can = []
move_list = []
total_tweets = 0

xml_users = []
photo_users = []

print("Number of tweets are being controlled...")
## Check if user has more than 100 tweets
for xml in tqdm(os.listdir(path_to_xmls)):
    if xml.endswith("xml"):

        tree = ET.parse(os.path.join(path_to_xmls, xml))
        root = tree.getroot()

        total_tweets += len(root[0])

        if len(root[0]) < threshold_of_total_tweets:
            thrash_can.append(xml.split(".")[0])

        else:
            numof_rt = 0
            for tweet in root.findall('documents')[0].findall('document'):
                if tweet.text.startswith("RT"):
                    numof_rt += 1

            if (len(root[0]) - numof_rt) < threshold_of_tweets:
                move_list.append(xml.split(".")[0])

            else:
                xml_users.append(xml.split(".")[0])


print("There are " + str(total_tweets) + " number of tweets")


print("Number of photos are being controlled...")
## check if user has more than 10 photos or if there are users with photo but without tweet
for photo_dir in os.listdir(path_to_photos):
    if len(os.listdir(os.path.join(path_to_photos, photo_dir))) < threshold_of_photos:
        thrash_can.append(photo_dir)

    elif photo_dir not in xml_users:
        thrash_can.append(photo_dir)

    else:
        photo_users.append(photo_dir)


print("Checking that every user has both enough photo and tweet...")
for xml_user in xml_users:
    if xml_user not in photo_users:
        thrash_can.append(xml_user)



print("Deleting users without enough information...")
## Below 2 fors empties the thrash can, means removing unuseful data
for xml in os.listdir(path_to_xmls):
    if xml.endswith("xml"):
        if xml.split(".")[0] in thrash_can:
            os.remove(os.path.join(path_to_xmls, xml))

for photo_dir in os.listdir(path_to_photos):
    if photo_dir in thrash_can:
        shutil.rmtree(os.path.join(path_to_photos, photo_dir))


print("Moving users which have niosy information...")
## Below for moves the suspicious data objects to another folder
for xml in os.listdir(path_to_xmls):
    if xml.endswith("xml"):
        if xml.split(".")[0] in move_list:
            shutil.move(os.path.join(path_to_xmls, xml), os.path.join(path_to_problematic_users, "text"))

for photo_dir in os.listdir(path_to_photos):
    if photo_dir in move_list:
        shutil.move(os.path.join(path_to_photos, photo_dir), os.path.join(path_to_problematic_users,"photo"))


print("Adjusting truth file...")
## Below for adjusts the truth file according to the desired
for line in lines:
    thrash = False

    for xml in thrash_can:
        if xml in line.strip().split(":::"):
            thrash = True

    if thrash == False:
        truth_file.write(line)

truth_file.close()

