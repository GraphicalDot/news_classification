news_classification
===================

Scripts to parse and classify news on the basis of categories which are being scraped from different news sources

Arguments example:
                source: Source of the news which in our case could be of three types yet.
                        HT_NDLS
                        HIN_NDLS
                        TOI_NDLS
                published_date:
                        Get news on the basis of the day it was published.Right now you cannot get news on the basis of
                        source from which its been published and the published date
                        Format:
                                "18 jun 2014"
                skip:
                        News to be skipped in the db before the count starts.For example if skip = 100, 100 latest news will
                        be skipped before new news will be delivered.

                count: NUmber of new article to be delivered.

Response: Every get request will return following fields for every new article present in the database
		full_text: This key will have the whole article of the news
		id: unique id of the news article, this will be used to when sending a post request to update the tag filed for the news.
		link: Whole link of the news from which it was been scraped.
		source: As mentioned above
		tag: empty is its not been tagged yet or tag name if it was tagged before.

Get Request:

	Example1: http://ec2-54-236-232-96.compute-1.amazonaws.com/news?skip=10&count=1
		This will return 1 news articles after skipping 10 news articles from the db but it can be of any source as no source was mentioned.
		Count can be changed to increase the number of articles.
	
	Example2:
		http://ec2-54-236-232-96.compute-1.amazonaws.com/news?source=HT_NDLS&skip=20&count=1
		This will return 1 news articles after skipping 10 news articles having source hindustan times.

	Example3:
		http://ec2-54-236-232-96.compute-1.amazonaws.com/news?published_date=11 jan 2014&skip=20&count=1
		This will give you one news article published on 11 jan 2014 after skippping 20 news article.	
	

Post request
Data to be posted in post request example
	[{'id': '52cecec60d0cee0dc8e577a8', 'tag': 'event'},
 	{'id': '52cecec60d0cee0dc8e577a9', 'tag': ''},
 	{'id': '52ced1be0d0cee0dc8e577c7', 'tag': 'announcement'},
 	{'id': '52cedef60d0cee0dc8e577a8', 'tag': 'crime'},
	{'id': '52cecec60d0cee0dc8e57798', 'tag': 'event'}]

	The post request shall have the list od dictionaries to be posted under the argument news_list to be posted at the below mentioned url
	
	http://ec2-54-236-232-96.compute-1.amazonaws.com/tags
	This url wil return a success = True if all the ids being uploaded are present in the db(i.e every id is correct as it was sent in get request)
	and will have three lists being returned:
		invalid_ids: Ids which were not present in the databse.
		success_ids: All the ids which was tagged successfully.
		scraped_ids = ids of the news articles which either have empty tag or id length less than 24 characters.
