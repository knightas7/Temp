import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


url = "https://www.iea.org/policies?page="

url2 = 'https://www.iea.org/'

master = {"Policy":{"Country":'',"Year":'',"Status":'',"Jurisdiction":'',"link":'','Title':'','Source_Last_Updated':'','Content':'','Topics':'','Policy_Types':'','Sectors':'','Technologies':''}}

for x in range(261):
    print(x)
    flag = 0
    while flag == 0 :
        try:
            resp = requests.get(url+str(x+1))
            flag = 1
        except:
            time.sleep(60)
            continue
        
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    
    ul = soup.find('ul', {'class':'m-policy-listing-items'})
    div_list = ul.find_all('div',{'class':'m-policy-listing-item-row__content'})
    
    temp = {"Policy":{"Country":'',"Year":'',"Status":'',"Jurisdiction":'',"link":'','Title':'','Source_Last_Updated':'','Content':'','Topics':'','Policy_Types':'','Sectors':'','Technologies':''}}
    
    for div in div_list:
        policy = div.find('a',{'class':'m-policy-listing-item__link'}).text.strip()
        country = div.find('span',{'class':'m-policy-listing-item__col m-policy-listing-item__col--country'}).text.strip()
        year = div.find('span',{'class':'m-policy-listing-item__col m-policy-listing-item__col--year'}).text.strip()
        status = div.find('span',{'class':'m-policy-listing-item__col m-policy-listing-item__col--status'}).text.strip()
        jurisdiction = div.find('span',{'class':'m-policy-listing-item__col m-policy-listing-item__col--jurisdiction'}).text.strip()
        link = div.find('a',{'class':'m-policy-listing-item__link'})['href']
        
        temp[policy] = {"Country":'',"Year":'',"Status":'',"Jurisdiction":'',"link":'','Title':'','Source_Last_Updated':'','Content':'','Topics':'','Policy_Types':'','Sectors':'','Technologies':''}
        temp[policy]["Country"] = country
        temp[policy]["Year"] = year
        temp[policy]["Status"] = status
        temp[policy]["Jurisdiction"] = jurisdiction
        temp[policy]["link"] = link
    
    for policy in temp:
        time.sleep(5)
        if policy == "Policy":
            continue
        print(temp[policy]['link'])
        print(url2 + temp[policy]['link'])
        resp2 = requests.get(url2 + temp[policy]['link'])
        html2 = resp2.text
        soup2 = BeautifulSoup(html2, 'html.parser')
    
        title = soup2.find('h1',{'class':'o-hero-freepage__title f-title-3'}).text.strip()
        source_ld = soup2.find_all('span',{'class':'o-hero-freepage__meta'})[0].text.strip()
        try:
            source_ld += " // "
            source_ld += soup2.find_all('span',{'class':'o-hero-freepage__meta'})[1].text.strip()
        except:
            pass
        
        try:
            content = soup2.find('div',{'class':'m-block__content f-rte f-rte--block'}).find('p').text.strip()
        except AttributeError:
            content = soup2.find('div',{'class':'m-block__content f-rte f-rte--block'}).text.strip()
            
        
        topics = '-'
        policy_types = '-'
        sectors = '-'
        technologies = '-'
        
        ul_num = len(soup2.find_all('span',{'class':'m-policy-content-list__title'}))
        for k in range(ul_num):
            cat = soup2.find_all('span',{'class':'m-policy-content-list__title'})[k].text.strip()
            if cat == "Topics":
                topics = ''
                topic_list = soup2.find_all('ul',{'class':'m-policy-content-list__items'})[k].find_all('li',{'class':'m-policy-content-list__item'})
                for topic in topic_list:
                    topics += topic.find('span',{'class':'a-tag__label'}).text.strip()
                    topics += "/,/"
                    topics = topics[:-1]
            elif cat == 'Policy types':
                policy_types = ''
                pt_list = soup2.find_all('ul',{'class':'m-policy-content-list__items'})[k].find_all('li',{'class':'m-policy-content-list__item'})
                for pt in pt_list:
                    policy_types += pt.find('span',{'class':'a-tag__label'}).text.strip()
                    policy_types += "/,/"
                policy_types = policy_types[:-1]
            elif cat == 'Sectors':
                sectors = ''
                sector_list = soup2.find_all('ul',{'class':'m-policy-content-list__items'})[k].find_all('li',{'class':'m-policy-content-list__item'})
                for sector in sector_list:
                    sectors += sector.find('span',{'class':'a-tag__label'}).text.strip()
                    sectors += "/,/"
                sectors = sectors[:-1]
            elif cat == 'Technologies':
                technologies = ''
                technology_list = soup2.find_all('ul',{'class':'m-policy-content-list__items'})[k].find_all('li',{'class':'m-policy-content-list__item'})
                for tech in technology_list:
                    technologies += tech.find('span',{'class':'a-tag__label'}).text.strip()
                    technologies += "/,/"
                technologies = technologies[:-1]
            else:
                print(cat)
                pass
    
        temp[policy]["Title"] = title
        temp[policy]["Source_Last_Updated"] = source_ld
        temp[policy]["Content"] = content
        temp[policy]["Topics"] = topics
        temp[policy]["Policy_Types"] = policy_types
        temp[policy]["Sectors"] = sectors
        temp[policy]["Technologies"] = technologies
        
        for t in temp.keys():
            if t == "Policy":
                continue
            master[t] = temp[t]
        
        df = pd.DataFrame(master)
        df.to_excel("Crawl.xlsx")
        


