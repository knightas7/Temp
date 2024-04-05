# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:33:34 2021

@author: Kar
"""

from bs4 import BeautifulSoup
import requests
import time
import xlsxwriter

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


def SaveExcel(results, resultFilePath):
    m = max(len(l) for l in results)
    
    results = [l + ['']*(m-len(l)) for l in results]
    wb = xlsxwriter.Workbook(resultFilePath)
    sheet = wb.add_worksheet()    
        
    for row in range(len(results)):
        for col in range(len(results[0])):
            sheet.write(row, col, results[row][col])
    
    wb.close()

def Get_data(board, category, kwd):
    row_list = board.find_all("div",{"class":"row"})
    result_temp = []
    for r in row_list:
        
        temp = r.find_all("span",{"class":["mr txt_grey","mr txt_grey hide_data"]})
        temp2 = []
        temp2.append(category)
        temp2.append(kwd)
        temp2.append(r.find("span",{"class":"txt_left row_txt_tit"}).text)
        for z in temp:
            temp2.append(z.text)
        result_temp.append(temp2)
        
    return result_temp




search_list = ["고양","덕양","일산","고봉","행주"]
category_list = ["도서", "고문헌", "잡지/학술지", "멀티미디어", "장애인자료", "외부연계자료", "기타", "해외한국관련기록물"]
master = []

for category in category_list:
    for kwd in search_list:
        pg = 1
        while True:
            time.sleep(1)
            url = "https://www.nl.go.kr/NL/contents/search.do?resultType=&pageNum="+str(pg)+"&pageSize=100&order=&sort=&srchTarget=total&kwd="+kwd+"&systemType=&lnbTypeName=&category="+category+"&hanjaFlag=&reSrchFlag=&licYn=&kdcName1s=&manageName=&langName=&ipubYear=&pubyearName=&seShelfCode=&detailSearch=&seriesName=&mediaCode=&offerDbcode2s=&f1=&v1=&f2=&v2=&f3=&v3=&f4=&v4=&and1=&and2=&and3=&and4=&and5=&and6=&and7=&and8=&and9=&and10=&and11=&and12=&isbnOp=&isbnCode=&guCode2=&guCode3=&guCode4=&guCode5=&guCode6=&guCode7=&guCode8=&guCode11=&gu2=&gu7=&gu8=&gu9=&gu10=&gu12=&gu13=&gu14=&gu15=&gu16=&subject=&sYear=&eYear=&sRegDate=&eRegDate=&typeCode=&acConNo=&acConNoSubject=&infoTxt="
            
            
            e_count = 0
            e_flag = 0
            while True:
                e_count += 1
                try:
                    html = getHtml(url)
                    soup = BeautifulSoup(html, 'html.parser')
                    board = soup.find("div", {"class" : "cont_list list_type"})
                    temp_result = Get_data(board, category,kwd)
                    e_flag = 0
                    break
                except AttributeError as e:
                    print(e)
                    time.sleep(10)
                    if e_count > 3:
                        e_flag = 1
                        break
                    else:
                        pass
            if e_flag ==1:
                break
            else:
                pass
            
            master += temp_result
            
            pg_total = soup.find("span",{"class":"total_num"}).text
            print(category + " : " + kwd + " : " +str(pg)+" / " +pg_total)
            if pg == int(pg_total):
                break
            else:
                pg += 1
        if e_flag == 1:
            continue
        else:
            SaveExcel(master,"NL_result.xlsx")
        