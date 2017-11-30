import multiprocessing as mp

POISON_PILL = "STOP"

def process_odds(in_queue, shared_list):
        while True:
            # block until something placed on the queue
            new_value = in_queue.get()

            #   check to see if we just got the poison pill
            if new_value == POISON_PILL:
                break

            # we didn't, so do the processing and put the result in the shared data structure
            shared_list.append(new_value/2)
        return

def process_evens(in_queue, shared_list):
    while True:
        new_value = in_queue.get()
        if new_value == POISON_PILL:
            break

        shared_list.append(new_value/-2)

    return

def main():
    # create a manager - it lets us share native Python object types like
    # lists and dictionaries without worrying about synchronization -
    # the manager will take care of it
    manager = mp.Manager()

    # now using the manager, create our shared data structures
    odd_queue = manager.Queue()
    even_queue = manager.Queue()
    shared_list = manager.list()

    #lastly, create our pool of workers - this spawns the processes,
    # but they don't start actually doing anything yet
    pool = mp.Pool()

    # now we'll assign two function to the pool for them to run
    # one to handle even number, one to handle odd numbers
    odd_result = pool.apply_async(process_odds, (odd_queue, shared_list))
    even_result = pool.apply_async(process_evens, (even_queue, shared_list))
    # this code doesn't do anything with the odd_result and even_result
    # variables, but you have flexibility to check exit codes
    # and other such things if you want - see docs for AsyncResult objects

    #now that the processes are running and waiting for their queues
    # to have something, lets give them some work to do by iterating over our data, deciding who should process it, and putting it in
    # their queue
    for i in range(10):
        if(i%2) == 0: # use mod operator to see if "i" is even
            even_queue.put(i)
        else:
            odd_queue.put()