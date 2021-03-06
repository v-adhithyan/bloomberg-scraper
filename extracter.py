import time
from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
import csv
import datetime as dt
import os

def write_output(filename, field_names, rows):
    print "writing to file {}".format(filename)
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, delimiter = ",", fieldnames = field_names)
        writer.writeheader()
        writer.writerows(rows)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.binary_location = "chromedriver.exe"
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.bloombergquint.com/markets")

# Extract top Gainers
tables = driver.find_elements_by_xpath("//table[@class='stripped-table stripped-table--nowrap']")

# extract headings
file_suffixes = ["Top_Gainers", "Top_Losers", "Active"]
j = 0
for table in tables:
    ths = table.find_elements_by_tag_name("th")
    field_names = []
    for th in ths:
        for col_name in str(th.text).split("\n"):
            field_names.append(col_name)

    print field_names
    # extract rows
    rows = []
    trs = table.find_elements_by_tag_name("tr")
    for tr in trs:
        tds = tr.find_elements_by_tag_name("td")
        i = 0
        row = {}
        for td in tds:
            for row_val in str(td.text).split("\n"):
                row[field_names[i]] = row_val
                i = i + 1
                print row_val
        rows.append(row)

    # write to csv
    today = dt.datetime.today()
    # save working directory so that we can switch to it later
    cwd = os.getcwd()
    # change to date directory where data files are organized month wise
    os.chdir("data")

    # check if a current month directory exists under data, if not create it
    directory = today.strftime("%b_%y")
    if not os.path.exists(directory):
        os.mkdir(directory)

    os.chdir(directory)
    # change to cuurent month dir, so that we can save files there
    filename = today.strftime("%d_%b_%y") + "_{}.csv".format(file_suffixes[j])
    j = j + 1

    write_output(filename, field_names, rows)

    # go back to original working directory
    os.chdir(cwd)

driver.quit()
