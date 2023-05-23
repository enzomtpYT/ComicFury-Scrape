import re, sys, os, threading, requests, time

print("Version 1.0 by enzomtp")

def dlimg(imgurl, folder, nmb, ft):
    b = requests.get(imgurl).content
    with open(f'{folder}/{str(nmb)}.{ft}', "wb") as f:
        f.write(b)
    print(f"Downloaded {str(nmb)} : {imgurl} (as {nmb}.{ft})\n")

def searchwithnm(nm):
    webs = requests.get("https://"+argment+".thecomicseries.com/comics/"+str(nm)).text
    x = re.findall('(?<="https:\/\/img\.comicfury\.com\/comics\/)(.*)(?=\.*")', webs)
    try:
        imgurl = "https://img.comicfury.com/comics/"+x[0]
        filetype = x[0].split(".")[1]
    except:
        print("ERROR")
        print("Array : "+str(x))
        print(webs)
    threading.Thread(target=dlimg, args=(imgurl, argment, nm, filetype)).start()


if len(sys.argv) > 1:
    argment = str(sys.argv[1])
else:
    argment = input("Enter comic ID > ")
print(f'argment : {argment}')


if len(sys.argv) > 2:
    pages = int(sys.argv[2])
else:
    pages = int(input("Number of pages (0 = don't know) > "))
print(f'pages : {pages}')

if not os.path.isdir(argment):
    os.makedirs(argment)

tic = time.perf_counter()
if pages == 0:
    n = 1
    lastimgurl=None
    while 1==1:
        webs = requests.get("https://"+argment+".thecomicseries.com/comics/"+str(n)).text
        x = re.findall('(?<="https:\/\/img\.comicfury\.com\/comics\/)(.*)(?=\.*")', webs)
        try:
            imgurl = "https://img.comicfury.com/comics/"+x[0]
            filetype = x[0].split(".")[1]
        except:
            print("ERROR")
            print("Array : "+str(x))
            print(webs)

        if lastimgurl == imgurl:
            break
        threading.Thread(target=dlimg, args=(imgurl, argment, n, filetype)).start()
        lastimgurl = imgurl
        n += 1
else:
    while pages > 0:
        threading.Thread(target=searchwithnm, args=(pages,)).start()
        pages -= 1

msg = False
while not threading.active_count() == 1:
    if msg == False:
        print("Finished search, waiting for threads")
        msg = True

toc = time.perf_counter()
print(f"Script ended in {toc - tic:0.4f} seconds")
