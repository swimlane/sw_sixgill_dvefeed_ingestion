from sixgill.sixgill_feed_client import SixgillFeedClient
import requests
from sixgill.sixgill_utils import is_indicator
from sixgill.sixgill_base_client import SixgillBaseClient
from sixgill.sixgill_constants import FeedStream


class SixgillDvefeedIngestionBaseClass:

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


    def __init__(self, created, modified, external_id, cve_type, rating_current, rating_highest_date,
                 rating_highest_value, rating_previously_exploited, event_name, event_type, event_action, prev_level,
                 event_description, event_datetime, nvd_base_score_v3, nvd_base_severity_v3, nvd_link, nvd_modified,
                 nvd_published, nvd_score_2_0, nvd_severity_2_0, nvd_vector_v2, nvd_vector_v3, x_cybersixgill_info):
        self.created = created
        self.modified = modified
        self.external_id = external_id
        self.type = cve_type
        self.rating_current = rating_current
        self.rating_highest_date = rating_highest_date
        self.rating_highest_value = rating_highest_value
        self.rating_previously_exploited = rating_previously_exploited
        self.event_name = event_name
        self.event_type = event_type
        self.event_action = event_action
        self.prev_level = prev_level
        self.event_description = event_description
        self.event_datetime = event_datetime
        self.nvd_base_score_v3 = nvd_base_score_v3
        self.nvd_base_severity_v3 = nvd_base_severity_v3
        self.nvd_link = nvd_link
        self.nvd_modified = nvd_modified
        self.nvd_published = nvd_published
        self.nvd_score_2_0 = nvd_score_2_0
        self.nvd_severity_2_0 = nvd_severity_2_0
        self.nvd_vector_v2 = nvd_vector_v2
        self.nvd_vector_v3 = nvd_vector_v3
        self.x_cybersixgill_info = x_cybersixgill_info