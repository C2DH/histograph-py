from requests import request
import json
import urllib

from .util import to_slug
from .error import HistographError

API_PREFIX = 'api/v1'

DEFAULT_DISCOVERY_PARAMETERS = {
  "nedMethod": "opentapioca", 
	"entityFilter": "openTapiocaCumulativeScore"
}

def _get_default_headers(api_key):
  return {
    'Authorization': 'Bearer {}'.format(api_key),
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }

def _handle_error(response):
  if response.status_code >= 400:
    try:
      body = response.json()
    except json.decoder.JSONDecodeError:
      body = None
    if body is None:
      response.raise_for_status()
    raise HistographError(body.get('message'), body.get('stack'), response.status_code)

class HistographApiClient:
  def __init__(self, url, api_key):
    self.__url = url.strip('/')
    self.__api_key = api_key

  def __request(self, path, method = 'GET', payload = {}):
    url = '{}/{}{}'.format(self.__url, API_PREFIX, path)
    response = request(method, url, data=json.dumps(payload), headers=_get_default_headers(self.__api_key))
    _handle_error(response)
    return response.json()

  def get_user_details(self):
    return self.__request('/users/self').get('user', {})

  def get_curated_resources(self):
    return self.__request('/resources/curated').get('resources', [])

  def create_resource(self, resource, entities = None, entities_locations = None, skip_ner = False):
    '''
    Create and POST create resource payload.
    '''
    payload = {
      'resource': resource,
      'skipNER': skip_ner
    }

    if entities is not None:
      payload['entities'] = entities
    if entities_locations is not None:
      payload['entitiesLocations'] = entities_locations

    return self.__request('/resources', 'POST', payload).get('resource')

  def add_resource(
    self,
    type,
    start_date,
    end_date,
    language,
    title,
    caption,
    content,
    slug = None,
    mime_type = None,
    index_content = False,
    previous_resource_uuid=None,
    iiif_url=None):
    '''
    TODO: Add a method to add a multi language resource.
    '''
    payload = {
      'type': type,
      'start_date': start_date,
      'end_date': end_date,
      'slug': slug if slug is not None else to_slug(title),
      'title': { language: title },
      'caption': { language: caption },
      'content': { language: content }
    }

    if mime_type is not None:
      payload['mime_type'] = mime_type

    if previous_resource_uuid is not None:
      payload['previous_resource_uuid'] = previous_resource_uuid

    if index_content is True:
      payload['index_content'] = True

    if iiif_url is not None:
      payload['iiif_url'] = iiif_url

    resource_payload = {
      'resource': payload
    }

    return self.__request('/resources', 'POST', resource_payload).get('resource')

  def start_discovery(self, parameters = DEFAULT_DISCOVERY_PARAMETERS):
    return self.__request('/resources/discovery-processes', 'POST', parameters).get('refId')

  def get_discovery_process_logs(self, id):
    return self.__request('/resources/discovery-processes/{}'.format(id), 'GET')

  def start_pipeline_process(self, name, parameters):
    return self.__request('/pipelines/processes', 'POST', { 'name': name, 'parameters': parameters }).get('refId')

  def get_pipeline_process_logs(self, id):
    return self.__request('/pipelines/processes/{}'.format(id), 'GET')

  def update_resource_topic_modelling_scores(self, slug_or_id, scores):
    return self.__request(urllib.request.quote('/resources/{}/topic-modelling-scores'.format(slug_or_id)), 'PUT', { 'scores': scores })

  def update_topic(self, topic_set, topic_index, label = None, keywords = None):
    payload = {}
    if label:
      payload['label'] = label
    if keywords:
      payload['keywords'] = keywords
    if len(payload.keys()) == 0:
      return

    return self.__request(urllib.request.quote('/topics/{}/{}'.format(topic_set, topic_index)), 'PUT', payload)
