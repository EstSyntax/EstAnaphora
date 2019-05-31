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

## ChangeLog / Muudatused

- May 2019 Added/lisati 100,000 words/sõna


