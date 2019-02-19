use warnings;
use strict;
use WWW::Mechanize;
sub main{
    my $mech = WWW::Mechanize->new();
    for my $i (1..32){ #There are 32 books
        my $filepath = &getfile($i);
        print $filepath, "\n";
        my $tempfile = "C:\\Users\\user\\Desktop\\novel\\Novel$i.txt"; #Path for novels
        $mech->get($filepath);
        $mech->save_content($tempfile, binmode=> ':raw', decoded_by_headers => 1);
        #$mech->get($filepath, ':content_file' => $tempfile); #Use this code will cause encoding problem.
    }
}
sub getfile{
    my ($num) = @_;
    if ($num > 0 && $num < 100){
        $num = substr "00$num", -3;
    } else {
        print "Wrong index! Failure on getting file.";
        exit;
    }
    my $filename = 'http://www.geocities.jp/louisng888jp/yuen/'; #Website of novels
    return "$filename$num.txt";
}
&main;
