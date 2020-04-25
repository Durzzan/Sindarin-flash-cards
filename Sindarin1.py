import csv
import random
import numpy as np
from datetime import datetime  #datetime.date(datetime.now())
#random.seed()

def wordcompare(Responce,Answer):
    
    #need to remove special characters, possibly find and replace
    specialchars = [[['â','ä','à','á','À','Á','Â','Ä'],'a'],[['ê','ë','è','é','È','É','Ê','Ë'],'e'],[['î','ì','í','ï','Ì','Í','Î','Ï'],'i'],[['ö','ò','ô','ó','Ò','Ó','Ô','Ö'],'o'],[['ú','ù','û','ü','Ù','Ú','Û','Ü'],'u']]
    for i in range(0,len(Answer)):
        for j in range(0,5):
            if Answer[i]  in specialchars[j][0]:
                Answer = Answer.replace(Answer[i],specialchars[j][1])
                break
            
    #change to lower case      
    Answer = Answer.lower()
    Responce = Responce.lower()
        
    #split any multi answers up
    loc = Answer.find('/')
    answertemp = Answer
    Answer = []
    while loc != -1:
        Answer.append(answertemp[0:loc])
        answertemp = answertemp[loc+1:]
        loc = answertemp.find('/')
    Answer.append(answertemp)
           
    #compare against all answers
    correct = 0
    for i in range(0,len(Answer)):
        if Answer[i] == Responce:
            correct = 1
    
    return correct



with open('Nouns.csv', newline='') as csvfile:
    Nouns = csv.reader(csvfile, delimiter = ',')
    nouns = []
    Id = 0
    for row in Nouns:
        
        print(row)
        nouns.append([Id, int(row[0]),int(row[1]), int(row[2]), row[3:len(row)]])
        Id = Id +1
        
with open('Scores.csv', newline = '') as csvfile:
    Scores = csv.reader(csvfile,delimiter = ',')
    scores = []
    for row in Scores:
        print(row)
        scores.append([int(row[0]),int(row[1])])
        for i in range(0,int(row[1])):
            scores[len(scores)-1].append([int(row[((i*2)+2)]),int(row[((i*2)+3)])])
        
while len(scores)<len(nouns):
    num_words = nouns[len(scores)][3]
    scores.append([len(scores),num_words])
    for i in range(0,num_words):
        scores[len(scores)-1].append([0,0])
        
#flashcards begin
Lesson_No = input("Which lesson would you like to do flash cards for,\n type the number: ")

#sort out a lessons words
Words = []
for i in range(0,len(nouns)):
    if nouns[i][1] == int(Lesson_No):
        Words.append(nouns[i])
        

#load up chosen lesson either 10 or all
Lesson_Type = input("Type 'all' to test all or '10' to test just 10: ")

#Translate  english to sindarin or visa versa 
Language = input("For English to Sindarin type 'E', for Sindarin to English type 'S': ")


total_words = sum([Words[n][3] for n in range(0,len(Words))])
cumsumwords = np.cumsum([Words[n][3] for n in range(0,len(Words))])
if Lesson_Type == 'all':
    
    Order = random.sample(range(0,total_words), total_words)
else:
    
    Order = random.sample(range(0,total_words), 10)

    #new weighted sampling
    Weights = []
    for i in range(0,len(Words)):
        for j in range(0,Words[i][3]):
            streak = scores[Words[i][0]][j+2][0]
            if streak == 0:
                Weights.append(1)
                
            else:
                timesincecorrect = datetime.date(datetime.now()) - scores[Words[i][0][j+2][1]]
                if timesincecorrect < 1:
                    weight = (1./streak)*0.2
                elif timesincecorrect < 7:
                    weight = (1./streak)*0.4
                elif timesincecorrect < 14:
                    weight = (1./streak)*0.5
                elif timesincecorrect < 28:
                    weight = (1./streak)*0.6
                else:
                    weight = (1./streak)*0.6
                Weights.append(weight)
    
    Order = []
    while len(Order) < 10:
        sample = random.choices(range(0,total_words),weights = Weights)
        if sample not in Order :
            Order.append(sample[0])





#right and wrong counters
right = 0
wrong = 0


#TEST showing english
for i in range(0,len(Order)):
    for j in range(0,len(cumsumwords)):
        if Order[i] <= cumsumwords[j]:
            if Words[j][2] == 1: #checks if noun
                if Words[j][3] == 2: #checks if there are singulare and plural
                    if cumsumwords[j] - 1 == Order[i]:  #checks if it is refering to the singular
                        if Language == 'E':
                            if Words[j][4][0] == Words[j][4][1]:
                                answer = input(Words[j][4][0]+" (S): ")
                            else:
                                answer = input(Words[j][4][0]+": ")
                            if wordcompare(answer,Words[j][4][2]):
                                print("Correct!")
                                right = right +1
                                scores[Words[j][0]][2] = [scores[Words[j][0]][2][0] +1,datetime.date(datetime.now())] 
                            else:
                                print("Sorry the answer was ", Words[j][4][2])
                                wrong = wrong + 1
                                scores[Words[j][0]][2][0] = 0
                        else:
                            if Words[j][4][2] == Words[j][4][3]:  
                                answer = input(Words[j][4][2]+" (S): ")
                            else:
                                answer = input(Words[j][4][2]+": ")
                            if wordcompare(answer,Words[j][4][0]):
                                print("Correct!")
                                right = right +1
                                scores[Words[j][0]][2] = [scores[Words[j][0]][2][0] +1,datetime.date(datetime.now())]
                            else:
                                print("Sorry the answer was ", Words[j][4][0])
                                wrong = wrong + 1
                                scores[Words[j][0]][2][0] = 0
                    else:
                        if Language == 'E':
                            if Words[j][4][0] == Words[j][4][1]:
                                answer = input(Words[j][4][1]+" (P): ")
                            else:
                                answer = input(Words[j][4][1]+": ")
                            if wordcompare(answer,Words[j][4][3]):
                                print("Correct!")
                                right = right +1
                                scores[Words[j][0]][3] = [scores[Words[j][0]][3][0] +1,datetime.date(datetime.now())]
                                
                            else:
                                print("Sorry the answer was ", Words[j][4][3])
                                wrong = wrong + 1
                                scores[Words[j][0]][3][0] = 0
                        else:
                            if Words[j][4][2] == Words[j][4][3]:
                                answer = input(Words[j][4][3]+" (P): ")
                            else:
                                answer = input(Words[j][4][3]+": ")
                            if wordcompare(answer,Words[j][4][1]):
                                print("Correct!")
                                right = right +1
                                scores[Words[j][0]][3] = [scores[Words[j][0]][3][0] +1,datetime.date(datetime.now())]
                            else:
                                print("Sorry the answer was ", Words[j][4][1]) 
                                wrong = wrong + 1
                                scores[Words[j][0]][3][0] = 0
                            
                            
         
                elif Words[j][4][1] == '0':
                    if Language == 'E':
                        answer = input(Words[j][4][0]+": ")
                        if wordcompare(answer,Words[j][4][2]):
                            print("Correct!")
                            right = right +1 
                            scores[Words[j][0]][2] = [scores[Words[j][0]][2][0] +1,datetime.date(datetime.now())]
                        else:
                            print("Sorry the answer was ", Words[j][4][2])
                            wrong = wrong + 1
                            scores[Words[j][0]][2][0] = 0
                    else:
                        answer = input(Words[j][4][2]+": ")
                        if wordcompare(answer,Words[j][4][0]):
                            print("Correct!")
                            right = right +1
                            scores[Words[j][0]][2] = [scores[Words[j][0]][2][0] +1,datetime.date(datetime.now())]
                        else:
                            print("Sorry the answer was ", Words[j][4][0])
                            wrong = wrong + 1
                            scores[Words[j][0]][2][0] = 0
                else:
                    if Language == 'E':
                        answer = input(Words[j][4][1]+": ")
                        if wordcompare(answer,Words[j][4][3]):
                            print("Correct!")
                            right = right +1
                            scores[Words[j][0]][2] = [scores[Words[j][0]][2][0] +1,datetime.date(datetime.now())]
                        else:
                            print("Sorry the answer was ", Words[j][4][3])
                            wrong = wrong + 1
                            scores[Words[j][0]][2][0] = 0
                    else:
                        answer = input(Words[j][4][3]+": ")
                        if wordcompare(answer,Words[j][4][1]):
                            print("Correct!")
                            right = right +1
                            scores[Words[j][0]][2] = [scores[Words[j][0]][2][0] +1,datetime.date(datetime.now())]
                        else:
                            print("Sorry the answer was ", Words[j][4][1])
                            wrong = wrong + 1
                            scores[Words[j][0]][2][0] = 0
                    
            elif Words[j][2] == 2:
                if Language == 'E':
                    if Words[j][4][6] == '1':
                        formal = '(F)'
                    else:
                        formal = ''
                    if Words[j][4][4] == '1':
                        answer = input(Words[j][4][0]+" (" + Words[j][4][2] + ")"+formal+": ")
                    elif Words[j][4][5] == '1':
                        answer = input(Words[j][4][0]+" (" + Words[j][4][3] + ")"+formal+": ")
                    else:
                        answer = input(Words[j][4][0]+": ")
                    if wordcompare(answer,Words[j][4][1]):
                        print("Correct!")
                        right = right +1
                        scores[Words[j][0]][2] = [scores[Words[j][0]][2][0] +1,datetime.date(datetime.now())]
                    else:
                        print("Sorry the answer was ", Words[j][4][0])
                        wrong = wrong + 1
                        scores[Words[j][0]][2][0] = 0
                else:
                    if Words[j][4][7] == '1':
                        answer = input(Words[j][4][1]+" (" + Words[j][4][2] + "): ")
                    elif Words[j][4][8] == '1':
                        answer = input(Words[j][4][1]+" (" + Words[j][4][3] + "): ")
                    else:
                        answer = input(Words[j][4][1]+": ")
                    if wordcompare(answer,Words[j][4][0]):
                        print("Correct!")
                        right = right +1
                        scores[Words[j][0]][2] = [scores[Words[j][0]][2][0] +1,datetime.date(datetime.now())]
                    else:
                        print("Sorry the answer was ", Words[j][4][1])   
                        wrong = wrong + 1
                        scores[Words[j][0]][2][0] = 0
                        
            elif Words[j][1] == 3:
                if Language == 'E':
                    con = Order[i] - cumsumwords[j-1]
                    if con == 1: #First person I
                        answer = input("I " + Words[j][4][3] + ": ")
                        sindarin = "Ni " + Words[j][4][2][0:-1] +"on"
                    elif con == 2: #First person plural we exclusive
                        answer = input("we " + Words[j][4][3] + " (exclusive): ")
                        sindarin = "Mí " + Words[j][4][2] +"m"
                    elif con == 3: #First person plural inclusive
                        answer = input("we " + Words[j][4][3] + " (inclusive): ")
                        sindarin = "Mí " + Words[j][4][2] +"nc"
                    elif con == 4: #Second perosn formal singular
                        answer = input("You " + Words[j][4][3] + " (formal,Singular): ")
                        sindarin = "Le " + Words[j][4][2] +"l"
                    elif con == 5: #Second person formal plural
                        answer = input("You " + Words[j][4][3] + " (formal,plural): ")
                        sindarin = "Le " + Words[j][4][2] +"lir"
                    elif con == 6: #Second person singular
                        answer = input("You " + Words[j][4][3] + " (singular): ")
                        sindarin = "Ci " + Words[j][4][2][0:-1] +"og"
                    elif con == 7: #Second person plural
                        answer = input("You " + Words[j][4][3] + " (Plural): ")
                        sindarin = "Ci " + Words[j][4][2] +"gir"
                    elif con == 8: #Third person singular
                        answer = input("He " + Words[j][4][4] + ": ")
                        sindarin = "Ho " + Words[j][4][2]
                    elif con == 9: #Third person singualr
                        answer = input("She " + Words[j][4][4] + ": ")
                        sindarin = "He " + Words[j][4][2]
                    elif con == 10: #Third person singular
                        answer = input("It " + Words[j][4][4] + ": ")
                        sindarin = "Ha " + Words[j][4][2]
                    elif con == 11: #Third person plural
                        answer = input("They " + Words[j][4][3] + ": ")
                        sindarin = "Hy " + Words[j][4][2] +"r/Hi " + Words[j][4][2] +"r/Hai " + Words[j][4][2] +"r"
                    elif con == 12: #emphatic I
                        answer = input("It is I who " + Words[j][4][4] + ": ")
                        sindarin = "Im " + Words[j][4][2]
                    elif con == 13: #infinitive
                        answer = input("to " + Words[j][4][1] + ": ")
                        sindarin = Words[j][4][2][0:-1] +"o"
                    elif con == 14: #imperative
                        answer = input(Words[j][4][1] + ": ")
                        sindarin = Words[j][4][2][0:-1] +"o"
                    elif con == 15: #Gerun
                        answer = input(Words[j][4][5] + ": ")
                        sindarin = Words[j][4][2] +"d"
                    if wordcompare(answer,sindarin):
                        print("Correct!")
                        right = right +1
                        scores[Words[j][0]][con+1] = [scores[Words[j][0]][con+1][0] +1,datetime.date(datetime.now())]
                    else:
                        print("Sorry the answer was ", sindarin)
                        wrong = wrong + 1
                        scores[Words[j][0]][con+1][0] = 0
                else:
                    con = Order[i] - cumsumwords[j-1]
                    if con == 1: #First person I
                        answer = input("Ni " + Words[j][4][2][0:-1] + "on: ")
                        english = "I " + Words[j][4][3]
                    elif con == 2: #First person plural we exclusive
                        answer = input("Mí " + Words[j][4][2] +"m" + " (exclusive): ")
                        english = "we " + Words[j][4][3]
                    elif con == 3: #First person plural inclusive
                        answer = input("Mí " + Words[j][4][2] +"nc" + " (inclusive): ")
                        english = "we " + Words[j][4][3]
                    elif con == 4: #Second perosn formal singular
                        answer = input("Le " + Words[j][4][2] +"l" + " (formal,Singular): ")
                        english = "You " + Words[j][4][3]
                    elif con == 5: #Second person formal plural
                        answer = input("Le " + Words[j][4][2] +"lir" + " (formal,plural): ")
                        english = "You " + Words[j][4][3]
                    elif con == 6: #Second person singular
                        answer = input("Ci " + Words[j][4][2][0:-1] +"og" + " (singular): ")
                        english = "You " + Words[j][4][3]
                    elif con == 7: #Second person plural
                        answer = input("Ci " + Words[j][4][2] +"gir" + " (Plural): ")
                        english = "You " + Words[j][4][3]
                    elif con == 8: #Third person singular
                        answer = input("Ho " + Words[j][4][2] + ": ")
                        english = "He " + Words[j][4][4]
                    elif con == 9: #Third person singualr
                        answer = input("He " + Words[j][4][2] + ": ")
                        english = "She " + Words[j][4][4]
                    elif con == 10: #Third person singular
                        answer = input("Ha " + Words[j][4][2] + ": ")
                        english = "It " + Words[j][4][4]
                    elif con == 11: #Third person plural
                        answer = input("Hy/Hi/Hai " + Words[j][4][2] +"r" + ": ")
                        english = "They " + Words[j][4][3]
                    elif con == 12: #emphatic I
                        answer = input("Im " + Words[j][4][2] + ": ")
                        english = "It is I who " + Words[j][4][4]
                    elif con == 13: #infinitive
                        answer = input(Words[j][4][2][0:-1] +"o" + ": ")
                        english = "to " + Words[j][4][1]
                    elif con == 14: #imperative
                        answer = input(Words[j][4][2][0:-1] +"o" + ": ")
                        english = Words[j][4][1]
                    elif con == 15: #Gerun
                        answer = input(Words[j][4][2] +"d" + ": ")
                        english = Words[j][4][5]
                    if wordcompare(answer,english):
                        print("Correct!")
                        right = right +1
                        scores[Words[j][0]][con+1] = [scores[Words[j][0]][con+1][0] +1,datetime.date(datetime.now())]
                    else:
                        print("Sorry the answer was ",english )
                        wrong = wrong + 1
                        scores[Words[j][0]][con+1][0] = 0

            elif Words[j][1] == 4:
                if Language == 'E':
                    
                else:
            break
    

#Fix scores for saving
for i in range(0,len(scores)):
    num_words = nouns[i][3]
    newscores = [scores[i][0],scores[i][1]]
    for j in range(0,num_words):
        newscores.append(scores[i][j+2][0])
        newscores.append(scores[i][j+2][1])
    scores[i] = newscores
        
with open('Scores.csv', 'w' ,newline='') as csvfile:
    writer = csv.writer(csvfile,delimiter = ',')
    writer.writerows(scores)