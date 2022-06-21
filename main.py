def lookupWord(keyword):

    try:
        from googlesearch import search

    except ImportError:
        print("No module named 'google' found")
 
    # to search
    urls = set()
    for j in search(keyword, tld="co.in", num=10, stop=10, pause=2):
        urls.add(j)

    return urls


def tag_visible(element):

    try:
        from bs4 import Comment
    except ImportError:
        print("No module named 'bs4' found")

    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'nav']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def scrapeSites(urls):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("No module named 'bs4' found")

    try:
        import requests as req
    except ImportError:
        print("No module named 'requests' found")
    
    useragent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

    totalWords = []

    for adres in urls:
        page = req.get(adres, headers=useragent, timeout=10)
        soup = BeautifulSoup(page.content, 'html.parser')
        texts = soup.body.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        collectedData = " ".join(t.strip() for t in visible_texts)
        collectedData = ' '.join(collectedData.split())
        totalWords.append(collectedData)
    return totalWords


def datacleaning(text):
    try:
        from gensim.parsing.preprocessing import remove_stopwords
    except ImportError:
        print("No module named 'gensim' found")

    import re

    newArr = []


    ## Stopwoorden verwijderen
    for page in text:
        print(len(page))
        newPage = remove_stopwords(page)
        page = newPage

    ## Speciale tekens verwijderen. 
    for page in text:
        newPage = re.sub(r'[^a-zA-Z0-9]', '', page)
        page = newPage

    for page in text:
        newPage = page.lower()
        page = newPage

    return text

def keywords(totalData):
    try:
        from collections import Counter
    except ImportError:
        print("No module named 'collections' found")

    Text = datacleaning(totalData)
    allText = ' '.join(Text)
    allWords = allText.split(' ')
    counter = Counter(allWords)
    return counter


urls = lookupWord(str(input('Geef een woord in:')))
alltext = scrapeSites(urls)
keywords = keywords(datacleaning(alltext))