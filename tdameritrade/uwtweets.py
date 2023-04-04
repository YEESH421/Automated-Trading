from sandbox import *
import datetime

x = datetime.datetime.now()
f = open("uwtweets" + x.strftime("%b") + x.strftime("%d")  +".txt", "x")
f.write('Date\tStock\tContract\tBid-Ask\tIntr\tVol\tIV\t%Diff\tUnderlying\tDailyVolume\tSector')
uwTweets = loadTweets(100, '1200616796295847936')
data = uwTweets['data']
for t in data:
    text = t['text']
    date = t['created_at']
    word = text.split()
    if len(word) > 25:
        stock = word[0]
        contract = word[1] + word[2] + word[3]
        bidask = word[6] + word[7] + word[8]
        interest = word[10]
        vol = word[12]
        iv = word[14]
        diff = word[17]
        under = word[19]
        dailyV = word[23]
        sector = word[25]
        print(date)
        if word[0][0] == '$' and word[1][0].isdigit() and word[1][1].isdigit():
            f.write('\n'+date + '\t' +  stock + '\t' +  contract + '\t' +  bidask + '\t' +  interest+ '\t' +  vol+ '\t' +  iv + '\t' +  diff + '\t' +  under+ '\t' + dailyV+ '\t' + sector)
f.close()