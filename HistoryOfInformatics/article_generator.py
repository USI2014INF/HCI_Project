import common
import json

sections = ['HOME','SOFTWARE','HARDWARE','INTERNET','GAMES','HCI']

def create_article(section,article):
    jsonSend = {}
    article_data = common.getArticleForURL(section, article)
    html_code = ''
    # html_code += common.jinjaSubstitution(article_data,'head')
    article_data['navElement'] = ''
    for element in sections:
        if section == element.lower():
            article_data['navElement'] += common.jinjaSubstitution({'sectonNameSelected':element.lower()+' selected', 'sectionName':element, 'sectonNameHref':element.lower()},'navbarList')
        else:
            article_data['navElement'] += common.jinjaSubstitution({'sectonNameSelected':element.lower(), 'sectionName':element, 'sectonNameHref':element.lower()},'navbarList')
    jsonSend['body'] = common.jinjaSubstitution(article_data,'navbarMain')

    jsonSend['body'] += common.jinjaSubstitution(article_data,'topicPage')

    jsonSend['title'] = article_data['title']

    jsonSend['section'] = section

    if html_code.count('</div') % 2 == 1:
        splitted_html_code = html_code.split('<div class="externalLinks">')
        html_code = splitted_html_code[0] + \
            '<div class="externalLinks"></div>' + \
            splitted_html_code[1]

    return json.dumps(jsonSend)

def hci(section):
    jsonSend = {}
    html_code = ''
    article_data = common.getSectionIndexPage(section)
    article_data['navElement'] = ''
    for element in sections:
        if section == element.lower():
            article_data['navElement'] += common.jinjaSubstitution({'sectonNameSelected':element.lower()+' selected', 'sectionName':element, 'sectonNameHref':element.lower()},'navbarList')
        else:
            article_data['navElement'] += common.jinjaSubstitution({'sectonNameSelected':element.lower(), 'sectionName':element, 'sectonNameHref':element.lower()},'navbarList')
    
    jsonSend['body'] = common.jinjaSubstitution(article_data,'navbarMain')

    jsonSend['body'] += common.jinjaSubstitution(article_data,'topicPage')

    jsonSend['title'] = section

    jsonSend['section'] = section
    return json.dumps(jsonSend)