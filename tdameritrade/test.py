from streamtweets import *
from trade import *
import unittest

class TestStringMethods(unittest.TestCase):
    def test_parseDig1(self):
        s = "4th"
        t = parseDig(s)
        self.assertEqual(t, "4")
    def test_parseDig2(self):
        s = "$900s"
        t = parseDig(s)
        self.assertEqual(t, "900")

waitTime = 3
money = 0
c = authenticate()
Jtweet1 = '$GIK up calls, starting to collect March 19th 2021 $12.50 calls, with all cannabis related stocks running $TLRY $ACB etc.., this one can be huge since they need the software for gov tracking, etc.'
Jtweet2 = '$ACB Goin to get some $8 calls, March 26th expiration, small entry. RSI and MACD about to turn +, bounced off of support levels. Chart looks like it is ready for a bounce above $8 soon. SL should be placed just below $7.'
JtweetPenny1 = '$RHE On scanner, this should move up nicely once it breaks $7, getting a small position here'
JtweetPenny2 =  '$ACY goin to get an entry here, low floater jumper to $38 few weeks back now hovering around support. Can be huge'
Ctweet = 'For those following $CLOV, trust the process and the facts.'
Rtweet = '$DVA #addalert \nFollowing Buffet here, started a position\nWill post chart later'
Ztweet = '$KERN $10 for those in from the swing. orig call was $4s'
Stweet = 'Love this Holy Grail setup in $NNDM.... explosive stock and looks about ready now... \nFirst target: $8\n\nGood spot by @GaelicAidan'
PJtweet1 = '$SNDL added 2.13/2.14'
PJtweet2 = '$CBAT added huge here. 16% short float on this. $LODE is up 300%! It will keep these in play. I guess you can say I’m LODEing $CBAT. 50%++'
PJtweet3 = 'Added $ONTX dip here'
Mtweet1 = 'This is going to be a monster $TSCRF $SCR.TO'
Mtweet2 = 'Buyer 6000 $CBAT 2/26 $12.50 calls for 13 cents these are cheap CBAK energy lottos'
Mtweet3 = 'Insider/institutional buy in $SALM today'
Mtweet4 = 'Dollar Will’s Lotto of the Day Buyer 17,000 $GE 6/18 $20 calls for 9 cents GE is one the blue chip stock that I think can double this year.'
Mtweet5 = 'Unusual call option activity leaders this morning Over 65,000 $SNDL 2/26 $5 calls for 85 cents Over 126,000 $DNN 3/19 $2.50 calls for 35 cents Over 6000 $SONO Jan2022 $45 calls for $6.55'
segments = Jtweet1.split('\n')
for s in segments:
    if s:
        parseAndBuyJoeAlert(s, waitTime, money, c)
segments = Jtweet2.split('\n')
for s in segments:
    if s:
        parseAndBuyJoeAlert(s, waitTime, money, c)
segments = JtweetPenny1.split('\n')
for s in segments:
    if s:
        parseAndBuyJoeAlert(s, waitTime, money, c)
segments = JtweetPenny2.split('\n')
for s in segments:
    if s:
        parseAndBuyJoeAlert(s, waitTime, money, c)
parseAndBuyChamathAlert(Ctweet, waitTime, money, c)
parseAndBuyRipsterAlert(Rtweet, waitTime, money, c)
parseAndBuyZackAlert(Ztweet, waitTime, money, c)
parseAndBuyStewieAlert(Stweet, waitTime, money, c)
parseAndBuyPJAlert(PJtweet1, waitTime, money, c)
parseAndBuyPJAlert(PJtweet2, waitTime, money, c)
parseAndBuyPJAlert(PJtweet3, waitTime, money, c)
parseAndBuyMeadeAlert(Mtweet1, waitTime, money, c)
parseAndBuyMeadeAlert(Mtweet2, waitTime, money, c)
parseAndBuyMeadeAlert(Mtweet3, waitTime, money, c)
parseAndBuyMeadeAlert(Mtweet4, waitTime, money, c)
parseAndBuyMeadeAlert(Mtweet5, waitTime, money, c)