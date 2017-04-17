COUNTER=0
for BULKSUPPRESSOR in "0.006" "0.012"
do
    for APPLIEDPOTENTIAL in "-0.16" "-0.18" "-0.20" "-0.22" "-0.24"
    do
        smt run -t provisional2 provisional/params.json totalSteps=2000 appliedPotential="${APPLIEDPOTENTIAL}" bulkSuppressor="${BULKSUPPRESSOR}" > out.${COUNTER} 2>&1 &
        let COUNTER++
    done
done
