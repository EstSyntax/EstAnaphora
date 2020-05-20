# EstAnaphora

## Estonian Treebank annotated with coreference relations

This corpus containing ca 200,000 words of running text, is annotated for pronouns and their antecendents. 
There are 7800 annotated pronouns, among them 6000 are linked with their antecendents. The remaining 1800 pronouns have no clearly identifiable antecendent in text. 
Majority of the texts come from Estonian newspapers plus one scientific (medical) text, namely an issue of journal „Eesti Arst” (Estonian Doctor).

Programs to convert Estonian dependency trees (VISLCG format) to brat annotations and back (pronoomentykeldaja.pl and brat2inforem) are in the tools folder, authors Kaili Müürisep and Katrin Tsepelina.

## Anafooride suhtes märgendatud Eesti sõltuvuspuude pank

Anafooride suhtes märgendatud korpuses on praegu ca 200000 sõna mahus tekste, milles on u 7800 märgendatud asesõna, millest u 6000 on ühendatud oma viitealusega, ülejäänud tuhandel asesõnal viitealus tekstis puudub.
Tekstideks on ajalehetekstid ning üks teadustekst (ajakirja Eesti Arst 2004. aasta aastakäik). 
Märgendatud on järgmised asesõnad kõigis käändevormides ja nende viitealused:
- isikulised asesõnad (mina/ma, sina/sa, tema/ta, meie/me, teie/te, nemad/nad). Kokku on korpuses 3180 isikulist asesõna, neist 2576 on ühendatud viitealustega.
- näitav asesõna see esineb korpuses 2844 korral, neist 2132 korral on tal tekstis olemas viitealus.
- siduvad asesõnad kes ja mis esinevad tekstis kokku 1981 korda, neist 1611 juhul on neil olemas viitealus tekstis.

Programmid, mis teisendavad puudepanga formaadis faili brati märgendajale sobivaks ja tagasi (pronoomentykeldaja.pl ja brat2inforem) on kataloogis tools. Programmide autorid on Kaili Müürisep ja Katrin Tsepelina.

Korpuse formaat on Eesti keele sõltuvuspuude panga (EDT) oma, kuhu on lisatud asesõnade ja nende viitealuste märgendid. EDT märgendite kohta vt https://github.com/EstSyntax/EDT/blob/master/syntmargendus.pdf 

## UD Treebank with corefence relations

The same treebank, annotation is in the misc-field. Antecedents havebeen annotated with keyword Antecedent=Sent_No.Word_No,  and words referring to them have the keyword Coref and the address of the antecedent.
CorefType indicates whether the antecedent is a noun or a clause.

```
# sent_id = aja_ee199920_11
# text = "Tegutsesime nende võimaluste piirides, mis meile on antud," ütleb ta.
1	"	"	PUNCT	Z	_	2	punct	_	SpaceAfter=No
2	Tegutsesime	tegutsema	VERB	V	Mood=Ind|Number=Plur|Person=1|Tense=Past|VerbForm=Fin|Voice=Act	0	root	_	_
3	nende	see	DET	P	Case=Gen|Number=Plur|PronType=Dem	4	det	_	Coref=11.10|CorefType=Cl
4	võimaluste	võimalus	NOUN	S	Case=Gen|Number=Plur	5	nmod	_	Antecedent=11.4
5	piirides	piir	NOUN	S	Case=Ine|Number=Plur	2	obl	_	SpaceAfter=No
6	,	,	PUNCT	Z	_	10	punct	_	_
7	mis	mis	PRON	P	Case=Nom|Number=Plur|PronType=Int,Rel	10	obj	_	Coref=11.4|CorefType=N
8	meile	mina	PRON	P	Case=All|Number=Plur|Person=1|PronType=Prs	10	obl	_	Coref=8.2|CorefType=N
9	on	olema	AUX	V	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	10	aux	_	_
10	antud	andma	VERB	V	Tense=Past|VerbForm=Part|Voice=Pass	5	acl:relcl	_	Antecedent=11.10|SpaceAfter=No
11	,	,	PUNCT	Z	_	2	punct	_	SpaceAfter=No
12	"	"	PUNCT	Z	_	2	punct	_	_
13	ütleb	ütlema	VERB	V	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	2	parataxis	_	_
14	ta	tema	PRON	P	Case=Nom|Number=Sing|Person=3|PronType=Prs	13	nsubj	_	Coref=9.6|CorefType=N|SpaceAfter=No
15	.	.	PUNCT	Z	_	2	punct	_	_
```

## ChangeLog / Muudatused

- May 2019 Added/lisati 100,000 words/sõna
- May 2020 UD version of the treebank


