import os
import subprocess
import psutil
import time
import csv

datasets = {
    'RV11':[[],[]], 'RV12':[[],[]], 'RV20':[[],[]], 'RV30':[[],[]], 
    'RV40':[[]], 'RV50':[[],[]], 'covid-19':[]
           }
for ref in datasets.keys():
    if ref != 'covid-19':
        bbr = os.listdir(f"dataset/BAliBASE_R1-5/bb3_release/{ref}/")
        for file in bbr:            
            if file[-3:] == 'tfa':
                if file[:3] == 'BBS':
                    datasets[ref][1].append(file)
                else:
                    datasets[ref][0].append(file)
    else:
        datasets[ref] = os.listdir(f"dataset/{ref}/")

path = "/home/sam7/Downloads/CS466/algorithm"

def benchmark(command):
    start_time = time.time()
    
    # Start the subprocess and monitor its memory usage
    process = subprocess.Popen(command, shell=True)
    peak_memory = 0
    
    try:
        while process.poll() is None:
            # Get the current memory info of the subprocess
            current_memory = psutil.Process(process.pid).memory_info().rss
            peak_memory = max(peak_memory, current_memory)
            time.sleep(0.1)  # Polling interval
    except psutil.NoSuchProcess:
        pass  # Process has already terminated

    end_time = time.time()
    total_time = end_time - start_time
    
    return total_time, peak_memory

def run_performance_test(data, writer):    
    input_file = f"datasets/{data}"
    base_name = data.split('.')[0]
    clustalw_cmd = f"{path}/clustalw2 -INFILE={input_file} -OUTFILE=aligned/clustalw/clustalw_{base_name}.aln -quiet"
    t_coffee_cmd = f"{path}/t_coffee -seq {input_file} -output aln -outfile aligned/t_coffee/tcoffee_{base_name}.aln -quiet"
    muscle_cmd = f"{path}/muscle -align {input_file} -output aligned/muscle/muscle_{base_name}.afa -quiet"
    
    clustalw_time, clustalw_memory = benchmark(clustalw_cmd)
    tcoffee_time, tcoffee_memory = benchmark(t_coffee_cmd)
    muscle_time, muscle_memory = benchmark(muscle_cmd)

    writer.writerow([data, clustalw_time, clustalw_memory, muscle_time, muscle_memory, tcoffee_time, tcoffee_memory])

# Test on BALIBASE
bb_dataset_names = [
    'RV11_full', 'RV11_homo', 
    'RV12_full', 'RV12_homo', 
    'RV20_full', 'RV20_homo',
    'RV30_full', 'RV30_homo',
    'RV40_full',
    'RV50_full', 'RV50_homo'
    ]

bb_datasets = [
    datasets['RV11'][0], datasets['RV11'][1],
    datasets['RV12'][0], datasets['RV12'][1],
    datasets['RV20'][0], datasets['RV20'][1],
    datasets['RV30'][0], datasets['RV30'][1],
    datasets['RV40'][0],
    datasets['RV50'][0], datasets['RV50'][1] 
    ]

for name, dataset in zip(bb_dataset_names, bb_datasets):
    with open(f'{name}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header row
        writer.writerow(["Dataset", "ClustalW_Time", "ClustalW_Memory",  "MUSCLE_Time", "MUSCLE_Memory", "T-Coffee_Time", "T-Coffee_Memory"])
        # Loop through each dataset and run the performance test
        for data in dataset:
            run_performance_test(data, writer)

# Test on Covid-19
rw_dataset = datasets['covid-19']
with open(f'covid-19.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Dataset", "ClustalW_Time", "ClustalW_Memory",  "MUSCLE_Time", "MUSCLE_Memory", "T-Coffee_Time", "T-Coffee_Memory"])
    for data in rw_dataset:
        run_performance_test(data, writer)