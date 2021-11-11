from sw_cybersixgill_dvefeed_ingestion import SixgillDvefeedIngestionBaseClass


class SwMain(SixgillDvefeedIngestionBaseClass):

    def execute(self):
        try:
            self.auth_test()
        except Exception as e:
            return {'successful': False,
                    'errorMessage': str(e)}
        return {'successful': True}
