import scrapy
from scrapy.http import HtmlResponse


class UpworkSpider(scrapy.Spider):
    name = "upwork"
    allowed_domains = ["upwork.com"]

    def __init__(self, search_query: str, *args, **kwargs):
        super(UpworkSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            f"https://www.upwork.com/search/jobs/?q={search_query}&sort=recency"
        ]

    def parse(self, response: HtmlResponse):
        for job in response.css("article.job-tile.cursor-pointer"):
            yield {
                "job_title": job.css("a.up-n-link::text").get(),
            }
