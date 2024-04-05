# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 19:54:37 2021

@author: Kar-Prime
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 19:45:03 2021

@author: Kar-Prime
"""
#필요 모듈 임포트
from bs4 import BeautifulSoup
import requests
import time
import xlsxwriter

global driver

#html 불러오기, 에러시 1분 후 재실행
def getHtml(url):
    _html = ""
    resp = ""
    # url에서 요청을 받아줄 때까지 get 요청을 보냄
    while resp == "":
        try:
            resp = requests.get(url)
        # 네트워크 연결 에러시
        except requests.exceptions.ConnectionError:
            print("Connection Error")
            time.sleep(60)
        except requests.exceptions.Timeout:
            # for a retry, or continue in a retry loop
            print("Retry or continue loop")
            time.sleep(60)
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print("Connection Error")
            time.sleep(60)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print("Connection Error")
            time.sleep(60)
        except requests.exceptions.ChunkedEncodingError as e:
            print("ChunkedEncodingError, Incompleted Error")
            time.sleep(60)

    # 정상적인 응답이 올 경우에만 텍스트를 받아옴
    if resp.status_code == 200:
        _html = resp.text
        
    return _html

#results 변수를 resultFilePath에 저장
def SaveExcel(results, resultFilePath):
    m = max(len(l) for l in results)
    
    results = [l + ['']*(m-len(l)) for l in results]
    wb = xlsxwriter.Workbook(resultFilePath)
    sheet = wb.add_worksheet()    
        
    for row in range(len(results)):
        for col in range(len(results[0])):
            sheet.write(row, col, results[row][col])
    
    wb.close()

#검색어 리스트, 필요 검색어 리스트에 따라 수정 가능
search_list = ["행주"]
#search_list = ["고봉","일산","덕양","고양","행주산성","애니골","창릉","능곡"]
search_list_2 = ["고봉","일산","덕양","고양","행주산성","창릉","능곡"]

#검색 구분 리스트
option_list = [["국내학술논문","re_a_kor"],["학위논문","bib_t"],["해외학술논문","re_a_over"],["학술지","re_s"],["단행본","bib_m"],["연구보고서","re_t"]]

#검색 구분 별 칼럼 헤드
re_a_kor = ["구분","검색어","제목","저자","학회","연도","학회지명","권호사항","요약","KCI등"]
bib_t = ["구분","검색어","제목","저자","학교명","연도","석/박사"]
re_s = ["구분","검색어","제목", "발행기관"]
bib_m = ["구분","검색어","제목","저자","발행사","연도"]
re_t = ["구분","검색어","제목","저자","발행기관","연도","자료형태"]


master = []




#국내학술논문 검색
o = option_list[0]
for s in search_list: 
    num = 0
    pg = 0
    while True:
        
        #url 검색 및 BeautifulSoup로 파싱
        url = "https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query="+s+"&queryText=&iStartCount="+str(pg)+"&iGroupView=5&icate=all&colName="+o[1]+"&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=1000&orderBy=&fsearchMethod=search&isFDetailSearch=N&sflag=1&searchQuery=%EA%B3%A0%EB%B4%89&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword=%EA%B3%A0%EB%B4%89&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
        html = getHtml(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        
        #검색 결과 수 가져오기
        result_num = soup.find("div",{"class":"searchBox"}).find("dl").find("dd").find("span").find("span").text
        result_num = result_num.replace(",","")
        if pg > int(result_num):
            break
        else:
            pass
        
        #각 검색 결과에 대해서 정보 가져오기
        each_thing = soup.find("div",{"class":"srchResultListW"}).find("ul").find_all("li")
        for e in each_thing:
            num += 1
            
            #kci 정보 가져오기
            try:
                kci = e.find("div",{"class":"markW"}).find("span").find("img")["alt"]
            except AttributeError:
                kci = ""
            
            #제목 정보 가져오기
            try:
                title = e.find("div",{"class":"cont"}).find("p",{"class":"title"}).text
            except AttributeError:
                continue
            
            #저자 정보 가져오기
            try:
                author = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span",{"class":"writer"}).text
            except AttributeError:
                author = ""
            #발행 기관 정보 가져오기
            org = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span",{"class":"assigned"}).text
            #기타 정보 가져오기
            ex1 = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find_all("span")[-3].text
            ex2 = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find_all("span")[-2].text
            ex3 = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find_all("span")[-1].text
            
            #초록 정보 가져오기
            try:
                abstract = e.find("div",{"class":"cont"}).find("p",{"class":"preAbstract"}).text
            except AttributeError:
                abstract = ""
            #master 변수에 추가
            master.append([o[0],s,title,author,org,ex1,ex2,ex3,abstract,kci])
        #페이지 이동
        pg += 1000

'''
#학위논문
o = option_list[1]
for s in search_list: 
    num = 0
    pg = 0
    while True:    
        
        url = "https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query="+s+"&queryText=&iStartCount="+str(pg)+"&iGroupView=5&icate=all&colName="+o[1]+"&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=1000&orderBy=&fsearchMethod=search&isFDetailSearch=N&sflag=1&searchQuery=%EA%B3%A0%EB%B4%89&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword=%EA%B3%A0%EB%B4%89&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
        html = getHtml(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        
        result_num = soup.find("div",{"class":"searchBox"}).find("dl").find("dd").find("span").find("span").text
        result_num = result_num.replace(",","")
        print(result_num)
        if pg > int(result_num) and int(result_num) != 0:
            break
        else:
            pass
        
        
        while True:
            try:    
                time.sleep(30)
                url = "https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query="+s+"&queryText=&iStartCount="+str(pg)+"&iGroupView=5&icate=all&colName="+o[1]+"&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=1000&orderBy=&fsearchMethod=search&isFDetailSearch=N&sflag=1&searchQuery=%EA%B3%A0%EB%B4%89&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword=%EA%B3%A0%EB%B4%89&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
                html = getHtml(url)
                soup = BeautifulSoup(html, 'html.parser')
                check = soup.find("div",{"class":"srchResultListW"}).find("div", {"class":"noResultW"}).find("p")    
            except AttributeError:
                break
            
            
        
        
        each_thing = soup.find("div",{"class":"srchResultListW"}).find("ul").find_all("li")
        for e in each_thing:
            num += 1
        
            try:
                kci = e.find("div",{"class":"markW"}).find("span").find("img")["alt"]
            except AttributeError:
                kci = ""
                
            try:
                title = e.find("div",{"class":"cont"}).find("p",{"class":"title"}).text
            except AttributeError:
                continue
            
            try:
                author = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span",{"class":"writer"}).text
            except AttributeError:
                author = ""
            org = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span",{"class":"assigned"}).text
            
            ex2 = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find_all("span")[-2].text
            ex3 = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find_all("span")[-1].text
            

            try:
                abstract = e.find("div",{"class":"cont"}).find("p",{"class":"preAbstract"}).text
            except AttributeError:
                abstract = ""
            
            master.append([o[0],s,title,author,org,ex2,ex3,abstract,kci])
            
        pg += 1000


#단행본
o = option_list[4]
for s in search_list: 
    num = 0
    pg = 0
    while True:    
        
        url = "https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query="+s+"&queryText=&iStartCount="+str(pg)+"&iGroupView=5&icate=all&colName="+o[1]+"&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=1000&orderBy=&fsearchMethod=search&isFDetailSearch=N&sflag=1&searchQuery=%EA%B3%A0%EB%B4%89&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword=%EA%B3%A0%EB%B4%89&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
        print(url)
        html = getHtml(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        
        result_num = soup.find("div",{"class":"searchBox"}).find("dl").find("dd").find("span").find("span").text
        result_num = result_num.replace(",","")
        print(result_num)
        if pg > int(result_num) and int(result_num) != 0:
            break
        else:
            pass
        
        
        while True:
            try:    
                time.sleep(30)
                url = "https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query="+s+"&queryText=&iStartCount="+str(pg)+"&iGroupView=5&icate=all&colName="+o[1]+"&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=1000&orderBy=&fsearchMethod=search&isFDetailSearch=N&sflag=1&searchQuery=%EA%B3%A0%EB%B4%89&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword=%EA%B3%A0%EB%B4%89&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
                html = getHtml(url)
                soup = BeautifulSoup(html, 'html.parser')
                check = soup.find("div",{"class":"srchResultListW"}).find("div", {"class":"noResultW"}).find("p")    
            except AttributeError:
                break
            
            
        
        
        each_thing = soup.find("div",{"class":"srchResultListW"}).find("ul").find_all("li")
        for e in each_thing:
            num += 1
        
            try:
                kci = e.find("div",{"class":"markW"}).find("span").find("img")["alt"]
            except AttributeError:
                kci = ""
                
            try:
                title = e.find("div",{"class":"cont"}).find("p",{"class":"title"}).text
            except AttributeError:
                continue
            
            try:
                author = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span",{"class":"writer"}).text
            except AttributeError:
                author = ""
            try:
                org = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span",{"class":"assigned"}).text
            except AttributeError:
                org = ""
            
            
            ex_list = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span", {"class":""})
            try:
                ex1 = str(int(ex_list.text))
            except AttributeError:
                ex1 = ""
                
            
            master.append([o[0],s,title,author,org,ex1])
            
        pg += 1000
        


#연구보고서
o = option_list[5]
for s in search_list: 
    num = 0
    pg = 0
    while True:    
        
        url = "https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query="+s+"&queryText=&iStartCount="+str(pg)+"&iGroupView=5&icate=all&colName="+o[1]+"&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=1000&orderBy=&fsearchMethod=search&isFDetailSearch=N&sflag=1&searchQuery=%EA%B3%A0%EB%B4%89&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword=%EA%B3%A0%EB%B4%89&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
        print(url)
        html = getHtml(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        
        result_num = soup.find("div",{"class":"searchBox"}).find("dl").find("dd").find("span").find("span").text
        result_num = result_num.replace(",","")
        print(result_num)
        if pg > int(result_num) and int(result_num) != 0:
            break
        else:
            pass
        
        
        while True:
            try:    
                time.sleep(30)
                url = "https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query="+s+"&queryText=&iStartCount="+str(pg)+"&iGroupView=5&icate=all&colName="+o[1]+"&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=1000&orderBy=&fsearchMethod=search&isFDetailSearch=N&sflag=1&searchQuery=%EA%B3%A0%EB%B4%89&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&resultKeyword=%EA%B3%A0%EB%B4%89&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
                html = getHtml(url)
                soup = BeautifulSoup(html, 'html.parser')
                check = soup.find("div",{"class":"srchResultListW"}).find("div", {"class":"noResultW"}).find("p")    
            except AttributeError:
                break
            
            
        
        
        each_thing = soup.find("div",{"class":"srchResultListW"}).find("ul").find_all("li")
        for e in each_thing:
            num += 1
        
            try:
                kci = e.find("div",{"class":"markW"}).find("span").find("img")["alt"]
            except AttributeError:
                kci = ""
                
            try:
                title = e.find("div",{"class":"cont"}).find("p",{"class":"title"}).text
            except AttributeError:
                continue
            
            try:
                author = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span",{"class":"writer"}).text
            except AttributeError:
                author = ""
            try:
                org = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find("span",{"class":"assigned"}).text
            except AttributeError:
                org = ""
            
            
            ex_list = e.find("div",{"class":"cont"}).find("p",{"class":"etc"}).find_all("span", {"class":""})
            if len(ex_list) == 2:
                ex1 = ex_list[0].text
                ex2 = ex_list[1].text
            else:
                try:
                    ex1 = str(int(ex_list[0].text))
                    ex2 = ""
                except ValueError:
                    ex1 = ""
                    ex2 = ex_list[0].text
                
            
            master.append([o[0],s,title,author,org,ex1, ex2])
            
        pg += 1000
'''

#유니코드 에러 테스트
'''
test = [[]]
master.pop(7062)
for r in range(len(master)):
    test[0] = master[r]
    try:
        SaveExcel(test,"test.xlsx")
    except UnicodeEncodeError:
        print(r)
        print(master[r])

master.pop(7408)
'''
#엑셀로 저장
SaveExcel(master,"result.xlsx")