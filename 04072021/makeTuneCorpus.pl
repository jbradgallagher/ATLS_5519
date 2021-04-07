open(FILE, "$ARGV[0]");
@lines = <FILE>;
close(FILE);

$rnum = int($ARGV[1]);

$rand = int(rand($rnum)) + 25;
$istart = 0;
$cnt = 0;

$dnum = sprintf("%04d", $cnt);
$ofile = "ashbery_"."$dnum".".txt";

open(OUT, ">$ofile");
print OUT "<|startoftext|>\n";
for($i=0; $i<=$#lines; $i++) {
     if($i < $istart + $rand) {
	print OUT "$lines[$i]";
     } else {
	print OUT "$lines[$i]";
	print OUT "<|endoftext|>\n";
	close(OUT);
	$cnt++;
	$dnum = sprintf("%04d", $cnt);
	$ofile = "ashbery_"."$dnum".".txt";
	open(OUT, ">$ofile");
	print OUT "<|startoftext|>\n";
	$rand = int(rand($rnum)) + 25;
	$istart = $i;
    }
}
      
