'''
Created on May 7, 2018

@author: Joseph Waller
'''

#Dictionary of the English alphabet and each letters corresponding frequency of use in language 
frequency_table = {
    "A":.082,
    "B":.015,
    "C":.028,
    "D":.043,
    "E":.127,
    "F":.022,
    "G":.02,
    "H":.061,
    "I":.07,
    "J":.002,
    "K":.008,
    "L":.04,
    "M":.024,
    "N":.067,
    "O":.075,
    "P":.019,
    "Q":.001,
    "R":.06,
    "S":.063,
    "T":.091,
    "U":.028,
    "V":.01,
    "W":.024,
    "X":.002,
    "Y":.02,
    "Z":.001
    }


def frequency_test(letterList,maxCipherLength,minCipherLength):
    """ 
    Takes ciphered text along with the maximum and minimum cipher lengths allowed
    Outputs is decryption key as a list of numbers 
    """
    Decipher = []
    currentCipher = []
    lowestCipherVarence = 999999
    for currentTest in range(minCipherLength,maxCipherLength):
        letter_change_counter = 0
        currentCipherVarence = 0
        currentCipher.clear()
        letterfrequencyChecker = [([0] * 26) for x in range(currentTest)]
        for letter_change in letterList:
            holdingShiftCharNum = ord(letter_change)-65
            letterfrequencyChecker[letter_change_counter][holdingShiftCharNum] = letterfrequencyChecker[letter_change_counter][holdingShiftCharNum] + 1
            letter_change_counter = letter_change_counter + 1
            if letter_change_counter == currentTest:
                letter_change_counter = 0
        for x in range(currentTest):
            tempDataStorage = frequency_variation_test(letterfrequencyChecker[x])
            currentCipher.append(tempDataStorage[0])
            currentCipherVarence = tempDataStorage[1]+currentCipherVarence
        currentCipherVarence = currentCipherVarence / currentTest
        if currentCipherVarence < lowestCipherVarence and len(currentCipher) > 0:
            Decipher.clear()
            Decipher.extend(currentCipher)
            lowestCipherVarence = currentCipherVarence
        letterfrequencyChecker.clear()
    return Decipher

def frequency_variation_test(letterOccurencesList):
    """
    Takes in a list with a length of 26 which each list item is a number of how many times a letter occurs
    List number 0 is A, 1 is B, and so on
    Outputs the shift or key matching most closely to English letter frequency, and what the variation is 
    IE how far off that key is from an exact letter frequency 
    """ 
    letter_label = 'A'
    lowest_variation = 9999999
    best_shift = 9999999
    letter_variation = []
    for x in range(26):
        variation_check = 0
        letter_label = chr(65+x)
        for letter_count in letterOccurencesList:
            variation_check = abs((letter_count/sum(letterOccurencesList) - frequency_table[letter_label])) + variation_check
            letter_label = chr(ord(letter_label)+1)
            if ord(letter_label) > 90:
                letter_label = 'A'
        if lowest_variation > variation_check:
            lowest_variation = variation_check
            best_shift = x
        letter_variation.append(variation_check)
    return best_shift,lowest_variation

def letter_shift(shiftNumList,letterList):
    '''
    Takes in the cipher key number list and the encrypted text
    Outputs a new letter list which has been decrypted
    '''
    newLetterList = []
    cipherLength = len(shiftNumList)
    letterPosision = 0;
    for numberOfLetters in letterList:
        holdingnum = ord(numberOfLetters) + shiftNumList[letterPosision]
        if holdingnum > 90:
            holdingnum = (holdingnum % 90) + 64;
        newLetterList.append(chr(holdingnum))
        letterPosision = letterPosision + 1
        if letterPosision == cipherLength:
                letterPosision = 0
    return newLetterList

def reformat(letterList):
    '''
    Reformats a character list adding a space after every fourth entry
    Outputs this new list
    '''
    newLetterList = []
    spaceCounter = 0
    for numberOfLetters in letterList:
        if(spaceCounter%4 == 0 and spaceCounter != 0):
            newLetterList.append(' ')
        newLetterList.append(numberOfLetters)
        spaceCounter = spaceCounter + 1
    return newLetterList

def cipherToWord(cipherList):
    '''
    Takes in the int list which corresponds to cipher key
    Returns the cipher key as a string
    '''
    letterHolder = []
    for i in range(len(cipherList)):
        if cipherList[i] == 0:
            letterHolder.append('A')
        else:
            letterHolder.append(chr(91-cipherList[i]))
    return ("".join(letterHolder))
        
def letter_information(characterList):
    '''
    Takes in a character List and prints out data on it
    Used for testing and finding info out on the mystery.txt cipher
    '''
    letters = [0] * 26
    for character in characterList:
        charNum = ord(character)-65
        letters[charNum] = letters[charNum] + 1
        
    print('Number of times letter is used:')
    letter_label = 'A'
    for letter in letters:
        print("Variation from Average: " , abs((letter/sum(letters) - frequency_table[letter_label])))
        print(letter_label + ': ' , letter)
        letter_label = chr(ord(letter_label)+1)
    
def caesarCheck(cipherList):
    """
    Returns true if all characters in the cipher list are the same
    Meaning it's a Caesar Encyption otherwise it'll return false
    """
    for x in range(len(cipherList)-1):
        if cipherList[x] != cipherList[x+1]:
            return False 
    return True
     
def user_interface():
    """
    Contains the user interface for the code, and prints out data for the user
    """
    noFile = True
    print("rngDecyption the Caesar/Vigenere Decryption tool")
    print("***NOTE ONLY WITH VIGENERE KEYS UP TO 100 CHAR***")
    print("\n")
    while noFile:
        try:
            filename = input('Copy and paste the full file name of the text file you wish to decrypt:\n')
            with open(filename, 'r') as encryptedFile:
                encryptedText = encryptedFile.read().replace(' ','').replace(chr(10),'')
                encryptedTextList = list(encryptedText)
                if encryptedTextList == []:
                    print("That file is blank, please try again with an encrypted text")
                else:
                    noFile = False
        except FileNotFoundError as wrongFileName:
            print("That file name was incorrect, make sure you're typing it correctly")
    tempFilename = filename.replace('.txt', '')
    newFilename = tempFilename + "-decryption.txt"
    cipherKey = frequency_test(encryptedTextList,100,3)
    decryptedText = reformat(letter_shift(cipherKey,encryptedTextList))
    with open(newFilename,'w') as decryptedFile:
        decryptedFile.write("".join(decryptedText))
    if caesarCheck(cipherKey):
        print("Encrpytion Type: Caesar")
        print("Shift Number:   " , ((26-cipherKey[0])%26))
        print("Decrypted File: ", newFilename)
    else:
        print("Encrpytion Type: Vigenere")
        print("Cipher Key    : " , cipherToWord(cipherKey))
        print("Decrypted File: ", newFilename)
        
        
user_interface()
        
