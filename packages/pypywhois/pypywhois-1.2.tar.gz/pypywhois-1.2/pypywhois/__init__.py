"""
    Python module/library for retrieving WHOIS information of domains.

    By DDarko.org  ddarko@ddarko.org  http://ddarko.org/
    License MIT  http://www.opensource.org/licenses/mit-license.php

    Usage example
    >>> import pypywhois
    >>> domain = pypywhois.query('google.com')
    >>> print(domain.__dict__)  # print(whois.get('google.com'))

    {
        'expiration_date':  datetime.datetime(2020, 9, 14, 0, 0),
        'last_updated':     datetime.datetime(2011, 7, 20, 0, 0),
        'registrar':        'MARKMONITOR INC.',
        'name':             'google.com',
        'creation_date':    datetime.datetime(1997, 9, 15, 0, 0)
    }

    >>> print(domain.name)
    google.com

    >>> print(domain.expiration_date)
    2020-09-14 00:00:00

"""
__all__ = ["query", "get"]

import os
import re
import socket
import sys
from functools import wraps
from typing import Optional, List

from ._1_query import do_query
from ._2_parse import do_parse, TLD_RE
from ._3_adjust import Domain
from .exceptions import (
    UnknownTld,
    FailedParsingWhoisOutput,
    UnknownDateFormat,
    WhoisCommandFailed,
    WhoisPrivateRegistry,
    WhoisQuotaExceeded,
)

CACHE_FILE = None
SLOW_DOWN = 0


Map2Underscore = {
    ".ac.uk": "ac_uk",
    ".co.il": "co_il",
    # uganda
    ".ca.ug": "ca_ug",
    ".co.ug": "co_ug",
    # th
    ".co.th": "co_th",
    ".in.th": "in_th",
    # .jp
    ".ac.jp": "ac_jp",
    ".ad.jp": "ad_jp",
    ".co.jp": "co_jp",
    ".ed.jp": "ed_jp",
    ".go.jp": "go_jp",
    ".gr.jp": "gr_jp",
    ".lg.jp": "lg_jp",
    ".ne.jp": "ne_jp",
    ".or.jp": "or_jp",
    ".geo.jp": "geo_jp",
    #
    ".com.au": "com_au",
    ".com.sg": "com_sg",
    #
    # TÜRKİYE (formerly Turkey)
    ".com.tr": "com_tr",
    ".edu.tr": "edu_tr",
    ".org.tr": "org_tr",
    #
    ".edu.ua": "edu_ua",
    # dynamic dns without whois
    ".hopto.org": "hopto_org",
    ".duckdns.org": "duckdns_org",
    # 2022-06-20: mboot
    ".ac.th": "ac_th",
    ".co.ke": "co_ke",
    ".com.bo": "com_bo",
    ".com.ly": "com_ly",
    ".com.tw": "com_tw",
    ".com.np": "com_np",
    ".go.th": "go_th",
    ".com.ec": "com_ec",
    ".gob.ec": "gob_ec",
    ".co.zw": "com_zw",
    ".org.zw": "org_zw",
}

PythonKeyWordMap = {
    "global": "global_",
    ".id": "id_",
    ".in": "in_",
    ".is": "is_",
}

Utf8Map = {
    ".xn--p1ai": "ru_rf",
}


IPV4_OR_V6 = re.compile(r"((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))")
suffixes = None


def extract_domain(url):
    """Extract the domain from the given URL

    >>> logger.info(extract_domain('http://www.google.com.au/tos.html'))
    google.com.au
    >>> logger.info(extract_domain('abc.def.com'))
    def.com
    >>> logger.info(extract_domain(u'www.公司.hk'))
    公司.hk
    >>> logger.info(extract_domain('chambagri.fr'))
    chambagri.fr
    >>> logger.info(extract_domain('www.webscraping.com'))
    webscraping.com
    >>> logger.info(extract_domain('198.252.206.140'))
    stackoverflow.com
    >>> logger.info(extract_domain('102.112.2O7.net'))
    2o7.net
    >>> logger.info(extract_domain('globoesporte.globo.com'))
    globo.com
    >>> logger.info(extract_domain('1-0-1-1-1-0-1-1-1-1-1-1-1-.0-0-0-0-0-0-0-0-0-0-0-0-0-10-0-0-0-0-0-0-0-0-0-0-0-0-0.info'))
    0-0-0-0-0-0-0-0-0-0-0-0-0-10-0-0-0-0-0-0-0-0-0-0-0-0-0.info
    >>> logger.info(extract_domain('2607:f8b0:4006:802::200e'))
    1e100.net
    >>> logger.info(extract_domain('172.217.3.110'))
    1e100.net
    """
    if IPV4_OR_V6.match(url):
        # this is an IP address
        return socket.gethostbyaddr(url)[0]

    # load known TLD suffixes
    global suffixes
    if not suffixes:
        # downloaded from https://publicsuffix.org/list/public_suffix_list.dat
        tlds_path = os.path.join(os.getcwd(), os.path.dirname(__file__), 'data', 'public_suffix_list.dat')
        with open(tlds_path, encoding='utf-8') as tlds_fp:
            suffixes = set(line.encode('utf-8') for line in tlds_fp.read().splitlines() if line and not line.startswith('//'))

    if not isinstance(url, str):
        url = url.decode('utf-8')
    url = re.sub('^.*://', '', url)
    url = url.split('/')[0].lower()

    # find the longest suffix match
    domain = b''
    split_url = url.split('.')
    for section in reversed(split_url):
        if domain:
            domain = b'.' + domain
        domain = section.encode('utf-8') + domain
        if domain not in suffixes:
            if not b'.' in domain and len(split_url) >= 2:
                # If this is the first section and there wasn't a match, try to
                # match the first two sections - if that works, keep going
                # See https://github.com/richardpenman/whois/issues/50
                second_order_tld = '.'.join([split_url[-2], split_url[-1]])
                if not second_order_tld.encode('utf-8') in suffixes:
                    break
            else:
                break
    return domain.decode('utf-8')


def validTlds():
    # --------------------------------------
    # we should map back to valid tld without underscore
    # but remove the starting . from the real domain
    rmap = {}  # build a reverse dict from the original tld translation maps
    for i in Map2Underscore:
        rmap[Map2Underscore[i]] = i.lstrip(".")

    for i in PythonKeyWordMap:
        rmap[PythonKeyWordMap[i]] = i.lstrip(".")

    for i in Utf8Map:
        rmap[Utf8Map[i]] = i.lstrip(".")

    # --------------------------------------
    tlds = []
    for tld in TLD_RE.keys():
        if tld in rmap:
            tlds.append(rmap[tld])
        else:
            tlds.append(tld)
    return sorted(tlds)


def filterTldToSupportedPattern(
        domain: str,
        d: List[str],
        verbose: bool = False,
) -> str:
    # the moment we have a valid tld we can leave:
    # no need for else or elif anymore
    # that is the "leave early" paradigm
    # also known as "dont overstay your welcome" or "don't linger"

    tld = None

    if len(d) > 2:
        for i in Map2Underscore:
            if domain.endswith(i):
                tld = Map2Underscore[i]
                return tld

    for i in PythonKeyWordMap:
        if domain.endswith(i):
            tld = PythonKeyWordMap[i]
            return tld

    for i in Utf8Map:
        if domain.endswith(i):
            tld = Utf8Map[i]
            return tld

    if domain.endswith(".name"):
        # some special case with xxx.name -> domain=xxx.name and tld is name
        d[0] = "domain=" + d[0]
        tld = d[-1]
        return tld

    # just take the last item as the top level
    return d[-1]


def internationalizedDomainNameToPunyCode(d: List[str]) -> List[str]:
    return [k.encode("idna").decode() or k for k in d]


def result2dict(func):
    @wraps(func)
    def _inner(*args, **kw):
        r = func(*args, **kw)
        return r and vars(r) or {}

    return _inner


def query(
        domain: str,
        force: bool = False,
        cache_file: Optional[str] = None,
        slow_down: int = 0,
        ignore_returncode: bool = False,
        server: Optional[str] = None,
        verbose: bool = False,
        with_cleanup_results=False,
        internationalized: bool = False,
) -> Optional[Domain]:
    """
    force=True          Don't use cache.
    cache_file=<path>   Use file to store cache not only memory.
    slow_down=0         Time [s] it will wait after you query WHOIS database.
                        This is useful when there is a limit to the number of requests at a time.
    server:             if set use the whois server explicitly for making the query:
                        propagates on linux to "whois -h <server> <domain>"
                        propagates on Windows to whois.exe <domain> <server>
    with_cleanup_results: cleanup lines starting with % and REDACTED FOR PRIVACY
    internationalized:  if true convert internationalizedDomainNameToPunyCode
    """
    assert isinstance(domain, str), Exception("`domain` - must be <str>")

    cache_file = cache_file or CACHE_FILE
    slow_down = slow_down or SLOW_DOWN

    domain = domain.lower().strip().rstrip(".")  # Remove the trailing dot to support FQDN.
    domain = extract_domain(domain)
    d = domain.split(".")

    if d[0] == "www":
        d = d[1:]

    if len(d) == 1:
        return None

    tld = filterTldToSupportedPattern(domain, d, verbose)

    if tld not in TLD_RE.keys():
        a = f"The TLD {tld} is currently not supported by this package."
        b = "Use validTlds() to see what toplevel domains are supported."
        msg = f"{a} {b}"
        raise UnknownTld(msg)

    # allow server hints using "_server" from the tld_regexpr.py file
    thisTld = TLD_RE.get(tld)
    if thisTld.get("_privateRegistry"):
        msg = "This tld has either no whois server or responds only with minimal information"
        raise WhoisPrivateRegistry(msg)

    # allow explicit whois server usage
    thisTldServer = thisTld.get("_server")
    if server is None and thisTldServer:
        server = thisTldServer
        if verbose:
            print(f"using _server hint {server} for tld: {tld}", file=sys.stderr)

    # allow a configrable slowdown for some tld's
    slowDown = thisTld.get("_slowdown")
    if slow_down == 0 and slowDown and slowDown > 0:
        slow_down = slowDown
        if verbose:
            print(f"using _slowdown hint {slowDown} for tld: {tld}", file=sys.stderr)

    # if the tld is a multi level we should not move further down than the tld itself
    # we currently allow progressive lookups until we find something:
    # so xxx.yyy.zzz will try both xxx.yyy.zzz and yyy.zzz
    # but if the tld is yyy.zzz we should only try xxx.yyy.zzz
    tldLevel = tld.split("_")

    if internationalized and isinstance(internationalized, bool):
        if verbose:
            print(d, file=sys.stderr)
        d = internationalizedDomainNameToPunyCode(d)
        if verbose:
            print(d, file=sys.stderr)

    while 1:
        q = do_query(
            dl=d,
            force=force,
            cache_file=cache_file,
            slow_down=slow_down,
            ignore_returncode=ignore_returncode,
            server=server,
            verbose=verbose,
        )

        pd = do_parse(
            whois_str=q,
            tld=tld,
            dl=d,
            verbose=verbose,
            with_cleanup_results=with_cleanup_results,
        )

        # do we have a result and does it have a domain name
        if pd and pd["domain_name"][0]:
            return Domain(
                pd,
                verbose=verbose,
            )

        if len(d) > (len(tldLevel) + 1):
            d = d[1:]  # strip one element from the front and try again
            if verbose:
                print(f"try again with {d}, {len(d)}, {len(tldLevel) + 1}", file=sys.stderr)
            continue
        elif pd and (len(d) == len(tldLevel) + 1):
            pd["domain_name"] = [".".join(d)]
            return Domain(
                pd,
                verbose=verbose,
            )
        # no result or no domain but we can not reduce any further so we have None
        return None

        """
        # not a or not b == not ( a and b )
        if len(d) > 2 and (not pd or not pd["domain_name"][0]):
            d = d[1:]
        else:
            break
        """

    return None


# Add get function to support return result in dictionary form
get = result2dict(query)
