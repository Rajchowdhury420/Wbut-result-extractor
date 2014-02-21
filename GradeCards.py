import urllib, urllib2, httplib, os, string

URL = 'http://www.wbutech.net/show-result.php'

class RedirectHandler(urllib2.HTTPRedirectHandler):
  def http_error_302(self, req, fp, code, msg, headers):
    response = urllib2.HTTPRedirectHandler.http_error_302(
      self, req, fp, code, msg, headers)
    response.status = code
    return response
  
def getName(data):
  start = string.find(data, 'Name :') + len('Name :') + 1
  end = string.find(data, '<', start)
  name = data[start:end]
  return name

def getSGPA(data):
  start = string.find(data, 'SEMESTER :') + len('SEMESTER :') + 1
  end = string.find(data, '<', start)
  return data[start:end]
  
def Post(data):
  roll = data['rollno']
  data = urllib.urlencode(data)
  opener = urllib2.build_opener(RedirectHandler())
  opener.addheaders = [('User-agent', 'Mozilla/5.0'),('Referer', 'http://www.wbutech.net/result.php')]
  res = opener.open(URL, data, timeout=10)
  print '\nFetching result of ' + roll + '...',
  try:
    if(res.status == 302):
      print '\nRoll no. :' + roll + ' not found!'
    
    return None
  except AttributeError:
    return res.read()
  
  
def Write(data, name, roll):
  with open('Results/' + name + '_' + roll[-2:] + '.html', 'wb') as result:
    result.write(data)
  
roll_prefix = '104002100'
def main():
  semno = 5 #The results will be fetched of this semester
  start, end = 1, 78
  if not os.path.exists('Results'):
    os.makedirs('Results')
  for i in range(start, end + 1):
    rollno = roll_prefix + str(i).zfill(2);
    a = Post({'rollno':rollno, 'semno':semno})
    if a is not None:
      name = getName(a)
      sgpa = getSGPA(a)
      print name, sgpa
      Write(a, name, rollno)
  
if __name__ == '__main__':
  main()
