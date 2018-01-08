from time import sleep
from bs4 import BeautifulSoup as bs
import time
import sys
import re
import requests

# Creates the link that we will be going to, and continually check to see
# if its there
def execute_requests():
    # Check to see how long code runs
    #startTime = time.time()

    # Constants to be used through out code
    baseUrl1 = 'http://www.supremenewyork.com/shop/all'
    x = True

    # Keywords
    productCategory = 'Jackets'
    productKeyword = 'Hooded Suede Work Jacket'
    productStyle = 'Tree Camo'
    baseUrl2 = '{}/{}'.format(baseUrl1, productCategory)

    while x:
        try:
            response = requests.get(baseUrl2)
            soup = bs(response.text, 'html.parser')
            findProduct = soup.find('a', string=productKeyword)
            findStyle = findProduct.find_next('a', string=productStyle)
            productLink = findStyle.get('href')
            sUrl = '{}{}'.format('http://www.supremenewyork.com', productLink)
            x = False
            print('Link Found!')
        except AttributeError:
            print('loading...')
            x = True
            sleep(3)
    return sUrl

# Creating the Add to car function used in main code
def add_to_cart(session, sUrl):
    productSize = 'Medium'
    response = session.get(sUrl)
    soup = bs(response.text, 'html.parser')
    sizeTag = soup.find('option', text=productSize)
    sizeContainer = sizeTag.get('value')
    tokenTag = soup.find(attrs={'name' : 'csrf-token'})['content']
    form = soup.find('form', {'action': re.compile('(?<=/shop/)(.*)(?=/add)')})

    payload = {
        'st': tokenTag,
        'commit': 'add to cart',
        's': sizeContainer,
        'utf8': '✓'
    }

    headers = ({
        'User Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8'
    })
    response = session.post('http://www.supremenewyork.com' + form['action'], data = payload, headers = headers)
    if response.status_code == 200:
        print('Your item was added')

    return session

# Creating the Check out function
def checkout(session):
    formUrl = 'https://www.supremenewyork.com/checkout'
    response = session.get(formUrl)
    soup = bs(response.text, 'html.parser')
    token = soup.find(attrs={'name': 'csrf-token'})['content']

    headers = ({
    'User Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/52.0.2743.116 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8'
    })

    payload = {
        'authenticity_token' : token,
        'credit_card[cnb]' : '4111 1111 1111 1111',
        'credit_card[month]' : '09',
        'credit_card[type]' : 'visa',
        'credit_card[vval]' : '423',
        'credit_card[year]' : '2016',
        'hpcvv': "",
        'order[billing_address]': '2222 Nottingham Dr' ,
        'order[billing_address_2]': "",
        'order[billing_city]': 'Garland',
        'order[billing_country]': 'USA',
        'order[billing_name]': 'Rodney Moreno',
        'order[billing_state]': 'TX',
        'order[billing_zip]':  '75041',
        'order[email]': 'Rodney.Moreno14@gmail.com',
        'order[tel]': '(469) 438 - 5890',
        'order[terms]': '1',
        'same_as_billing_address': '1',
        'store_address': '1',
        'store_credit_id': "",
        'utf8': '✓'
    }

    response = session.post(formUrl, data = payload, headers = headers)
    if 'Your order has been submitted' in response.text:
        print('Checkout was successful!')
        #print(time.time() - startTime)
        sys.exit(0)
    else:
        soup = bs(response.text, 'html.parser')
        for i in soup.findAll('div', {'class' : 'errors'}):
            print(i)
        #print(time.time() - startTime)
        sys.exit(0)

def main():
    session = requests.Session()
    session.headers.update({
        'User Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/52.0.2743.116 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8'
    })

    sUrl = execute_requests()
    session = add_to_cart(session, sUrl)
    checkout(session)

if __name__ == '__main__':
    main()
