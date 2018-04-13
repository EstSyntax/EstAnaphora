# -*- coding: utf-8 -*-

"""

Proovime kirjutada utiliidi, mis gtmrf-1 failist teed Brat tarkvarale söödava faili
gtmrf-1 faili parsimise osa kopeerime scriptist gt2cg.py v 144

Esiteks proovime kirja panna


Current version of gt2cg doesn't support input from STDIN.
Supported input format inforem format as shown below:

"<s>"

"<“>"
	"“" Z Oqu #1->1
"<Ma>"
	"mina" L0 P pers ps1 sg nom @SUBJ #2->3
"<olen>"
	"ole" Ln V main indic pres ps1 sg ps af @FMV #3->0
"<optimist>"
	"optimist" L0 S com sg nom @PRD #4->3
"<.>"
	"." Z Fst #5->5
"<”>"
	"”" Z Cqu #6->6
"</s>"

Output format:

brat.txt and brat.ann format

brat.txt
Testid
First second third.

 brat.ann
T1	Person 7 12	First
T2	Organization 13 19	second
T3	GPE 20 25	third
R1	Employment Arg1:T1 Arg2:T3
T4	Person 20 25	third
#1	AnnotatorNotes T4	comment third token
T5	Divorce 0 6	Testid
E1	Divorce:T5
brat.txt
Testid
First second third.



"""



######## libraries ########
from __future__ import print_function


import pprint
import re
import codecs

import sys



from argparse import ArgumentParser

######## common helping functions ########

class bColors:

	colors = (
		'\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m', '\033[1;37m', '\033[1;38m',
		'\033[1;39m'
	)
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'



def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)



def open_output_files():
	global out_filename, file_count, f_out_ann, f_out_txt
	output_filename_pattern_txt = "%s.%04d.txt"
	output_filename_pattern_ann = "%s.%04d.ann"
	f_out_txt = codecs.open((output_filename_pattern_txt%(out_filename,file_count )), "w", "utf-8")
	f_out_ann = codecs.open((output_filename_pattern_ann%(out_filename,file_count )), "w", "utf-8")
	file_count += 1
	return

	
	

######## dictonary functions ########
#siia tuleb Brat märgendite dict


####### sentence table functions ########

def transform_ann(sentence_dict):
	sentence_string=''
	global tag_nr, rel_nr, f_out_ann, f_out_txt, tokens_count, max_tokens
	sentence_word_positions={}
	global file_pos
	relation_pattern = '^(\d+)->(\d+)$'
	for lineid in sorted(sentence_dict['lines']):
		if sentence_dict['lines'][lineid]['type'] == 'token':
			for i,v in enumerate(sentence_dict['lines'][lineid]['info']['analys']['lemma']):
				tag_nr +=1
				sentence_string += sentence_dict['lines'][lineid]['info']['token']+' '
				morf = sentence_dict['lines'][lineid]['info']['analys']['morf'][i]
				pos   = sentence_dict['lines'][lineid]['info']['analys']['pos'][i]
				lemma  = sentence_dict['lines'][lineid]['info']['analys']['lemma'][i]
				relation = sentence_dict['lines'][lineid]['info']['analys']['relation'][i]
				function = sentence_dict['lines'][lineid]['info']['analys']['function'][i]
				sentence_word_positions[lineid]={}
				sentence_word_positions[lineid]['start']=file_pos
				sentence_word_positions[lineid]['end'] = file_pos+len(sentence_dict['lines'][lineid]['info']['token'])
				file_pos = file_pos+len(sentence_dict['lines'][lineid]['info']['token']+' ')
				sentence_word_positions[lineid]['tag_nr'] = tag_nr
				
							  
				
				#print ("T%d\t%s %d %d\t%s"%(tag_nr, pos,sentence_word_positions[lineid]['start'],sentence_word_positions[lineid]['end'], sentence_dict['lines'][lineid]['info']['token']))
				f_out_ann.write ("T%d\t%s %d %d\t%s\n"%(tag_nr, pos,sentence_word_positions[lineid]['start'],sentence_word_positions[lineid]['end'], sentence_dict['lines'][lineid]['info']['token']))
			 
				#4      Lemma T4         olla
			   
				#print ("#%d\tLemma T%d\t%s"%(tag_nr, tag_nr, lemma))
				f_out_ann.write ("#%d\tLemma T%d\t%s\n"%(tag_nr, tag_nr, lemma))
				
				
						
    #ja nyyd eraldi loop relationite jaoks, kuna kõikide tag-ide numbreid pole alguses teada
						#relation
	for lineid in sorted(sentence_dict['lines']):
		tokens_count += 1
		if sentence_dict['lines'][lineid]['type'] == 'token':
			for i,v in enumerate(sentence_dict['lines'][lineid]['info']['analys']['lemma']):
				
				relation = sentence_dict['lines'][lineid]['info']['analys']['relation'][i]
				function = sentence_dict['lines'][lineid]['info']['analys']['function'][i]
				function = function.replace("@", "").replace(">", "").replace("<", "")
				
				match_relation = re.match(relation_pattern, relation)
				if (function != ''  and match_relation and match_relation.group(1)!=match_relation.group(2) and match_relation.group(2)!='0'):
					rel_nr +=1
					#print (match_relation.groups(), lineid)
					f_out_ann.write ( ("R%d\t%s Arg1:T%d Arg2:T%d\n"%(rel_nr
					          , function
					          , sentence_word_positions[int(match_relation.group(1))]['tag_nr']
							  , sentence_word_positions[int(match_relation.group(2))]['tag_nr']
							)))
	
				
				
	#print (sentence_string.strip())
	f_out_txt.write(sentence_string.strip()+"\n")
	if tokens_count//max_tokens == 1:
		open_output_files()
		tokens_count = 0
		file_pos = 0
		tag_nr = 0
		rel_nr = 0
		
	
	
	return sentence_string.strip()
	
#esialgne loogika vïks olla selline
#loetakse failist sisse kïk åhe lause read, märgendist <s> kuni märgendini </s> vï siis faili lõpuni

def makeDictFromArray(aSentence):
	sentence_dict={}
	sentence_dict = {'lines':{}}
	#sentence_dict['lines'][lineid]['type'] == 'token'
	#dict['analys']={}
	#           dict['analys']['lemma']=[]
	#          dict['analys']['case']=[]
	#         dict['analys']['morf']=[]
	#        dict['analys']['lemma'].append('ERROR!!! '+line)
	#        dict['analys']['case'].append('')
	#        dict['analys']['morf'].append(line)
	pp = pprint.PrettyPrinter(indent=4)
	""""
		<Kord>"
			"kord" L0 D @ADVL #1->4
		"<olid>"
			"ole" Lid V aux indic impf ps3 pl ps af @FCV #2->4
		"<need>"
			"see" Ld P dem pl nom @OBJ #3->4
		"<suunatud>"
			"suuna" Ltud V main partic past imps @IMV #4->0
	"""
	token_line_pattern = '^"<([^"]+)>"$'
	lemma_line_pattern ='"([^"]*)" ([^\@]+)(\@[^\s]+)* #(\d+->\d+)$'
	morf_pattern = '^(L([^\s]+) )*([A-Z])([A-Za-z\d\s]+)*$'
	
	line_id=0
	for str in aSentence:
		
		#print (str)
		
		match_token = re.match(token_line_pattern,str)
		match_lemma = re.match(lemma_line_pattern,str)
		
		if match_token:
			line_id+=1
			sentence_dict['lines'][line_id] = {}
			sentence_dict['lines'][line_id]['type'] = 'token'
			sentence_dict['lines'][line_id]['info'] = {}
			sentence_dict['lines'][line_id]['info']['analys'] = {}
			sentence_dict['lines'][line_id]['info']['analys']['lemma']=[]
			sentence_dict['lines'][line_id]['info']['analys']['case']=[]
			sentence_dict['lines'][line_id]['info']['analys']['morf']=[]
			sentence_dict['lines'][line_id]['info']['analys']['pos']=[]
			sentence_dict['lines'][line_id]['info']['analys']['function']=[]
			sentence_dict['lines'][line_id]['info']['analys']['relation']=[]
			sentence_dict['lines'][line_id]['info']['token'] = match_token.group(1)
		elif match_lemma:
			#print (line_id, "\tlemma:\t", match_lemma.group(1))
			#print (line_id, "\tmorf:\t", match_lemma.group(2))
			#print (line_id, "\tfunction:\t", match_lemma.group(3))
			#print (line_id, "\tref:\t", match_lemma.group(4))
			lemma = match_lemma.group(1).strip()
			morf = match_lemma.group(2).strip()
			function = match_lemma.group(3)
			if function:
				function=function.strip()
			else:
				function=''
			relation = match_lemma.group(4).strip()
			
			match_morf = re.match(morf_pattern,morf)
			if  match_morf:
				#print (match_morf.groups())
				if match_morf.group(2):
					case = match_morf.group(2)
				else:
					case = ''
				
				pos =  match_morf.group(3)
				if (match_morf.group(4)):
					morf =   match_morf.group(4).strip()
				else:
					morf = ''
				
			else:
				eprint (bColors.colors[0]+'UNABLE TO PARSE MORF INFO!'+bColors.ENDC,morf)
				case = ''
				pos =  '__'
			
			sentence_dict['lines'][line_id]['info']['analys']['lemma'].append(lemma)
			sentence_dict['lines'][line_id]['info']['analys']['case'].append(case)
			sentence_dict['lines'][line_id]['info']['analys']['morf'].append(morf)
			sentence_dict['lines'][line_id]['info']['analys']['pos'].append(pos)
			sentence_dict['lines'][line_id]['info']['analys']['function'].append(function)
			sentence_dict['lines'][line_id]['info']['analys']['relation'].append(relation)
		else:
			eprint (bColors.colors[0]+'INVALID LINE FORMAT!'+bColors.ENDC,str)
			eprint (aSentence)


		#pp.pprint()
		
	return sentence_dict
	




######### command line args and default values ##########
file_pos =0
tag_nr = 0
rel_nr = 0
tokens_count = 0
file_count = 0
max_tokens = 500




parser = ArgumentParser(description="description")
parser.add_argument("-i", dest="i_filename", required=True,
	help="Input file name", metavar="FILE")


args = parser.parse_args()

out_filename = re.sub("\.[^\.]*$", '', args.i_filename)
out_filename = re.sub("^.*\/", '', out_filename)



stdin = True
if args.i_filename :
	stdin = False
	eprint ('Read from FILE:', args.i_filename)



default_format = 'inforem'

######### program logic ########


if __name__ == '__main__':
	if (sys.stdout.encoding is None):
		eprint ("please set python env PYTHONIOENCODING=UTF-8, example: export PYTHONIOENCODING=UTF-8, when write to stdout.")
		exit(1)


missing_morf = {}

if args.i_filename:
	try:
		f = codecs.open(args.i_filename, "r", "utf-8")
	except IOError:
		eprint(bColors.colors[0]+'Cannot open'+bColors.ENDC, args.i_filename)
		exit();


#hetkel siin, failid, kuhu kirjutatakse tulemus
#hiljem peab mujale t6stma, sest yhest sisendfailist luuakse mitu v2ljundfaili
open_output_files()

iter=0
arr_sentence=[]
in_sentence=False
with f as fp:
	for line in fp:
		line = line.strip()
		if line=='':
			continue
		elif line=='"<s>"' and in_sentence==False:
			iter +=1
			in_sentence=True
		elif line=='"</s>"' and in_sentence==True:
	
			in_sentence=False
			sentence = makeDictFromArray (arr_sentence)
			transform_ann(sentence)
			arr_sentence = []
			
			
		else:
			arr_sentence.append(line)

		

f_out_txt.close()
f_out_ann.close()
