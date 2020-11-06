from flask import Flask, flash, redirect, render_template,request, url_for
import math
import base64
import concurrent.futures
import itertools
import http.client
import time
from multiprocessing.pool import ThreadPool
from threading import Thread
import ast
import pandas as pd
import random
import os
import io
import math
import boto3
from io import StringIO
app = Flask(__name__)
app.secret_key = os.urandom(24)


def estimate_pi(args,result,index):
    shots = args[0]
    rate_reporting = args[1]
    id_process = args[2]
    c = http.client.HTTPSConnection("eqfupdwvib.execute-api.eu-west-2.amazonaws.com")
    json= '{"shots":"'+str(shots)+'","reporting_rate":"'+str(reporting_rate)+'","process_id":'+str(process_id)+'}'
    
    c.request("POST", "/default/pi_estimation", json)
    
    response = c.getresponse()
    data = ast.literal_eval(response.read().decode("utf-8").strip('"'))
    result[index] = data





@app.route('/get_user_data', methods=['POST','GET'])
def userpath():

    # number of Shots 
    shots = int(request.form["shots"])
    if shots%1000 != 0:
        flash('Error')
        return redirect(url_for('index'))

    
    service = request.form["service"] 

    #Reporting rate
    reporting_rate = int(request.form["reporting_rate"])
    if reporting_rate > shots:
        flash('Reporting rate should be less than shots')
        return redirect(url_for('index'))            

    #resources
    resources_count = int(request.form["resources"] )
    if resources_count > shots:
        flash('resources should be less than shots')
        return redirect(url_for('index'))  

    #Resource functionality
    ten_percent = int(0.1 * (shots/resources_count))
    result_1= [int(shots/resources_count)] * resources_count
    result_1[0] = result_1[0] + max(reporting_rate,ten_percent_s_by_r)
    result_1[-1] = result_1[-1] - max(reporting_rate,ten_percent_s_by_r)


    counter = itertools.count(0)
    processes = [[shots,reporting_rate,next(counter)] for shots in result_1]

    if service == 'Lambda':
        triplets = []
        start = time.time()

        pool = ThreadPool(processes=len(processes))


        threads = [None] * len(processes)
        results = [None] * len(processes)

        for i in range(len(threads)):
            threads[i] = Thread(target=estimate_pi, args=(processes[i], results, i))
            threads[i].start()

        # do some other stuff

        for i in range(len(threads)):
            threads[i].join()

   
                
      
        

        time_taken = time.time() - start

        total_list = [a for b in results for a in b]

        triple_table = pd.DataFrame(total_list,columns = ["process","incircle","shots","iterating_shots_val"])

        distinct_processes = list(triple_table['process'].unique())

        #print(distinct_processes)
        estimates = []
        for k in range(0,len(distinct_processes)):
            
            if distinct_processes[k] == distinct_processes[0]:
                base_shots = 0
                base_incircle = 0
            else:
                base_df = triplets_table[triplets_table['process'] == distinct_processes[k-1]].reset_index(drop=True)
                base_shots = base_df['shots'][len(base_df)-1]
                base_incircle = base_df['incircle'][len(base_df)-1]    
            
            current_process_results = triplets_table[triplets_table['process'] == distinct_processes[k]].reset_index(drop=True)

            for q in range(0,len(current_process_results)):
                pi_estimates.append(4*(base_incircle+current_process_results['incircle'][q])/(base_shots+current_process_results['iterating_shots_val'][q]))


        #image Charts
        final_pi_val = estimates[-1]
        pi_estimates_str = [str(z) for z in estimates]
        pi_estimates_str = ",".join(pi_estimates_str)
        
        const_line = ",".join([str(math.pi) for o in range(0,len(estimates))])

       

        return render_template('chart.htm',tables=[triplets_table.to_html(classes='data')],  piestimates =pi_estimates_str ,piline =const_line, titles=triplets_table.columns.values,text = "Estimated value of pi is "+str(final_pi_val))


@app.route('/', methods=['GET','POST'])
def index():

    return render_template('index.htm')


if __name__ == "__main__":
    #run_server()
    app.run(threaded=True,debug=True)



