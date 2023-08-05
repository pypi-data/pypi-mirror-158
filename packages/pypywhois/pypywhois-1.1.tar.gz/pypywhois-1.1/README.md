# whois
A Python package for retrieving WHOIS information of domains.

## Features
 * Python wrapper for Linux "whois" command.
 * Simple interface to access parsed WHOIS data for a given domain.
 * Able to extract data for all the popular TLDs (com, org, net, biz, info, pl, jp, uk, nz,  ...).
 * Query a WHOIS server directly instead of going through an intermediate web service like many others do.
 * Works with Python 3.x.
 * All dates as datetime objects.
 * Possibility to cache results.
 * Verbose output on stderr during debugging to see how the internal functions are doing their work
 * raise a exception on Quota ecceeded type responses
 * raise a exception on PrivateRegistry tld's where we know the tld and know we don't know anything
 * allow for optional cleaning the whois response before extracting information

## Help Wanted
Fork from: https://github.com/DannyCork/python-whois/labels/help%20wanted

## Usage example

Install `pypywhois` package from your distribution (e.g apt install pypywhois)

```
$pip install pypywhois

>>> import pypywhois
>>> domain = pypywhois.query('google.com')

>>> print(domain.__dict__)
{
	'expiration_date': datetime.datetime(2020, 9, 14, 0, 0),
	'last_updated': datetime.datetime(2011, 7, 20, 0, 0),
	'registrar': 'MARKMONITOR INC.',
	'name': 'google.com',
	'creation_date': datetime.datetime(1997, 9, 15, 0, 0)
}

>>> print(domain.name)
google.com

>>> print(domain.expiration_date)
2020-09-14 00:00:00

>>> domain = pypywhois.get('meta.com')
>>> print(domain)

>>> domain = pypywhois.get('meta.中文网', internationalized=True)
>>> print(domain)
```

## ccTLD & TLD support
see the file: ./whois/tld_regexpr.py
or call whois.validTlds()

## Issues
Raise an issue https://github.com/DannyCork/python-whois/issues/new

## Changes:
2022-07-05: by kleex:
 新增了部分中文域名后缀的支持
    中国
    娱乐
    机构
    组织机构
    公司
    集团
    网站
    网络
    政府
    游戏
    企业
    政务

## Support
Python 3.x is supported.

Python 2.x IS NOT supported.
