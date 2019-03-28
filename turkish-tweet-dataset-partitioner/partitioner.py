import os
import sys
import shutil
from tqdm import tqdm
import hashlib
import numpy as np
from organiser import organise_photos, organise_xml


tweets_path = "/mnt/671728fd-b9e2-46ed-b18b-9f45f387f63e/turkish_tweets_dataset/turkish_tweets"
photo_tweets_path = os.path.join(tweets_path, "photo")
text_tweets_path = os.path.join(tweets_path, "text")
truth_tweets_path = os.path.join(text_tweets_path, "truth.txt")

controlled = "/home/darg2/Desktop/truth_dataset-truth_dataset_2.csv"

training_resulting_dataset_path = "/home/darg2/Desktop/turkish_tweets_dataset_training"
training_photo_resulting_dataset_path = os.path.join(training_resulting_dataset_path, "photo")
training_text_resulting_dataset_path = os.path.join(training_resulting_dataset_path, "text")
training_truth_resulting_dataset_path = os.path.join(training_text_resulting_dataset_path, "truth.txt")

test_resulting_dataset_path = "/home/darg2/Desktop/turkish_tweets_dataset_test"
test_photo_resulting_dataset_path = os.path.join(test_resulting_dataset_path, "photo")
test_text_resulting_dataset_path = os.path.join(test_resulting_dataset_path, "text")
test_truth_resulting_dataset_path = os.path.join(test_text_resulting_dataset_path, "truth.txt")

male_users = []
female_users = []

training_split = 2510


if not os.path.exists(training_resulting_dataset_path):
	os.mkdir(training_resulting_dataset_path)

if not os.path.exists(training_text_resulting_dataset_path):
	os.mkdir(training_text_resulting_dataset_path)

if not os.path.exists(training_photo_resulting_dataset_path):
	os.mkdir(training_photo_resulting_dataset_path)

if not os.path.exists(test_resulting_dataset_path):
	os.mkdir(test_resulting_dataset_path)

if not os.path.exists(test_text_resulting_dataset_path):
	os.mkdir(test_text_resulting_dataset_path)

if not os.path.exists(test_photo_resulting_dataset_path):
	os.mkdir(test_photo_resulting_dataset_path)


controlled_file = open(controlled,"r")

# parsing the controlled users
for line in controlled_file:
	user_info = line.strip().split(',')

	if user_info[5] == "0": # if there is no problem with the user
		if user_info[2] == "female":
			female_users.append(user_info)
		else:
			male_users.append(user_info)

controlled_file.close()

# equalizing the ratio of male and female
if len(female_users)/(len(female_users)+len(male_users)) > 0.52:
	ratio = len(female_users)/(len(female_users)+len(male_users))

	while ratio > 0.507:
		selected_to_delete = np.random.randint(0,len(female_users),50) # delete by 50 until %50.7 precision

		new_female_users = []

		for i in range(len(female_users)):
			if i not in selected_to_delete:
				new_female_users.append(female_users[i])

		female_users = new_female_users.copy()

		ratio = len(female_users)/(len(female_users)+len(male_users))


elif len(male_users)/(len(female_users)+len(male_users)) > 0.52:
	ratio = len(male_users) / (len(female_users) + len(male_users))

	while ratio < 0.507:
		selected_to_delete = np.random.randint(0, len(male_users), 50) # delete by 50 until %50.7 precision

		new_male_users = []

		for i in range(len(male_users)):
			if i not in selected_to_delete:
				new_male_users.append(male_users[i])

		male_users = new_male_users.copy()

		ratio = len(male_users) / (len(female_users) + len(male_users))


# hash the names in the dataset
dataset = female_users + male_users
hashed_name_dict = {}

for user in dataset:
	hashed_name_dict[str(user[1])] = hashlib.md5(bytes(str(user[1]), "utf-8")).hexdigest()

training_dataset = []
test_dataset = []

training_indexes = np.random.choice(range(0,len(dataset)), training_split, replace=False)

for i in range(len(dataset)):
	if i in training_indexes:
		training_dataset.append(dataset[i])
	else:
		test_dataset.append(dataset[i])

test_female = 0
test_male = 0
for user in test_dataset:
	if user[2] == "female":
		test_female += 1
	else:
		test_male += 1

training_female = 0
training_male = 0
for user in training_dataset:
	if user[2] == "female":
		training_female += 1
	else:
		training_male += 1

print("test size: " + str(len(test_dataset)) + "\ntraining size: " + str(len(training_dataset)))
print("# of males for training: " + str(training_male) + "\n # of females for training: " + str(training_female))
print("# of males for test: " + str(test_male) + "\n # of females for test: " + str(test_female))
print("size of total dataset: " + str(len(dataset)))
print("ratio for total dataset: " + str(len(male_users) / (len(female_users) + len(male_users))))

legal_users = []
# copying files by organising them in wanted structure
for user in tqdm(training_dataset):
	user_xml = str(user[1])+".xml"
	new_user_xml = hashed_name_dict[str(user[1])]+".xml"

	temp_xml_file = organise_xml(os.path.join(text_tweets_path, user_xml)) # get new xml if user has nice tweets

	if temp_xml_file != -1:
		temp_photos_file = organise_photos(os.path.join(photo_tweets_path, user[1]), hashed_name_dict[user[1]])# get new photo dir if user has allowed # of photos

		if temp_photos_file != -1: # if user passes both xml and photo check
			legal_users.append(user)
			shutil.copytree(os.path.join(temp_photos_file), os.path.join(training_photo_resulting_dataset_path, hashed_name_dict[str(user[1])])) # copy photo dir
			shutil.copy2(os.path.join(temp_xml_file), os.path.join(training_text_resulting_dataset_path, new_user_xml)) # copy xml


print(len(os.listdir(training_text_resulting_dataset_path)))

hashed_list_file = open(os.path.join(training_resulting_dataset_path,"name_hash_match.txt"),"w")


# storing hashes and real names in a new txt
for key, value in hashed_name_dict.items():
	line = str(key) + ":::" + str(value) + "\n"
	hashed_list_file.write(line)

hashed_list_file.close()


# creating truth file

truth_file = open(training_truth_resulting_dataset_path,"w")

for user in legal_users:
	line = str(hashed_name_dict[user[1]]) + ":::" + str(user[2]) + "\n"
	truth_file.write(line)

truth_file.close()

######################################################################################
###############################     TEST    ##########################################
######################################################################################


legal_users = []
# copying files by organising them in wanted structure
for user in tqdm(test_dataset):
	user_xml = str(user[1])+".xml"
	new_user_xml = hashed_name_dict[str(user[1])]+".xml"

	temp_xml_file = organise_xml(os.path.join(text_tweets_path, user_xml)) # get new xml if user has nice tweets

	if temp_xml_file != -1:
		temp_photos_file = organise_photos(os.path.join(photo_tweets_path, user[1]), hashed_name_dict[user[1]])# get new photo dir if user has allowed # of photos

		if temp_photos_file != -1: # if user passes both xml and photo check
			legal_users.append(user)
			shutil.copytree(os.path.join(temp_photos_file), os.path.join(test_photo_resulting_dataset_path, hashed_name_dict[str(user[1])])) # copy photo dir
			shutil.copy2(os.path.join(temp_xml_file), os.path.join(test_text_resulting_dataset_path, new_user_xml)) # copy xml


print(len(os.listdir(test_text_resulting_dataset_path)))

hashed_list_file = open(os.path.join(test_resulting_dataset_path,"name_hash_match.txt"),"w")


# storing hashes and real names in a new txt
for key, value in hashed_name_dict.items():
	line = str(key) + ":::" + str(value) + "\n"
	hashed_list_file.write(line)

hashed_list_file.close()


# creating truth file

truth_file = open(test_truth_resulting_dataset_path,"w")

for user in legal_users:
	line = str(hashed_name_dict[user[1]]) + ":::" + str(user[2]) + "\n"
	truth_file.write(line)

truth_file.close()

