from webbrowser import Chrome
from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import uuid
import os
import json
import urllib.request
import urllib3.exceptions
import requests
import boto3
import botocore
from sqlalchemy import create_engine, table
import pandas as pd
import psycopg2
from sqlalchemy import inspect
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
import yaml

class PerfumeScraper: 
    '''
    This scraper class scrapes perfume product data from the website bloomperfume.co.uk.
    It can upload product data to AWS RDS database, upload raw data (images and files) to an S3 datalake and create a local json file of product data.
    It can be used on a local machine (Mac) or used remotely
    Args:
        url: base product page with all products to be scraped
        container: toggles whether being used on local computer or remotely on a docker container (default on)
    Outputs:
        Table on RDS database
        Files and images on AWS S3 bucket
        JSON file of product data
    '''
    def __init__(self, url:str, container=True, creds: str='/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/Data_Collection_Pipeline/creds/rds_creds.yaml'):
        self.url = url
        self.dict = {"href":['test', 'test'], "complete":['test', 'test'], "uuid":['test', 'test'], "name":['test', 'test'], "id":['123', '123'], "price":['£135', '£135'], "strength":['75ml / EdP', '75ml / EdP'], "category":['test', 'test'], "brand":['test', 'test'], "flavours":[['test', 'test'],['test', 'test']], "top notes":[['test', 'test'],['test', 'test']], "heart notes":[['test', 'test'],['test', 'test']], "base notes":[['test', 'test'],['test', 'test']], "image link":['test', 'test']}
        self.s3 = boto3.client('s3')
        self.bucket = 'imagebucketaic'
        self.table = 'PerfumeScraper'
        
        if container:
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage') 
            options.add_argument('--remote-debugging-port=9222')
            self.driver = webdriver.Chrome(options=options)
            DATABASE_TYPE=os.environ.get('DATABASE_TYPE')
            DBAPI=os.environ.get('DBAPI')
            USER='postgres'
            PASSWORD=os.environ.get('RDS_PASSWORD')
            ENDPOINT=os.environ.get('ENDPOINT')
            PORT=os.environ.get('PORT')
            DATABASE=os.environ.get('DATABASE')

        else:
            self.driver = webdriver.Chrome("/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/chromedriver")
            # self.driver = Chrome(ChromeDriverManager().install(), options=options)
            with open(creds, 'r') as f:
                creds = yaml.safe_load(f)
            DATABASE_TYPE= creds['DATABASE_TYPE']
            DBAPI= creds['DBAPI']
            USER= creds['USER']
            PASSWORD= creds['PASSWORD']
            ENDPOINT= creds['ENDPOINT']
            PORT= creds['PORT']
            DATABASE= creds['DATABASE']
            self.bucket = 'imagebucketaic'

        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        self.engine.connect() 

    # FOR WEBSITE NAVIGATION

    def open_webpage(self, url:str):
        '''
        Takes in url and opens the webpage
        '''
        self.driver.get(url)
        time.sleep(2)
        try:
            cookies_button = self.driver.find_element(By.CLASS_NAME, "accept")
            cookies_button.click()
        except NoSuchElementException:
            pass

    def close_webpage(self):
        '''
        Closes browser
        '''
        self.driver.quit()

    def go_back(self):
        '''
        Goes back to previous loaded page
        '''
        self.driver.back()

    def get_current_url(self) -> str:
        '''
        Returns current url
        '''
        return self.driver.current_url

    def search_website(self, input:str):
        '''
        Loads search results from bloom website
        Args: 'input' the word to be searched 
        '''
        url = 'https://bloomperfume.co.uk/search?q=' + input
        self.driver.get(url)

    def scroll_down(self, no_seconds:int):
        '''
        Scrolls down the current webpage for the number of seconds specified in the args
        '''
        start_time = time.time()
        while (time.time() - start_time) < no_seconds:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
        else:
            pass
    
    def scroll_up(self, no_seconds:int):
        '''
        Scrolls up the current webpage for the number of seconds specified in args
        '''
        start_time2 = time.time()
        while (time.time() - start_time2) < no_seconds:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
        else:
            pass

    def get_full_height(self) -> str:
        '''
        Finds the total height of the webpage
        '''
        total_height = str(self.driver.execute_script("return document.body.scrollHeight"))
        return total_height
        
    def get_scroll_height(self) -> str:
        '''
        Finds the current scroll height of the webpage
        '''
        current_height = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
        return current_height

    # COLLECTING DATA FROM THE WEBSITE

    def get_links(self, url:str) -> list:
        '''
        Scrapes product urls from webpage
        Args: 'url': full product list webpage
        Returns: list of urls scraped from the webpage
        '''
        self.open_webpage(url)
        time.sleep(1)
        try:
            product_container = self.driver.find_element(By.XPATH, '//div[@class="products-list"]')
            prod_list = product_container.find_elements(By.CLASS_NAME, "product-name")
            link_list = [] 
            for p in prod_list:
                href = p.get_attribute("href")
                link_list.append(href)
        except:
            pass
        return link_list

    def get_multiple_links(self, number_pages:int) -> list:
        '''
        Scrapes urls from multiple product pages
        Args: number_pages: number of pages to be scraped for urls
        Returns: a list of product urls 
        '''
        all_links = []
        for i in range(1, (number_pages+1), 1):
            paged_url = self.url + "?page=" + str(i)
            list_i = self.get_links(paged_url)
            all_links += list_i
        return all_links

    def clean_list(self, list:list) -> list:
        '''
        Removes null values from a list
        '''
        cleaned_list = []
        for l in list:
            if l != None:
                cleaned_list.append(l)
        return cleaned_list

    def scrape_product(self, url:str) -> dict:
        '''
        Scrapes the product webpage for required information
        Args: url: product page url to be scraped
        Returns: a product dictionary with the variable name as key and result as the value
        '''
        self.open_webpage(url)
        product_dictionary = {"href":[], "complete":[], "uuid":[], "name":[], "id":[], "price":[], "strength":[], "category":[], "brand":[], "flavours":[], "top notes":[], "heart notes":[], "base notes":[], "image link":[]}
        current_url = self.driver.current_url
        split = current_url.split("s/")
        product_dictionary['href']=split[1]
        product_dictionary['complete']='True'
        product_dictionary['uuid']=str(uuid.uuid4())

        try:
            main_details = self.driver.find_element(By.XPATH, '//*[@id="product-page"]/div/div[3]/div/div[1]/div[1]/div[1]/a')
            product_number = main_details.get_attribute("data-product") 
            product_dictionary['id']=product_number
            product_price = main_details.get_attribute("data-price")
            product_dictionary['price']=product_price
            product_title = main_details.get_attribute("data-title")
            product_dictionary['name']=product_title
            product_vtitle = main_details.get_attribute("data-vtitle")
            product_dictionary['strength']=product_vtitle
            product_category = main_details.get_attribute("data-cat")
            product_dictionary['category']=product_category
            product_brand = main_details.get_attribute("data-vendor")
            product_dictionary['brand'] = product_brand

            flavours = self.driver.find_element(By.XPATH, '//*[@id="product-page"]/div/div[1]/div/div[2]')
            flavs = flavours.find_elements(By.TAG_NAME, "div")
            perfume_flavours = []
            for f in flavs:
                flav = f.get_attribute("data-flavor")
                perfume_flavours.append(flav)
            product_dictionary['flavours']= perfume_flavours

            top_notes = self.driver.find_element(By.XPATH, '//*[@id="product-page"]/div/div[3]/div/div[6]/div[1]')
            t_notes = top_notes.find_elements(By.TAG_NAME, "span")
            top = []
            for t in t_notes:
                note = t.get_attribute("data-search")
                top.append(note)
            top = self.clean_list(top)
            product_dictionary['top notes']= top

            heart_notes = self.driver.find_element(By.XPATH, '//*[@id="product-page"]/div/div[3]/div/div[6]/div[2]')
            h_notes = heart_notes.find_elements(By.TAG_NAME, "span")
            heart = []
            for h in h_notes:
                note2 = h.get_attribute("data-search")
                heart.append(note2)
            heart = self.clean_list(heart)
            product_dictionary['heart notes'] = heart

            base_notes = self.driver.find_element(By.XPATH, '//*[@id="product-page"]/div/div[3]/div/div[6]/div[3]')
            b_notes = base_notes.find_elements(By.TAG_NAME, "span")
            base = []
            for b in b_notes:
                note3 = b.get_attribute("data-search")
                base.append(note3)
            base = self.clean_list(base)
            product_dictionary['base notes'] = base

            im_link = self.driver.find_element(By.XPATH, '//*[@id="product_pic_1"]')
            i_link = im_link.find_element(By.TAG_NAME, 'img')
            image_link = i_link.get_attribute('src')
            product_dictionary['image link']=image_link
            
        except NoSuchElementException: 
            product_dictionary['id'] = "None"
            product_dictionary['price'] = "None"
            product_dictionary['name'] = "None"
            product_dictionary['strength'] = "None"
            product_dictionary['category'] = "None"
            product_dictionary['brand'] = "None"
            product_dictionary['flavours'] = ["None"]
            product_dictionary['top notes'] = ["None"]
            product_dictionary['heart notes'] = ["None"]
            product_dictionary['base notes'] = ["None"]
            product_dictionary['image link'] = "None"
            product_dictionary['href'] = split[1] 
            product_dictionary['complete'] = 'False'
        return(product_dictionary)

    def scrape_add(self, url_list:list, original_dict:dict) -> dict:
        '''
        Takes in a list of product urls to be scraped and an existing dictionary: scrapes and adds to dictionary
        Args:
            list: list of urls to be scraped
            original_dict: dictionary to be added to
        Returns: dictionary updated with the new product data
        '''
        for url in url_list:
            perfume = self.scrape_product(url)
            original_dict["href"].append(perfume["href"])
            original_dict["complete"].append(perfume["complete"])
            original_dict["uuid"].append(perfume["uuid"])
            original_dict["name"].append(perfume["name"])
            original_dict["id"].append(perfume["id"])
            original_dict["price"].append(perfume["price"])
            original_dict["strength"].append(perfume["strength"])
            original_dict["category"].append(perfume["category"])
            original_dict["brand"].append(perfume["brand"])
            original_dict["flavours"].append(perfume["flavours"])
            original_dict["top notes"].append(perfume["top notes"])
            original_dict["heart notes"].append(perfume["heart notes"])
            original_dict["base notes"].append(perfume["base notes"])
            original_dict["image link"].append(perfume["image link"])
        return original_dict

    def download_image(self, url:str, file_name:str, dir_path:str):
        '''
        Downloads image from given product url
        Args:
            url: product url
            file_name: name of file 
            dir_path: name of directory to downloaded to
        
        '''
        self.driver.get(url) 
        time.sleep(1)
        try:
            im_link = self.driver.find_element(By.XPATH, '//*[@id="product_pic_1"]')
            i_link = im_link.find_element(By.TAG_NAME, 'img')
            image_link = i_link.get_attribute('src')
            self.driver.implicitly_wait(2)
            self.driver.get(image_link)
            full_path = dir_path + file_name + '.jpg'
            if os.path.exists(full_path) == False:
                urllib.request.urlretrieve(image_link, full_path)
        except NoSuchElementException:
            pass

    def downloads_multiple_img(self, url_list:list, dir_path:str):
        '''
        Downloads multiple images to the directory path given
        Args:
            url_list: list of urls with images to be downloaded
            dir_path: path to directory to download to
        '''
        for url in url_list:
            split = url.split("s/")
            href = split[1]
            full_path = dir_path + href +'.jpg'
            if os.path.exists(full_path) == False:
                self.download_image(url=url, file_name=href, dir_path=dir_path)
            else:
                pass

    # MANIPULATING AND STORING THE DATA 

    def dump_json(self, filepath:str, dict:dict, dict_name:str):
        '''
        Stores ditionary as json file
        Args:
            filepath: path to the directory to store the json
            dict: dictionary to be stored
            dict_name: name of json file (must end .json)
        '''
        with open(os.path.join(filepath, dict_name), mode='w') as f:
            json.dump(dict, f)

    def data_clean(self, dictionary:dict) -> pd.DataFrame:
        '''
        Converts dictionary to pandas dataframe and cleans the data
        Args: dictionary: dictionary to be converted
        Returns: a cleaned dataframe
        '''

        def split_rename(df_column, new_name_stem):
            new_df = pd.DataFrame(df_column.tolist())
            column_list = new_df.columns

            def create_mapper(list, string):
                length = len(list)
                dict = {}
                for i in range(length):
                    no = str(i)
                    dictvalue = string + no
                    dict[i] = dictvalue
                return dict
            mapper = create_mapper(list=column_list, string=new_name_stem)
            renamed_df = new_df.rename(mapper=mapper, axis=1)
            return renamed_df

        df1 = pd.DataFrame.from_dict(dictionary, orient='index')
        df1 = df1.transpose()
    
        # data cleaning - strength and volume columns 
        df1['strength'] = df1['strength'].str.split('/')
        sub1 = pd.DataFrame(df1['strength'].tolist())
        sub1 = sub1.rename({0:'volume', 1:'strengths'}, axis=1)
        sub1['volume'] = sub1['volume'].str.replace('m','')
        sub1['volume'] = sub1['volume'].str.replace('l','')
        sub1['volume'] = sub1['volume'].str.replace(' ','')
        sub1['strengths'] = sub1['strengths'].str.replace('Extrait de Parfum', 'EdP')
        sub1['strengths'] = sub1['strengths'].str.replace('Parfum', 'Extrait')
        if sub1['volume'].empty:
            sub1['volume'] = sub1['volume'].astype(float)

        df2 = pd.concat([df1, sub1], axis=1)

        df2.drop(columns=['id'], inplace=True)
        df2.drop(columns=['category'], inplace=True)
        df2.drop(columns=['strength'], inplace=True)
        df2['price'] = df2['price'].str.replace('£','')
        if df2['price'].empty:
            df2['price'] = df2['price'].astype(float)   
    
        column_order = ['href', 'uuid', 'name', 'price', 'volume', 'strengths', 'brand', 'flavours', 'top notes',
       'heart notes', 'base notes', 'image link']
        df2 = df2.reindex(columns=column_order)

        subf = split_rename(df2['flavours'], 'F')
        subtn = split_rename(df2['top notes'], 'TN')
        subhn = split_rename(df2['heart notes'], 'HN')
        subbn = split_rename(df2['base notes'], 'BN')

        df3 = pd.concat([df2, subf, subtn, subhn, subbn], axis=1)
        return df3

    def open_json(self, file_path:str) -> dict:
        '''
        Opens json file to dictionary 
        Args: filepath: path to json file to be uploaded
        '''
        with open(file_path, mode='r') as f:
            data = json.load(f)
            return data

    def upload_directory(self, dir_path:str):
        '''
        Uploads a diretory directly to S3 bucket
        Args: dir_path: path to directory to be uploaded
        '''
        bucket = self.bucket
        for (root, dirs, files) in os.walk(dir_path):
            for file in files:
                self.s3.upload_file(os.path.join(root,file),bucket,file)

    def update_database_rds(self, data_frame:pd.DataFrame, table_name:str):
        '''
        Creates/ replaces an RDS table with data stored as a dataframe
        Args:
            data_frame: data to be uploaded
            table_name: RDS table name 
        '''
        data_frame.to_sql(table_name, self.engine, if_exists='replace')

    def update_table_rds(self, data_frame:pd.DataFrame, table_name:str):
        data_frame.to_sql(table_name, con = self.engine, if_exists = 'append')

    def inspect_rds(self, table_name:str) -> pd.DataFrame:
        '''
        Reads rds database data into a pandas database
        Args: table_name: table to be inspected
        '''
        table_data = pd.read_sql_table(self.table, self.engine)
        # pd.read_sql_query('''SELECT * FROM actor LIMIT 10''', engine)
        return table_data

    def key_exists(self, mykey, mybucket) -> bool:
        '''
        Inspects S3 bucket to see if a file exists
        Args:
            mykey: filename to be inspected
            mybucket: name of S3 bucket to be searched
        Returns: boolean value if the keys exists
        '''
        try:
            response = self.s3.list_objects_v2(Bucket=mybucket, Prefix=mykey)
            if response:
                for obj in response['Contents']:
                    if mykey == obj['Key']:
                        return True
        except:
            return False

    def find_rdsunscraped(self, scraped_href:list, rds_href:list) -> list:
        '''
        Takes in a list of scraped hrefs and compares to the hrefs stored on RDS
        Args:
            scraped_href: list of new product hrefs scraped 
            rds_href: list of hrefs stored on RDS database
        Returns: a list of urls of products that do not have results on RDS
        '''
        rds_unscraped_url = []
        rds_unscraped_href = []
        for x in scraped_href:
            if x not in rds_href:
                url = self.bloom_href(x)
                rds_unscraped_url.append(url)
                rds_unscraped_href.append(x)
        print('RDS new entries:', len(rds_unscraped_url))
        return rds_unscraped_url

    def url_to_href(self, url:str) -> str:
        '''
        Converts bloom product url to href
        '''
        split = url.split("s/")
        return split[1]

    def href_to_url(self, base_url:str, href:str) -> str:
        '''
        Adds href to a given url
        '''
        return base_url + href

    def bloom_href(self, href:str) -> str:
        '''
        Creates full url from product href
        '''
        return self.href_to_url(base_url='https://bloomperfume.co.uk/products/', href=href)

    def rds_columntolist(self, table:str, column:str) -> list:
        '''
        Converts data in a specified RDS table column to a list 
        Args:
            table: table to be insected
            column: name of column to be inspected
        Returns: a list containing all column data
        '''
        rds_df = self.inspect_rds(table_name=table)
        list = rds_df[column].tolist()
        return list 

    def check_S3(self, href_list:list, s3_bucket:str) -> list:
        '''
        Takes in list of hrefs, checks whether their corresponding images exist in S3 bucket
        Args:
            href_list: list of product hrefs to  be checked against images on S3 bucket
        Returns: list of urls of products without images on S3
        '''
        s3_noimg = []
        for href in href_list:
            mykey = str(href) + '.jpg'
            result = self.key_exists(mykey, s3_bucket)
            if result == False:
                url = self.bloom_href(href)
                s3_noimg.append(url)
            else:
                pass
        print("Not on s3: ", len(s3_noimg))
        return s3_noimg

    def url_href_list(self, urls:str) -> list:
        '''
        Takes list of urls
        Returns list of hrefs 
        '''
        scraped_href_list = []
        for x in urls:
            href = self.url_to_href(x)
            scraped_href_list.append(href)
        return scraped_href_list

    # INTEGRATING THE ABOVE

    def run_scraper(self, no_pages, RDS=True, S3=False, local=False):
        '''
        This method integrates the other methods above.
        Args:
            no_pages: number of product pages to be scraped
            RDS: toggles whether to check and update the RDS database (default on)
            S3: toggles whether to check and update S3 for product images (default off)
            local: toggles whether to check and update local json file of product data (default off)

        '''
        # scrapes the urls of all the products 
        new_urls = self.get_multiple_links(no_pages) # 42 maximum 
        new_hrefs = self.url_href_list(new_urls)

        if RDS:
            '''
            Compares cloud database entries to the newly scraped urls. 
            Only scrapes products that do not exist on the cloud. 
            '''
            # inspects the cloud database and produces a list of hrefs stored
            rds_hrefs = self.rds_columntolist(table=self.table, column='href')
            rds_tobescraped = self.find_rdsunscraped(new_hrefs, rds_hrefs)
            # scrape the new list and add to empty dictionary
            new_dict = self.scrape_add(rds_tobescraped, self.dict)
            # cleans the dictionary and turns into pd dataframe, appends to rds 
            clean_df = self.data_clean(new_dict)
            self.update_table_rds(data_frame=clean_df, table_name=self.table)

        if S3:
            '''
            Compares images stored on S3 with the newly scraped urls. 
            Only downloads and uploads images that do not exist on S3.  
            '''
            no_images_s3_urls = self.check_S3(new_hrefs, self.bucket)
            if len(no_images_s3_urls) > 1:
                self.downloads_multiple_img(no_images_s3_urls, '/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/data/')
                print("Downloading images..")
                self.upload_directory('/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/data/')
            elif len(no_images_s3_urls) == 1:
                filename = str(no_images_s3_urls[0])
                self.download_image(filename, '/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/data/')
                print("Downloading image..")
                self.upload_directory('/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/data/')
            else:
                pass
            print("Uploading folder to S3...")

        if local:
            '''
            Compares product data stored locally to newly scraped urls. 
            Only scrapes from products not present in the database. 
            Creates database if it does not exist already. 
            '''
            # opens local dictionary 
            data_directory = '/Users/emmasamouelle/Desktop/Scratch/data_collection_pipeline/data/'
            local_data = 'Sample_dict.json'
            if os.path.exists(data_directory + local_data) == True:
                stored_dict = self.open_json(data_directory + local_data)
            # compares new href to stored entry 
                href_list = stored_dict['href']
                dict_url_list = []
                for href in new_hrefs:
                    if href not in href_list:
                        url = self.bloom_href(href)
                        dict_url_list.append(url)
                updated_dict = self.scrape_add(dict_url_list, stored_dict)
            else:
                updated_dict = self.scrape_add(new_urls, self.dict)
            self.dump_json(data_directory, updated_dict, local_data)
            print("Storing data locally...")

        else: 
            print("No data format selected")
        print("Job complete")
        print("-------------------")
        # self.close_webpage()

if __name__ == '__main__':      
    my_scraper = PerfumeScraper("https://bloomperfume.co.uk/collections/perfumes", container=False)
    my_scraper.run_scraper(no_pages=1)
