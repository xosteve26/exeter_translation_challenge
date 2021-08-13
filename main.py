import csv
import re
import time
import os
import tracemalloc

 
tracemalloc.start()
time_start = time.perf_counter()
final={}
counts=[]
#Reading the french_dictionary.csv
with open('french_dictionary.csv','r') as csv_file:
    csv_reader=csv.reader(csv_file)
    d=dict(csv_reader)
    di=dict(d.items())

#Read the find_words.txt to create the English to French Translation dict, only for the words in the find_words.txt using the french_dictionary.csv file
with open('find_words.txt','r') as tx:
    tx_content=tx.read()
    for i in tx_content.split():
        try:
            final[i]=di[i]
        except:
            continue   
 
print("E-F Dictioanry Currated")  

#Read the t8.shakespeare.txt file to replace only the words from the list_words.txt file in the shakespeare.txt file
with open('t8.shakespeare.txt','r') as shks:
    shks_content=shks.read()
    for i,j in final.items():
        shks_content=shks_content.replace(i,final[i])
       
        if i.capitalize() in shks_content:
            shks_content=shks_content.replace(i.capitalize(),final[i].capitalize())
print("Read Shakespeare")

#Write the translated data into the t8.shakespeare.txt file
with open('t8.shakespeare.txt','w') as shks_w:
    shks_w.write(shks_content)
print("Translation Completed")


print("Start of Frequency calculation")
#Using Regex we 
for a in list(final.values()): #Iterate through the dictionariary's values(french words) 
        result = re.findall('\\b'+a+'|'+a+'s \\b', shks_content.lower()) #Check if each french word from the created dictionary is present in the newly trasnlated data and obtain a list.
        counts.append(len(result))#append the length of that result variable to the list
print(counts)

print("Frequency calculation completed")
#Open the frequency.csv file in write mode
with open('frequency.csv','w') as csvfile:
    writer=csv.writer(csvfile)
    headers=['English Word','French Word','Frequency']
    writer.writerow(headers)#Write the headers
    c=0
    for i,j in final.items():#iterate through the created dictionary
        writer.writerow([i,j,counts[c]])#Write in each row the english word, french equivalent alone with it's frequency
        c+=1

print("Frequency Written Successfully")
if os.name == 'posix':
    import resource
time_elapsed = (time.perf_counter() - time_start)
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB")
tracemalloc.stop()
print ("%5.1f secs" % (time_elapsed))


