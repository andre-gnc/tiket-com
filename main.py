# import json  # ===================================================================================================
import datetime
import random
import re
import socket
import time
from pprint import pprint

import pandas as pandas
import urllib3
from bs4 import BeautifulSoup

import requests


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def delay():
    sleep = random.randint(10, 20)  # Delay for 10 to 20 seconds. ====================================================
    print('Sleep:', sleep)  # =======================================================================================
    time.sleep(sleep)


def soup(sp_method, sp_url, sp_parser, sp_head, sp_parmters, sp_proxy, sp_payload):
    if sp_method == 'get':
        sp_response = requests.get(sp_url, headers=sp_head, params=sp_parmters, proxies=sp_proxy)
        print(sp_response)  # =========================================================================================
        delay()
    else:
        sp_response = requests.post(url=sp_url, data=sp_payload, headers=sp_head)
        print(sp_response)  # ======================================================================================
        delay()

    if sp_response.status_code == 200:
        sp_soup = BeautifulSoup(sp_response.text, sp_parser)
    else:
        sp_soup = 'no 200'

    return sp_soup


def scraper(s_url):
    if scraper_testing is True:
        s_url = 'http://webcache.googleusercontent.com/search?q=cache:https://www.tiket.com/hotel/indonesia/padma-resort-ubud-108001534490367508'

    s_head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107'}

    s_parmters = {
        'checkin': datetime.datetime.now().date(),
        'checkout': datetime.datetime.now().date() + datetime.timedelta(days=1),
        'room': '1',
        'adult': '1'
    }

    try:  # Sometimes connection got error. So catch some exceptions.

        s_soup = soup('get', s_url, 'html.parser', s_head, s_parmters, None, None)
        if scraper_testing is True and s_soup != 'no 200':
            print(s_soup.prettify())  # ============================================================================
            print(80 * '=')  # =====================================================================================
        elif s_soup == 'no 200':
            print('Request failed!')

        try:
            property_name = s_soup.find('h1', {'class': 'property-name'}).text
        except Exception:
            property_name = 'none'

        try:
            property_type = s_soup.find('div', {'class': 'property-type'}).text
        except Exception:
            property_type = 'none'

        try:
            location = s_soup.find('div', {'class': 'location ellipsis'}).text
        except Exception:
            location = 'none'

        try:
            rating = s_soup.find('div', {'class': 'score'}).text
        except Exception:
            rating = 'none'

        try:
            total_review = s_soup.find('div', {'class': 'review-badge-count'}).text
        except Exception:
            total_review = 'none'

        try:
            health_protocol_license = s_soup.find('div', {'class': 'tiket-info-desc',}).text
        except Exception:
            health_protocol_license = 'none'

        if scraper_testing is True:
            print('Today:', datetime.datetime.now().date())
            print('\n')
            print('Property Name:', property_name)
            print('Property Type:', property_type)
            print('Location:', location)
            print('Ratings:', rating )
            print('Total Reviews:', total_review)
            print('Health_Protocol_licenses:', health_protocol_license)
            print('\n')
            print('Sleep: 10')  # ==================================================================================
            time.sleep(10)  # ======================================================================================

        return [property_name, property_type, location, rating, total_review, health_protocol_license]

    except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
            requests.exceptions.ConnectionError) as err:

        print('Error connecting:', err)
        return 'error'


def sample_urls():
    su_head = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.107'}

    su_payload = {
        '__EVENTTARGET': None,  # ==================================================================================
        '__VIEWSTATE':
            '/wEPDwUKMTU2NDMxOTEwMw9kFgICAQ9kFggCCQ9kFgICAQ8PFgIeB1Zpc2libGVnZGQCFQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQhDaXR5TmFtZR4ORGF0YVZhbHVlRmllbGQFB0NpdHlfQ2QeC18hRGF0YUJvdW5kZ2QQFSEFW0FMTF0yQURESVNPTiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyQkFMQ0ggU1BSSU5HUyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyQ0FSUk9MTFRPTiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyQ0VEQVIgSElMTCAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyQ09DS1JFTEwgSElMTCAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyQ09NQklORSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyQ09QUEVMTCAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyREFMTEFTICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyREVTT1RPICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyRFVOQ0FOVklMTEUgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyRkFSTUVSUyBCUkFOQ0ggICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyRkVSUklTICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyR0FSTEFORCAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyR0xFTk4gSEVJR0hUUyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyR1JBTkQgUFJBSVJJRSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyR1JBUEVWSU5FICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAySElHSExBTkQgUEFSSyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAySFVUQ0hJTlMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAySVJWSU5HICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyTEFOQ0FTVEVSICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyTEVXSVNWSUxMRSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyTUVTUVVJVEUgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyTk8gVE9XTiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyT1ZJTExBICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyUklDSEFSRFNPTiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyUk9XTEVUVCAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyU0FDSFNFICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyU0VBR09WSUxMRSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyU1VOTllWQUxFICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyVU5JVkVSU0lUWSBQQVJLICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyV0lMTUVSICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAyV1lMSUUgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAVIQABMQEyATMBNgE3ATkCMTACMTICMTUCMTYCMTcCMTgCMjACMjICMjQCMjgCMjkCMzACMzECMzICMzMCMzQCMzcCMzgCMzkCNDACNDICNDMCNDUCNDYCNDgCNDkUKwMhZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCLQ9kFgJmDxBkDxYDZgIBAgIWAxAFC1JFU0lERU5USUFMBQExZxAFCkNPTU1FUkNJQUwFATJnEAUDQlBQBQEzZxYDZgIBAgJkAjEPZBYCAgIPPCsACwBkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYEBSBBY2N0VHlwZUNoZWNrTGlzdDE6Y2hrQWNjdFR5cGU6MAUgQWNjdFR5cGVDaGVja0xpc3QxOmNoa0FjY3RUeXBlOjEFIEFjY3RUeXBlQ2hlY2tMaXN0MTpjaGtBY2N0VHlwZToyBSBBY2N0VHlwZUNoZWNrTGlzdDE6Y2hrQWNjdFR5cGU6MqQj0T23okq1s5oe9VDS/CdpQJ46PB4aCVgsvr91G6tb',
        '__EVENTVALIDATION':
            '/wEdADV5ZqOFrVTVBjMqsygMQjkEzJw9xl+n12qTBvgCDxJSn60uB4RFow1TdcK502ZPoS0IIwI505MYo1DlrDvTkUTYwY4d2tz3O/2I1pLCtA5ck0352jB3D8e8ZV27WnF/pN4RlDWnS95WkLM0FFLIilWAO9Ccsa4xhvCk1OzehKGeeNU3YE6RpIpPMBNWOsZ91+wDEfV43SInvonE/itluxMi5KIsZNLw/l+ZjR2ogDzMC3zUyJo+TXdK3q1ZE+ThC32s2myzryV5TYvvwEi9AIJmqM78JkZwAki/amT5TRPUK5kyCjisk6luAcu4MVCxhKo6+a8iI86FCkC4Tj8Kf7/P9BFcPx+bNpVIyqbmEF9w+ynq5np40wmbkLRgYi91ib1VOGdBcONtAI8h+dxYprX4xcReKWtw3D/XFjhfks3xE+LphFuR0j64tr/cJcgDwbo/1pjgL4/ed8dACpI2yBHV7+2bWQFo52wKXlwJRCoQzWnodklvgx2v5ga0ntQUo+TILrZOe1lDQ07/il1sSB+VHs5RYjjE9ZnbtsVLMW6oH/kzh4hUf602pj+1TCOXSmr46DHdFh+8UAIDyxnBq5VRWCZKTJFh77bKKQ6h84uUfp99NWeg5cWqQ/pKq99yPvhPbImEd5CpCbDar3K4Yf579LRDAtH2N8AilKHrzPyX/FWEVNJf+2ZFb1IOdpQKjdC9j2DSQVVDH675ZDqqTDShOaPZpGum2GMqY3TJPHI6IyEnw4MKjSqnDdupOefxgFQuZ1p/JU4c+ib/7Ts7fvfyFz6D7Bl5NpWfBQhXhIcYrntOdq8ySfqp2vr3v9MELIfG7gpE2kpWPArgnAX7Rr3PkSRUk79WZHGjLj5hOomClCFHq8oIl9DnjY8xzDEoegkHaYGXKlbOUgY8lJlN1/k3YNfB/ZYtKi3wj+s4nZmMvqj4dIteZi8qgXkSLKODCW9gxmiX9NFNL2QEVOa0L2+dNk091z2hdToxv1UsnF92MJgC5WqJsDcGswus5i++Rao36+rqaEBiLlf+ZLMWEimvPYRW60HLmv6/zHn0RnZ8Hwe32I1ect2MIe8QNHFrabFAUT+wCI305ofMm3mYKmhjvdRv8ms4l8a1m70NfO3YC4B6bHZFTLvBnW6l3e0bPp/7RliyGKdWZdqp7RNS9Xlu',
        'txtStName': '%EL',
        'listCity': '1',
        'cmdSubmit': 'Search',  # ==================================================================================
        'AcctTypeCheckList1:chkAcctType:0': '1',
        'AcctTypeCheckList1:chkAcctType:1': '2',
        'AcctTypeCheckList1:chkAcctType:2': '3'
    }

    su_entry_list = ['https://www.dallascad.org/SearchAddr.aspx']

    su_entry_urls = []
    try:  # Sometimes connection got error. So catch some exceptions.
        for su_cat_urls_cnt, su_cat_url in enumerate(su_entry_list):
            su_soup = soup('post', su_cat_url, 'html.parser', su_head, None, None, su_payload)
            # print(su_soup.prettify())  # ===========================================================================
            # print(80 * '=')  # =====================================================================================

            su_entry_url_tags = su_soup.find_all('a', {'id': 'Hyperlink1'})
            for su_entry_url_tags_cnt, su_entry_url_tag in enumerate(su_entry_url_tags):
                su_entry_urls.append('https://www.dallascad.org/' + su_entry_url_tag.get('href'))

            su_loop = su_soup.find(string=re.compile('matches')).find_next('td').text
            su_loop = su_loop[su_loop.index('of') + 3:]
            su_loop = int(su_loop)
            print('Loop:', su_loop)  # =============================================================================

            su_payload['__EVENTTARGET'] = 'SearchResults1$dgResults$_ctl1$_ctl1'
            su_payload['cmdSubmit'] = None

            print('This is #1 from ' + str(su_loop) + ' pages.')
            print('Current urls:', len(su_entry_urls))
            print(80 * '=')  # =====================================================================================

            for su_cnt in range(1, int(su_loop)):
                su_payload['__VIEWSTATE'] = su_soup.find('input', {'id': '__VIEWSTATE'}).get('value')
                su_payload['__EVENTVALIDATION'] = su_soup.find('input', {'id': '__EVENTVALIDATION'}).get('value')
                su_soup = soup('post', su_cat_url, 'html.parser', su_head, None, None, su_payload)

                su_entry_url_tags = su_soup.find_all('a', {'id': 'Hyperlink1'})
                for su_entry_url_tags_cnt, su_entry_url_tag in enumerate(su_entry_url_tags):
                    su_entry_urls.append('https://www.dallascad.org/' + su_entry_url_tag.get('href'))

                print('This is #' + str(su_cnt + 1) + ' from ' + str(su_loop) + ' pages.')
                print('Current urls:', len(su_entry_urls))
                print(80 * '=')  # ===============================================================================

                if len(su_entry_urls) >= 100:
                    break

        pprint(su_entry_urls)  # ===================================================================================
        print('Sample urls:', len(su_entry_urls))
        print('Sleep: 10')  # ======================================================================================
        time.sleep(10)  # ==========================================================================================

        su_entry_urls_df = pandas.DataFrame(su_entry_urls)
        su_entry_urls_df = su_entry_urls_df.sample(frac=1)  # Make it random.
        su_entry_urls_df.to_csv('sample urls.csv', index=False)

    except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
            requests.exceptions.ConnectionError) as err:
        print('Error connecting:', err)
        return 'error'


def sample():
    sl_headers = ['URL', 'Owner Name 1', 'Owner Name 2', 'Owner Address', 'Owner City', 'Owner State', 'Owner Zip',
                  'Owner Zip Extension', 'Owner Country', 'Ownership', 'Legal Description', 'Deed Transfer Date',
                  'Deed Transfer Year', 'Improvement', 'Land', 'Market Value', 'Building Class',
                  'Construction Type', 'Baths', 'Year Built', 'Foundation', 'Kitchens', 'Roof Type', 'Bedrooms',
                  'Roof Material', 'Wet Bars', 'Desirability', 'Fence Type', 'Fire Places', 'Living Area',
                  'Wall Material', 'Sprinkler', 'Total Area', 'Deck', 'Heating', 'Spa', 'Stories', 'Air Condition',
                  'Pool', 'Sauna', 'Improvement Type', 'Construction', 'Area', 'State Code', 'Zoning',
                  'Frontage', 'Depth', 'Land Area']

    sl_entry_urls_df = pandas.read_csv('sample urls.csv')
    # pprint(sl_entry_urls_df) # =====================================================================================

    sl_df = pandas.DataFrame(columns=sl_headers)

    for cnt in range(1, len(sl_entry_urls_df) + 1):
        if cnt % team[1] == team[0]:
            sl_url = sl_entry_urls_df.iloc[cnt - 1]['0']
            sl_row = scraper(sl_url)

            if sl_row == 'error':
                break
            else:
                sl_series = pandas.Series(sl_row, index=sl_headers)
                sl_df = sl_df.append(sl_series, ignore_index=True)

                # Below: Counting, so that you can know which row is it.  # ==========================================
                print('The above is #' + str(cnt) + ' from ' + str(len(sl_entry_urls_df)) + ' entries.')
                print(80 * '=')  # =================================================================================

    pprint(sl_df)  # ===========================================================================================
    sl_df.to_csv(path_or_buf='sample ' + str(team[0]) + '.csv', index=False)


if __name__ == '__main__':
    scraper_testing = True
    team = [0, 1]  # [(#), (Total)]
    print('To check function scraper(), input \'1\' and press ENTER.')
    # print('To populate urls by function sample_urls(), input \'2\' and press ENTER.')
    # print('To scrape data by function sample(), input \'3\' and press ENTER.')
    inp = input()
    if inp == '1':
        scraper(None)
    elif inp == '2':
        sample_urls()
    elif inp == '3':
        scraper_testing = False
        print('How many urls do you want to scrape?')
        team[1] = 100 // int(input())
        print('And you are person #.. of the team.')
        team[0] = int(input())
        sample()

