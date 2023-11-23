import requests, fake_useragent, time, json
from bs4 import BeautifulSoup


def get_page(text):
    user_agent = fake_useragent.UserAgent()
    data = requests.get(
        url=f"https://hh.ru/search/resume?text={text}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&page=1",
        headers={"user-agent": user_agent.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        page_count = int(soup.find('div', attrs={'class':'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(
                url=f"https://hh.ru/search/resume?text={text}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&page={page}",
                headers={"user-agent": user_agent.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for a in soup.find_all('a', attrs={'class':'serp-item__title'}):
                yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
        except Exception as er:
            print(f"{er}")
        time.sleep(1)


def get_resume(page):
    user_agent = fake_useragent.UserAgent()
    data = requests.get(
        url=page,
        headers={"user-agent": user_agent.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        name = soup.find(attrs={'class':'resume-block__title-text'}).text
    except:
        name = ''
    try:
        salary = soup.find(attrs={'class':'resume-block__salary'}).text.replace('\u2009', '').replace('\xa0', '')
    except:
        salary = ''
    resume = {
        'name': name,
        'salary': salary
    }
    return resume


if __name__ == '__main__':
    data = []
    for i in get_page('python'):
        data.append(get_resume(i))
        time.sleep(1)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
