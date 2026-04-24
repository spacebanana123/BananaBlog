### A small blogging utility that fits my own needs. Should be able to host using minimal serverside compute and hopefully only static assets

Organization:
	/blog:
		blog entries themselves.
	/public:
		should be all of the end product html, js, and css. It does not contain any server side code. 
	/src:
		should contain the necessary tools to build the public folder. 
		if necessary, it will contain serverside compute code.

Nice to haves:
	Way to edit or change the md files without needing to open up a code editor. 
		Adding md files should be relatively easy. Set up an input page and a quick text box.
		It seems more difficult to write an editor?
			Maybe query the git repo if it is public?
			Need to have some form of storage of what has been written. 