import requests
from bs4 import BeautifulSoup

import time

def code_n_verdict(url):
    page=requests.get(url)
    time.sleep(0.5)

    soup = BeautifulSoup(page.content,'html.parser')

    split_url=url.split('/')
    problem_no=split_url[4]
    problem_code="/contest/"+problem_no+"/problem/"
    problem_alphabet=""
    
    for link in soup.find_all('a',href=True):
        check=link['href']
        if(check[:-1]==problem_code):
            problem_alphabet=check[-1]
        elif(check[:-2]==problem_code):
            problem_alphabet=check[-2:]
        
    results=soup.find(id="program-source-text")
    x=str(results.text)
    
    a_divs=soup.find_all("span",{"class": "verdict-accepted"})
    r_divs=soup.find_all("span",{"class": "verdict-rejected"})

    a_len=len(a_divs)
    r_len=len(r_divs)

    y="error"
    if(a_len==1):
        y="accepted"
    elif(r_len==1):
        y="rejected"

    return (x,y,problem_no,problem_alphabet)


def display(url):
    print(url)
    out=code_n_verdict(url)
    print(out[2]+out[3])
    print(out[1])
    print("Code: ")
    print(out[0])
    return out


def make_url(contest,index):
    contest=str(contest)
    index=str(index)
    return "https://codeforces.com/contest/"+contest+"/submission/"+index



user="satanclaws"

def download(user,py=0,rej=1,ver=1):
    p_url="https://codeforces.com/submissions/"+user
    p_page=requests.get(p_url)
    p_soup=BeautifulSoup(p_page.content,'html.parser')
    submissions=[]
    for link in p_soup.find_all('a',href=True):
        temp=(link['href'])
        temp_s=temp.split('/')
        if(len(temp_s)==5):
            if(temp_s[3]=="submission"):
                submissions.append([temp_s[2],temp_s[4]])
    count=0
    print(submissions)
    
    for sub in submissions:
        count+=1
        print(count)
        url=make_url(sub[0],sub[1])
        data=display(url)
        to_save=data[0]
        
        if(rej==1):
            verdict=""
            if(ver==1):
                if(data[1]=="accepted"):
                    verdict="a"
                else:
                    verdict="r"
            ext=".txt"
            if(py==1):
                ext=".py"
            name=str(data[2])+str(data[3])+" "+str(sub[1])+" "+verdict+ext
            f=open(name,"w")
            f.write(to_save)
            f.close()
        elif(data[1]=="accepted"):
            verdict=""
            if(ver==1):
                if(data[1]=="accepted"):
                    verdict="a"
                else:
                    verdict="r"
            ext=".txt"
            if(py==1):
                ext=".py"
            name=str(data[2])+str(data[3])+" "+str(sub[1])+" "+verdict+ext
            f=open(name,"w")
            f.write(to_save)
            f.close()
        time.sleep(0.5)

#main
            
print("Enter username:",end=" ")
user=str(input())
print("write files as txt [0] or .py [1]",end=" ")
py=int(input())
print("do you want the rejected submissions too?[y/n]", end=" ")
rej=str(input())
if(rej=="y") or (rej=="Y"):
    rej=1
else:
    rej=0
print("do you want the verdict written on your files? [y/n]",end=" ")
ver=str(input())
if(ver=="y") or (ver=="Y"):
    ver=1
else:
    ver=0

download(user,py,rej,ver)

