import unittest
from scraper import PerfumeScraper
import os.path
import uuid
from pandas import DataFrame
from time import sleep

class ScraperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('setUpClass')
        cls.instance = PerfumeScraper("https://bloomperfume.co.uk/collections/perfumes", container=False)
        cls.url = "https://bloomperfume.co.uk/collections/perfumes"
        cls.stem = "https://bloomperfume.co.uk"
        cls.test_filepath = '/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/testingdata/'
        cls.dict = {"href":['test', 'test'], "complete":['test', 'test'], "uuid":['test', 'test'], "name":['test', 'test'], "id":['123', '123'], "price":['£135', '£135'], "strength":['75ml / EdP', '75ml / EdP'], "category":['test', 'test'], "brand":['test', 'test'], "flavours":[['test', 'test'],['test', 'test']], "top notes":[['test', 'test'],['test', 'test']], "heart notes":[['test', 'test'],['test', 'test']], "base notes":[['test', 'test'],['test', 'test']], "image link":['test', 'test']}

    @classmethod
    def tearDownClass(cls):
        cls.instance.close_webpage()

    def test_open_webpage(self):
        test_value = self.url
        self.instance.open_webpage(test_value)
        actual_value = str(self.instance.get_current_url())
        self.assertMultiLineEqual(test_value, actual_value)

    def test_search_website(self):
        test_value = self.stem + "/search?q=product"
        string = 'product'
        self.instance.search_website(string)
        actual_value = str(self.instance.get_current_url())
        self.assertTrue(test_value==actual_value)

    def test_scroll_down(self):
        self.instance.open_webpage(self.url)
        start = float(self.instance.get_scroll_height())
        self.instance.scroll_down(4)
        end = float(self.instance.get_scroll_height())
        self.assertTrue(end > start)

    def test_scroll_up(self):
        # self.instance.open_webpage(self.url)
        self.instance.scroll_down(4)
        start = float(self.instance.get_scroll_height())
        self.instance.scroll_up(4)
        end = float(self.instance.get_scroll_height())
        self.assertTrue(end < start)

    def test_go_back(self):
        self.instance.open_webpage(self.url)
        test_url = self.stem + '/products/ibiza-nights'
        self.instance.open_webpage(test_url)
        self.instance.go_back()
        original_page = self.instance.get_current_url()
        self.assertTrue(original_page == self.url)

    def test_clean_list(self):
        expected_value = ['one', 'two', 'three']
        list = ['one', None, 'two', None, 'three']
        actual_value = self.instance.clean_list(list)
        self.assertEqual(expected_value, actual_value)

    def test_get_links(self):
        actual_value = self.instance.get_links(self.url)
        self.assertTrue(type(actual_value) == list)
        self.assertTrue(type(actual_value[0]) == str)
        self.assertTrue(len(actual_value) >= 20)
        for a in actual_value:
            split = a.split("/p")
            self.assertMultiLineEqual(split[0], self.stem)

    def test_get_multiple_links(self):
        actual_value = self.instance.get_multiple_links(2)
        self.assertTrue(type(actual_value) == list)
        self.assertTrue(type(actual_value[0]) == str)
        self.assertTrue(len(actual_value) > 20)
        for a in actual_value:
            split = a.split("/p")
            self.assertMultiLineEqual(split[0], self.stem)
    
    def test_scrape_product(self):
        test_url = self.stem + "/products/ibiza-nights"
        actual_value = self.instance.scrape_product(test_url)
        self.assertTrue(type(actual_value) == dict)
        # self.assertTrue(len(actual_value.keys()) == 13)
        self.assertTrue(type(actual_value['href']) == str)
        self.assertMultiLineEqual(actual_value['href'], "ibiza-nights")
    
    def test_download_image(self):
        perfume = 'erose'
        test_url = self.stem + '/products/' + perfume
        test_filename = str(uuid.uuid4())
        self.instance.download_image(test_url, test_filename, self.test_filepath)
        test_file_path = str(self.test_filepath) + test_filename + '.jpg'
        test = os.path.exists(test_file_path)
        self.assertTrue(test == True)
        
    def test_mult_img_dowload(self):
        perfume1 = 'wilde'
        perfume2 = 'junky'
        test_url1 = self.stem + '/products/' + perfume1
        test_url2 = self.stem + '/products/' + perfume2
        list = [test_url1, test_url2]
        test_file_path1 = self.test_filepath + 'wilde.jpg'
        test_file_path2 = self.test_filepath + 'junky.jpg'
        if os.path.exists(test_file_path1):
            os.remove(test_file_path1)
        if os.path.exists(test_file_path2):
            os.remove(test_file_path2)
        self.instance.downloads_multiple_img(list, self.test_filepath)
        test = os.path.exists(test_file_path1)
        self.assertTrue(test == True)
        test2 = os.path.exists(test_file_path2)
        self.assertTrue(test2 == True)

    def test_data_clean(self):
        data_frame = self.instance.data_clean(self.dict)
        list2 = data_frame.columns
        self.assertTrue(len(list2) == 20)
        column = "volume"
        self.assertTrue(column in list2)
        test = data_frame['top notes'][0]
        self.assertIsInstance(test, list)
        test2 = data_frame['href'][0]
        self.assertIsInstance(test2, str)
        self.assertIsInstance(data_frame, DataFrame)

    def test_scrape_add(self):
        test_url = ['https://bloomperfume.co.uk/products/junky', 'https://bloomperfume.co.uk/products/wilde']
        new_dict = self.instance.scrape_add(url_list = test_url, original_dict=self.dict)
        test = new_dict['href']
        self.assertIsInstance(new_dict, dict)
        self.assertTrue(len(test) == 4)

    def test_open_json(self):
        pass

    def test_close_json(self):
        pass

    def test_runscraper(self):
        '''
        Just to set up.. 
        '''
        self.instance.run_scraper(no_pages=1, RDS=True, S3=True, local=True)

    def test_scraper(self):
        test_urls = self.instance.get_links(self.url)
        test_url = test_urls[0]
        test_href = self.instance.url_to_href(test_url)
        full_path = '/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/data/' + test_href + '.jpg'
        downloaded = os.path.exists(full_path)
        self.assertTrue(downloaded == True)
        test = test_href + '.jpg'
        s3 = self.instance.key_exists(test, 'imagebucketaic')
        self.assertTrue(s3 == True)
        sample_data = self.instance.open_json('/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/data/Sample_dict.json')
        href_list = sample_data['href']
        self.assertIn(test_href, href_list)
        rds_list = self.instance.rds_columntolist('PerfumeScraper', 'href')
        self.assertIn(test_href, rds_list)

if __name__ == '__main__':
    unittest.main()