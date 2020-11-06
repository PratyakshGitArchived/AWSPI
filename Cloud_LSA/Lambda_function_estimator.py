import random
def lambda_handler(event, context):
    shots = int(event['shots'])
    reporting_rate = int(event['reporting_rate'])
    process_id = (event['process_id'])

    triplets = []
    incircle = 0
    for i in range(1, shots+1):
        random1 = random.uniform(-1.0, 1.0)
        random2 = random.uniform(-1.0, 1.0)
        if( ( random1*random1 + random2*random2 ) < 1 ):
            incircle += 1
        if i%reporting_rate == 0:
            triplets.append([process_id,incircle,shots,i])
    return triplets