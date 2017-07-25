'''
For django's parameters setting.
'''
import os
import re


def getSystemTimeZone():
    '''
    get system time zone info
    '''

    result = ''

    tzinfo = os.popen('timedatectl').readlines()
    pattern = re.compile('\ [a-zA-Z]+(\/[a-zA-Z\_\-]+){1,2}\ ')
    for i in range(len(tzinfo)):
        if "Timezone" in tzinfo[i] or "Time zone" in tzinfo[i]:
            target = pattern.search(tzinfo[i])
            if target is not None:
                result = target.group()
            break
    return result.strip()
