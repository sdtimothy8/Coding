'''
this module is used to control user access
'''
import time
import crypt
from django.core.exceptions import PermissionDenied
from django.conf import settings
from public import functions
from session.permission import KSMP_Permission
from ksmp import logger
import userStatus


class SessionAuthticationMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, request):
        '''
        process the request object from upper middleware
        the request with valid authcode will be allowed to access resource,
        if without valid authcode, but with valid username and password will be allowed,
        otherwise access will be denied.
        '''
        request.isPermissioned = True
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        current_time = time.time()

        # delete expire auth
        deleteExpireAuth(session_key, current_time)

        # fetch new auth
        permission = KSMP_Permission()
        pms = permission.get_permission(session_key)
        authlist = permission.get_all_auth()

        data = {}
        urls = ['/login/validatecode/', '/monitor/cpu/load/', '/monitor/mem/', '/resources/psnetinfo/', '/monitor/disk/io/']
        if pms in authlist:
            permission.save_to_auth(pms, current_time)
        elif letpass(urls, request.path):
            pass
        else:
            if request.method == "GET":
                data = request.GET.copy()
            elif request.method == "POST":
                data = request.POST
            try:
                username = data['username']
                password = data['password']
            except KeyError:
                request.session.flush()
                raise PermissionDenied
            else:
                username = functions.unicorn_decrypt(username)
                password = functions.unicorn_decrypt(password)

                if not isrootuser(username):
                    request.isPermissioned = False
                    raise PermissionDenied

                # try_choices = request.COOKIES.get(settings.TRY_TIMES
                # check whether is existed or not.
                logger.debug(username)
                if not userStatus.isUserExist(username):
                    userStatus.initUserStatus(username)
                    logger.debug(username + 'check exist')
                # check whether username is locked
                # check access_time is over age.  if both yes, raise denied
                if userStatus.isUserLocked(username):
                    # request.isLocked = True
                    # check whether lock is over age.
                    logger.debug(username + 'check locked')
                    lastAccessTime = userStatus.getLastAccessTime(username)
                    if lastAccessTime and (current_time - float(lastAccessTime) < settings.LOCKEDAGE):
                        request.isPermissioned = False
                        # request.isLocked = True
                        raise PermissionDenied

                # check username and password. if right, get permissed and reset username's status
                if isvalidpassword(username, password):
                    authcode = permission.set_permission(username)
                    request.session._session_key = authcode
                    userStatus.initUserStatus(username)

                # raise deny. update access_time and try_times++
                else:
                    request.isPermissioned = False
                    logger.debug(username + 'update status')
                    userStatus.updateUserStatus(username=username, access_time=current_time)
                    raise PermissionDenied

    def process_response(self, request, response):
        '''
        process response from upper middle ware
        add authcode or update expires time into cookie if request is permissed
        otherwise return forbidden response
        #try:
        #    isLocked = request.isLocked
        #except AttributeError:
        #    pass
        #else:
        #    response.set_cookie(key=settings.USERLOCKED_NAME,
        #                        value=1,
        #                        max_age=settings.LOCKEDAGE,
        #                        path='/',
        #                        expires=None,
        #                        domain=None,
        #                        secure=None,
        #                        httponly=False)
        #    return response
        '''

        session_key = request.session.session_key
        if session_key is None:
            request.session.flush()
            if settings.SESSION_COOKIE_NAME not in request.COOKIES:
                request.COOKIES[settings.SESSION_COOKIE_NAME] = None

        else:
            # pass
            # request.session._session_key = session_key
            response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                                value=session_key,
                                max_age=None,
                                expires=None,
                                path='/',
                                domain=None,
                                secure=None,
                                httponly=True)

        return response


def letpass(urls, requestpath):
    '''
    request on these usls can be permissed without login.
    '''

    for url in urls:
        if url in requestpath:
            return True
    return False


def deleteExpireAuth(session_key, current_time):
    '''
    delete auths over time
    '''

    permission = KSMP_Permission()
    pms = permission.get_permission(session_key)
    authlist = permission.get_all_auth()

    # delete all empire auth
    session_empiry_time = settings.SESSION_COOKIE_AGE
    items = []
    for item in authlist:
        if (current_time - authlist[item]) > session_empiry_time:
            items.append(item)
    for i in range(len(items)):
        permission.delete_auth(items[i])


def isvalid(username, password):
    '''
    validate username and password is valid for the service
    username must be system root user
    :params: username string
        password string
    :return: boolean
    '''
    if not isrootuser(username):
        return False
    else:
        if not isvalidpassword(username, password):
            return False
    return True


def isrootuser(username):
    '''
    validate a username is system root user or not
    :params: username string
    :return: boolean
    '''
    passwd = open('/etc/passwd')
    line = passwd.readline()
    while line:
        contents = line.split(":")
        if len(contents) >= 3:
            if contents[0] == username and contents[2] == '0':
                passwd.close()
                return True
        line = passwd.readline()
    passwd.close()
    return False


def isvalidpassword(username, password):
    '''
    validate whether the username and password is valid or not
    :params: username string
        password string
    :return: boolean
    '''
    shadow = open('/etc/shadow')
    line = shadow.readline()

    isexist = False
    while line:
        contents = line.split(":")
        if len(contents) < 2:
            line = shadow.readline()
            continue
        if contents[0] == username:
            isexist = True
            pword = contents[1]
            if pword[0] == '$':
                psaltindex = pword.rindex('$')
                psalt = pword[0:psaltindex+1]
            else:
                psalt = ''
            break
        line = shadow.readline()
    shadow.close()
    if not isexist:
        return False
    else:
        finalps = crypt.crypt(password, psalt)
        if finalps == pword:
            return True
    return False
