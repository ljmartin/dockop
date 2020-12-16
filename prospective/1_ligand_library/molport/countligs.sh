for i in {1..750};
do
    gunzip -c $i.db2.gz > temp
    echo `grep 'ZINC' temp | wc`
    
done
