import discord
from bs4 import BeautifulSoup
import urllib
import urllib.request
import csv
t1='ODA2MjE1'
t2='NDY3MTgxNTM5MzQ4'
t3='.YBmMqg.eXhvcDJYP'
t4='-87Qt7YIwx4ZbP32p4'
TOKEN=t1+t2+t3+t4

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    userinp = message.content
    tu = userinp.split()
    forlink = tu[1] + "/" + tu[2]
    nupage = int(tu[0]) / 10

    def innerHTML(element):
        return element.decode_contents(formatter="html")

    def get_name(body):
        return body.find('span', {'class': 'jcn'}).a.string

    def which_digit(html):
        mappingDict = {'icon-ji': 9,
                       'icon-dc': '+',
                       'icon-fe': '(',
                       'icon-hg': ')',
                       'icon-ba': '-',
                       'icon-lk': 8,
                       'icon-nm': 7,
                       'icon-po': 6,
                       'icon-rq': 5,
                       'icon-ts': 4,
                       'icon-vu': 3,
                       'icon-wx': 2,
                       'icon-yz': 1,
                       'icon-acb': 0,
                       }
        return mappingDict.get(html, '')

    def get_phone_number(body):
        i = 0
        phoneNo = "No Number!"
        try:

            for item in body.find('p', {'class': 'contact-info'}):
                i += 1
                if (i == 2):
                    phoneNo = ''
                    try:
                        for element in item.find_all(class_=True):
                            classes = []
                            classes.extend(element["class"])
                            phoneNo += str((which_digit(classes[1])))
                    except:
                        pass
        except:
            pass
        body = body['data-href']
        soup = BeautifulSoup(body, 'html.parser')
        for a in soup.find_all('a', {"id": "whatsapptriggeer"}):
            # print (a)
            phoneNo = str(a['href'][-10:])

        return phoneNo

    def get_address(body):
        return body.find('span', {'class': 'mrehover'}).text.strip()

    def get_location(body):
        text = body.find('a', {'class': 'rsmap'})
        if text == None:
            return
        text_list = text['onclick'].split(",")

        latitutde = text_list[3].strip().replace("'", "")
        longitude = text_list[4].strip().replace("'", "")

        return latitutde + ", " + longitude

    page_number = 1
    service_count = 1

    fields = ['Name', 'Phone', 'Address', 'Location']
    out_file = open(tu[1] + "-" + tu[2] + ".csv", 'w')
    csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

    # Write fields first
    # csvwriter.writerow(dict((fn,fn) for fn in fields))
    while True:
        # Check if reached end of result
        if page_number > nupage:
            break

        url = "https://www.justdial.com/" + forlink + "/page-%s" % (page_number)
        print(url)
        req = urllib.request.Request(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"})
        page = urllib.request.urlopen(req)
        # page=urllib2.urlopen(url)

        soup = BeautifulSoup(page.read(), "html.parser")
        services = soup.find_all('li', {'class': 'cntanr'})

        # Iterate through the 10 results in the page
        for service_html in services:

            # Parse HTML to fetch data
            dict_service = {}
            name = get_name(service_html)
            print(name);
            phone = get_phone_number(service_html)
            address = get_address(service_html)
            location = get_location(service_html)
            if name != None:
                dict_service['Name'] = name
            if phone != None:
                print('getting phone number')
                dict_service['Phone'] = phone
            if address != None:
                dict_service['Address'] = address
            if location != None:
                dict_service['Address'] = location

            # Write row to CSV
            csvwriter.writerow(dict_service)

            print("#" + str(service_count) + " ", dict_service)
            service_count += 1
        await message.channel.send(page_number)
        page_number += 1

    out_file.close()
    filesend = tu[1] + "-" + tu[2] + ".csv"

    msg=message.content
    print(message.content)
    #if message.content.startswith('!'):
    await message.channel.send(page_number)
    await message.channel.send(file=discord.File(filesend))

client.run(TOKEN)
