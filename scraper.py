from bs4 import BeautifulSoup
import requests
import threading
base_url = 'https://en.wikipedia.org/'

def soupify(current_url):
     response = requests.get(current_url)
     return BeautifulSoup(response.content, 'html.parser')

def obtain_paragraphs(current_url):
        # We make a request to the current url
        body_content = soupify(current_url).find('div',attrs={'id':'bodyContent'})
        main_article = body_content.find('div',attrs={'id':'mw-content-text'})
        return main_article.find_all('p')

def obtain_first_link(paragraphs):
    links = []
    for paragraph in paragraphs:
        try:
            # The recursive=False option allows us to ignore bibliography and references
            link = paragraph.find('a',recursive=False).get('href')
            links.append(link)
        except Exception as e:
            #If there is no a tag, just continue
            pass
        #If previous lines worked, stop looking
        if len(links) != 0:
             break
    return links[False]

def steps_to_philosophy(start_url):
    visited_urls = []
    current_url = requests.get(start_url).url
    visited_urls.append(current_url[len(base_url)-1:])
    print('Starting at ', current_url[len(base_url)-1:])
    for i in range(50):
        link = obtain_first_link(obtain_paragraphs(current_url))
        # Check if we just finished (either loop or philosophy)
        if link == '/wiki/Philosophy':
            print(f'It took {i} steps to reach the philosophy page')
            return i
        if link in visited_urls:
             print('Loop found')
             return None
        # Update the url to which the next request will be done
        current_url = base_url+link
        visited_urls.append(link)

#main('https://en.wikipedia.org/wiki/Special:Random')
def main(start_url):
    threads = []
    for _ in range(10):
        t= threading.Thread(target=steps_to_philosophy,args=[start_url])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    

if __name__ == "__main__":
    random_article_url='https://en.wikipedia.org/wiki/Special:Random' 
    main(random_article_url)
