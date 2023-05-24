#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

import os
from ghidra.program.util import DefinedDataIterator
from ghidra.program.flatapi import FlatProgramAPI

def get_unique_words_from_files(file_paths):
    unique_words = {}
    curcd = os.getcwd()
    for file_path in file_paths:
        if os.path.isfile(file_path):
            print("Opening: " + curcd+"\\"+file_path)
            with open(curcd+"\\"+file_path, 'r') as file:
                for line in file:
                    words = line.strip().split()
                    for word in words:
                        if word in unique_words:
                            unique_words[word] += 1
                        else:
                            unique_words[word] = 1
    return unique_words

def formatWords(unique_words):
    words = unique_words.keys()
    formated_words = []
    for word in words:
        if '=' in word:
            words.remove(word)
            assignments = word.split('=')
            for assign in assignments:
                words.append(assign)
        else:
            changed_word = word.replace('<', '')
            changed_word = changed_word.replace('>', '')
            changed_word = changed_word.replace('/', '')
            changed_word = changed_word.replace('"', '')
            if not (changed_word.isdigit() or (changed_word.count('.') == 1 and changed_word.replace('.', '').isdigit())):
                formated_words.append(changed_word)
    return formated_words
        
def find_words(words):
    currentProgram = getCurrentProgram()
    addresses = {}
    for data in DefinedDataIterator.definedStrings(currentProgram):
        strAddr = data.getMinAddress()
        strValue = getDataContaining(strAddr)
        try: 
            for word in words:
                if (word in str(strValue)):
                    if word in addresses:
                        addresses[word].append(strAddr)
                    else:
                        addresses[word] = [strAddr]
        except:
            pass
    return addresses
    
def get_functions(addrs):
    flat_api = FlatProgramAPI(currentProgram)
    func = set()
    for key in addrs:
        for addr in addrs[key]:
            referenceIterator = currentProgram.getReferenceManager().getReferencesTo(addr)
            for fun in referenceIterator:
                func.add(fun)
            codeUnit = getCurrentProgram().getListing().getCodeUnitAt(addr)
            codeUnit.setComment(codeUnit.POST_COMMENT, str(key))
    return func

def rename_functions(funcs):
    currentProgram = getCurrentProgram()
    symbol_table = currentProgram.getSymbolTable()
    num = 0
    for fun in funcs:
        symbol = symbol_table.getSymbol(fun.getName(), fun.getEntryPoint())
        symbol.setName("___" + str(num), ghidra.program.model.symbol.SourceType.USER_DEFINED)
        num += 1

def main():
    words = get_unique_words_from_files(["blank_movie.wlmp"])
    formated_words = formatWords(words)
    addrs = find_words(formated_words)
    functions = get_functions(addrs)
    rename_functions(functions)

    

if __name__ == "__main__":
    main()
