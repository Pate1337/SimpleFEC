class FileHandling(object):
  def __init__(self, fileName):
    self.file = open(fileName, 'rb+')
  
  def read_next_bytes(self):
    #return self.file.read(100).decode('utf-8')
    return self.file.read(100).decode('utf-8')
  
  def read_bytes(self, index):
    self.file.seek(index)
    return self.file.read(100).decode('utf-8')
  
  def close(self):
    self.file.close()
  
  def text_matches_file_part(self, index, text):
    text_from_file = self.read_bytes(index)
    return text == text_from_file
