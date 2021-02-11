class Span:
  def __init__(self, text, label):
    self.text = text
    self.label_ = label

class Doc:
  ents = (Span("Alex", "PERSON"), Span("test", "TEST_LABEL"))
  
  def __init__(self, text):
    self.text = text

class Nlp:
  @staticmethod
  def load(model):
    return Doc