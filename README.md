Miscellaneous scripts for manipulating table files (files that have column format and a header line with column names).

# Installation guide
```
mkdir ~/tools
cd ~/tools
git clone https://github.com/maragkakislab/tabletools.git

# Install dependencies
cpan App:cpanminus
cpanm Modern::Perl
cpanm GenOO

# Check if your bin is in your $PATH
echo $PATH

# Create the bin directory if not already created.
mkdir ~/bin

# Create symbolic links of the scripts to the bin.
ln -s ~/tools/tabletools/table-cat/table-cat.pl ~/bin/table-cat
ln -s ~/tools/tabletools/table-join/table-join.pl ~/bin/table-join
ln -s ~/tools/tabletools/table-paste-col/table-paste-col.pl ~/bin/table-paste-col
ln -s ~/tools/tabletools/table-cut-columns/table-cut-columns.pl ~/bin/table-cut-columns
ln -s ~/tools/tabletools/table-merge-columns/table-merge-columns.pl ~/bin/table-merge-columns
```

