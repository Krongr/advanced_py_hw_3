from tqdm import tqdm
import requests
import bs4


if __name__ == "__main__":
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']

    url = 'https://habr.com/ru/all/'
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    main_page = requests.get(url, headers=my_headers).text
    soup = bs4.BeautifulSoup(main_page, 'html.parser')
    articles_list = soup.find_all(class_="tm-articles-list__item")
    list_of_selected_articles = {}
    
    for _article in tqdm(articles_list):

        title = _article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").find('span').text
        link = (
            'https://habr.com' + 
            _article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").find('a').attrs['href']
        )
        body = _article.find(class_="article-formatted-body article-formatted-body_version-2")
        if body == None:
            body = _article.find(class_="article-formatted-body article-formatted-body_version-1")
        text = body.text
        
        for _word in KEYWORDS:
            if title in list_of_selected_articles:
                break
            
            if _word in text:
                list_of_selected_articles[title] = link
            else:
                article_page = requests.get(link, headers=my_headers).text
                nested_soup = bs4.BeautifulSoup(article_page, 'html.parser')
                article_text = nested_soup.find(class_="tm-article-body").text
                if _word in article_text:
                    list_of_selected_articles[title] = link

    for _title, _link in list_of_selected_articles.items():
        print(f'{_title}\n{_link}\n')