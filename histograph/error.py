
class HistographError(Exception):
  def __init__(self, message, stack_trace=None, status_code=None):
    super().__init__(message)
    self.stack_trace = stack_trace
    self.status_code = status_code
