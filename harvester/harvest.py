from google.appengine.api import urlfetch
import json, logging

class Harvest(object):

    url_base = 'https://%s.harvestapp.com'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Harvester by SPW'
    }

    def __init__(self, app_name, auth_key, user_id=None):
        self.url = self.url_base % app_name
        self.headers['Authorization'] = 'Basic %s' % auth_key
        self.user_id = user_id

    def get_api_response(self, url, **kwargs):
        try:
            result = urlfetch.fetch("%s/%s" % (self.url, url), headers=self.headers, deadline=10, **kwargs)
            logging.critical(result.content)
            return json.loads(result.content)
        except urlfetch.DeadlineExceededError:
            return None

    def _get_user(self):
        return self.get_api_response('account/who_am_i')

    def get_project(self, project_id):
        return self.get_api_response('projects/%s' % project_id)

    def get_report(self, from_date, to_date):
        url = 'people/%s/entries?from=%s&to=%s' % (self.user_id, from_date, to_date)
        report = self.get_api_response(url)

        entries = {}
        total_hours = 0.0

        for entry in report:
            hours = float(entries.get(entry.get('day_entry').get('project_id'), 0))
            hours += float(entry.get('day_entry').get('hours'))

            # project = self.get_project(entry.get('day_entry').get('project_id'))
            # entries[project.get('name')] = hours
            entries[entry.get('day_entry').get('project_id')] = hours

        for (project_id, hours) in entries.iteritems():
            total_hours = total_hours + hours

        return {
            'entries': entries,
            'total_hours': total_hours
        }
