import os
import shutil

truth_file = "/home/darg2/Desktop/truth_truth_dataset_2.csv"
dataset = "/mnt/671728fd-b9e2-46ed-b18b-9f45f387f63e/turkish_tweets_dataset/turkish_tweets/text"
portion_of_dataset = "/home/darg2/Desktop/portion_dataset"

person = ["Algın Poyraz Arslan", "Hasan Para", "Elgun Jabrayilzade", "Erhan Sezerer"]

users_to_copy = []

with open(truth_file, "r", encoding="utf8") as f:
	for line in f:
		if line.strip().split(",")[0] == person[1]:
			users_to_copy.append(line.strip().split(",")[1])


for user in users_to_copy:
	filename = str(int(user))+".xml"

	text_file_path_src = os.path.join(dataset, filename)
	text_file_path_dest = os.path.join(portion_of_dataset, filename)

	try:
		shutil.copy2(text_file_path_src, text_file_path_dest)
	except:
		print(user)

