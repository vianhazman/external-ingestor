from unittest import TestCase
import pandas as pd
from mock import patch
from sqlalchemy import create_engine

from external_ingestor.sink.PostgresSink import PostgresSink


class PostgresSinkTest(TestCase):
    def setUp(self):
        payload = [{'url': 'https://vianhazman.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None, 'via_channel': 'sample_ticket', 'via_source_rel': None, 'created_at': '2020-07-01 01:52:49 UTC', 'updated_at': '2020-07-01 01:52:50 UTC', 'type': 'incident', 'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket', 'description': "Hi Favian,\n\nThis is your first ticket. Ta-da! Any customer request sent to your supported channels (email, chat, voicemail, web form, and tweet) will become a Support ticket, just like this one. Respond to this ticket by typing a message above and clicking Submit. You can also see how an email becomes a ticket by emailing your new account, support@vianhazman.zendesk.com. Your ticket will appear in ticket views.\n\nThat's the ticket on tickets. If you want to learn more, check out: \nhttps://support.zendesk.com/hc/en-us/articles/203691476\n", 'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 900441301423, 'submitter_id': 900440868623, 'assignee_id': 900440868623, 'organization_id': None, 'group_id': 900001417543, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'brand_id': 900000531763, 'allow_channelback': False, 'allow_attachments': True, 'generated_timestamp': '2020-07-01 08:52:50 UTC'}, {'url': 'https://vianhazman.zendesk.com/api/v2/tickets/2.json', 'id': 2, 'external_id': None, 'via_channel': 'web', 'via_source_rel': None, 'created_at': '2020-07-01 01:57:22 UTC', 'updated_at': '2020-07-01 01:57:22 UTC', 'type': None, 'subject': 'Ticket 1', 'raw_subject': 'Ticket 1', 'description': '1234', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 900442133526, 'submitter_id': 900440868623, 'assignee_id': 900440868623, 'organization_id': None, 'group_id': 900001417543, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': [], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'brand_id': 900000531763, 'allow_channelback': False, 'allow_attachments': True, 'generated_timestamp': '2020-07-01 08:57:22 UTC'}]
        self.df = pd.DataFrame.from_dict(payload)
        self.settings = {
            "user":"postgres",
            "pass": "postgres",
            "port": 5432,
            "db": "postgres",
            "host": "localhost",
            "table_name":"test_table"
        }
        self.conn = PostgresSink(self.settings)

    def test_jdbc_url(self):
        actual_url = self.conn.url
        expected_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
        self.assertEqual(actual_url, expected_url)

    @patch.object(pd.DataFrame, 'to_sql')
    def test_write_df(self, mock_request):
        self.conn.sink(self.df)
        expected_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
        assert mock_request.called