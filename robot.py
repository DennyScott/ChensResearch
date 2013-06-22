##
## Module to retrieve robots.txt for a given url, and check if the path is allowed.
## The function is_allowed(robots, url) returns True if robots.txt found,
## and path not disallowed by robots.txt, False otherwise.
## The robots={} cache will be updated with host rules.
## If you want to access it, the cache is of the form:
## {'host_1': ['disallowed_path_1', ... 'path_n'], ... 'host_n': [...]}
##

import urllib
def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def split_url(url):
    '''splits a URL into host and path parts, returns (host, path)'''
    if not url.startswith(('http://', 'https://', 'ftp://')):
        return  url,''
    skip = url.find('//') + 2
    start = url.find('/', skip) # find start of path after 'protocol://'
    if start == -1:               # if there's no path...
        return url, '/'
    host, path =  url[skip:].split('/', 1)
    return url[:skip] + host, '/' + path # prepend the protocol to the host.

def parse_robots(robots_txt):
    '''parses a robots.txt and extracts rules for 'User-agent: *', returned as a list of paths'''
    rules = []
    start = robots_txt.find('User-agent: *') + 14 # 14 is length of 'User-agent: *\n'
    if start == -1:                               # 'User-agent: *' not found
        return None, 0
    end = robots_txt.find('User-agent:', start)   # there shouldn't be another user-agant after *, but in case of malformed robots.txt...
    lines = robots_txt[start:end].splitlines()
    for line in lines:
        if 'Disallow:' in line:
            rules.append(line[10:])
    return rules

def get_robots(robots, host):
    '''read robots.txt from host and add rules to robots dict'''
    robots[host] = parse_robots(get_page(host+'/robots.txt'))

def check_robots(robots, host, path):
    '''check if path is allowed according to rules in rbots dict'''
    if host not in robots or path == '':    # if we still don't have a robots.txt for this host,
        return False                        # play nice and don't crawl
    for rule in robots[host]:
        if path.startswith(rule):
            return False
    return True

def is_allowed(robots, url):
    '''check if there is a robots entry for the host, get one if not,
       then check if the path is allowed, returting True or False'''
    host, path = split_url(url)
    if host not in robots:
        get_robots(robots, host)
    return check_robots(robots, host, path)

#### Test cases
##robots ={}
##tests = [['http://www.udacity.com/cs101x/urank/index.html', True],
##        ['http://www.udacity.com/ajax', False],
##        ['https://google.com/', True],
##        ['https://google.com/search', False],
##        ['not a URL', False],
##        ['', False]]
##for test in tests:
##    print is_allowed(robots, test[0]) == test[1]
##### ==> True