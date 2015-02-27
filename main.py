'''
Created on Nov 19, 2014
 
@author: Mohan/ Ishan
'''
import facebook
import json
import requests
from prettytable import PrettyTable
from collections import Counter
 
ACCESS_TOKEN = 'CAAB5NsAFl9sBAKuA033KkjaQnDMW4tLlPSZBBYRvFuW97WwmFGWK9ZAZBOheQNdb6kIhXi6aRoWmgb52jbZAvmfJKeE37HJ9n9OWNyqovgHJY78S1dAapdMrbfQ5e0tSXEW1zAyZAelzQPwM8tJSZAKKqKYmZCTZAaU2bRpO2sojiVE4fwgzBVCSZCVuOZCorgmncbkYvuvp1NlvoZBU0q4kZBFl'
#ACCESS_TOKEN = 'CAAMsxJFavtgBAADgqMoOUnpxZBuArYVNI5rZA7GmLGTQ6p0xvrjE0Qar2a6ZBlkG5k3kl2e2KPOM3dxxyBcPgEvgGdRb0VUMugJJszaCTsHaFGE1YG0l3MUHZB86zZCsINKnJjwgYhzpaYj7UMbyo9gJj3SZB3VbSACt4pYhAvRfmZCMHv1SAyTfG623OmzA2ptdrTa31AYgPdGeZBm3rha969Ca5LZCZCQc8ZD'
base_url = 'https://graph.facebook.com/me'
#fields = 'id,name,likes,friends.limit(100).fields(likes)'
#fields = 'id,name,likes,friends,statuses'
#url = '%s?fields=%s&access_token=%s' % \
#    (base_url, fields, ACCESS_TOKEN,)
#content = requests.get(url).json()
#json.dumps(content, indent=1)
globalFriends = []
 
 
def main(self):
    getAllfriends()
    g = facebook.GraphAPI(ACCESS_TOKEN)
    friends = g.get_connections("me", "friends")['data']
    print len(friends)
    likestemp = g.get_connections("me", "likes")['data']
    print len(likestemp)
    my_likes = [ like['name'] for like in g.get_connections("me", "likes")['data'] ]
    pt = PrettyTable(field_names=["Name"])
    pt.align = 'l'
    [ pt.add_row((ml,)) for ml in my_likes ]
    print "My likes"
    print pt
    friends = g.get_connections("me", "friends")['data']
    likes = { friend['name'] : g.get_connections(friend['id'], "likes")['data'] 
          for friend in friends }
    print likes
    friends_likes = Counter([like['name']
                         for friend in likes 
                           for like in likes[friend]
                               if like.get('name')])
    common_likes = list(set(my_likes) & set(friends_likes))
    pt = PrettyTable(field_names=["Name"])
    pt.align = 'l'
    [ pt.add_row((cl,)) for cl in common_likes ]
     
    similar_friends = [ (friend, friend_like['name']) 
                     for friend, friend_likes in likes.items()
                       for friend_like in friend_likes
                         if friend_like.get('name') in common_likes ]
    print similar_friends
 
def getAllfriends():
    fields = 'id,name,friends.limit(5000)'
    url = '%s?fields=%s&access_token=%s' % (base_url, fields, ACCESS_TOKEN,)
    token = ACCESS_TOKEN
    while True:
        content = requests.get(url).json()
        json.dumps(content, indent=1)
        g = facebook.GraphAPI(token)
        url = g.get_connections("me", "friends")['paging']['next']
        temp = url.split("=")
        temp = temp[1][:-6]
        token = temp
        localFriends = g.get_connections("me", "friends")['data']
        print localFriends
        globalFriends.append(localFriends[0])
        print len(globalFriends)
        break
 
def getAllLikes(userid, accessid):
    url = 'https://graph.facebook.com/v2.0/'+userid+'/likes?access_token=' + accessid
    shouldBreak = False
    likes = []
    while True:
        if shouldBreak:
            break
        content = requests.get(url).json()
        if len(content['data']) == 0:
            break
        json.dumps(content, indent=1)
        if 'next' in content['paging']:
            url = content['paging']['next']
        else:
            shouldBreak =  True
        localLikes = content['data']
        for x in range(0, len(localLikes)):
            likes.append(localLikes[x]['name'])
    return likes    
 
def getAllItems(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.0/' + userid + '/' + context + '?access_token=' + accessid
    shouldBreak = False
    games = []
    while True:
        if shouldBreak:
            break
        content = requests.get(url).json()
        if len(content['data']) == 0:
            break
        json.dumps(content, indent=1)
        if 'next' in content['paging']:
            url = content['paging']['next']
        else:
            shouldBreak =  True
        localGames = content['data']
        if context == 'tagged_places':
            for x in range(0, len(localGames)):
                games.append(localGames[x]['place']['name'])
        elif context == 'location':
            for x in range(0, len(localGames)):
                games.append(localGames[x]['location']['name'])
        else:
            for x in range(0, len(localGames)):
                games.append(localGames[x]['name'])
    return games    
 
def getUserLocation(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.0/' + userid + '?fields=' + context + '&access_token=' + accessid
    content = requests.get(url).json()
    json.dumps(content, indent=1)
    return content['location']['name']
 
def getPublicUserLocation(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.0/' + userid + '?access_token=' + accessid
    content = requests.get(url).json()
    json.dumps(content, indent=1)
    if 'location' in content:
        return content['location']['name']
    else:
        return ''

def getPublicUserName(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.0/' + userid + '?access_token=' + accessid
    content = requests.get(url).json()
    json.dumps(content, indent=1)
    if 'name' in content:
        return content['name']
    else:
        return ''

def getUserEvents(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.0/' + userid + '/' + context + '?access_token=' + accessid
    content = requests.get(url).json()
    json.dumps(content, indent=1)
    eventNames = []
    eventLocations = []
    localEvents = content['data']
    for x in range(0, len(localEvents)):
        eventNames.append(localEvents[x]['name'])
        eventLocations.append(localEvents[x]['location'])
    return eventNames, eventLocations
 
def getUserEducation(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.0/' + userid +  '/?access_token=' + accessid
    #print url;
    content = requests.get(url).json()
    json.dumps(content, indent=1)
    educations = []
    localEducations=""
    if 'education' in content:
        localEducations = content['education']
    else :
        return ''
    
    for x in range(0, len(localEducations)):
        educations.append(localEducations[x]['school']['name'])
    return educations

def getUserDetails(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.0/' + userid + '?fields=' + context + '&access_token=' + accessid
    content = requests.get(url).json()
    json.dumps(content, indent=1)

    if 'hometown' in content:
        return content['hometown']['name']
    else:
        return ''
def getUserLanguages(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.0/' + userid +'/?access_token=' + accessid# '?fields=' + context + 
    
    content = requests.get(url).json()
    json.dumps(content, indent=1)
    userLanguages=[]
    localLang=""
    if 'languages' in content:
        localLang = content['languages']
    else :
        return ''
#    print content['languages']
    for x in range(0, len(localLang)):
        userLanguages.append(localLang[x]['name'])
    return userLanguages

person1Id = '10152902349338734'
person2Id = '10204366238390282'
person1Access = 'CAACEdEose0cBAFuifKYO4jKXfQyhI4c3iP88HUfWRTNAJrxZBecWtZCtf3evR5vhyU7xu1Pphq5CSEV5EExBQpZBNZBS1iJasZBUiQBwAqdV5bX12NZA3svCj9jM5FSBbu0y5sC3gyJVpteJGiiD2mAKaEsUQaPzxsHdJrVByATuExN4gC6UrpsXtJ3h1vjoatZAlpsddHA5p2ZAbNeVfW5hC9ZCooDTWFrkZD'
person2Access = 'CAACEdEose0cBAMbZCyOuBiI03QvVhlQWzeJLmzaXR39M6X3jd0Qd5fx3P6LYN8sSHj8efkIRZCkXSMsKenL3QniEZBRf1wXwIPao2ZAP6hzvZBJSZBcSewCMFI4jXxHWKMc5NoSDoZB0kqgmb6bsTi8wOO7pHYuC1Mk9mstLorhMaz14lH3N5dornhzINcicj15IJhg0akAEvcvX6uiT23u'

def getUserInterests(userid, context, accessid):
    url = 'https://graph.facebook.com/v2.2/' + userid+'?access_token=' + accessid# 
    
    content = requests.get(url).json()
    json.dumps(content, indent=1)
    userLanguages=[]
    #localLang = content['interested_in']
    if 'interested_in' in content:
      #  print content['interested_in']
        return content['interested_in']
    else:
        return ''
    


def task1():
    finalScore=0
    
    print 'Compatibility Analysis: '
    person1Name= getPublicUserName(person1Id, 'name', person1Access)
    person2Name= getPublicUserName(person2Id, 'name', person2Access)
    print "\n"+'Analyzing Details for '+ person1Name +' and '+ person2Name+"\n"

    person1Games = getAllItems(person1Id, 'games', person1Access)
    person2Games = getAllItems(person2Id, 'games', person2Access)
    commonGames = list(set(person1Games).intersection(set(person2Games)))
    ptGames=PrettyTable(['Common Games '])
    print "\n"
    for x in commonGames:
        ptGames.add_row([x])
    print ptGames
    
    person1Music = getAllItems(person1Id, 'music', person1Access)
    person2Music = getAllItems(person2Id, 'music', person2Access)
    commonMusic = list(set(person1Music).intersection(set(person2Music)))
    ptMusic=PrettyTable(['Common Music '])
    print "\n"
    for x in commonMusic:
        ptMusic.add_row([x])
    print ptMusic
    person1Places = getAllItems(person1Id, 'tagged_places', person1Access)
    person2Places = getAllItems(person2Id, 'tagged_places', person2Access)
    commonPlaces = list(set(person1Places).intersection(set(person2Places)))
    ptPlaces=PrettyTable(['Common Places'])
    print "\n"
    for x in commonPlaces:
        ptPlaces.add_row([x])
    print ptPlaces
    person1Education = getUserEducation(person1Id, 'education', person1Access)
    person2Education = getUserEducation(person2Id, 'education', person2Access)
    commonEducation = list(set(person1Education).intersection(set(person2Education)))
    ptEducation=PrettyTable(['Common Education'])
    print "\n"
    for x in commonEducation:
        ptEducation.add_row([x])
    print ptEducation
    person1Location = getUserLocation(person1Id, 'location', person1Access)
    person2Location = getUserLocation(person2Id, 'location', person2Access)
    print "\n"
    print 'Common Location'
    if(person1Location== person2Location):
        print person1Location
    #print person2Location
        print "\n"
        finalScore=finalScore+6
    else:
        print 'No Common Location Found\n'
    person1EventNames, person1EventLocations = getUserEvents(person1Id, 'events', person1Access)
    person2EventNames, person2EventLocations = getUserEvents(person2Id, 'events', person2Access)
    commonEventNames = list(set(person1EventNames).intersection(set(person2EventNames)))
    commonEventLocations = list(set(person1EventLocations).intersection(set(person2EventLocations)))
    ptEvents=PrettyTable(['Common Event','Location'])
    count=0;
    print "\n"
    for x in commonEventLocations:
       ptEvents.add_row([commonEventNames[count],commonEventLocations[count]])
       count=count+1
    print ptEvents
    threshold=20;
    print 'The Threshold Value for Compatibility : 20 '+"\n" 
    
    finalScore=finalScore+ 1*len(commonEventNames) + 5*len(commonGames)+4*len(commonMusic)  +2*len(commonPlaces) + 3*len(commonEducation)  
    print 'Calculated Score : '
    print finalScore
    print "\n"

    if( finalScore>=threshold):
        print 'Given User is Compatible'+"\n"
    else:
        print 'Given User is Not-Compatible' +"\n"
def getAllFriends(userid,accessid):
    url='https://graph.facebook.com/v2.0/'+userid+'/friends?access_token='+accessid
    shouldBreak = False
    friends= []
    while True:
        if shouldBreak:
            break
        content = requests.get(url).json()
        if len(content['data']) == 0:
            break
        json.dumps(content, indent=1)
        if 'next' in content['paging']:
            url = content['paging']['next']
        else:
            shouldBreak =  True
        localFriends = content['data']
        for x in range(0, len(localFriends)):
            friends.append(localFriends[x]['id'])
    return friends    



def task2():
    allFriends= getAllFriends(person1Id, person1Access)
    Location=[]
    dictLocation={}
    dictHomeTown={}
    dictLanguages={}
    dictInterested_In={}
    dictEducation={}

    userLocation = getPublicUserLocation(person1Id, 'location', person1Access)
    userLanguages=getUserLanguages(person1Id,'languages',person1Access)
    userEducation=getUserEducation(person1Id,'languages',person1Access)
    userInterested_In=getUserInterests(person1Id,'interested_in',person1Access)
    userHomeTown = getUserDetails(person1Id,'hometown',person1Access)


    dictLocation_Score={}
    dictHomeTown_Score={}
    dictLanguages_Score={}
    dictEducation_Score={}
    dictInterested_In_Score={}

    for x in allFriends:
        y = getPublicUserLocation(x, 'location', person1Access)
        
        if y!='':
            if userLocation== y:
                dictLocation_Score[x]=dictLocation_Score.get(x,0) + 5
                #print dictLocation_Score
        
        z=getUserDetails(x,'hometown',person1Access)

        if z!='':
            if userHomeTown== z:
                dictHomeTown_Score[x]=dictHomeTown_Score.get(x,0) + 2
               # print dictHomeTown_Score
        
        e=getUserLanguages(x,'languages',person1Access)

        for ue1 in userLanguages:
            for e1 in e:
                if e1!='':
                    if ue1== e1:
                        dictLanguages_Score[x]=dictLanguages_Score.get(x,0) + 3
                        #print dictLanguages_Score
        
        edu=getUserEducation(x,'languages',person1Access)

        for ed1 in userEducation:# our
            for ed in edu:#friends
                if ed!='':
                    if ed1== ed:
                        dictEducation_Score[x]=dictEducation_Score.get(x,0) + 4
                       # print dictEducation_Score
        
        
        I=getUserInterests(x,'interested_in',person1Access)

        if I!='':
            if userInterested_In== I:
                dictInterested_In_Score[x]=dictInterested_In_Score.get(x,0) + 1
                #print dictEducation_Score
        

        
        dictInterested_In[x]=I;
        
        dictLocation[x] = y
        
        dictHomeTown[x]=z;
        
        dictLanguages[x]=e;
        
        dictEducation[x]=edu;
  

    finalCandidate={}
    finalCandidate= dict(dictLocation_Score.items() + dictHomeTown_Score.items()+dictLanguages_Score.items() + dictEducation_Score.items()+ dictInterested_In_Score.items())
    

    sorted(finalCandidate,key=finalCandidate.get,reverse= True);
    #count =0;
    print " Top 5 Friends with common category with" + getPublicUserName(person1Id, 'name', person1Access) +": "
    
    ptOutput=PrettyTable(['Similar Friends'])
    count=0;
    print "\n"
    for x in finalCandidate:
        if count>=5:
            break
        ptOutput.add_row([getPublicUserName(x, 'name', person1Access)])
        count=count+1
    print ptOutput


if __name__ == '__main__':
   task1()
   #task2()
   
   
