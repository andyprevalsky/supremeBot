READ ME

Steps to Use this Bot
----------------------------------------------------------------

NOTE: Steps below are for OSX, Windows steps may vary

1. Install python
	- https://www.python.org/

2. Install Homebrew (type below command in terminal)
	- /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

2. Run pip commands in terminal
	- pip install beautifulsoup4
	- pip install requests
	- pip install selenium

3. Make sure XCode is installed from AppStore and Terms & Service are Accepted

4. Setup Depot_Tools
	- $ mkdir Tools_Folder cd Tools_Folder
	- $ git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
	- $ export PATH="$PATH:/path/to/depot_tools" ; use your own path

5. Setup Chromium
	- $ mkdir Chromium cd Chromium
	- $ fetch Chromium ; note this will take longer then 30 min to complete
	- $ cd src
	- $ gclient runhooks

7. Edit file "call_function.js"
	-	search for file name in established folder "src"
	-	open and edit "function getPageCache(opt_doc)"
		-	replace var key value with randnom string value
			: "$cdc" -> "Kswisha"
	- save file

8. Install Ninja
	- $ brew install ninja

9. Build files for Ninja
	- while in src folder...
	- $ gn gen out/Default

10. Build chromedriver
	- while in src folder...
	- $ ninja -C out/Default chromedriver

11. Edit path in supbot.py
	-	Under function "server_setup"
		-	Change value YOUR_PATH to path of newly built chromedriver
		- 	driver = webdriver.Chrome('YOUR_PATH', chrome_options=chromeOptions)
. Run bot
	- $ python3 ./supbot.py
