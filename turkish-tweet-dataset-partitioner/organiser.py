from tqdm import tqdm
import numpy as np
import os
import sys
import shutil
import xml.etree.ElementTree as ET



def organise_xml(path):

	temp_file = path.split("text")[0]+"text/temp.xml" #temp file to write new xml

	with open(path, 'r', encoding="utf8") as xml_file:
		tree = ET.parse(xml_file)
		root = tree.getroot()

		documents = root[0]

		allowed_tweets = []

		for i in range(len(documents)):
			if "RT" not in documents[i].text:  # we dont want retweets
				if "…" not in documents[i].text: # we dont want shortened tweets"
					if "I'm at" not in documents[i].text:
						if "Az önce bir fotoğraf paylaştı" not in documents[i].text:
							if "account has been withheld" not in documents[i].text:
								if "letgo'da ne sattığıma bak" not in documents[i].text:
									if "Günlük istatistiğim, Takipçi" not in documents[i].text:
										allowed_tweets.append(documents[i].text)


		if len(allowed_tweets) < 100: # user has no useful tweets
			return -1

		elif len(allowed_tweets) > 100: # user has more than 100 tweets, need sampling
			selections = np.random.choice(range(0,len(allowed_tweets)), 100, replace=False)

			tweets = []

			for index in selections:
				tweets.append(allowed_tweets[index])

			allowed_tweets = tweets # now allowed tweets has selected nice 100 tweets

	root = ET.Element("author", attrib={"lang":"tr"})
	documents = ET.SubElement(root, "documents")

	for tweet in allowed_tweets:
		ET.SubElement(documents, "document").text = str(tweet)

	tree = ET.ElementTree(root)
	tree.write(temp_file, encoding="utf8", xml_declaration=False) # writing them to temp file

	return temp_file



def organise_photos(path, hashed_name):

	temp_file  = path.split("photo")[0]+"photo/temp"

	if os.path.isdir(temp_file):
		shutil.rmtree(temp_file)

	os.mkdir(temp_file)

	if len(os.listdir(path)) < 10:
		return -1

	else:
		photos = os.listdir(path)

		if len(photos) > 10:
			selected_indexes = np.random.choice(range(0,len(photos)), 10, replace=False) # we will randomly select 10 photos

			selected_photos = []
			for index in selected_indexes:
				selected_photos.append(photos[index])

			photos = selected_photos #then assign it to photos

		suffix = 0
		for photo in photos:
			new_name = hashed_name + "." + str(suffix)
			shutil.copy2(os.path.join(path, photo), os.path.join(temp_file, new_name))
			suffix += 1



		return temp_file



