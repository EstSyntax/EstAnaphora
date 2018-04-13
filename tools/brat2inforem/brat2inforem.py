# -*- coding: utf-8 -*-
from __future__ import print_function

import glob
import os
import re
import sys
import codecs
import pprint

from argparse import ArgumentParser


class bColors:
	colors1 = (
		'\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m', '\033[1;37m', '\033[1;38m',
		'\033[1;39m'
	)
	
	style = {
		'bold': '\033[1m'
		, 'red': '\033[1;31m'
		, 'green': '\033[0;32m'
		, 'yellow': '\033[0;33m'
		, 'blue': '\033[0;34m'
		, 'endc': '\033[0m'
	}
	pattern_red = style['red'] + '%s' + style['endc']
	pattern_yellow = style['yellow'] + '%s' + style['endc']
	pattern_green = style['green'] + '%s' + style['endc']
	pattern_blue = style['blue'] + '%s' + style['endc']
	pattern_bold = style['bold'] + '%s' + style['endc']
	
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


if __name__ == '__main__':
	if sys.stdout.encoding is None:
		eprint(
			bColors.pattern_red % "please set python env PYTHONIOENCODING=UTF-8, example: export PYTHONIOENCODING=UTF-8, when write to stdout.")
		exit(1)




def findSpecialTokens(inforemfilename):
	specialTokens = {}
	special_token_line_pattern = '^"<(.+ .+)>"$'
	f_inforem = None
	try:
		f_inforem = codecs.open(inforemfilename, "r", "utf-8")
	except IOError:
		eprint(bColors.pattern_red % ('Cannot open ' + args.m_inforem))
		exit()
	with f_inforem as fp:
		for line in fp:
			line = line.strip()
			match_token = re.match(special_token_line_pattern, line)
			if match_token:
				specialTokens[match_token.group(1)] = match_token.group(1).replace(' ','+++')
	f_inforem.close()

	return specialTokens


# browse folder for files

def findInputFiles(path):
	# os.chdir(args.i_folder)
	eprint()
	eprint(bColors.pattern_bold % 'Searching for Brat files')
	a_ann_files = glob.glob(path + "*.ann")
	a_txt_files = glob.glob(path + "*.txt")
	
	# failide kogus ei klapi
	if len(a_ann_files) != len(a_txt_files):
		eprint("ann and txt files' count doesn't match")
		eprint(a_ann_files)
		eprint(a_txt_files)
		exit()
	
	# kontrollime, et failide nimed matchivad
	
	input_files = []
	for annfile in a_ann_files:
		filename = re.sub("\.[^\.]*$", '', annfile)
		if filename + '.txt' not in a_txt_files:
			eprint(filename + '.txt', "not found!")
			exit()
		else:
			input_files.append(filename)
	
	eprint('%d files found' % (len(a_ann_files) * 2))
	eprint("\n".join(a_ann_files))
	eprint("\n".join(a_txt_files))
	return input_files

def invert_dict(d):
    return dict([(v, k) for k, v in d.iteritems()])



# loetakse sisse brat text ja parsitakse vastavalt struktuurile
def readText(filename, d_text, d_pos, specialTokens):
	f_txt = None
	try:
		f_txt = codecs.open(filename + '.txt', "r", "utf-8")
	except IOError:
		eprint(bColors.pattern_red % ('Cannot open ' + filename + '.txt'))
		exit()
	# positions for relations
	
	txt_pos = 0
	global sentence_nr
	reversedSpecialTokens = invert_dict(specialTokens)
	with f_txt as fp_txt:
		for line in fp_txt:
			
			sentence_nr += 1
			sys.stderr.write('%d..' % sentence_nr)
			sys.stderr.flush()

			for key in specialTokens:
				pattern_spec_token = ''
				line = (re.sub('^%s '%key, specialTokens[key]+' ', line))
				line = (re.sub(' %s '%key, ' '+specialTokens[key]+' ', line))

			
			d_text[sentence_nr] = {}
			tokens = line.split()
			token_nr = 0
			for token in tokens:
				token_nr += 1
				if  token in reversedSpecialTokens:
					token = reversedSpecialTokens[token]
					
				d_text[sentence_nr][token_nr] = {}
				d_text[sentence_nr][token_nr]['token'] = token
				pos1 = str(txt_pos)
				pos2 = str(txt_pos + len(token))
				
				d_pos[pos1 + '_' + pos2] = [sentence_nr, token_nr]
				# print (token, txt_pos, txt_pos+len(token))
				txt_pos += len(token) + 1
			
			eol_space=re.match('^.*\s\n$',line)
			if eol_space:
				txt_pos += 1  # rea l6pus on yleliigne tyhik
	
	eprint()
	return [d_text, d_pos]


def parseAnn(filename, d_txt, d_pos):
	f_ann = None
	try:
		f_ann = codecs.open(filename + '.ann', "r", "utf-8")
	except IOError:
		eprint(bColors.pattern_red % ('Cannot open ' + filename + '.ann'))
		
		exit()
	
	tags = {}
	relation_pattern = '^(R\d+)\s([^\s]+)\sArg1\:(T[\d]+)\sArg2\:(T[\d]+)\s*$'
	tag_pattern = '^(T\d+)\s([^\s]+)\s([\d]+)\s([\d]+)\s(.+)\s*$'
	errors = []
	
	with f_ann as fp_ann:
		for line in fp_ann:
			sys.stderr.write('.')
			sys.stderr.flush()
			if line.strip() == '':
				continue
			if line[:1] == '#':
				errors.append("Ignored line:\t" + line.strip())
				continue
			elif line[:1] == 'T':
				match_tag = re.match(tag_pattern, line)
				if match_tag:
					tag = match_tag.group(1)
					ttype = match_tag.group(2)
					pos1 = match_tag.group(3)
					pos2 = match_tag.group(4)
					token = match_tag.group(5)
					
					dict_ann = {}
					dict_ann['token'] = token
					dict_ann['tag'] = tag
					dict_ann['type'] = ttype
					dict_ann['relations'] = {}
					dict_ann['pos'] = pos1 + '_' + pos2
					
					if pos1 + '_' + pos2 in d_pos:
						
						(key1, key2) = d_pos[pos1 + '_' + pos2]
						d_txt[key1][key2] = dict_ann
					else:
						errors.append("Invalid tag:\t" + line.strip())
					
					tags[tag] = pos1 + '_' + pos2
				
				
				else:
					
					errors.append("Invalid line in ann file:\t" + line.strip())
			
			elif line[:1] == 'R':
				match_relation = re.match(relation_pattern, line)
				if match_relation:
					# print (match_relation.groups())
					relation = match_relation.group(2)
					t1 = match_relation.group(3)
					t2 = match_relation.group(4)
					if t1 in tags and t2 in tags:
						pos1 = tags[t1]
						pos2 = tags[t2]
						if pos1 in d_pos and pos2 in d_pos:
							# print ('add',d_pos[pos1], d_pos[pos2])
							(key1, key2) = d_pos[pos1]
							(key3, key4) = d_pos[pos2]
							if 'relations' not in d_txt[key1][key2]:
								d_txt[key1][key2]['relations'] = {}
							if relation not in d_txt[key1][key2]['relations']:
								d_txt[key1][key2]['relations'][relation] = []
						
							d_txt[key1][key2]['relations'][relation].append(str(key3) + '.' + str(key4))
						else:
							errors.append("Invalid reference:\t" + line.strip())
					
					
					else:
						
						errors.append("Invalid reference:\t" + line.strip())
					
					# print ('t1', d_pos[tags[t1]])
					# print ('t2', d_pos[tags[t2]])
					# print (d_pos)
					# dict_ann[tags[t1]]['relations'][tags[t2]] = type
					# print (dict_ann[tags[t1]])
					# print (dict_ann[tags[t2]])
				
				else:
					errors.append("Invalid line in ann file:\t" + line.strip())
			else:
				errors.append("Invalid line in ann file:\t" + line.strip())
	
	eprint()
	for error in errors:
		eprint(bColors.pattern_blue % error)
	f_ann.close()
	return d_txt


def makeDictFromArray(aSentence):
	sentence_dict = {'lines': {}}
	# sentence_dict['lines'][lineid]['type'] == 'token'
	# dict['analys']={}
	#           dict['analys']['lemma']=[]
	#          dict['analys']['case']=[]
	#         dict['analys']['morf']=[]
	#        dict['analys']['lemma'].append('ERROR!!! '+line)
	#        dict['analys']['case'].append('')
	#        dict['analys']['morf'].append(line)
	
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
	token_line_pattern = '^"<(.+)>"$'
	lemma_line_pattern = '"(.+)" ([^\@]+)(\@.+)* #(\d+->\d+)$'
	morf_pattern = '^(L([^\s]+) )*([A-Z])([A-Za-z\d\s\?<>]+)*$'
	
	line_id = 0
	for s in aSentence:
		
		# print (s)
		
		match_token = re.match(token_line_pattern, s)
		match_lemma = re.match(lemma_line_pattern, s)
		
		if match_token:
			line_id += 1
			sentence_dict['lines'][line_id] = {}
			sentence_dict['lines'][line_id]['type'] = 'token'
			sentence_dict['lines'][line_id]['info'] = {}
			sentence_dict['lines'][line_id]['info']['analys'] = {}
			sentence_dict['lines'][line_id]['info']['analys']['lemma'] = []
			sentence_dict['lines'][line_id]['info']['analys']['case'] = []
			sentence_dict['lines'][line_id]['info']['analys']['morf'] = []
			sentence_dict['lines'][line_id]['info']['analys']['pos'] = []
			sentence_dict['lines'][line_id]['info']['analys']['function'] = []
			sentence_dict['lines'][line_id]['info']['analys']['relation'] = []
			sentence_dict['lines'][line_id]['info']['token'] = match_token.group(1)
		elif match_lemma:
			#eprint (line_id, "\tlemma:\t", match_lemma.group(1))
			#eprint (line_id, "\tmorf:\t", match_lemma.group(2))
			#eprint (line_id, "\tfunction:\t", match_lemma.group(3))
			#eprint (line_id, "\tref:\t", match_lemma.group(4))
			lemma = match_lemma.group(1).strip()
			morf = match_lemma.group(2).strip()
			function = match_lemma.group(3)
			if function:
				function = function.strip()
			else:
				function = ''
			relation = match_lemma.group(4).strip()
			
			match_morf = re.match(morf_pattern, morf)
			
			if match_morf:
				# print (match_morf.groups())
				if match_morf.group(2):
					case = match_morf.group(2)
				else:
					case = ''
				
				pos = match_morf.group(3)
				if match_morf.group(4):
					morf = match_morf.group(4).strip()
				else:
					morf = ''
			
			else:
				eprint()
				eprint(bColors.pattern_blue % 'Unable to parse morf info, line %d ' % line_id, morf)
				case = ''
				pos = '__'
			
			sentence_dict['lines'][line_id]['info']['analys']['lemma'].append(lemma)
			sentence_dict['lines'][line_id]['info']['analys']['case'].append(case)
			
			sentence_dict['lines'][line_id]['info']['analys']['morf'].append(morf)
			sentence_dict['lines'][line_id]['info']['analys']['pos'].append(pos)
			sentence_dict['lines'][line_id]['info']['analys']['function'].append(function)
			sentence_dict['lines'][line_id]['info']['analys']['relation'].append(relation)
		else:
			eprint()
			eprint(bColors.pattern_red % 'Unknown line format, line %d ' % line_id, s)
		# eprint (aSentence)
		
		
		# pp.pprint()
	
	return sentence_dict


def construct_line_inforem(dict_info):
	# print (dict_info)
	# Seoses    Seos+s //_H_ Sg Ine, //    Seose+s //_H_ Sg Ine, //    Seoses+0 //_H_ Sg Nom, //    seos+s //_S_ Sg Ine, //    seoses+0 //_K_ //
	return_line_pattern = '"<%s>"%s'
	morf_pattern1 = "\n\t" + '"%s" L%s %s%s%s%s%s%s'
	morf_pattern2 = "\n\t" + '"%s" %s %s%s%s%s%s'
	function_pattern = ' %s'
	relation_pattern = ' #%s'
	
	pattern_synt_rel = ' {%s:%s}'
	
	pattern_synt_type = ' {%s}'
	pattern_pos = '%s '
	synt_relations = ''
	if 'ann_relations' in dict_info:
		# synt_relations =   dict_info['ann_relations']
		for rel in dict_info['ann_relations']:
			synt_relations += (pattern_synt_rel % (rel, ','.join(dict_info['ann_relations'][rel])))
	
	synt_type = ''
	if 'ann_type' in dict_info:
		synt_type = pattern_synt_type % dict_info['ann_type']
	str_morf = ''
	
	for i, v in enumerate(dict_info['analys']['lemma']):
		lemma = v
		morf = dict_info['analys']['morf'][i]
		case = dict_info['analys']['case'][i]
		pos = dict_info['analys']['pos'][i]
		functions = ''
		relations = ''
		
		if dict_info['analys']['function'][i] != '':
			functions = function_pattern % (dict_info['analys']['function'][i])
		if dict_info['analys']['relation'][i] != '':
			relations = relation_pattern % (dict_info['analys']['relation'][i])
		if pos:
			pos = pattern_pos % pos
		if case != '':
			str_morf = str_morf + (morf_pattern1 % (lemma, case, pos, morf, functions, relations, synt_type, synt_relations))
		else:
			str_morf = str_morf + (morf_pattern2 % (lemma, pos, morf, functions, relations, synt_type, synt_relations))
		str_morf = str_morf.replace('  ',' ')
	
	return return_line_pattern % (dict_info['token'], str_morf)


def merge_info(sentence, ann_sentence):
	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(sentence)
	
	for line_id in sentence:
		
		if 'type' in ann_sentence[line_id] and sentence[line_id]['info']['token']==ann_sentence[line_id]['token']:
			sentence[line_id]['info']['ann_type'] = ann_sentence[line_id]['type']
		if 'relations' in ann_sentence[line_id] and sentence[line_id]['info']['token']==ann_sentence[line_id]['token']:
			sentence[line_id]['info']['ann_relations'] = ann_sentence[line_id]['relations']
	
	return sentence


##################################


parser = ArgumentParser(description="description")
parser.add_argument("-i", dest="i_path", required=True,
                    help="Brat files path and prefix", metavar="BratFolderName")



parser.add_argument("-o", dest="i_out", required=True,
                    help="Output file name", metavar="OutputFileName")

parser.add_argument("-m", dest="m_inforem", required=True,
                    help="Origin inforem file name", metavar="InforemFile")

args = parser.parse_args()

inputfiles = findInputFiles(args.i_path)

# if no files to parse
if inputfiles == []:
	exit()

# alustame failide sisse lugemist

sentence_nr = 0
d_txt = {}
d_txt_pos = {}


specialTokens = findSpecialTokens(args.m_inforem)

for filename in sorted(inputfiles):
	eprint()
	eprint(bColors.pattern_bold % 'Parsing %s.txt' % filename)
	[d_txt, d_txt_pos] = readText(filename, d_txt, d_txt_pos, specialTokens)
	eprint()
	eprint(bColors.pattern_bold % 'Parsing %s.ann' % filename)
	d_txt = parseAnn(filename, d_txt, d_txt_pos)

# merge inforem failiga

f_inforem = None
try:
	f_inforem = codecs.open(args.m_inforem, "r", "utf-8")
except IOError:
	eprint(bColors.pattern_red % ('Cannot open ' + args.m_inforem))
	exit()

f_out = None
# open output file
try:
	f_out = codecs.open(args.i_out, "w", "utf-8")
except IOError:
	eprint(bColors.pattern_red % ('Cannot open ' + args.i_out))
	exit()

eprint()
eprint(bColors.pattern_bold % 'Merging Brat and inforem info')
pp = pprint.PrettyPrinter(indent=4)
i = 0

arr_sentence = []
in_sentence = False
with f_inforem as fp:
	for line in fp:
		line = line.strip()
		if line == '':
			continue
		elif line == '"<s>"' and in_sentence == False:
			i += 1
			in_sentence = True
		
		
		elif line == '"</s>"' and in_sentence == True:
			
			in_sentence = False
			sentence = makeDictFromArray(arr_sentence)
			if i in d_txt:
				sentence['lines'] = merge_info(sentence['lines'], d_txt[i])
				sys.stderr.write(bColors.pattern_bold % ('%d..' % i))
			
			else:
				sys.stderr.write('%d..' % i)
			
			arr_sentence = []
			sys.stderr.flush()
			f_out.write("\"<s id=\"%d\">\"\n\n" % i)
			for line_id in sorted(sentence['lines']):
				f_out.write(construct_line_inforem(sentence['lines'][line_id]['info']) + "\n")
			f_out.write('"</s>"' + "\n" + "\n")
		
		else:
			arr_sentence.append(line)

f_out.close()

eprint()
eprint('Done.')
eprint('Result saved to %s' % args.i_out)

exit()
