#!/usr/bin/env perl

use Modern::Perl;
use autodie;
use Getopt::Long::Descriptive;

# Define and read command line options
my ($opt, $usage) = describe_options(
	"Usage: %c %o",
	["Cut selected columns from table"],
	[],
	['table=s',
		'TSV file. Use - for STDIN',
		{required => 1}],
	['col=s@',
		'Column name.'.
		'Use multiple times to specify multiple columns.',
		{required => 1}],
	['sep=s',
		'Table delimiter',
		{default => "\t"}
	],
	['verbose|v', 'Print progress'],
	['help|h', 'Print usage and exit',
		{shortcircuit => 1}],
);
print($usage->text), exit if $opt->help;

my $sep = $opt->sep;

warn "opening input table\n" if $opt->verbose;
my $IN = filehandle_for($opt->table);
my $header = $IN->getline();
chomp $header;

my @colnames = split(/$sep/, $header);
my @col_indices;
foreach my $col_name (@{$opt->col}) {
	my $idx = column_name_to_idx(\@colnames, $col_name);
	die "Error: cannot find column $col_name\n" if not defined $idx;
	push @col_indices, $idx;
}

print join($sep, @colnames[@col_indices])."\n";
while (my $line = $IN->getline) {
	chomp $line;
	my @splitline = split(/$sep/, $line);
	print join($sep, @splitline[@col_indices])."\n";
}

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


sub column_name_to_idx {
	my ($names, $name) = @_;

	for (my $i=0; $i<@$names; $i++) {
		return $i if $name eq $names->[$i];
	}
	return undef;
}
