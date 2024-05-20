import random

All = ['rock', 'scissors', 'paper']
scores = 0
while True:
    user_input = input('Enter your choice:(From:rock, scissors, paper)').lower()
    if user_input not in All:
        print('Invalid input， please try again')
        continue

    computer_input = random.choice(All)
    print('Computer choice:',computer_input)

    if user_input == computer_input:
        print('平局')
    elif (user_input == 'rock' and computer_input == 'scissors') or \
        (user_input == 'scissors' and computer_input == 'paper') or \
        (user_input == 'paper' and computer_input == 'rock'):
        print('You win')
        scores += 1
    else:
        print('You lose')
        scores -= 1

    print('Your scores:',scores)

    play_again = ''
    while True:
        play_again = input("Do you want to play again?(yes/no)").lower()
        if play_again == 'no':
            break
        elif play_again == '' or play_again == 'yes':
            break
        else:
            print('Invalid input, please try again')
            continue

    if play_again == 'no':
        break
    

