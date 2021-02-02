import discord
from bs4 import BeautifulSoup
import urllib2
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

    nupage = int(tu[0]) / 10

    def get_name(body):
        return body.find('span', {'class': 'jcn'}).string

    def get_phone_number(body):
        for item in body.find_all('a', href=True):
            if "tel:" in item['href']:
                return str(item.string)
        return None

    def get_rating(body):
        rating = 0.0
        text = body.find('span', {'class': 'star_m'})
        if text is not None:
            for item in text:
                rating += float(item['class'][0][1:]) / 10

        return rating

    def get_rating_count(body):
        text = body.find('span', {'class': 'rt_count'}).string

        # Get only digits
        rating_count = ''.join(i for i in text if i.isdigit())
        return rating_count

    def get_address(body):
        return body.find('span', {'class': 'mrehover'}).text.strip()

    def get_location(body):
        text = body.find('a', {'class': 'rsmap'})
        text_list = text['onclick'].split(",")

        latitutde = text_list[3].strip().replace("'", "")
        longitude = text_list[4].strip().replace("'", "")

        return latitutde + ", " + longitude

    page_number = 1
    service_count = 1

    fields = ['Name', 'Phone', 'Rating', 'Rating Count', 'Address', 'Location']
    out_file = open(tu[1]+'.csv', 'wb')
    csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

    # Write fields first
    csvwriter.writerow(dict((fn, fn) for fn in fields))

    while True:

        # Check if reached end of result
        if page_number > nupage:
            break

        url = tu[2]+"/page-%s" % (page_number)
        page = urllib2.urlopen(url)

        soup = BeautifulSoup(page.read(), "html.parser")
        services = soup.find_all('li', {'class': 'cntanr'})

        # Iterate through the 10 results in the page
        for service_html in services:
            # Parse HTML to fetch data
            dict_service = {}
            dict_service['Name'] = get_name(service_html)
            dict_service['Phone'] = get_phone_number(service_html)
            dict_service['Rating'] = get_rating(service_html)
            dict_service['Rating Count'] = get_rating_count(service_html)
            dict_service['Address'] = get_address(service_html)
            dict_service['Location'] = get_location(service_html)

            # Write row to CSV
            csvwriter.writerow(dict_service)

            service_count += 1
        await message.channel.send(page_number * 10)
        page_number += 1

    out_file.close()
    filesend = tu[1]+ ".csv"

    msg = message.content
    print(message.content)
    # if message.content.startswith('!'):
    await message.channel.send(file=discord.File(filesend))


client.run(TOKEN)
