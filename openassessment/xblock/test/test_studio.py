"""
View-level tests for Studio view of OpenAssessment XBlock.
"""

import json
import datetime as dt
import lxml.etree as etree
import pytz
from ddt import ddt, file_data
from .base import scenario, XBlockHandlerTestCase


@ddt
class StudioViewTest(XBlockHandlerTestCase):
    """
    Test the view and handlers for editing the OpenAssessment XBlock in Studio.
    """

    @scenario('data/basic_scenario.xml')
    def test_render_studio_view(self, xblock):
        frag = self.runtime.render(xblock, 'studio_view')
        self.assertTrue(frag.body_html().find('openassessment-edit'))

    @scenario('data/basic_scenario.xml')
    def test_get_editor_context(self, xblock):
        resp = self.request(xblock, 'editor_context', '""', response_format='json')
        self.assertTrue(resp['success'])
        self.assertEqual(resp['msg'], u'')

        # Verify that the Rubric has criteria, and that they are a list of dictionaries
        self.assertTrue(isinstance(resp['rubric']['criteria'], list))
        self.assertTrue(isinstance(resp['rubric']['criteria'][0], dict))

        # Verify that every assessment in the list of assessments has a name.
        for assessment_dict in resp['assessments']:
            self.assertTrue(assessment_dict.get('name', False))
            if assessment_dict.get('name') == 'student-training':
                examples = etree.fromstring(assessment_dict['examples'])
                self.assertEqual(examples.tag, 'examples')

    @file_data('data/update_xblock.json')
    @scenario('data/basic_scenario.xml')
    def test_update_context(self, xblock, data):
        xblock.published_date = None
        resp = self.request(xblock, 'update_editor_context', json.dumps(data), response_format='json')
        self.assertTrue(resp['success'], msg=resp.get('msg'))

    @file_data('data/invalid_update_xblock.json')
    @scenario('data/basic_scenario.xml')
    def test_update_context_invalid_request_data(self, xblock, data):
        xblock.published_date = None
        resp = self.request(xblock, 'update_editor_context', json.dumps(data), response_format='json')
        self.assertFalse(resp['success'])
        self.assertIn(data['expected_error'], resp['msg'].lower())

    @file_data('data/invalid_rubric.json')
    @scenario('data/basic_scenario.xml')
    def test_update_rubric_invalid(self, xblock, data):
        request = json.dumps(data)

        # Store old XBlock fields for later verification
        old_title = xblock.title
        old_prompt = xblock.prompt
        old_assessments = xblock.rubric_assessments
        old_criteria = xblock.rubric_criteria

        # Verify the response fails
        resp = self.request(xblock, 'update_editor_context', request, response_format='json')
        self.assertFalse(resp['success'])
        self.assertIn("the following keys were missing", resp['msg'].lower())

        # Check that the XBlock fields were NOT updated
        # We don't need to be exhaustive here, because we have other unit tests
        # that verify this extensively.
        self.assertEqual(xblock.title, old_title)
        self.assertEqual(xblock.prompt, old_prompt)
        self.assertItemsEqual(xblock.rubric_assessments, old_assessments)
        self.assertItemsEqual(xblock.rubric_criteria, old_criteria)

    @scenario('data/basic_scenario.xml')
    def test_check_released(self, xblock):
        # By default, the problem should be released
        resp = self.request(xblock, 'check_released', json.dumps(""), response_format='json')
        self.assertTrue(resp['success'])
        self.assertTrue(resp['is_released'])
        self.assertIn('msg', resp)

        # Set the problem to unpublished with a start date in the future
        xblock.published_date = None
        xblock.start = dt.datetime(3000, 1, 1).replace(tzinfo=pytz.utc)
        resp = self.request(xblock, 'check_released', json.dumps(""), response_format='json')
        self.assertTrue(resp['success'])
        self.assertFalse(resp['is_released'])
        self.assertIn('msg', resp)
