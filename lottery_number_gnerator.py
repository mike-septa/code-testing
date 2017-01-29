from collections import Counter
import random
import sys

# lottery number generator 
class Person(object):
    '''
    This is an employee. It may be instantiated directly with the following params.

    :param first_name: String
    :param last_name: String
    '''
    
    def __init__(self, first_name='', last_name=''):
        # Each employee chooses their favorite numbers.
        self.first_name = first_name
        self.last_name = last_name
        self.first = 0
        self.second = 0
        self.third = 0
        self.fourth = 0
        self.fifth = 0
        self.sixth = 0
        self.powerball = 0
        self.stashbox = {x:True for x in range(1,70)}

    def GetExclusions(self):
        '''
        Function to provide a diplay indicating favorite numbers already chosen by this person

        :return: String
        '''
        result = ''
        exclusions = []
        for x in range(1,70):
            if not self.stashbox[x]:
                exclusions.append(x)

        if len(exclusions) > 1:
            last = exclusions.pop()
            result = ' '.join(str(e) for e in exclusions) + ' and ' + str(last)
                
        else: # for the 1st chosen 
            result = str(exclusions[0])

        return result

    def Display(self):
        '''
        Format the person's favorite numbers for display
        
        :returns: String
        '''
        result = ' '.join(str(e) for e in [self.first_name, self.last_name, self.first, self.second, self.third, self.fourth, self.fifth, 'Powerball:', self.powerball])
        return result
    
    

def get_duplicates(c):
    '''
    Find the duplicate values in Count or List objects

    :param c: Counter or List
    :returns: List
    '''
    try: # validate whether the type is List or Count
        q = list(c.elements())
    except AttributeError:
        q = c

    result = set([x for x in q if q.count(x) > 1])
                 
    return list(result)

    
def get_final_num(c):
    '''
    Determine the value for the Powerball
    Retrieve the max count of each unique duplicate number and use them as the Powerball numbers.
    if there is a tie based on the max counts randomly select the tied number.

    Note: I found the above instructions ambiguous and interpreted them as best as I could
          i.e. it doesn't specify the max counts of only powerball numbers so all numbers are included
          since the instruction says each unique duplicate number
          and the results are forced within the numeric range of a powerball number.
          .
          Regarding tied max counts it says nothing of how to handle more than a single tie so
          in the event of more than one tie I send them all to be randomly selected from.
          No instruction was provided for a catch-all in case the above process failed so
          I incorporated a random powerball generator for this case.
          


    :param c: Counter
    :returns: List
    '''
    common = c.most_common(5)
    i = 0
    limit = len(common) - 1
    # This is an ugly but functional way of trapping for tied values
    duplicates = []
    while i <= limit:
        index = common[i][1]
        for k, v in common:
            if v == index:
                duplicates.append(k)

        i += 1

    ties = get_duplicates(duplicates) # lazy way to avoid having to pop values above
    s = ''
    if len(ties) > 0:
        s = set([x for x in ties if x <= 26])

    # let's randomly select one from the tied values
    if len(s) > 0:
        result = random.choice(list(s))
    else: # in case all else fails
        print 'selecting random powerball\n'
        result = random.randint(1, 26)
    
    
    return result

def get_winner(c):
    '''
    Keep count of each individual favorite number
    provided to determine which numbers to use in our final winning number.
    (i.e. count the duplicates).
    possibly a cheat but it meets the requirments as I understood them

    :param c: Counter 
    :returns: List
    '''
    common = c.most_common(5)
    result = []
    for x, y, in common:
        result.append(x)

    return result
    
    

def main():    
    people = []
    cnum = Counter() # The collection of all number values entered by all players
    cpow = Counter() # The collection of all powerball values entered by all players 

    while True:
        i = 1
        p = Person()
        p.first_name = raw_input('Please enter your 1st name: ')
        p.last_name = raw_input('\nPlease enter your last name: ')
        while i < 6:
            # begin collecting favorite numbers
            number = None
            print '\n Choose favorite number %s\n' % i
            if i > 1:                  
                prompt = 'Enter a unique # between 1 and 69 excluding %s: ' % p.GetExclusions()
            else:
                prompt = 'Enter a unique # between 1 and 69: '
                
            while True:
                try:
                    number = int(raw_input(prompt))
                # catch error if the value is not a number and prompt to try again
                except ValueError:
                    print '0-9 Only! - Please try again...\n'
                    continue
                if number in range(1, 70): # check to see if number within range
                    if p.stashbox[number]: # check to see if already chosen
                        p.stashbox[number] = False
                        if i == 1:
                            p.first = number
                            break
                        elif i == 2:
                            p.second = number
                            break
                        elif i == 3:
                            p.third = number
                            break
                        elif i == 4:
                            p.fourth = number
                            break
                        elif i == 5:
                            p.fifth = number
                            break
                        else:
                            raise IndexError('totally not cool dude!')

                    else:
                        print 'Chosen number (%s) already selected! Please try again...\n' % number
                        continue

                else:
                    print 'Chosen number (%s) is out of range 1-69! Please try again...\n' % number
                    continue
            i += 1
            cnum.update([number])

            
        print '\nChoose your favorite Powerball #\n'
        while True:
            try:
                number = int(raw_input('Enter a unique # between 1 and 26: '))
            except ValueError:
                print '0-9 Only! - Please try again...\n'
                continue

            if number in range(1, 27): # check to see if number within range
                p.sixth = number
                p.powerball = number
                cpow.update([number])
                break


        print '%s, all your number are belong to us!' %p.first_name
        people.append(p)
        if raw_input('\nContinue? (Y=Yes, N=No)\n').upper() == 'Y':
            continue # add more people
        else: # or go to the end game
            for person in people: # Display all employees with their corresponding number entries.
                print person.Display()
                print '\n'

            # let's get our winning numbers
            winning_number = ' '.join(str(x) for x in get_winner(cnum))
            combined = cnum | cpow
            winning_powerball = get_final_num(combined)
            print 'Powerball winning number:\n %s Powerball: %s \n' % (winning_number, winning_powerball)
            print '\n'
            if raw_input(' Please type Q to quit\n').upper() == 'Q':
                print '\nGood luck!'
                break
                sys.exit()
            else:
                # lets review result values
                powball = get_final_num(cnum)
                print 'displaying raw values for debugging purposes...' 
                print cnum
                print cpow
                print 'duplicates: ' + str(get_duplicates(cnum))
                print 'powerball: ' + str(powball)
                print 'get_final_num: ' + str(get_final_num(cpow))
                print 'raandom: ' + str(random.randint(1, 26))
                print 'winner: ' + str(get_winner(cnum))
                break
                sys.exit()
            
    


if __name__ == '__main__':
    # This will only be executed when this module is run directly.
    # Invoke main() function
    main()
            
                

        


     

        
        
        
