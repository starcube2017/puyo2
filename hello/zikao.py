def dedao_zikao_wang_mulu():
    r = requests.get("http://www.zikao365.com/web/lnst/")
    r.encoding = 'gbk'
    s = BeautifulSoup(urllib.parse.unquote(r.text),"html.parser")
    mulu,mulu_dizhi = [],[]
    for i in range(10):
        mulu.append(s.find(id="sub_d" + str(i)))
    for zong_leixing in mulu:
        leixing = zong_leixing.find_all("ul")
        for kecheng in leixing:
            ke = kecheng.find_all("li")
            for dizhi in ke:
                mulu_dizhi.append("http://www.zikao365.com" + dizhi.a['href'])
    return mulu_dizhi

def xie_zikao_ti(mulu_dizhi):
    for dizhi in mulu_dizhi:
        try:
            r = requests.get(dizhi)
            r.encoding = 'gbk'
            s = BeautifulSoup(urllib.parse.unquote(r.text),"html.parser")
            ye_dizhi = s.find("td",align="center").find_all("a")
            ye_dizhi = ["http://www.zikao365.com" + dz["href"] for dz in ye_dizhi]
            neirong_dizhi = s.find_all("td",title=re.compile("\d\d\d\d\-\d\d\-\d\d"))
            neirong_dizhi = ["http://www.zikao365.com" + dz.a['href'] for dz in neirong_dizhi]
            for xiazai_dizhi in neirong_dizhi:
                rr = requests.get(xiazai_dizhi)
                rr.encoding = 'gbk'
                ss= BeautifulSoup(urllib.parse.unquote(rr.text),"html.parser")
                wenjian_dizhi = ss.find_all("a",onclick=re.compile(".*"))
                if wenjian_dizhi:
                    wenjian_dizhi = wenjian_dizhi[0]['href']
                    wenjian_ming = wenjian_dizhi.split("/")
                    if wenjian_ming:
                        wenjian_ming = wenjian_ming[-1]
                        time.sleep(1)
                        wenjian_request = requests.get(wenjian_dizhi)
                        with open("d:/所有考卷/" + wenjian_ming,'wb') as fd:
                            for chunk in wenjian_request.iter_content(chunk_size=128):
                                fd.write(chunk)
            for ye in ye_dizhi:
                rrr = requests.get(ye)
                rrr.encoding = 'gbk'
                sss= BeautifulSoup(urllib.parse.unquote(rrr.text),"html.parser")
                neirong_dizhi = sss.find_all("td",title=re.compile("\d\d\d\d\-\d\d\-\d\d"))
                neirong_dizhi = ["http://www.zikao365.com" + dz.a['href'] for dz in neirong_dizhi]
                for xiazai_dizhi in neirong_dizhi:
                    rr = requests.get(xiazai_dizhi)
                    rr.encoding = 'gbk'
                    ss= BeautifulSoup(urllib.parse.unquote(rr.text),"html.parser")
                    wenjian_dizhi = ss.find_all("a",onclick=re.compile(".*"))
                    if wenjian_dizhi:
                        wenjian_dizhi = wenjian_dizhi[0]['href']
                        wenjian_ming = wenjian_dizhi.split("/")
                        if wenjian_ming:
                            wenjian_ming = wenjian_ming[-1]
                            time.sleep(1)
                            wenjian_request = requests.get(wenjian_dizhi)
                            with open("d:/doc/" + wenjian_ming,'wb') as fd:
                                for chunk in wenjian_request.iter_content(chunk_size=128):
                                    fd.write(chunk)
        except:
            a = "a"