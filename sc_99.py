#########################################################################################
#                                                                                       #
#                               THIS CODE WAS AUTO-GENERATED                            #
#                                                                                       #
#   Manual changes to this file MAY cause unexpected behavior in your application.      #
#   Manual changes to this file WILL be overwritten if the code is regenerated.         #
#                                                                                       #
#########################################################################################


import config
from scrapex import *
from scrapex import common
from scrapex.node import Node
from scrapex.excellib import *
from scrapex.http import Proxy
from proxy_list import random_proxy
import common_lib
import os
import argparse
import csv, random
import json
from time import sleep
from datetime import datetime
import sys  
from agent import random_agent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as EX
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

reload(sys)  
sys.setdefaultencoding('utf8')

lock = threading.Lock()

global_s = Scraper(
	use_cache=False, #enable cache globally
	retries=2,
	timeout=240,
	delay=0.5,
	#proxy_file = 'proxy.txt',
	#proxy_auth= 'silicons:1pRnQcg87F',
	use_cookie=True
	)

output_file = "output.csv"

DRIVER_WAITING_SECONDS                  = 60
DRIVER_MEDIUM_WAITING_SECONDS           = 10
DRIVER_SHORT_WAITING_SECONDS            = 5

driver = None

start_url = "https://www.naukri.com/browse-jobs"

username = "prasoon13.chourasia@gmail.com"
userpwd = "P@##w*r4"

keywords = config.keywords

total_applied_job_count = 0

screenshot_enable = True
class AnyEc:
	""" Use with WebDriverWait to combine expected_conditions
		in an OR.
	"""

	def __init__(self, *args):
		self.ecs = args

	def __call__(self, driver):
		for fn in self.ecs:
			try:
				if fn(driver): return True
			except:
				pass

def put_screenshot(file_name):
	if screenshot_enable == True:
		print "++++++++++++++++" + file_name + " was saved."
		driver.save_screenshot("logs/" + file_name)

def wait():
	sleep(random.randrange(1, DRIVER_SHORT_WAITING_SECONDS))

def wait_medium():
	offset_time = random.randrange(DRIVER_SHORT_WAITING_SECONDS +1 ,
		DRIVER_MEDIUM_WAITING_SECONDS)

	# print("Sleep Time: {} ".format(offset_time))
	sleep(offset_time)

def show_exception_detail(e):
	print (e)
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print("{}, {}, {}".format(exc_type, fname, str(exc_tb.tb_lineno)))

def create_url():
	global driver, start_url, total_applied_job_count
	
	# @todo Check to make sure that we have the information needed for this retailer in the DB
	try:
		# @TODO Timeout does not seem to be working here
		login_url = "https://login.naukri.com/nLogin/Login.php"
		print('login url... , {}'.format(login_url))
		
		driver.get(login_url)
		wait_medium()

		put_screenshot("login.png");
		print "Login with user"
	
		driver.find_element_by_xpath("//input[@id='emailTxt']").send_keys(username)
		wait()

		pwd_obj = driver.find_element_by_xpath("//input[@id='pwd1']")
		pwd_obj.send_keys(userpwd)
		wait()

		print "click login button"
		submit_btn = driver.find_element_by_xpath("//input[@value='Login']")
		submit_btn.click()
		wait_medium()

		# print('loading url... , {}'.format(start_url))

		# driver.get(start_url)
		# wait_medium()

		# put_screenshot("login.png");
		# print "Login with user"
		# driver.find_element_by_xpath("//a[@id='login_Layer']").click()
		# wait_medium()
		
		# driver.find_element_by_xpath("//input[@id='eLogin']").send_keys(username)
		# wait()

		# pwd_obj = driver.find_element_by_xpath("//input[@id='pLogin']")
		# pwd_obj.send_keys(userpwd)
		# wait()

		# pwd_obj.send_keys(Keys.ENTER)
		# wait_medium()

		# print "click login button"
		# submit_btn = driver.find_element_by_xpath("//button[@value='Login']")
		
		# try:
		# 	print submit_btn.get_attribute("value")
		# except:
		# 	pass

		

		# submit_btn.click()
		# print submit_btn

		# actions = ActionChains(driver)
		# actions.move_to_element(submit_btn)
		# actions.click(submit_btn)
		# actions.perform()
		# wait_medium()
		
		# url = "https://www.naukri.com/job-listings-Financial-Analyst-Financial-Modelling-corporate-Finance-6-to-10-year-Synophic-Systems-Private-Limited-Mumbai-6-to-8-years-020817008328?src=jobsearchDesk&sid=15017381397620&xp=3&qp=finance&srcPage=s"
		# driver.get(url)
		# wait_medium()

		# html_page = Doc(html = driver.page_source)

		# job_desc = html_page.q("//div[@class='JD']//text()").join(" ")

		# print "************************"
		# print job_desc
		# return

		put_screenshot("after login.png");

		user = driver.find_element_by_xpath("//ul[@class='rghtSec fr menu logged']/li/a/div[@class='mTxt']")
		print user.text
		
		common_lib.phantom_Quit(driver)
		# return
		for key_index, keyword in enumerate(keywords):
			total_applied_job_count = 0
			
			wait_medium()
			driver.get(start_url)
			wait()
			
			put_screenshot("search.png");    
			search_div = driver.find_element_by_xpath("//div[@class='qsbfield']")

			#finance, mumbai, 5, 8
			skill_item = search_div.find_element_by_xpath("//div[@id='skill']//input")
			skill_item.click()
			skill_item.send_keys(keyword["Skill"])
			wait()

			location_item = search_div.find_element_by_xpath("//div[@id='location']//input")
			location_item.click()
			location_item.send_keys(keyword["Location"])
			wait()

			experience_item = search_div.find_element_by_xpath("//div[@id='exp_dd']//input")
			experience_item.click()

			li_divs = search_div.find_elements_by_xpath(".//div[@id='exp_dd']/div[@class='sDrop']//ul/li")
			print "Experience Len=", len(li_divs)

			for li_div in li_divs:
				if li_div.text.strip() == str(keyword["Experience"]):
					print "Select", li_div.text
					li_div.click()

			wait()

			salary_item = search_div.find_element_by_xpath(".//div[@id='salary_dd']//input")
			salary_item.click()
			li_divs = search_div.find_elements_by_xpath(".//div[@id='salary_dd']/div[@class='sDrop']//ul/li")
			print "Experience Len=", len(li_divs)

			for li_div in li_divs:
				if li_div.text.strip() == str(keyword["Salary"]):
					print "Select", li_div.text
					li_div.click()

			wait()
			
			print "Click submit to search"
			driver.find_element_by_xpath("//button[@id='qsbFormBtn']").click()
			wait_medium()

			print "Sort by date"        
			sort_div = driver.find_element_by_xpath("//div[@class='sortBy']")
			# sort_div.click()
			actions = ActionChains(driver)
			actions.move_to_element(sort_div)
			actions.click(sort_div)
			actions.perform()
			wait_medium()

			put_screenshot("sortby.png");    
			sort_date_div = sort_div.find_element_by_xpath("//ul[@class='list']/li[contains(text(), 'Date')]")
			actions = ActionChains(driver)
			actions.move_to_element(sort_date_div)
			actions.click(sort_date_div)
			actions.perform()
			wait_medium()

			put_screenshot("job_listing.png");    

			print "Loading job listing"
			job_listings = driver.find_elements_by_xpath("//div[contains(@class, 'srp_container fl')]//div[@type='tuple']")
			stop_find_job = False

			main_window_handle = driver.window_handles[0]
			
			print "Jobs = ", len(job_listings)

			for job_ind, job_listing in enumerate(job_listings):
				print "******************** Handles *******************"
				print driver.window_handles

				for handle_id in driver.window_handles:
					if handle_id != main_window_handle:
						driver.switch_to.window(handle_id)
						close_tabs(driver)

				print "******************** Handles After removing *******************"
				print driver.window_handles

				driver.switch_to.window(main_window_handle)
				post_date_str = job_listing.find_element_by_xpath(".//div[@class='rec_details']/span").text

				print "****************************"
				print "Search Index = ", key_index
				print keyword
				print "Applied Job = ", total_applied_job_count, " Job Index=", job_ind, " Post Date =", post_date_str
				print "****************************"

				if ("Today" in post_date_str) or ("day ago" in post_date_str):
					stop_find_job = True
					break

				job_title = job_listing.find_element_by_xpath(".//ul/li[@itemprop='title']").get_attribute("title")

				nkeyword_exist = False
				for nkeyword in config.nkeywords:
					if nkeyword in job_title:
						nkeyword_exist = True

				if nkeyword_exist == True:
					print "+++++++++++++++++ Can't Apply 1 +++++++++++++++++"
					continue

				actions = ActionChains(driver)
				actions.move_to_element(job_listing)
				actions.click(job_listing)
				actions.perform()

				# job_listing.click()
				wait_medium()
				
				print "**************************"                
				print job_title
				
				
				if len(driver.window_handles) > 1:
					driver.switch_to.window(driver.window_handles[1])
					wait_medium()

				else:
					continue
				
				put_screenshot("job_desc.png");
				html_page = Doc(html = driver.page_source)

				job_desc = html_page.q("//div[@class='JD']//text()").join(" ").strip()

				# print "**************************"
				# print job_desc
				
				nkeyword_exist = False
				for nkeyword in config.nkeywords:
					if nkeyword in job_title:
						nkeyword_exist = True


				if (job_desc == "") or (nkeyword_exist == True):
					print "+++++++++++++++++ Can't Apply 2 +++++++++++++++++"
					continue
				
				# WebDriverWait(driver, DRIVER_WAITING_SECONDS).until(
				#     AnyEc(
				#         EC.presence_of_element_located(
				#             (By.XPATH, "//button[contains(text(), 'Apply')]")
				#         ),
				#         EC.presence_of_element_located(
				#             (By.XPATH, "//a[contains(text(), 'Apply')]")
				#         )
				#     )
				# )
				# put_screenshot("apply.png");    
				
				print "**************************"            
				print "Find Apply Button"
				apply_btn = None
				try:
					for item_div in driver.find_elements_by_xpath("//button"):
						button_text = item_div.text
						print button_text

						if button_text == "Apply":
							apply_btn = item_div

				except Exception as e:
					# print e
					try:
						for item_div in driver.find_elements_by_xpath("//a"):
							button_text = item_div.text
							print button_text

							if button_text == "Apply":
								apply_btn = item_div

					except Exception as e:
						# print e
						pass
				
				print "*****************************"
				print apply_btn

				if apply_btn != None:
					actions = ActionChains(driver)
					actions.move_to_element(apply_btn)
					actions.click(apply_btn)
					actions.perform()
					#apply_btn.click()
					wait_medium()
					   
				else:
					print "Not found apply button"
					continue

				print "Find Skip Link & Apply Job Button"
				exist = 0
				try:
					item1 = driver.find_element_by_xpath("//a[@id='skip_qup']")
					exist = 1
				except:
					pass

				try:
					item2 = driver.find_element_by_xpath("//a[@id='qup_skip']")
					exist = 2
				except:
					pass

				try:
					item3 = driver.find_element_by_xpath("//button[@id='qupSubmit']")
					exist = 3
				except:
					pass

				try:
					item4 = driver.find_element_by_xpath("//button[@id='qusSubmit']")
					exist = 4
				except:
					pass

				print "Exist = ", exist
				if exist == 0:
					print 'Not found any job submit button'
					close_tabs(driver)
					continue

				# try:
					# WebDriverWait(driver, DRIVER_WAITING_SECONDS).until(
					# 	AnyEc(
					# 		EC.presence_of_element_located(
					# 			(By.XPATH, "//a[@id='skip_qup']")
					# 		),
					# 		EC.presence_of_element_located(
					# 			(By.XPATH, "//a[@id='qup_skip']")
					# 		),
					# 		EC.presence_of_element_located(
					# 			(By.XPATH, "//button[@id='qupSubmit']")
					# 		),
					# 		EC.presence_of_element_located(
					# 			(By.XPATH, "//button[@id='qusSubmit']")
					# 		),
					# 	)
					# )
				# except TimeoutException as t:
				# 	print 'Not found any job submit button'
				# 	close_tabs(driver)
				# 	continue
				
				put_screenshot("skip_and_apply.png");    
			
				if skip_and_apply(driver) == False:
					# Skip and apply not found
					print "Update and Apply button detect"
					put_screenshot("update_and_apply.png");    
					update_and_apply(driver, keyword) 
				
				close_tabs(driver)
	   
	except TimeoutException as ex:
		print('***********Exception1*************')
		show_exception_detail(ex)

	except Exception, e:
		print('***********Exception2*************')
		show_exception_detail(e)

def close_tabs(self_driver):
	driver = self_driver

	while len(driver.window_handles) > 1:
		driver.switch_to.window(driver.window_handles[1])
		driver.close()
def skip_and_apply(self_driver):
	global total_applied_job_count
	driver = self_driver
	skip_link = None

	try:
		skip_link = driver.find_element_by_xpath("//a[@id='skip_qup']")
	except Exception as e:
		#print e
		try:
			skip_link = driver.find_element_by_xpath("//a[@id='qup_skip']")
		except Exception as e:
			#print e
			pass

	if skip_link != None:
		actions = ActionChains(driver)
		actions.move_to_element(skip_link)
		actions.click(skip_link)
		actions.perform()
		wait_medium()

		total_applied_job_count += 1

		print "Click skip and apply button"
		return True

	return False

def question_apply(self_driver):
	global total_applied_job_count
	submit_btn = driver.find_element_by_xpath("//button[@id='qusSubmit']")

	question_divs = driver.find_elements_by_xpath("//div[@class='row txtL']")
	print "Question Div Length = ", len(question_divs)

	for quetion_div in question_divs:
		input_options = quetion_div.find_elements_by_xpath(".//ul[@class='ans']/li/input")
		
		print "Len = ", len(input_options)

		if len(input_options) > 0:
			random_value = random.randrange(0, len(input_options))
			
			for i, li_div in enumerate(input_options):
				if i == random_value:
					actions = ActionChains(driver)
					actions.move_to_element(li_div)
					actions.click(li_div)
					actions.perform()

					print "Select Answer", li_div.get_attribute("value")
					# li_div.click()
					wait()

	print "Click Submit Button"
	actions = ActionChains(driver)
	actions.move_to_element(submit_btn)
	actions.click(submit_btn)
	actions.perform()
	wait_medium()

	skip_and_apply(driver)

def update_and_apply(self_driver, keyword):
	global total_applied_job_count

	driver = self_driver

	button_value_str = ""
	try:
		submit_btn = driver.find_element_by_xpath("//button[@id='qupSubmit']")
		button_value_str = submit_btn.text.strip()
	except:
		submit_btn = driver.find_element_by_xpath("//button[@id='qusSubmit']")
		button_value_str = submit_btn.text.strip()

	print "Button Value = '", button_value_str ,"'"
	if button_value_str == "Submit and Apply":
		question_apply(driver)
		return

	apply_div = driver.find_element_by_xpath("//div[@id='imsLBMain']")
	
	print "Select Preferred Job Location"
	try:    
		preferred_job_location = apply_div.find_elements_by_xpath("//select[@id='prfLoc']/option")
		
		select_job_location = False
		for i, li_div in enumerate(preferred_job_location):
			if li_div.text.lower().strip() == keyword["Location"].lower():
				print "Select Location", li_div.text
				li_div.click()
				select_job_location = True
				break

			if (i == len(preferred_job_location)) and  (select_job_location == False):
				print "Select Location", li_div.text
				li_div.click()
	except:
		print "Not found preferred job location"

	print "Input resume headline"
	try:
		resume_headline = apply_div.find_element_by_xpath("//textarea[@id='resHd']")
	
		resume_headline.send_keys(Keys.CONTROL + "a");
		resume_headline.send_keys(Keys.DELETE);
		resume_headline.send_keys("I have 5 years of experience in Finance")
	except:
		print "Not found resume"

	
	print "Try to find Current Salary Min"    
	try:
		current_salary_div = apply_div.find_element_by_xpath("//div[@id='qupMinSal_dd']")
		current_salary_input = current_salary_div.find_element_by_xpath("//input[@id='qupMinSal']")
		current_salary_input.click()
		wait()
		current_salary_drop = current_salary_div.find_elements_by_xpath(".//div[@class='sDrop']//ul/li")

		for li_div in current_salary_drop:
			if li_div.text.strip() == str(keyword["Salary"]):
				actions = ActionChains(driver)
				actions.move_to_element(li_div)
				actions.click(li_div)
				actions.perform()

				print "Select Current Salary Min", li_div.text
				# li_div.click()
				wait()
	except:
		print "Not Found Current Salary Min"

	print "Try to find Current Salary Max"    
	try:
		current_salary1_div = apply_div.find_element_by_xpath("//div[@id='qupMaxSal_dd']")
		current_salary1_input = current_salary1_div.find_element_by_xpath("//input[@id='qupMaxSal']")
		current_salary1_input.click()
		wait()
		current_salary1_drop = current_salary1_div.find_elements_by_xpath(".//div[@class='sDrop']//ul/li")

		print "Len = ", len(current_salary1_drop)
		random_value = random.randrange(2, len(current_salary1_drop))
		for i, li_div in enumerate(current_salary1_drop):
			if i == random_value:
				actions = ActionChains(driver)
				actions.move_to_element(li_div)
				actions.click(li_div)
				actions.perform()

				print "Select Current Salary Max", li_div.text
				# li_div.click()
				wait()
	except:
		print 'Not found current salary max'

	print "Try to find course"
	try:
		course_div = apply_div.find_element_by_xpath("//div[@id='courCja']")
		course_input = course_div.find_element_by_xpath("//input[@id='inp_courCja']")
		course_input.click()
		wait()
		course_drop = course_div.find_elements_by_xpath(".//div[@id='dp_courCja']//ul/li/a")
		print "Len = ", len(course_drop)
		random_value = random.randrange(1, len(course_drop))
		for i, li_div in enumerate(course_drop):
			if i == random_value:
				actions = ActionChains(driver)
				actions.move_to_element(li_div)
				actions.click(li_div)
				actions.perform()

				print "Select Course", li_div.text
				# li_div.click()
				wait()

		print "Try to find specialization"
		try:
			specialization_div = apply_div.find_element_by_xpath("//div[@id='specCja']")
			specialization_input = specialization_div.find_element_by_xpath("//input[@id='inp_specCja']")
			specialization_input.click()
			wait()
			specialization_drop = specialization_div.find_elements_by_xpath(".//div[@id='dp_specCja']//ul/li/a")

			print "Len = ", len(specialization_drop)
			random_value = random.randrange(1, len(specialization_drop))

			for i, li_div in enumerate(specialization_drop):
				if i == random_value:
					actions = ActionChains(driver)
					actions.move_to_element(li_div)
					actions.click(li_div)
					actions.perform()

					print "Select Specialization", li_div.text
					# li_div.click()
					wait()
		except:
			print "Not Found Specialization"

	except:
		print "Not Found Course Part"

	print "Try to find institute"
	try:
		institute = apply_div.find_element_by_xpath("//input[@id='Sug_ugInst']")
		institute.send_keys("Mumbai Science Institute")
		wait()
	except:
		print "Not Found Institute Part"

	print "Try to find passing year"
	try:
		passing_year_div = apply_div.find_element_by_xpath("//div[@id='quppasY_dd']")
		passing_year_input = passing_year_div.find_element_by_xpath("//input[@id='qupPasY']")
		passing_year_input.click()
		wait()
		passing_year_drop = passing_year_div.find_elements_by_xpath(".//div[@class='sDrop']//ul/li")

		print "Len = ", len(passing_year_drop)

		random_value = random.randrange(1, len(passing_year_drop))
		for i, li_div in enumerate(passing_year_drop):
			if i == random_value:
				actions = ActionChains(driver)
				actions.move_to_element(li_div)
				actions.click(li_div)
				actions.perform()
				# li_div.click()

				print "Select Passing Year", li_div.text
				wait()
	except:
		print "Not Found Passing Year Part"

	print "Try to find industry"
	try:
		industry_div = apply_div.find_element_by_xpath("//div[@id='ind_dd_qup']")
		industry_input = industry_div.find_element_by_xpath("//input[@id='qupInd']")
		industry_input.click()
		wait()
		industry_drop = industry_div.find_elements_by_xpath(".//div[@class='sDrop']//ul/li")

		print "Len = ", len(industry_drop)

		random_value = random.randrange(1, len(industry_drop))
		for i, li_div in enumerate(industry_drop):
			if i == random_value:
				actions = ActionChains(driver)
				actions.move_to_element(li_div)
				actions.click(li_div)
				actions.perform()
				# li_div.click()

				print "Select Industry", li_div.text
				wait()
	except:
		print "Not Found Industry"

	
	print "Click Submit Button"
	actions = ActionChains(driver)
	actions.move_to_element(submit_btn)
	actions.click(submit_btn)
	actions.perform()
	wait_medium()

	html = Doc(html = driver.page_source)
	passing_year_err = html.x("//i[@id='qupPasY_err']/text()").strip()
	institute_err = html.x("//i[@id='Sug_ugInst_err']/text()").strip()
	salary_min_err = html.x("//i[@id='qupMinSal_err']/text()").strip()
	resume_err = html.x("//i[@id='resHd_err']/text()").strip()
	ind_err = html.x("//i[@id='qupInd_err']/text()").strip()
	
	if passing_year_err != "" or institute_err != "" or salary_min_err != "" or resume_err != "" or ind_err != "":
		print "manadatory field is required"
	else:
		total_applied_job_count += 1

if __name__ == '__main__':
	#create_url()
	parser = argparse.ArgumentParser(description="Do something.")
	parser.add_argument('-t', '--threads', type=int, required=False, default=10, help='Number of threads, defaults to 5')
	parser.add_argument('-p', '--proxy', type=int, required=False, default=0, help='Proxy type: 0(standard), 1(Micro leave), 2(Rotating)')
	
	args = parser.parse_args()

	threads_number = args.threads
	proxy_type = args.proxy

	driver, ua, proxy_ip, screen_resolution = common_lib.create_phantomjs_driver()
	# driver = common_lib.create_chrome_driver(None)
	print driver
	create_url() 
	common_lib.phantom_Quit(driver)
