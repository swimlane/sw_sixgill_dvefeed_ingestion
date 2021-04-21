from sixgill.sixgill_feed_client import SixgillFeedClient
import requests
from sixgill.sixgill_utils import is_indicator
from sixgill.sixgill_base_client import SixgillBaseClient
from sixgill.sixgill_constants import FeedStream


class SixgillDvefeedIngestionBaseClass(object):

    def __init__(self, context):
        self.client_id = context.asset.get('client_id', '')
        self.client_secret = context.asset.get('client_secret', '')
        self.verify = context.asset.get('verify_ssl', False)
        http_proxy = context.asset.get('http_proxy')
        session = requests.Session()
        session.proxies = {} if not http_proxy else http_proxy
        self.proxy = session
        self.state = context.state
        self.channel_id = '9edd89168582842d84430bac51a06eb3'

    def auth_test(self):
        """checks to see if asset inputs are valid."""
        response = SixgillBaseClient(self.client_id, self.client_secret, self.channel_id, verify=self.verify,
                                     session=self.proxy).get_access_token()

        return response


class SixgillAPIRequests(SixgillDvefeedIngestionBaseClass):

    def __init__(self, context):
        super(SixgillAPIRequests, self).__init__(context)
        self.sixgill_dvefeed_client = SixgillFeedClient(client_id=self.client_id, client_secret=self.client_secret,
                                                        channel_id=self.channel_id, feed_stream=FeedStream.DVEFEED,
                                                        verify=self.verify, bulk_size=2000)

    def get_dvefeed(self):
        """returns the bundle of dvefeeds."""
        raw_response = self.sixgill_dvefeed_client.get_bundle()
        return list(filter(is_indicator, raw_response.get("objects", [])))


class SwimlaneDVEFeedFields:
    """returns the required fields to store in the swimlane platform."""

    def __init__(self, feed_id, created, external_references, event_id, action, description, event_datetime, level,
                 name, prev_level, score_type, base_score_v3, base_severity_v3, link, modified, published, score_2_0,
                 severity_2_0, vector_v2, vector_v3, current, highest_date, highest_value, previously_exploited,
                 x_sixgill_info):
        self.feed_id = feed_id
        self.created = created
        self.external_references = external_references
        self.event_id = event_id
        self.action = action
        self.description = description
        self.event_datetime = event_datetime
        self.level = level
        self.name = name
        self.prev_level = prev_level
        self.score_type = score_type
        self.base_score_v3 = base_score_v3
        self.base_severity_v3 = base_severity_v3
        self.link = link
        self.modified = modified
        self.published = published
        self.score_2_0 = score_2_0
        self.severity_2_0 = severity_2_0
        self.vector_v2 = vector_v2
        self.vector_v3 = vector_v3
        self.current = current
        self.highest_date = highest_date
        self.highest_value = highest_value
        self.previously_exploited = previously_exploited
        self.x_sixgill_info = x_sixgill_info
