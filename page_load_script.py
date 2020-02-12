from selenium import webdriver
import csv

links = []

with open('some_input_file_with_urls.csv', 'r') as file:
  reader = csv.DictReader(file)
  for row in reader:
    links.append(row['url'])

with open('output_file.csv', 'a') as file:
  fieldnames = ['url', 'redirect', 'dns', 'tcp', 'request', 'response', 'processing', 'onload', 'frontend', 'backend', 'total']
  writer = csv.DictWriter(file, fieldnames = fieldnames)
  writer.writeheader()

chrome_options = webdriver.chrome.options.Options()
PROFILE_PATH = "path_to_chrome_profile"
chrome_options.add_argument("--user-data-dir=" + PROFILE_PATH)
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome("path_to_chromedriver", chrome_options = chrome_options)

for link in links:
  for i in range(3):
    # opening link three times consecutively
    driver.get(link)

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    redirectStart = driver.execute_script("return window.performance.timing.redirectStart")
    redirectEnd = driver.execute_script("return window.performance.timing.redirectEnd")
    domainLookupStart = driver.execute_script("return window.performance.timing.domainLookupStart")
    domainLookupEnd = driver.execute_script("return window.performance.timing.domainLookupEnd")
    connectStart = driver.execute_script("return window.performance.timing.connectStart")
    connectEnd = driver.execute_script("return window.performance.timing.connectEnd")
    requestStart = driver.execute_script("return window.performance.timing.requestStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    responseEnd = driver.execute_script("return window.performance.timing.responseEnd")
    domLoading = driver.execute_script("return window.performance.timing.domLoading")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    loadEventStart = driver.execute_script("return window.performance.timing.loadEventStart")
    loadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

    redirect_calc = redirectEnd - redirectStart
    dns_calc = domainLookupEnd - domainLookupStart
    tcp_calc = connectEnd - connectStart
    request_calc = responseStart - requestStart
    response_calc = responseEnd - responseStart
    processing_calc = domComplete - domLoading
    onload_calc = loadEventEnd - loadEventStart
    frontend_calc = domComplete - responseStart
    backend_calc = responseStart - navigationStart
    total_calc = frontend_calc + backend_calc

    print("url: %s" % link, "redirect: %s" % redirect_calc, "dns: %s" % dns_calc, "tcp: %s" % tcp_calc, "request: %s" % request_calc, "response: %s" % response_calc, "processing: %s" % processing_calc, "onload: %s" % onload_calc, "frontend: %s" % frontend_calc, "backend: %s" % backend_calc, "total: %s" % total_calc)

    # writing result metrics in file
    with open('output_file.csv', 'a') as file:
      fieldnames = ['url', 'redirect', 'dns', 'tcp', 'request', 'response', 'processing', 'onload', 'frontend', 'backend', 'total']
      writer = csv.DictWriter(file, fieldnames = fieldnames)
      row = {'url': link, 'redirect': redirect_calc, 'dns': dns_calc, 'tcp': tcp_calc, 'request': request_calc, 'response': response_calc, 'processing': processing_calc, 'onload': onload_calc, 'frontend': frontend_calc, 'backend': backend_calc, 'total': total_calc}
      writer.writerow(row)

    # opening some website in between consecutive load
    # driver.get("https://www.github.com")
driver.quit()
