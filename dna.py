import re
import pygame
import time


# Constant variables for DNA bases
ADENINE = "A"
GUANINE = "G"
CYTOSINE = "C"
THYMINE = "T"

# Dictionary of DNA bases to musical note names
DNA_TO_NOTES = {
    ADENINE: "C",
    GUANINE: "D",
    CYTOSINE: "E",
    THYMINE: "G"
}

NOTE_FILES = {
    "C": "sounds/c1.wav",
    "D": "sounds/d1.wav",
    "E": "sounds/e1.wav",
    "G": "sounds/g1.wav"  
    }

program_running = True
sequences = [] #Stores valid DNA sequences
dna_sequence = ("")  # Initialize an individual dna sequence
melodies = []  #Stores melodies generated from DNA sequences
tempo = 120 #initialize Pygame mixer

#innitialize Pygame mixer
pygame.mixer.init()

def display_sequences(): 
    # Function that allows user to display their sequences
    if sequences:
        print("\nStored Sequences: ")
        for index, seq in enumerate(sequences, start=1):
            print(f"{index}: {seq}")
    else:
        print("\nThere are no sequences stored. ")
        
def ask_for_data(): #Prompts the user for a unique DNA sequence and stores it if unique and fits input criteria
    global dna_sequence
    while True: 
        try:
            dna_sequence = str(input("Please enter a AGCT sequence: ")).upper().strip().replace(" ", "")
            
            if not re.fullmatch(r'[AGCT]+', dna_sequence): #If input does not contain correct characters, restart loop, re-ask question
                print("Invalid input, please only enter 'A' 'G' 'C' and 'T'.")
                continue
            
            if dna_sequence in sequences: #Prevents duplicate sequences
                print("This sequence has already been entered. Please attempt a new sequence.")
                continue
            
            print("Your sequence was stored.") #Stores sequence in list
            sequences.append(dna_sequence)
            break
        
        except ValueError as error:
            print(error)


def dna_melody_convert(dna_sequence):
    """Converts a DNA sequence into a melody based on notes corresponding with wav files"""
    melody = []
    prev_base = None
    counter = 0
    
    for base in dna_sequence:
        if base == prev_base:
            counter += 1
        else:
            if prev_base is not None:
                melody.append((DNA_TO_NOTES[prev_base], counter))
            prev_base = base #sets new base as previous base for the next iteration
            counter = 1 #Resetting the count for each new base
        
    if prev_base is not None:
        melody.append((DNA_TO_NOTES[prev_base], counter))
        
    return melody

def store_melodies():
   """This function receives all the DNA sequences that were stored,
   and converts them into musical melodies."""
  
   global melodies
   melodies.clear() #clears the old melody storage to account for duplicates

   for seq in sequences:
       melody = dna_melody_convert(seq)
       melodies.append(melody) #Stores the melody in global melodies list

def add_melody():
    while True: 
        try:
            new_sequence = str(input("Please enter a AGCT sequence: ")).upper().strip().replace(" ", "")
            
            if not re.fullmatch(r'[AGCT]+', new_sequence): #If input does not contain correct characters, restart loop, re-ask question
                print("Invalid input, please only enter 'A' 'G' 'C' and 'T'.")
                continue
            
            if new_sequence in sequences: #Prevents duplicate sequences
                print("This sequence has already been entered. Please attempt a new sequence.")
                continue
            
            print("Your sequence was stored.") #Stores sequence in list
            sequences.append(new_sequence)
            new_melody = dna_melody_convert(new_sequence)
            melodies.append(new_melody)
            break #Exits loop
        
        except ValueError as error:
            print(error)

def delete_melody(melody_number):
    try:
        melody_to_delete = melodies[melody_number] #Removed the inputted melody number from melodies list
        melodies.remove(melody_to_delete)

        sequence_to_delete = sequences[melody_number] #Removed the sequence from sequences list
        sequences.remove(sequence_to_delete)

        print(f"Melody {melody_number + 1} has been deleted.") #Adds 1 because index starts at 0

    except IndexError:
        print("Invalid index!")


def display_melodies():# Function that allows user to display their melodies as a list
    
    if melodies:
        print("\nStored Melodies: ")
        for index, (seq, melody) in enumerate(zip(sequences, melodies), start=1):
            print(f"\nMelody {index}: (From sequence: {seq}) ") #index is index number of stored melodies, seq is the DNA sequence
            print(melody)
    else:
        print("\nThere are no melodies stored. ")
        
        
def play_melody(melody):
    seconds_per_beat = 60 / tempo

    for note, duration in melody:
        file_path = NOTE_FILES.get(note)
        if file_path:
            try:
                sound = pygame.mixer.Sound(file_path)
                for i in range(duration):
                    sound.play()
                    time.sleep(duration * seconds_per_beat)
            
            except pygame.error as r:
                print(f"Error with {note}: {r}")

    print("Melody Complete...")

def end_program():
    global program_running
    program_running = False
    print("Exiting Project...")
    exit()


def menu_prompt():
    while True:
        user_choice = input("\nPress:\nA to add a melody.\nB to view melody list.\nC to play a melody.\nD view sequences list.\nR to remove a melody.\nQ to quit.\n ").lower()

        if user_choice == "d":
            display_sequences()

        elif user_choice == "b":
            display_melodies()

        elif user_choice == "c":
            if melodies:
                try:
                    melody_num = int(input("Which melody would you like to play?: ")) - 1
                    if 0 <= melody_num < len(melodies):   
                        play_melody(melodies[melody_num])
                    else:
                        print("There is no melody with that index.")
                except ValueError:
                    print("\nInvalid input. Please enter an integer :) ")
            else:
                print("It appears you have no melodies to select, please restart the program.")

        elif user_choice == "a":
                add_melody()

        elif user_choice == "r":
            if melodies:
                    try:
                        melody_num = int(input("Which melody would you like to delete?: ")) - 1
                        if 0 <= melody_num < len(melodies):   
                            delete_melody(melody_num)
                        else:
                            print("There is no melody with that index.")
                            
                    except ValueError:
                        print("Invalid input. Please enter an integer :) ")
                        
            else:
                print("It appears you have no melodies to select, please restart the program.")

        elif user_choice == "q":
                        end_program()
        else:
            print("Invalid, please enter a valid input.")                    
        

def main(): # Main Loop
    try:
        while True:
            if sequences:
                should_clear = input("Would you like to clear past generated sequences? (y/n): ").lower()
                if should_clear == "y":
                    sequences.clear()
                    break
                else:
                    break
            else:
                break


        while True:
            try: #Asks for the number of DNA sequences, ensures no errors
                num_sequences = int(input("\nEnter the number of DNA sequences you want to input, (this will be how many different melodies are created): "))
                if num_sequences < 1 or num_sequences > 10:
                    print("\nPlease enter a number greater than 0 and less than 10.")
                    continue
                break
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")

        for i in range(num_sequences):
            ask_for_data()

        global tempo
        while True:
            try:
                tempo = int(input("Please enter a bpm / tempo for your melodies (e.g. 120, 90, etc.):  "))
                if tempo <= 0 or tempo >= 300:
                    print("Please enter a number between 0 and 300.")
                    continue
                else:
                    break

            except ValueError:
                print("Invalid input. Please enter a valid bpm/number, reccomended over 60.")
        
        store_melodies()

        while True:     
            menu_prompt()
    
    except KeyboardInterrupt as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    print("Hello, welcome to DJ DNA 🎵.")
    print()
    print("This is a musical generator that will take an inputted sequence of DNA, and output a series of musical notes in accordance. Enjoy!")
    print("DNA Sequences are determined by the four chemical bases that make up DNA: Adenine (A), Thymine (T), Cytosine (C), and Guanine (G).\n")       
    main()
