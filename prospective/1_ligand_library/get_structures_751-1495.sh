for i in {751..1495};
do
    echo "Fetching $i"
    curl --remote-time --fail --create-dirs -o molport/${i}.db2.gz http://zinc.docking.org/catalogs/molport/protomers/subsets/for-sale.db2.gz?page=${i};
done
