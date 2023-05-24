import os
import csv
from tkinter import *

database = "SimpleView.tsv"
directory = 'Decks'
uniqueCardList = []
cardList = []
freqDict = {}
sortedFreqDict = {}


def decks_to_list(listname):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        if os.path.isfile(f):
            with open(f) as Deck:
                for line in Deck:
                    if "#" not in line:
                        if "!" not in line:
                            size = len(line)
                            modLine = line[:size - 1]
                            listname.append(modLine)


def IDs_to_names():
    for rawID in cardList:
        with open(database) as data:
            tsv_file = csv.DictReader(data, delimiter="\t")
            for row in tsv_file:
                if rawID == row['id']:
                    cardList[cardList.index(rawID)] = row['name']


def create_uniques_list(list1, uniquelist2):
    for x in list1:
        if x not in uniquelist2:
            uniquelist2.append(x)


def create_freq_dict(list1, uniquelist2, freqdict3):
    for x in uniquelist2:
        freqdict3[x] = list1.count(x)


def sort_freq_dict(freqdict):
    global sortedFreqDict
    sortedList = reversed(sorted(freqdict.items(), key=lambda x: x[1]))
    sortedFreqDict = dict(sortedList)


def run():
    global uniqueCardList
    global cardList
    global freqDict
    global sortedFreqDict
    uniqueCardList = []
    cardList = []
    freqDict = {}
    sortedFreqDict = {}
    try:
        try:
            decks_to_list(cardList)
            IDs_to_names()
            create_uniques_list(cardList, uniqueCardList)
            create_freq_dict(cardList, uniqueCardList, freqDict)
            sort_freq_dict(freqDict)
            with open("Export/"+fileNameEntry.get(), 'x') as export:
                export.write("These decks had a combined "+str(len(cardList))+" cards, and "+str(len(uniqueCardList)) +
                             " unique cards. \n")
                for key, value in sortedFreqDict.items():
                    export.write(key+" : "+str(value)+"\n")
        except PermissionError as e:
            popupWindow = Toplevel()
            warningLabel = Label(popupWindow,
                                 text=str(e)+"\nPlease do not leave the file name blank",
                                 font=("Times New Roman", 18),
                                 fg='red')
            warningLabel.pack()
    except FileExistsError as e:
        popupWindow = Toplevel()
        warningLabel = Label(popupWindow,
                             text=str(e)+"\nPlease choose a file name not already used",
                             font=("Times New Roman", 18),
                             fg='red')
        warningLabel.pack()


window = Tk()
window.geometry("1200x400")
window.title("Card Frequency Parser")
icon = PhotoImage(file="../../OneDrive/Desktop/ydks Freq Parser Application/icon.png")
window.iconphoto(True, icon)
instructions = Label(window,
                     text="Find the Decks folder in this application, then add the .ydk files you wish to add.\n "
                          "To get your exported data, name your export file using the entry box, then press the button below.",
                     font=("Times New Roman", 18),
                     padx=20,
                     pady=20)
instructions.pack(side='top')
runButton = Button(window,
                   command=run,
                   text="Run",
                   font=("Times New Roman", 18),
                   bg='black',
                   fg='white',
                   relief=RAISED,
                   padx=20,
                   pady=20)
runButton.pack(side='bottom', padx=10, pady=10)
fileNameEntry = Entry(window, font=("Times New Roman", 18))
fileNameEntry.pack(side='bottom')
plugLabel = Label(window,
                  text="Made by Chessprime1#0177",
                  font=("Times New Roman", 18),
                  fg='purple',
                  relief=SUNKEN)
plugLabel.pack(side='left', padx=10, pady=10)


window.mainloop()
