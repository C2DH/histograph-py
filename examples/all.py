from histograph import HistographApiClient
import time

if __name__ == "__main__":
  client = HistographApiClient('http://localhost:8000', '479d39b530bf5a7284a14df5ce30c940252e5c351cd57fd1')
  resources = client.get_curated_resources()
  print('\nCurated Resources:\n', resources)

  resource = client.add_resource(
    'external-text',
    '2019-05-01',
    '2019-05-02',
    'en',
    'Test resource from Python Client',
    'This is a Test resource from Python Client library',
    '''
    Python is an interpreted, high-level, general-purpose programming language. Created by Guido van Rossum and 
    first released in 1991, Python's design philosophy emphasizes code readability with its notable use of 
    significant whitespace. Its language constructs and object-oriented approach aims to help programmers 
    write clear, logical code for small and large-scale projects.
    '''
  )
  print('\nNew resource:\n', resource)
  discovery_process_id = client.start_discovery()
  print('\nDiscovery process ID:\n', discovery_process_id)

  print('\nsleeping...')
  time.sleep(3)

  discovery_logs = client.get_discovery_process_logs(discovery_process_id)
  print('\nStdout Logs:\n{}'.format(discovery_logs.get('stdout')))
  print('\nStderr Logs:\n{}'.format(discovery_logs.get('stderr')))
