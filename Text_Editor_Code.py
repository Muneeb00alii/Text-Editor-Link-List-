import os
from copy import deepcopy
from Link_List import DLL
# from DLL import Node

""" 
This Code is for a text editor program that allows users to perform various operations on a text document.

The program supports the following commands:

1. goto <row> <col> - Move Pointer to the specified row and column
2. forward - Move Pointer forward by one character
3. back - Move Pointer back by one character
4. home - Move Pointer to the start of the current line
5. end - Move Pointer to the end of the current line
6. insert <text> - Insert text at the current Pointer position
7. delete <num> - Delete the specified number of characters from the Pointer position
8. countCharacters - Count the total number of characters in the document
9. countLines - Count the total number of lines in the document
10. print - Print the document
11. clear - Clear the console
12. find <word> - Find the specified word in the document
13. undo - Undo the last operation
14. redo - Redo the last undone operation
15. quit - Exit the program

The program uses a Doubly Linked List (DLL) to represent the text document. 
It handles all the possible errors and exceptions that may occur during the execution of the program and
It provides a user-friendly interface for interacting with the text document.

""" 

class TextEditor:
    def __init__(self):
        self.doc = DLL()
        self.Total_Lines = 0
        self.Pointer_Line = None
        self.Pointer_Char = None
        self.Undo = []
        self.Redo = []
        self.Row = 0
        self.Col = 0

    
    def goto(self, Row, Col):

        while self.Total_Lines < Row:
            self.doc.insert_at_end('\n')
            self.Total_Lines += 1

        Current_Line = self.doc.head
        for i in range(Row-1):
            if Current_Line.next is None:
                break
            Current_Line = Current_Line.next
        self.Pointer_Line = Current_Line
        self.Row = Row

        try:
            i = self.Pointer_Line.characters
        except AttributeError:
            self.Pointer_Line.characters = DLL()
            self.Pointer_Char = self.Pointer_Line.characters.head
            self.Col = 1

        for j in range(Col - 1):
            if self.Pointer_Char is None:
                break
            self.Pointer_Char = self.Pointer_Char.next
            self.Col = self.Col +1

        if self.Pointer_Char is None:
            characters_1 = self.Pointer_Line.characters
            while len(characters_1) < Col:
                characters_1.insert_at_end(' ')
            self.Pointer_Char = characters_1.tail
        self.Col = Col


    def insert (self, string):
        self.pre_undo_redo()
        if self.Pointer_Line is None:
            self.goto_1(1,0)

        if self.Pointer_Line.characters is None:
            self.Pointer_Line.characters = DLL()

        Current = self.Pointer_Char

        for i in string:
            if Current is None:
                self.Pointer_Line.characters.insert_at_end(i)
                Current = self.Pointer_Line.characters.tail

            else:
                self.Pointer_Line.characters.insert_between(i, Current)
                Current = Current.next

        self.Pointer_Char = Current

        if self.Row > self.Total_Lines:
            self.Total_Lines = self.Row

        # goto_call = 0
        self.printDoc()
        self.save()

    def delete(self, num):
        self.pre_undo_redo()
        Current =  self.Pointer_Char
        if num <= 0:
            return
        move = False
        for i in range(num):
            if Current is None:
                break
            if Current.prev is None:
                self.Pointer_Line.characters.delete_start()
                move = True
                Current = self.Pointer_Line.characters.head
            else:
                back = Current.prev
                self.Pointer_Line.characters.delete_node(Current)
                Current = back
                if self.Col > 0:
                    self.Col = self.Col -1
                if self.Pointer_Char is None:
                    break
        if move:
            self.Pointer_Line = self.Pointer_Line.prev
            if self.Pointer_Line is not None:
                self.Pointer_Char = self.Pointer_Line.characters.tail
                self.Row -= 1
                self.Col = len(self.Pointer_Line.characters)
        else:
            self.Pointer_Char = Current

        self.printDoc()
        self.save()

    def forward(self):
        if self.Pointer_Char is None:
            return
        
        if self.Pointer_Char.next is not None:
            self.Pointer_Char = self.Pointer_Char.next

        elif self.Pointer_Line.next is not None:
            self.Pointer_Line = self.Pointer_Line.next
            self.Pointer_Char = self.Pointer_Line.head

        else:
            return

        self.printDoc()

    def back(self):
        if self.Pointer_Char is None:
            return

        if self.Pointer_Char.prev is not None:
            self.Pointer_Char = self.Pointer_Char.prev

        elif self.Pointer_Line.prev is not None:
            self.Pointer_Line = self.Pointer_Line.prev
            self.Pointer_Char = self.Pointer_Line.characters.tail

        else:
            return

        self.printDoc()

    def home(self):
        if self.Pointer_Line:
            self.Pointer_Char = self.Pointer_Line.characters.head
        else:
            return

        self.printDoc()

    def end(self):
        if self.Pointer_Line:
            self.Pointer_Char = self.Pointer_Line.characters.tail
        else:
            return

        self.printDoc()
    
    def countLines(self):
        return self.Total_Lines

    def countCharacters(self):
        # return len(self.doc)
        count = 0
        cl = self.doc.head
        while cl is not None:
            try:
                word = cl.characters.head
            except AttributeError:
                cl = cl.next
                continue
            while word is not None:
                if word.data.isalnum() or word.data.isspace() or word.data in "!@#$%^&*()_+=-{}[]|:;\"'<>,.?/":
                    count += 1
                word = word.next
            cl = cl.next
        return count
    
    def printDoc(self):
        print("\n**************************************************************************")
        print("Document:")
        cl = self.doc.head
        while cl:
            try:
                word = cl.characters.head
                while word:
                    if word is self.Pointer_Char:
                        print("|", end="")
                    print(word.data, end="")
                    word = word.next
            except AttributeError:
                print()
            cl = cl.next
        print("\n**************************************************************************\n\n")

    def save(self):
        with open ("C:\\Users\\92321\\OneDrive\\Desktop\\Text Editor\\Data_File.txt", "w") as f:
            cl = self.doc.head
            while cl is not None:
                try:
                    word = cl.characters.head
                    while word is not None:
                        f.write(word.data)
                        word = word.next
                except AttributeError:
                    f.write("\n")
                cl = cl.next

    def find(self, word):
        count = 0
        with open ("C:\\Users\\92321\\OneDrive\\Desktop\\Text Editor\\Data_File.txt", "r") as f:
            for line in f:
                if word in line:
                    count += 1
            if count > 0:
                print(f"'{word}' found {count} times in the document.")
            else:
                print(f"'{word}' not found in the document.")
    
    def pre_undo_redo(self):
        state = (deepcopy(self.doc), self.Total_Lines, self.Pointer_Line, self.Pointer_Char, self.Row, self.Col)

        self.Undo.append(state)
        self.Redo.clear()

    def undo(self):
        if self.Undo:
            state = self.Undo.pop()
            redo_state = (deepcopy(self.doc), self.Total_Lines, self.Pointer_Line, self.Pointer_Char, self.Row, self.Col)
            self.Redo.append(redo_state)

            self.doc, self.Total_Lines, self.Pointer_Line, self.Pointer_Char, self.Row, self.Col = state

            self.printDoc()
            self.save()
        else:
            print("Nothing more to Undo.")

    def redo(self):
        if self.Redo:
            state = self.Redo.pop()
            undo_state = (deepcopy(self.doc), self.Total_Lines, self.Pointer_Line, self.Pointer_Char, self.Row, self.Col)
            self.Undo.append(undo_state)

            self.doc, self.Total_Lines, self.Pointer_Line, self.Pointer_Char, self.Row, self.Col = state

            self.printDoc()
            self.save()
        else:
            print("Nothing more to Redo.")

def clear_():
    os.system('cls')

    print("**************************************************")
    print("       Welcome to Text Editor Program!")
    print("**************************************************")
    print("Commands:")
    print("1. Goto |Row| |Col|")
    print("2. Insert |Text|")
    print("3. Delete |Num|")
    print("4. Forward")
    print("5. Back")
    print("6. Home")
    print("7. End")
    print("8. CountLines")
    print("9. CountCharacters")
    print("10. Print")
    print("11. Find |Word|")
    print("12. Undo")
    print("13. Redo")
    print("14. Clear")
    print("15. Quit\n")

def clear():
    os.system('cls')

def rating():
    rate = int(input("Rate the program (1-5): "))

    if rate < 1 or rate > 5:
        print("Invalid Rating! Please Rate Between 1-5.")
        rating()
    else:
        match rate:
            case 1:
                print("Sorry to hear that! We will try to improve.")
            
            case 2:
                print("Thank you for your feedback! We will try to improve.")
            
            case 3:
                print("Thank you for your feedback! We will try to improve.")
            
            case 4:
                print("Thank you for your feedback! We are Happy to hear that you Liked Us.")
            
            case 5:
                print("Thank you for your feedback! We are Happy to hear that you Liked Us.")

def main():
    global goto_call
    goto_call = 0
    in_call = 0
    cl_call = 0
    text_editor = TextEditor()
    clear_()

    while True:
        command = input("Enter Command: ")

        try:
            if command.lower() == "goto" or command.lower() == "g" or command == "1":
                row = int(input("Enter Row: "))
                col = int(input("Enter Col: "))

                if row < 1 or col < 0:
                    print("Invalid Row or Col! Please Try Again.")

                if goto_call == 0:
                    text_editor.goto((row), (col))
                    goto_call = goto_call + 1

                else:
                    cl_call = cl_call + 1
                    row = row + goto_call
                    text_editor.goto((row), (col))
                    goto_call = goto_call + 1

            elif command.lower() == "insert" or command.lower() == "i" or command == "2":
                text = input("Enter Text: ")

                if in_call == 0 and goto_call == 0:
                    text_editor.insert(text)
                    in_call = in_call + 1
                    goto_call = goto_call + 1

                else:
                    text_editor.insert(text)
            
            elif command.lower() == "delete" or command.lower() == "d" or command == "3":
                number = int(input("Enter Number: "))
                text_editor.delete(number)
            
            elif command.lower() == "forward" or command.lower() == "fo" or command == "4":
                text_editor.forward()

            elif command.lower() == "back" or command.lower() == "b" or command == "5":
                text_editor.back()

            elif command.lower() == "home" or command.lower() == "h" or command == "6":
                text_editor.home()

            elif command.lower() == "end" or command.lower() == "e" or command == "7":
                text_editor.end()

            elif command.lower() == "countLines" or command.lower() == "cl" or command == "8":
                if cl_call == 0:
                    print("Total Number of Lines are: ", text_editor.countLines())
                    cl_call = cl_call + 1

                elif cl_call > 0:
                    text_editor.Total_Lines = text_editor.Total_Lines - 1
                    print("Total Number of Lines are: ", text_editor.countLines())

            elif command.lower() == "countCharacters" or command.lower() == "cc" or command == "9":
                print("Total Number of Characters are: ", text_editor.countCharacters())

            elif command.lower() == "print" or command.lower() == "p" or command == "10":
                text_editor.printDoc()

            elif command.lower() == "find" or command.lower() == "f" or command == "11":
                word = input("Enter the Word: ")
                text_editor.find(word)

            elif command.lower() == "undo" or command.lower() == "u" or command == "12":
                text_editor.undo()

            elif command.lower() == "redo" or command.lower() == "r" or command == "13":
                text_editor.redo()

            elif command.lower() == "clear" or command.lower() == "c" or command == "14":
                clear_()

            elif command.lower() == "quit" or command.lower() == "q" or command == "15":
                ratings = input("Do you want to rate us? (Yes/No): ")

                if ratings.lower() == "yes" or ratings.lower() == "y":
                    rating()
                    input("Press Enter to Exit.")
                    clear()
                    break

                elif rating.lower() == "no" or rating.lower() == "n":
                    clear()
                    break

                else:
                    raise ValueError("Invalid Input")
                
            else:
                print("Invalid Command. Please Try Again.")
                clear_()

        except(ValueError, IndexError) as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()


#! Coded By Muneeb Ali
