#!/usr/bin/env perl

use Modern::Perl;
use autodie;
use Getopt::Long::Descriptive;

# Define and read command line options
my ($opt, $usage) = describe_options(
	"Usage: %c %o",
	["Merge the values of given columns using a delimiter"],
	[],
	['table=s',
		'TSV file. Use - for STDIN',
		{required => 1}],
	['col=s@',
		'Column name.'.
		'Use multiple times to specify multiple columns.',
		{required => 1}],
	['col-as=s',
		'Name for output column with merged values.',
	],
	['delim=s',
		'Delimiter for merging columns [Default: | ]',
		{default => '|'}],
	['verbose|v', 'Print progress'],
	['help|h', 'Print usage and exit',
		{shortcircuit => 1}],
);
print($usage->text), exit if $opt->help;

my $sep = "\t";

warn "opening input table\n" if $opt->verbose;
my $IN = filehandle_for($opt->table);
my $header = $IN->getline();
chomp $header;

warn "validating output column name\n" if $opt->verbose;
if (!defined $opt->col_as) {
	$opt->{"col_as"} = join($opt->delim, @{$opt->col});
}

my @colnames = split(/$sep/, $header);
my @col_indices;
foreach my $col_name (@{$opt->col}) {
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

	if ($file eq '-'){
		open(my $IN, "<-");
		return $IN;
	}
	else {
		open(my $IN, "<", $file);
		return $IN
	}
}


sub column_name_to_idx {
	my ($names, $name) = @_;

	for (my $i=0; $i<@$names; $i++) {
		return $i if $name eq $names->[$i];
	}
	return undef;
}
