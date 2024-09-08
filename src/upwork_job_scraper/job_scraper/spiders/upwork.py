import scrapy
from scrapy.http import HtmlResponse
import random


class UpworkSpider(scrapy.Spider):
    name = "upwork"
    allowed_domains = ["upwork.com"]

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    ]

    def __init__(self, search_query: str, *args, **kwargs):
        super(UpworkSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            f"https://www.upwork.com/search/jobs/?q={search_query}&sort=recency"
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, headers={"User-Agent": random.choice(self.user_agents)}
            )

    def parse(self, response: HtmlResponse):
        for job in response.css("article.job-tile.cursor-pointer"):
            yield {
                "job_title": job.css("a.up-n-link::text").get(),
                "job_price": job.css(
                    "li[data-test='job-type-label'] strong::text"
                ).get(),
                "job_duration": job.css(
                    'li[data-test="duration-label"] strong:nth-child(2)::text'
                ).get(),
            }
