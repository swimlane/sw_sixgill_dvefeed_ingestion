from sw_sixgill_dvefeed_ingestion import SixgillDvefeedIngestionBaseClass


class SwMain(SixgillDvefeedIngestionBaseClass):

    def execute(self):
        try:
            self.auth_test()
        except Exception as e:
            return {'successful': False,
                    'errorMessage': "Auth request failed - please verify client_id and client_secret."}
        return {'successful': True}
