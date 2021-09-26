import random

#function to help underline what i need later on
def underline(string):
    emptystring = ''

    for i in range(0, len(string)):

        if string[i] == ' ':
            emptystring = emptystring + string[i]
        else:
            emptystring= emptystring+string[i]+str('\u0332')

    return emptystring


#the actual stuff

#read the definition file
definitions = {}
with open('definitions.txt') as f1:
    #each line should have 1 definition, tab seperated
    for line in f1:
        word, definition = line.strip().split('\t')
        definitions[word] = definition

#repeatedly ask user what they want
quit_flag = False
one_or_two = False #if i choose option one or two
while quit_flag == False:
    option = input('''
Please choose an option:
1. Enter a specific word (that you would like to define)
2. Random
3. Quit
''')
    if option == '1':
        one_or_two = True
        exist = False
        while exist == False:
            word = input('Please enter a word/phrase you would like to define: ')
            word = word.lower()
            if word in definitions:
                exist = True
            else:
                print('That word/phrase does not exist! Did you spell it right?')

        actual_definition = definitions[word]
        
    elif option == '2':
        one_or_two = True
        #choose a random pair
        word, actual_definition = random.choice(list(definitions.items())) 

    elif option =='3':
        print('Goodbye!')
        break
    
    else:
        print('That was neither 1, 2, or 3!')

    #So i dont need to repeat code
    #this is to enter the defnition and compare it with the choosen word
    #to get here should have word and defnition variables already
    if one_or_two == True:
        #ask user toenter their definition
        user_answer = input(f'Please define {word}: ')

        #get each individual word, so i can see which words i missed
        actual_definition_words = actual_definition.strip().split(' ') #this is for compare
        output_definition_words = actual_definition_words.copy() #this is my backup copy
        user_answer_words = user_answer.strip().split(' ')

        #compare
        for word in user_answer_words:
            word = word.lower()
            if (word in actual_definition_words):
                actual_definition_words.remove(word) #remove the word

            #sometimes the word is connected to the comma
            elif (word+',') in actual_definition_words:
                actual_definition_words.remove(word+',')
    
        #whatever is left in actual_definition_words would be the once i missed
        print('Here is the full definition. The underlined words are the words you missed:') 

        output = ''

        for word in output_definition_words:
            #if its in that list, means did not mention, so underline, somecommonuseless words
            if (word in actual_definition_words) and (word not in ['the', 'of', 'is', 'it']):
                word = underline(word)

            output += word + ' '

        print(output)
