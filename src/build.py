import os
import shutil
import libopensonic
from datetime import datetime

# --- Configuration ---
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
BLOG_DIR = os.path.join(ROOT_DIR, 'blog')
FAQ_DIR = os.path.join(ROOT_DIR, 'faq')
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')
TEMPLATE_DIR = os.path.join(SRC_DIR, 'templates')
TEMP_DIR = os.path.join(os.path.curdir, 'temp')

def insertion(text, file = "index.html", out = "index.html", target = "<!--INSERTION POINT-->", end = "<!--END POINT-->"):
	if not os.path.exists(TEMP_DIR):
		os.makedirs(TEMP_DIR)
	if not os.path.exists(os.path.join(TEMP_DIR, out)):
		with open(os.path.join(TEMPLATE_DIR, file), "r"):
			shutil.copy(os.path.join(TEMPLATE_DIR, file), os.path.join(TEMP_DIR, out))

	#Replace <!--INSERTION POINT--> with the text and then add a new insertion point above <!--END POINT-->
	with open(os.path.join(TEMP_DIR, out), "r+", encoding="utf-8") as f:
		data = f.read()
		data = data.replace(target, text)
		if(end != ""):
			data = data.replace(end, target + " \n <!--END POINT-->")
		f.seek(0)
		f.write(data)
	
def buildMainPagePost(post):
	outputText = "<div>"
	with open(os.path.join(BLOG_DIR, post), "r") as f:
		for line in f:
			if line.startswith("#"):
				line = line.replace("#", "<h2><a href='" + post.replace(".md", ".html") + "'>")
				line = line.replace("\n", "</a></h2>")
				outputText += line
			elif line.startswith("##"):
				line = line.replace("##", "<h3>")
				line = line.replace("\n", "</h3>")
				outputText += line
			else:
				line = "<p>" + line
				line = line.replace("\n", "</p>")
				outputText += line
	outputText += "</div>"
	insertion(outputText)
	return outputText

def buildFAQPage(post):
	outputText = "<div>"
	with open(os.path.join(FAQ_DIR, post), "r") as f:
		for line in f:
			if line.startswith("#"):
				line = line.replace("#", "<h2><a href='" + post.replace(".md", ".html") + "'>")
				line = line.replace("\n", "</a></h2>")
				outputText += line
			elif line.startswith("##"):
				line = line.replace("##", "<h3>")
				line = line.replace("\n", "</h3>")
				outputText += line
			else:
				line = "<p>" + line
				line = line.replace("\n", "</p>")
				outputText += line
	outputText += "</div>"
	insertion(outputText, file="faq.html", out="faq.html")
	if post.startswith("playlist"):
		reviewed = getPlaylist()[0]
		study = getPlaylist()[1]
		insertion(reviewed,file="faq.html",out="faq.html", target="<!--Review playlist-->", end="")
		insertion(study,file="faq.html",out="faq.html", target="<!--Saved playlist-->", end="")
		insertion(datetime.today().strftime('%m-%d-%Y'),file="faq.html",out="faq.html", target="<!--Date-->", end="")
	return outputText

def buildDedicatedPage(post, faq=False):
	outputText = "<div>"
	filePath = os.path.join(BLOG_DIR, post)
	if faq:
		filePath = os.path.join(FAQ_DIR, post)
	bypass = False
	with open(filePath, "r") as f:
		for line in f:
			if line.startswith("bypass=true"):
				bypass = True
			elif line.startswith("bypass=false"):
				bypass = False
			elif not bypass and line.startswith("# "):
				title = line.replace("#", "")
				line = line.replace("#", "<h2><a href='" + post.replace(".md", ".html") + "'>")
				line = line.replace("\n", "</a></h2>")
				outputText += line
			elif not bypass and line.startswith("## "):
				line = line.replace("##", "<h3>")
				line = line.replace("\n", "</h3>")
				outputText += line
			elif not bypass and line.startswith("---"):
				outputText += "<hr>"
			else:
				line = "<p>" + line
				line = line.replace("\n", "</p>")
				outputText += line
	outputText += "</div>"
	insertion(title,file="dedicated.html",out=post.replace(".md", ".html"), target="<!--TITLE-->", end="")
	insertion(outputText,file="dedicated.html",out=post.replace(".md", ".html"))
	if faq and post.startswith("playlist"):
		reviewed = getPlaylist()[0]
		study = getPlaylist()[1]
		insertion(reviewed,file="dedicated.html",out=post.replace(".md", ".html"), target="<!--Review playlist-->", end="")
		insertion(study,file="dedicated.html",out=post.replace(".md", ".html"), target="<!--Saved playlist-->", end="")
		insertion(datetime.today().strftime('%m-%d-%Y'),file="dedicated.html",out=post.replace(".md", ".html"), target="<!--Date-->", end="")
	return outputText

def getPlaylist():
	conn = libopensonic.Connection('https://music.spacebanana.dpdns.org' , 'subway' , 'Ft4DGUnZry5dHZq4KKME' , port=443)
	playlists = conn.get_playlists()
	reviewedID = ""
	studyID = ""
	for pl in playlists:
		if pl.name == "Reviewed":
			reviewedID = pl.id
		if pl.name == "Study":
			studyID = pl.id

	reviewedPlaylist = "#EXTM3U<br>#PLAYLIST:Reviewed<br>"

	for song in conn.get_playlist(reviewedID).entry:
		reviewedPlaylist += f"#EXTINF: {song.duration},{song.artist} - {song.title}<br>"
		
	songPlaylist = "#EXTM3U<br>#PLAYLIST:Study<br>"

	for song in conn.get_playlist(studyID).entry:
		songPlaylist += f"#EXTINF: {song.duration},{song.artist} - {song.title}<br>"
	
	return (reviewedPlaylist,songPlaylist)

def copy_playlists():
	with open (os.path.join(TEMP_DIR, "reviewed.m3u"), "w+", encoding="utf-8") as reviewed:
		reviewed.write(getPlaylist()[0].replace("<br>","\n"))
	
	with open (os.path.join(TEMP_DIR, "study.m3u"), "w+", encoding="utf-8") as study:
		study.write(getPlaylist()[1].replace("<br>","\n"))

def cleanup():
	if os.path.exists(TEMP_DIR):
		shutil.rmtree(TEMP_DIR)

def main():
	if os.path.exists(TEMP_DIR):
		shutil.rmtree(TEMP_DIR)
	if os.path.exists(PUBLIC_DIR):
		shutil.rmtree(PUBLIC_DIR)
	os.makedirs(PUBLIC_DIR)

	for file in sorted(os.listdir(BLOG_DIR), reverse=True):
		if file.endswith(".md"):
			buildMainPagePost(file)
			buildDedicatedPage(file)

	for file in sorted(os.listdir(FAQ_DIR)):
		if file.endswith(".md"):
			buildFAQPage(file)
			buildDedicatedPage(file, faq=True)
	
	copy_playlists()

	shutil.copy(os.path.join(TEMPLATE_DIR, "style.css"), PUBLIC_DIR)

	for file in os.listdir(os.path.join(SRC_DIR, "static")):
		shutil.copy(os.path.join(SRC_DIR, "static", file), PUBLIC_DIR)

	for file in os.listdir(TEMP_DIR):
		if file.endswith(".html") or file.endswith(".m3u"):
			shutil.copy(os.path.join(TEMP_DIR, file), PUBLIC_DIR)

	cleanup()

if __name__ == '__main__':
	main()