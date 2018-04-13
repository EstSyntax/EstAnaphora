#!/usr/bin/perl -w

# Programm puudepanga failis asesõnade viitealuste märgendmaiseks
# Puudepanga failist (antakse ette lipuga -f) teeb brati märgendaja jaoks 2 faili: sõnavormirida läheb txt-lõpuga faili, asesõnad märgenditega (P pers, P dem, P int rel lähevad ann-faili kui sidumist ootavad sõnad.
# Brat-märgendaja töötab lühemate failidega paremini, mistõttu tehakse failidest 300-lauselised tükid. 
# Juba märgendatud failid seob inforem-failiks tagasi programm brat2inforem
# Kaili Müürisep 2016

use strict;
use Getopt::Std;
use utf8;

my %option;
my $path;
my $output1;
my $output2;
my $ind;
my $target;
my $tind;
my $line;
my $end;

my $lno;
my $fno;

$lno=0;
$fno=1;

getopts("f:", \%option);

#ava sisendfail

if ($option{f}) { 
    $path= $option{f}; 
    if ($path =~ /(\S+)\.+(\S+)$/) {
      $output1 = $1 . "." .$fno . ".txt";
      $output2 = $1 . "." .$fno . ".ann";
    }
    else {
      die "Ebakorrektne failinimi\n";
    }  
}

#ava textfail
#ava annfail
print "Loetakse failist $path, kirjutatakse $output1 ja $output2\n";

    open(INPUT,"<:utf8", $path)
        || die "Cant open $path for input: $!\n";
    open(TXT,">:utf8", $output1) 
        || die "Cant open $output1 for output: $!\n";
    open(ANN,">:utf8", $output2) 
        || die "Cant open $output2 for output: $!\n";
        
    select(TXT);

$ind = -1;   
$end=0;
$target="";
$tind=1;
    
#loe sisendist sõnavorme
while($line=<INPUT>){
#arvuta index
  chomp($line);   
  if ($line =~ /^\s*$/){next;}
   if ($lno==300) {
     close(TXT);
     close(ANN);
     $fno++;
     $output1 =~ s/\.\d+\.txt/.$fno.txt/;
     $output2 =~ s/\.\d+\.ann/.$fno.ann/;
     open(TXT,">:utf8", $output1) 
        || die "Cant open $output1 for output: $!\n";
     open(ANN,">:utf8", $output2) 
        || die "Cant open $output2 for output: $!\n";
        
     select(TXT);
     $lno=0; $ind= -1; $tind=0;  $target="";
  }  
  
  if ($line =~ /^\"<s>\".*$/){ next; }
  if ($line =~ /^\"<\/s>\".*$/){ print "\n"; $ind++; $lno++; next; }
  if ($line =~ /^\"<(.*)>\".*$/) { 
#trüki textfaili
   $ind= $ind + length($target) + 1;
   print "$1 "; 
   $target=$1;
  }
#kui on tõlgendusrida
  if ($line =~ /^\s+/) {
# kui on asesõna
   if (($line =~ / P pers /)||($line =~ /\"see\".* P dem /) || ($line =~ / P inter rel /)){
    #  trüki annfaili
      $end=$ind+length($target);
      print ANN "T$tind\tPronoomen $ind $end\t$target\n";
      $tind++;
    } 
  }
}

#pane failid kinni
close(INPUT);
close(TXT);
close(ANN);
