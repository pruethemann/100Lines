## Bitly crawler
import requests
import random
import time
import csv

def gen_a0():
    return list('abcdefghijklmnopqrstuvwxyz0123456789')

def gen_Aa0():
    return list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890123456789')

def randomLetter(alphabeth):
    return alphabeth[random.randint(0,len(alphabeth)-1)]

def random_generator(source):
    while True:
        code = [randomLetter(source['alphabeth']) for i in range(source['size'])]
        yield ''.join(code)

def generator(source):
    start = source['start']
    alpha = source['alphabeth']
    size = len(alpha)
    for a in range(start[0], size):
        for b in range(start[1], size):
            start[1] = 0
            for c in range(start[2], size):
                start[2] = 0
                for d in range(start[3], size):
                    start[3] = 0
                    yield alpha[a] + alpha[b] + alpha[c] + alpha[d]


def request_status_code(code, source) -> bool:
    try:
        page = requests.get(source['url'] + code, timeout = 5)
        if page.status_code == 403:
            s = source['source']
            print(f'Error 403 {s} Code: {code} You got blocked')
            return False

        if page.status_code != 404:
                return page.url

    except Exception as e:
        s = source['source']
        print(f'Error 403 {s} Code: {code} Error: {e}')
    return False

def request_error(code, source) -> bool:
    try:
        page = requests.get(source['url'] + code)

        if source['error'] not in page.text:
            return page.url

    except Exception as e:
        s = source['source']
        print(f'Error 403 {s} Code: {code} Error: {e}')
    return False

def export(code, url, source):
    f = open('./Export/' + source['filename'], "a+")
    f.write(code + '    ' + url + '\n')
    f.close()

def save_lastcode(code, alpha):
    print('Code: ' + code)
    f = open('./Export/lastCode.txt', "w")
    positions = ''
    for l in list(code):
        positions += str(alpha.index(l)) + ' '
    f.write(positions.strip())
    f.close()
    print('postions ' + positions)

def import_lastcode():
    with open('./Export/lastCode.txt', 'r', encoding='utf8') as file:
        reader = csv.reader(file)

        for row in reader:
            code_str = row[0].split(' ')
            return list(map(int,code_str ))


db = {
    'source': 'dropbox',
    'size': 15,
    'alphabeth': gen_a0(),
    'generator': random_generator,
    'url': 'https://www.dropbox.com/s/',
    'request': request_error,
    'error': 'error_404',
    'filename': 'dropbox.txt'
}

bitly = {
    'source': 'bitly',
    'size': 7,
    'alphabeth': gen_Aa0(),
    'generator': random_generator,
    'url' : 'https://bit.ly/',
    'request': request_status_code,
    'filename': 'bitly.txt'
}

t1p = {
    'source': 't1p',
    'size': 4,
    'alphabeth': gen_a0(),
    'generator': generator,
    'start': import_lastcode(),
    'url' : 'https://t1p.de/',
    'request': request_status_code,
    'filename': 't1p.txt'
}

cuttly = {
    'source': 'cuttly',
    'size': 7,
    'alphabeth': gen_Aa0(),
    'generator': random_generator,
    'url' : 'https://cutt.ly/',
    'request': request_error,
    'error': 'https://www.googletagmanager.com/',
    'filename': 'cuttly.txt'
}


sources = [db, bitly, t1p, cuttly]
sources = [ t1p]

for s in sources:
    s['generator'] = s['generator'](s)

print(import_lastcode())

for i in range(10_000):
    for source in sources:
        #time.sleep(random.uniform(0.005, 0.01))

        code = next(source['generator'])

        if i%100 == 0:
            print(f'{i}th iteration')
            save_lastcode(code, source['alphabeth'])
            time.sleep(random.uniform(0.2, 1.04))

        url = source['request'](code, source)
        if url != False:
            export(code, url, source)
            print(url, source['source'])

last_code = next(t1p['generator'])
save_lastcode(last_code, t1p['alphabeth'])


