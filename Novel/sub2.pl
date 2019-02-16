use warnings;
use strict;
use WWW::Mechanize;

sub main{
    my $mech = WWW::Mechanize->new();
    for my $i (1..32){
        my $filepath = &getfile($i);
        print $filepath, "\n";
        my $tempfile = "C:\\Users\\user\\Desktop\\novel\\Novel$i.txt";
        $mech->get($filepath, ':content_file' => $tempfile); #Encoding problem here. To be fixed.
    }
}

sub getfile{
    my ($num) = @_;
    if ($num < 10 and $num > 0){
        $num = "00$num";
    } elsif ($num < 100){
        $num = "0$num";
    } else {
        $num = "$num";
    }
    my $filename = 'http://www.geocities.jp/louisng888jp/yuen/';
    return "$filename$num.txt";
}
&main;
