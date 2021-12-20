from sw_cybersixgill_dvefeed_ingestion import SixgillAPIRequests, SwimlaneDVEFeedFields


class SwMain(SixgillAPIRequests):

    @classmethod
    def process_feed_data(cls, feed):
        """Process the dvefeed data"""

        x_sixgill_info = feed.get('x_sixgill_info', {})
        event = x_sixgill_info.get('event', {})
        nvd = x_sixgill_info.get('nvd', {})
        rating = x_sixgill_info.get('score', {})

        raw_response = SwimlaneDVEFeedFields(
            feed.get('created', ''), feed.get('modified'),
            feed.get("external_references", [])[0].get("external_id", ''),
            feed.get('type', ''),
            rating.get('current', 0),
            rating.get('highest').get('date', ''),
            rating.get('highest').get('value', 0),
            rating.get('previouslyExploited', 0),
            event.get('name', ''),
            event.get('type', ''),
            event.get('action', ''),
            event.get('prev_level', ''),
            event.get('description', ''),
            event.get('event_datetime', ''),
            nvd.get('base_score_v3', 0),
            nvd.get('base_severity_v3', ''),
            nvd.get('link', ''),
            nvd.get('modified', ''),
            nvd.get('published', ''),
            nvd.get('score_2_0', 0),
            nvd.get('severity_2_0', ''),
            nvd.get('vector_v2', ''),
            nvd.get('vector_v3', ''),
            x_sixgill_info
        ).__dict__

        return raw_response

    def execute(self):
        dvefeed_data = self.get_dvefeed()

        processed_dvefeed = list(map(self.process_feed_data, dvefeed_data))

        self.sixgill_dvefeed_client.commit_indicators()

        return processed_dvefeed