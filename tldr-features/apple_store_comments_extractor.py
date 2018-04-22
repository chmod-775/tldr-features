import requests
import xmltodict
from dateutil import parser as date_parser
import os

class AppleStoreCommentsExtractor():
    def transform(self, X): # TODO: So, X here is 1 id that corresponds to many comments?
        for x in X:
            url = self.compose_url(x)
            resp = requests.get(url)
            return self.parse_xml(resp.content)

    def compose_url(self, id):
        base_url = 'https://itunes.apple.com/us/rss/customerreviews/'
        suffix = 'mostrecent/xml'
        return os.path.join(base_url, f"id={id}", suffix)

    def parse_xml(self, xml_text):
        raw_reviews_dict = xmltodict.parse(xml_text)
        entries = raw_reviews_dict['feed']['entry'][1:]
        review_types = [list(filter(lambda x: x['@type'] == 'text', entry['content'])) for entry in entries]
        review_text = [r_type[0]['#text'] for r_type in review_types]
        return [{
            'title': entry['title'],
            'content': rev_text,
            'updated_at': int(date_parser.parse(entry['updated']).timestamp()),
            'rating': entry['im:rating'],
        } for entry, rev_text in zip(entries, review_text)]
