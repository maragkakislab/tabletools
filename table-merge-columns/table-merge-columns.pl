#!/usr/bin/env perl

use Modern::Perl;
use autodie;
use Getopt::Long::Descriptive;
use IO::File;

# Define and read command line options
my ($opt, $usage) = describe_options(
	"Usage: %c %o",
	["Merge the values of given columns using a delimiter. Assumes that the input file has a header line with column names"],
	[],
	['table=s', 'Input table file; reads from STDIN if "-"', {required => 1}],
	['col-name=s@', 'Column name; selects multiple columns if used multiple times.'],
	['col=s@', 'Column name', {hidden => 1}], # for backwards compatibility
	['col-as=s', 'Name for the output column with merged values', ],
	['delim=s', 'Delimiter character for merging columns [Default: "|"]', {default => '|'}],
	['sep=s', 'Column separator character [Default => "\t" ]', {default => "\t"}],
	['verbose|v', 'Print progress'],
	['help|h', 'Print usage and exit', {shortcircuit => 1}],
);
print($usage->text), exit if $opt->help;

# For backwards compatibility: handles the deprecated col option.
if (defined $opt->col) {
	if (defined $opt->col_name) {
		die "Cannot specify both \'col\' and \'col-name\' parameters\n";
	}
	$opt->{'col_name'} = $opt->col
}
if (!defined $opt->col_name) {
	die "Mandatory parameter \'table\' missing\n";
}

my $sep = $opt->sep;

warn "opening input table\n" if $opt->verbose;
my $IN = filehandle_for($opt->table);
my $header = $IN->getline();
chomp $header;

warn "validating output column name\n" if $opt->verbose;
if (!defined $opt->col_as) {
	$opt->{"col_as"} = join($opt->delim, @{$opt->col_name});
}

my @colnames = split(/$sep/, $header);
my @col_indices;
foreach my $col_name (@{$opt->col_name}) {
	my $idx = column_name_to_idx(\@colnames, $col_name);
	die "Error: cannot find column $col_name\n" if not defined $idx;
	push @col_indices, $idx;
}

my @val_indices;
for (my $i = 0; $i < @colnames; $i++){
	next if value_in($i, \@col_indices);
	push @val_indices, $i;
}

print join($sep, $opt->col_as, @colnames[@val_indices])."\n";
while (my $line = $IN->getline) {
	chomp $line;
	my @splitline = split(/$sep/, $line);
	print join($sep, join($opt->delim, @splitline[@col_indices]), @splitline[@val_indices])."\n";
}

exit;

sub value_in {
	my ($value, $arrayref) = @_;
	foreach my $v (@{$arrayref}){
		if ($value == $v){return 1;}
	}
	return 0;
}

sub filehandle_for {
	my ($file) = @_;

	my $f;
	if ($file eq '-'){
		$f = IO::File->new("<-") or die "cannot open stdin: $!\n";
	}
	else {
		$f = IO::File->new($file, "<") or die "cannot open file $file: $!\n";
	}
	return $f;
}

sub column_name_to_idx {
	my ($names, $name) = @_;

	for (my $i=0; $i<@$names; $i++) {
		return $i if $name eq $names->[$i];
	}
}
