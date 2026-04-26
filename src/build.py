import os
import shutil

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
	with open(os.path.join(TEMP_DIR, out), "r+") as f:
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
	return outputText

def buildDedicatedPage(post, faq=False):
	outputText = "<div>"
	filePath = os.path.join(BLOG_DIR, post)
	if faq:
		filePath = os.path.join(FAQ_DIR, post)
	with open(filePath, "r") as f:
		for line in f:
			if line.startswith("#"):
				title = line.replace("#", "")
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
	insertion(title,file="dedicated.html",out=post.replace(".md", ".html"), target="<!--TITLE-->", end="")
	insertion(outputText,file="dedicated.html",out=post.replace(".md", ".html"))
	return outputText


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
	
	shutil.copy(os.path.join(TEMPLATE_DIR, "style.css"), PUBLIC_DIR)

	for file in os.listdir(TEMP_DIR):
		if file.endswith(".html"):
			shutil.copy(os.path.join(TEMP_DIR, file), PUBLIC_DIR)

	cleanup()

if __name__ == '__main__':
	main()