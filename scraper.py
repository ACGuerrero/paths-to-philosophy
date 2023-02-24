from bs4 import BeautifulSoup
import requests
baseurl = 'https://en.wikipedia.org/'
url='https://en.wikipedia.org/wiki/Special:Random'

def stop_at_philosophy(start_url):
    current_url = start_url
    print('Starting at: ', start_url)
    i=0
    while i<50:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        body_content = soup.find('div',attrs={'id':'bodyContent'})
        main_article = body_content.find('div',attrs={'id':'mw-content-text'})
        paragraphs = main_article.find_all('p')
        first_link = []
        for paragraph in paragraphs:
            try:
                link = paragraph.find('a',recursive=False).get('href')
                first_link.append(link)
            except Exception as e:
                pass
            if len(first_link) != 0:
                break
        print(first_link[0])
        current_url = baseurl+first_link[0]
        if first_link[0] == '/wiki/Philosophy':
            break
        i+=1
    print(f'It took {i} steps to reach the philosophy page')


stop_at_philosophy(url)
