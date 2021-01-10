import sys


def main():

    delay = {}
    processing_time = {}
    ready_time = {}
    current_time = [0, 0, 0, 0, 0]
    machine = {0: [], 1: [], 2: [], 3: [], 4: []}
    # loading data
    with open(sys.argv[1], 'r') as f:
        tasks_amount = int(f.readline())
        line = f.readline()
        line = line.split('\n')
        for idx, value in enumerate(line[0].split(' ')):
            if value != '':
                delay.update({idx: float(value)})
        for idx, line in enumerate(f):
            d = line.split("\n")
            d = d[0].split(' ')
            processing_time.update({idx: int(d[0])})
            ready_time.update({idx: int(d[1])})

    n = int(tasks_amount / 5)

    # sort machines by delay
    delay = dict(sorted(delay.items(), key=lambda item: item[1]))

    #sort ready time
    
    wspolczynnik = {}

    for task in processing_time:
        wspolczynnik.update({task:processing_time[task]+ready_time[task]})
    cost = 0
    # get first task for each machine
    for machine_idx in delay:
        task = min(wspolczynnik, key=wspolczynnik.get)
        del wspolczynnik[task]
        current_time[machine_idx] = ready_time[task] + processing_time[task]*delay[machine_idx]
        cost += current_time[machine_idx] - ready_time[task]
        del ready_time[task]
        del processing_time[task]
        machine[machine_idx].append(task)

    #loop for adding rest of tasks
    while ready_time:
        available_tasks=[]
        machine_idx = current_time.index(min(current_time))
        for task in ready_time:
            if ready_time[task] <= current_time[machine_idx]:
                    available_tasks.append(task)
        if not available_tasks:
            task = min(ready_time, key=ready_time.get)
            current_time[machine_idx] = ready_time[task] + processing_time[task]*delay[machine_idx]
        else:
            available_processing = []
            for t in available_tasks:
                if t in processing_time:
                    available_processing.append(processing_time[t])
            if not available_processing:
                task = available_tasks[0]
            else:
                task = available_tasks[available_processing.index(min(available_processing))]
            if task not in processing_time:
                task = min(ready_time, key=ready_time.get)
                current_time[machine_idx] = ready_time[task] + processing_time[task]*delay[machine_idx]
            else:
                current_time[machine_idx] += processing_time[task]*delay[machine_idx]
        cost += current_time[machine_idx] - ready_time[task]
        del ready_time[task]
        del processing_time[task]
        machine[machine_idx].append(task)


    with open('136736-solution-' + str(tasks_amount) + '.txt', 'w', newline='') as f:
        f.write(str(round(cost/tasks_amount,2)))
        f.write('\n')
        for i in machine:
            for j in machine[i]:
                f.write(str(j+1)+' ')
            f.write('\n')
if __name__ == "__main__":
    main()
