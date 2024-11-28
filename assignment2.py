import unittest, json

from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import defaultdict

ORIGINAL_URL = 'https://en.wikipedia.org/wiki/Software_metric'
CYCLES = 10

class TestGetPerformance(unittest.TestCase):
    def setUp(self):
        self.url = ORIGINAL_URL
        self.cycles = CYCLES

    def test_performance(self):
        # Getting and preparing the data! 
        map_of_urls = defaultdict(list)
        for x in range(self.cycles):
            opts = webdriver.ChromeOptions()
            opts.add_argument("--incognito")
            driver = webdriver.Chrome(options=opts)
            driver.get(self.url)
            title = driver.find_element(By.CSS_SELECTOR, "#firstHeading > span")
            self.assertIn('Software metric', title.text)
            script = "return window.performance.getEntries().map(x => [x.name, x.duration])"
            data = driver.execute_script(script)
            for key, value in data:
                map_of_urls[key].append(value)
            driver.quit()
        
        #testing if there are 10 values
        first_key = next(iter(map_of_urls))
        first_value = map_of_urls[first_key]
        self.assertEqual(len(first_value), CYCLES)
        
        # Saving the data!
        json_string = json.dumps(map_of_urls, indent=4)
        with open(f"./dataMap.json", 'w') as file:
            file.writelines(json_string)
        
        # Testing my formula for calculating averages
        test_avg = [1, 2, 3, 4, 5] # Avarage should be 3
        arr = list(filter(lambda x: x != 0, test_avg))
        res =  sum(arr) / len(arr)
        self.assertEqual(res, 3)
        
        # Processing the data!
        map_of_averages = defaultdict(list)
        for key, value in map_of_urls.items():
            arr = list(filter(lambda x: x != 0, value))
            if len(arr) == 0:
                map_of_averages[key].append(0)
                continue
            average_value = sum(arr) / len(arr)
            map_of_averages[key].append(average_value)
        
        #testing if there is only one value
        first_key = next(iter(map_of_averages))
        first_value = map_of_averages[first_key]
        self.assertEqual(len(first_value), 1)
        
        # Saving the data!
        json_string = json.dumps(map_of_averages, indent=4)
        with open(f"./processedMap.json", 'w') as file:
            file.writelines(json_string)
        
    def tearDown(self) -> None:
        print("done")
    
if __name__ == "__main__":    
    unittest.main()
    