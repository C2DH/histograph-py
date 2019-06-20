from requests import request
import json

from .util import to_slug
from .error import HistographError

API_PREFIX = 'api/v1'

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

  def get_curated_resources(self):
    return self.__request('/resources/curated').get('resources', [])

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
    mime_type = None):
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
      'content': { language: content },
    }

    if mime_type is not None:
      payload['mime_type'] = mime_type

    return self.__request('/resources', 'POST', payload).get('resource')

  def start_discovery(self):
    return self.__request('/resources/discovery-processes', 'POST').get('refId')

  def get_discovery_process_logs(self, id):
    return self.__request('/resources/discovery-processes/{}'.format(id), 'GET')
