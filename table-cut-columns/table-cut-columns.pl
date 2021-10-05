#!/usr/bin/env perl

use Modern::Perl;
use autodie;
use Getopt::Long::Descriptive;
use IO::File;

# Define and read command line options
my ($opt, $usage) = describe_options(
	"Usage: %c %o",
	["Cut selected columns from table. Assumes that the input file has a header line with column names"],
	[],
	['table=s', 'Input table file. Reads from STDIN if "-"'],
	['col-name=s@', 'Column name; selects multiple columns if used multiple times'],
	['col=s@', 'Column name', {hidden => 1}], # for backwards compatibility
	['col-name-as=s@', 'Optional output column name. Equal times and same order as col-name.'],
	['sep=s', 'Column separator character [Default => "\t"]', {default => "\t"}],
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
	die "Mandatory parameter \'col-name\' missing\n";
}

my @out_col_names;
if (defined $opt->col_name_as) {
	if (@{$opt->col_name} != @{$opt->col_name_as}) {
		print STDERR "Error: col-name and col-name-as must be given equal times.\n";
		print($usage->text);
		exit 1;
	}
	@out_col_names = @{$opt->col_name_as};
}

my $sep = $opt->sep;

my $IN = filehandle_for($opt->table);
my $header = $IN->getline();
chomp $header;

my @colnames = split(/$sep/, $header);
my @col_indices;
foreach my $col_name (@{$opt->col_name}) {
	my $idx = column_name_to_idx(\@colnames, $col_name);
	die "Error: cannot find column $col_name\n" if not defined $idx;
	push @col_indices, $idx;
}

if (!defined $opt->col_name_as) {
	@out_col_names = @colnames[@col_indices];
}
say join($sep, @out_col_names);
while (my $line = $IN->getline) {
	chomp $line;
	my @splitline = split(/$sep/, $line);
	say join($sep, @splitline[@col_indices]);
}

exit;

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
	return undef
}
