#!/usr/bin/env perl

use Modern::Perl;
use autodie;
use Getopt::Long::Descriptive;

# Define and read command line options
my ($opt, $usage) = describe_options(
	"Usage: %c %o",
	["Print the input table adding a new column with a constant value."],
	[],
	['table=s',
		'Input tab separated table file. Reads from STDIN if -'],
	['ifile=s',
		'Input file name. Reads from STDIN if -', {hidden => 1}], # for backwards compatibility
	['col-name=s',
		'Name for new column. Assumes input file already has a header line'],
	['col-val=s',
		'Value for new column'],
	['help|h',
		'Print usage and exit', {shortcircuit => 1}],
);
print($usage->text), exit if $opt->help;

my $delim = "\t";

if (defined $opt->ifile) {
	if (!defined $opt->table) {
		$opt->{'table'} = $opt->ifile
	} else {
		die "Cannot specify both \'table\' and \'ifile\' parameters\n";
	}
}
if (!defined $opt->table) {
	die "Mandatory parameter \'table\' missing\n";
}

my $IN = filehandle_for($opt->table);

if (defined $opt->col_name) {
	my $header = $IN->getline();
	print $opt->col_name . $delim . $header;
}

while (my $line = $IN->getline) {
	print $opt->col_val . $delim . $line;
}
$IN->close();

exit;

sub filehandle_for {
	my ($file) = @_;

	if ($file eq '-'){
		open(my $IN, "<-");
		return $IN;
	}
	else {
		open(my $IN, "<", $file);
		return $IN
	}
}
