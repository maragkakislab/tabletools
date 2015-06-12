#!/usr/bin/env perl

use Modern::Perl;
use autodie;
use Getopt::Long::Descriptive;


# Define and read command line options
my ($opt, $usage) = describe_options(
	"Usage: %c %o",
	["Join 2 or more tables based on key columns. The output table will"],
	["have the key columns plus one value column from each of the tables."],
	["Value columns will be named based on the -name option in the same"],
	["order as the -table option."],
	[],
	['table|t=s@',
		'tsv file. Use multiple times to specify multiple tables.',
		{required => 1}],
	['key|k=s@',
		'key column name (must be the same for all tables).'.
		'If given multiple times a composite key is used.',
		{ required => 1}],
	['value|l=s', 'value column name (must be the same for all tables).',
		{ required => 1}],
	['name|n=s@',
		'name of the value column in the output.'.
		'Must be given as many times as the -table option.',
		{required => 1}],
	['verbose|v', "print progress"],
	['help|h', 'print usage and exit',
		{shortcircuit => 1}],
);
print($usage->text), exit if $opt->help;

warn "reading tables\n" if $opt->verbose;
my @tables = map {read_table($_, $opt->key, $opt->value)} @{$opt->table};

warn "validating table sizes\n" if $opt->verbose;
for (my $i = 0; $i < @tables; $i++) {
	if (keys %{$tables[$i]} != keys %{$tables[$i-1]}) {
		die "Error: table sizes differ. Check input tables.\n";
	}
}

warn "joining tables\n" if $opt->verbose;
say join("\t", "key", @{$opt->name});
foreach my $key (keys %{$tables[0]}) {
	my @values = map {$_->{$key}} @tables;
	say join("\t", $key, @values);
}

######################################################################
sub read_table {
	my ($file, $key_names, $value_name) = @_;

	open(my $IN, "<", $file);
	my $header = $IN->getline;
	chomp $header;
	my @colnames = split(/\t/, $header);

	my @key_indices;
	foreach my $key_name (@$key_names) {
		my $idx = column_name_to_idx(\@colnames, $key_name);
		die "Error: cannot find column $key_name\n" if not defined $idx;
		push @key_indices, $idx;
	}
	my $value_idx = column_name_to_idx(\@colnames, $value_name);
	die "Error: cannot find column $value_name\n" if not defined $value_idx;

	my %data;
	while (my $line = $IN->getline) {
		chomp $line;
		my @splitline = split(/\t/, $line);
		my $key = join('|', @splitline[@key_indices]);
		if (exists $data{$key}) {
			die "Error: duplicate key $key found\n";
		}
		$data{$key} = $splitline[$value_idx];
	}
	$IN->close;

	return \%data;
}

sub column_name_to_idx {
	my ($names, $name) = @_;

	for (my $i=0; $i<@$names; $i++) {
		return $i if $name eq $names->[$i];
	}
	return undef;
}
