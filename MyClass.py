'''
Ce l’ho, mi è venuto in mente stanotte come PR per attrs, 
ma puoi farlo senza attrs. 
Un tool che prende una regex, una dataclass 
(o una classe attrs, ma se vuoi un esercizio non è necessaria) 
e un valore e ti ritorna un’instanza della dataclass 
popolata parsando il valore con la regex attraverso 
i named groups. 
Ovviamente i nomi dei gruppi dovrebbero matchare gli attributi 
della data class.

In uno scenario reale, l’ideale sarebbe avere un’API tipo:

#qui fa la validazione che la regex abbia i named groups della 
# data class
my_class_parser=MyClass.regex_parser(r"my_regex")

# qui prova a parsare e se la regex non matcha, 
# o tira un'eccezione o ritorna None
my_class_parser(some_value) 

Se funziona, possiamo adattarla ad attrs e fare una PR.
'''

#!/usr/bin/env python3 

import logging # to debug
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# This function read a dataclass and return the array containing 
# the name of its attribute
def mydataclass_parser(dataclass):
    logging.info("hello, I am the mydataclass_parser function")
    TBparsed = str(dataclass)

    logging.info('I am the dataclass ' + TBparsed)
    
    attribute_regex = re.compile(r'''
    (\(|\s)         # It start either with ( or blankspace and it start 
    ([a-zA-Z]       # Note that the regex request that it starts with an 
    (\w)*)          # alphabet letter and continue with a \w, because it's 
                    # a variable and therefore it can't start with a number or 
                    # a symbol like -
    ''', re.VERBOSE)
    
    # find all the attribute
    result = attribute_regex.findall(TBparsed)
    logging.info(result) # the result us a list of tuples


    attribute_list = []

    for attribute_tuple in result:
        logging.debug(attribute_tuple[1])
        attribute_list.append(attribute_tuple[1])

    return attribute_list # attribute_list is an empty list



# This function parse the regex and return an array with the named attribute
def myregex_parser(regex):

   
   logging.info("hello, I am the myregex_parser function")
   regex = str(regex) # I need to cast to string the regex
   logging.debug(regex) 
   regex_parser = re.compile(r'''
        <               # Beginning
        ([A-Za-z](\w)+) # It continue either with a letter and the a \w
        >               # Ending
        ''', re.VERBOSE)
   
   result = regex_parser.findall(regex)

   attribute_list = [] # attribute_list is an empty list

   for attribute_tuple in result:
       logging.debug('DEBUG ' + attribute_tuple[0])
       attribute_list.append(attribute_tuple[0])

   return attribute_list 



# This function check if dataclass have the list of attributes from 
# the regex is the same of the list of attributes of the dataclass
# To do this it just check if the content of the two list is the same

def comparer(attributes1, attributes2):
    len1 = len(attributes1)
    len2 = len(attributes2)
    
    if len1 != len2:
        # If the lenght is not equal they're not the same for sure
        return False
    
    # Now I alphabetically order the two list
    # NOTE: I'm not sure if this is useful
    sorted(attributes1)
    sorted(attributes2)

    for i in range(0, len1 - 1):
        logging.debug	('attributo1 ' + attributes1[i])
        logging.debug	('attributo2 ' + attributes2[i])
        if attributes1[i] != attributes2[i]:
            return False 
    
    logging.debug	('It is True!')
    return True # If I'm arrived here it must be true

# TODO: write the part where I fill the dataclass with values


# This function check if dataclass have the same attribute names
# of the named attributes of the regex
def my_parser(dataclass, regex):

    list_dataclass = mydataclass_parser(dataclass)
    list_regex = myregex_parser(regex)
    
    comparer(list_dataclass, list_regex)


# TODO:  return an istance of the dataclass populated
# parsing the value with the regex 
def filler(dataclass, regex, value):
    
    logging.debug('You launched filler function')
    logging.debug('dataclass: ' + str(dataclass))
    logging.debug('regex: ' + str(regex))
    logging.debug('value: ' + str(value))
    result = regex.search(value)
    logging.debug(result)
    logging.debug('example: name: ' + result.group('name'))
    #TODO: since logging has copyright what could be the licence of this program?
    list = myregex_parser(regex)
    logging.debug('list-> ' + str(list))
    for item in list:
        logging.debug('named_group: ' + str(item))
        logging.debug('test: ' + result.group(item))
        print(str(dataclass.__dict__))
        dataclass.__dict__[item] = result.group(item)
    
    #TODO understand why number was not filled
    logging.debug(str(dataclass))

import re
from dataclasses import dataclass

logging.debug('Test')

# The tool take a regex, this is my example regex
# TODO change the regex or the dataclass in order that the attributes match
regex_example = re.compile(r'(?P<name>.*) (?P<phone>.*)')

# Now I create my example dataclass
# The name of the group of regex should be the equal
# to the name of the attribute
@dataclass
class dataclass_example:
    name:  str
    number: str


# Now I create my example value
value_example = 'John 123456'

# Now I create an istance of the dataclass that I should fill and return
value1 = ''
value2 = ''
return_example = dataclass_example(value1, value2) # This is the example that I'll fill and return

# Here I try to see that the regex has the same named groups of the dataclass

my_parser(return_example, regex_example)
filler(return_example, regex_example, value_example)