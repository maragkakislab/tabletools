#!/usr/bin/env perl

use Modern::Perl;
use autodie;
use Getopt::Long::Descriptive;

# Define and read command line options
my ($opt, $usage) = describe_options(
	"Usage: %c %o",
	["Join 2 tables based on key columns. The output table will"],
	["have the key columns plus value columns from each of the tables."],
	["Value columns will be named based on the -value1-as and -value2-as option in the same"],
	["order as the -table option."],
	[],
	['type' => hidden => { one_of => [
			[ 'inner' => 'inner join (default)' ],
			[ 'left' => 'left join' ],
			[ 'right' => 'right join' ],
			[ 'full' => 'full join' ],
		], default => 'inner' }
	],
	['table1=s',
		'TSV file. Use - for STDIN',
		{ required => 1}],
	['key1=s@',
		'Key column name for table 1. '.
		'If given multiple times a composite key is used.',
		{ required => 1}],
	['value1=s@',
		'Value column names for table 1 - can be given multiple times',
	],
	['value1-as=s@',
		'Name of the value columns of table 1 in the output. '.
		'Must be given as many times as the -value1 option.',
	],
	['suffix1=s',
		'Suffix to be added to value1 column names'
	],
	['table2=s',
		'TSV file.',
		{ required => 1}],
	['key2=s@',
		'Key column name for table 2. '.
		'If given multiple times a composite key is used. '.
		'If not provided, key1 is used. '.
		'If provided, key-as must be provided.'],
	['value2=s@',
		'Value column names for table 2 - can be given multiple times.',
	],
	['value2-as=s@',
		'Name of the value columns of table 2 in the output. '.
		'Must be given as many times as the -value2 option.',
	],
	['suffix2=s',
		'Suffix to be added to value2 column names'
	],
	['key-as=s@',
		'Name for output columns of keys. '.
		'Must be provided equal number of times as key1, key2.'],
	['verbose|v', 'Print progress'],
	['help|h', 'Print usage and exit',
		{shortcircuit => 1}],
);
print($usage->text), exit if $opt->help;

warn "opening input tables\n" if $opt->verbose;
my $IN1 = filehandle_for($opt->table1);
my $header1 = $IN1->getline();
chomp $header1;
my $IN2 = filehandle_for($opt->table2);
my $header2 = $IN2->getline();
chomp $header2;

warn "validating key name parameters\n" if $opt->verbose;
if (!defined $opt->key2) {
	$opt->{"key2"} = $opt->key1;
	$opt->{"key_as"} = $opt->key1;
}
elsif (!defined $opt->key_as) {
	print STDERR "Error: if key2 provided, key-as must be provided.\n";
	print($usage->text);
	exit 1;
}
elsif (@{$opt->key1} != @{$opt->key2} or @{$opt->key1} != @{$opt->key_as}) {
	print STDERR "Error: key1, key2 and key-as must be provided equal times.\n";
	print($usage->text);
	exit 1;
}

if (!defined $opt->value1) {
	warn "guessing value columns for table1\n" if $opt->verbose;
	$opt->{"value1"} = extract_all_value_columns_from_header($header1, $opt->key1);
}
if (!defined $opt->value2) {
	warn "guessing value columns for table2\n" if $opt->verbose;
	$opt->{"value2"} = extract_all_value_columns_from_header($header2, $opt->key2);
}

warn "validating value/name parameters\n" if $opt->verbose;
if (!defined $opt->value1_as) {
	$opt->{"value1_as"} = $opt->value1;
}
if (!defined $opt->value2_as) {
	$opt->{"value2_as"} = $opt->value2;
}
if (@{$opt->value1} != @{$opt->value1_as} or @{$opt->value2} != @{$opt->value2_as}){
	print STDERR "Error: number of names and number of values differ.\n";
	warn @{$opt->value1}."\t".@{$opt->value1_as}."\t".@{$opt->value2}."\t".@{$opt->value2_as}."\n";
	print($usage->text);
	exit 1;
}
if (defined $opt->suffix1) {
	warn "adding suffix1\n" if $opt->verbose;
	$opt->{"value1_as"} = [map{$_.$opt->suffix1} @{$opt->{"value1_as"}}];
}
if (defined $opt->suffix2) {
	warn "adding suffix2\n" if $opt->verbose;
	$opt->{"value2_as"} = [map{$_.$opt->suffix2} @{$opt->{"value2_as"}}];
}

warn "reading table 1\n" if $opt->verbose;
my $data1 = read_table($IN1, $header1, $opt->key1, $opt->value1);
close $IN1;

warn "reading table 2\n" if $opt->verbose;
my $data2 = read_table($IN2, $header2, $opt->key2, $opt->value2);
close $IN2;

warn "joining tables\n" if $opt->verbose;
say join("\t", @{$opt->key_as}, @{$opt->value1_as}, @{$opt->value2_as});

if ($opt->type eq 'inner'){ #only for keys that exist in both
	foreach my $key (keys %{$data1}) {
		if (exists $$data2{$key}){
			say join("\t", $key, @{$data1->{$key}}, @{$data2->{$key}});
		}
	}
}
elsif ($opt->type eq 'left'){ #for all lines on table 1
	foreach my $key (keys %{$data1}) {
		if (!exists $$data2{$key}){
			say join("\t", $key, @{$data1->{$key}}, ("NA") x scalar(@{$opt->value2}));
		}
		else {
			say join("\t", $key, @{$data1->{$key}}, @{$data2->{$key}});
		}
	}
}
elsif ($opt->type eq 'right'){ #for all lines on table 1
	foreach my $key (keys %{$data2}) {
		if (!exists $$data1{$key}){
			say join("\t", $key, ("NA") x scalar(@{$opt->value1}), @{$data2->{$key}});
		}
		else {
			say join("\t", $key, @{$data1->{$key}}, @{$data2->{$key}});
		}
	}
}
elsif ($opt->type eq 'full'){ #for all lines
	my %allkeys;
	foreach my $k (keys %{$data1}){
		$allkeys{$k} = 1;
	}
	foreach my $k (keys %{$data2}){
		$allkeys{$k} = 1;
	}
	foreach my $key (keys %allkeys){
		if (!exists $$data1{$key}){
			say join("\t", $key, ("NA") x scalar(@{$opt->value1}), @{$data2->{$key}});
		}
		elsif (!exists $$data2{$key}){
			say join("\t", $key, @{$data1->{$key}}, ("NA") x scalar(@{$opt->value2}));
		}
		else {
			say join("\t", $key, @{$data1->{$key}}, @{$data2->{$key}});
		}
	}
}

exit;

sub extract_all_value_columns_from_header {
	my ($header, $key_names) = @_;
	
	my $sep = "\t";
	my @colnames = split(/$sep/, $header);
	
	my @val_names;
	COLNAME: foreach my $colname (@colnames) {
		foreach my $key (@{$key_names}) {
			if ($key eq $colname) {
				next COLNAME;
			}
		}
		push @val_names, $colname; 
	}
	return \@val_names;
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

sub read_table {
	my ($IN, $header, $key_names, $value_names) = @_;
	
	my $sep = "\t";
	my @colnames = split(/$sep/, $header);

	my @key_indices;
	my @val_indices;
	foreach my $key_name (@$key_names) {
		my $idx = column_name_to_idx(\@colnames, $key_name);
		die "Error: cannot find column $key_name\n" if not defined $idx;
		push @key_indices, $idx;
	}
	foreach my $value_name (@$value_names){
		my $idx = column_name_to_idx(\@colnames, $value_name);
		die "Error: cannot find column $value_name\n" if not defined $idx;
		push @val_indices, $idx;
	}
	
	my %data;
	while (my $line = $IN->getline) {
		chomp $line;
		my @splitline = split(/$sep/, $line);
		my $key = join($sep, @splitline[@key_indices]);
		if (exists $data{$key}) {
			die "Error: duplicate key $key found\n";
		}
		$data{$key} = [@splitline[@val_indices]];
	}

	return \%data;
}

sub column_name_to_idx {
	my ($names, $name) = @_;

	for (my $i=0; $i<@$names; $i++) {
		return $i if $name eq $names->[$i];
	}
	return undef;
}
