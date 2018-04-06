
# coding: utf-8

# In[1]:


player_ratings = {}
player_duelcount = {}
duels=[]
initialPlayers=["Kappa","Mycroft","FrozenLiquidity","GeoKnightV"]


# In[2]:


import pickle

win=1
draw=0.5
loss=0


def LoadData():
    with open('player_ratings.pickle', 'rb') as handle:
        player_ratings = pickle.load(handle)
    
    with open('player_duelcount.pickle', 'rb') as handle:
        player_duelcount = pickle.load(handle)    
 
    with open('duels.pickle', 'rb') as handle:
        duels = pickle.load(handle)
        
    return [player_ratings, player_duelcount, duels]
    
def SaveData():
    with open('player_ratings.pickle', 'wb') as handle:
        pickle.dump(player_ratings, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('player_duelcount.pickle', 'wb') as handle:
        pickle.dump(player_duelcount, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('duels.pickle', 'wb') as handle:
        pickle.dump(duels, handle, protocol=pickle.HIGHEST_PROTOCOL)    


def RecordKeeper(player1,player2,outcome,duels):
    "Adds a duel to a list of all duels"
    duels.append([player1,player2,outcome])
    
def AddPlayer(new_player,player_ratings,player_duelcount):
    "Adds a new player and assigns him the average score af all players"
    if new_player in player_ratings:
        print("Player already exists.")
    else:
        player_duelcount[new_player] = 0
        if len(player_ratings) == 0:
            player_ratings[new_player] = 1000                        
        else:    
            player_ratings[new_player] = sum(player_ratings.values())/(len(player_ratings))

def Expect(player1,player2):
    "Gives expected probability of a win"
    return 1/(1+10**(1/400*(player_ratings[player2]-player_ratings[player1])))

def Duel(player1,player2,outcome,player_ratings,player_duelcount):
    "Performs all necessary actions to update the duel statistics."
    RecordKeeper(player1,player2,outcome,duels)
    player_duelcount[player1] += 1
    player_duelcount[player2] += 1
    rating_change = (outcome-Expect(player1,player2))
    
    if player_duelcount[player1]>=5 and player_duelcount[player2]>=5:
        player_ratings[player1] += 32*rating_change
        player_ratings[player2] -= 32*rating_change
    
    elif player_duelcount[player1]<5 and player_duelcount[player2]<5:
        player_ratings[player1] += 64*rating_change
        player_ratings[player2] -= 64*rating_change
        
    elif player_duelcount[player1]>=5 and player_duelcount[player2]<5:
        player_ratings[player2] -= 64*rating_change
        
    else:
        player_ratings[player1] += 64*rating_change
        
def RestoreFromDuelList (filename):
    player_ratings = {}
    player_duelcount = {}
    with open(filename, 'rb') as handle:
        duels = pickle.load(handle)
        
    for i in range(0,(len(duels))):
        AddPlayer(duels[i][0],player_ratings,player_duelcount)
        AddPlayer(duels[i][1],player_ratings,player_duelcount)
        
    for i in range(0,(len(duels))):
        Duel(duels[i][0],duels[i][1],duels[i][2],player_ratings,player_duelcount)
    
    return [player_ratings, player_duelcount]
    


# In[3]:


player_ratings = LoadData()[0]
player_duelcount = LoadData()[1]
duels = LoadData()[2]


# In[4]:


for name in initialPlayers:
    AddPlayer(name, player_ratings, player_duelcount)


# In[5]:


Duel("Mycroft","FrozenLiquidity",win,player_ratings,player_duelcount)
Duel("GeoKnightV","Kappa",loss,player_ratings,player_duelcount)
Duel("GeoKnightV","FrozenLiquidity",draw,player_ratings,player_duelcount)
Duel("Kappa","Mycroft",loss,player_ratings,player_duelcount)
Duel("FrozenLiquidity","GeoKnightV",win,player_ratings,player_duelcount)


# In[6]:


for name in player_ratings.keys():
    print(name,player_ratings[name])


# In[7]:


for name in duels:
    print(name)


# In[8]:


for name in player_duelcount:
    print(name, player_duelcount[name])


# In[9]:


SaveData()

