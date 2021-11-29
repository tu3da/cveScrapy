# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import datetime
import os
import sqlite3

class CvescrapingPipeline(object):
    _db = None
    
    @classmethod
    def get_database(cls):
        cls._db = sqlite3.connect(
            os.path.join(os.getcwd(), 'cvescraping.db')
        )
        cursor = cls._db.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS cvescraping(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                url TEXT UNIQUE NOT NULL, \
                tags TEXT NOT NULL, \
                summary TEXT NOT NULL, \
                site TEXT NOT NULL \
            );')
        return cls._db

    def process_item(self, item, spider):
        self.save_cvescraping(item)
        return item
    
    def save_cvescraping(self, item):
        if self.find_cvescraping(item['url']):
            return
        
        db = self.get_database()
        db.execute(
            'INSERT INTO cvescraping (url, tags, summary, site) VALUES (?, ?, ?, ?)',(
                item['url'],
                item['tags'],
                item['VulnSummary'],
                'Vulmon',
            )
        )
        db.commit()
    
    def find_cvescraping(self, url):
        db = self.get_database()
        cursor = db.execute(
            'SELECT * FROM cvescraping WHERE url=?',
            (url,)
        )
        return cursor.fetchone()