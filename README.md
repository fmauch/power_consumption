# Power consumption evaluation
A collection of utility scripts to make use of the el4000 data. 

## evaluate_data.py
Will create a report such as

```
Analyzing data from nas_data.csv
Average power consumption: 4.0439108803 W
Time passed: 88.8708333333 h
Total energy used: 8.62516637056 kWh
Estimated energy consumption in one year: 35.4489227767 kWh
Estimated annual costs: 8.35176620619 EUR
```

and will open an a graph with the power consumption over time afterwards.
The csv file could in theory come from anywhere and should have the format

```
timestamp,voltage,current,power_factor
2017-10-30 15:46,227.9,0.000,0.000
2017-10-30 15:47,227.3,1.950,0.170
...
```

## exract_data.sh
Extracts a csv-file as needed for the **evaluate_data.py** script from the binary data recorded from
an ELV el4000 device.

Note that for this you will have the [el4000](https://github.com/fmauch/el4000) package installed.

Then place the binary files inside **somedir/device_data** and call

```
./extract_data.sh somedir/device_data
```

This will create a **device_data.csv** file in the current directory.
