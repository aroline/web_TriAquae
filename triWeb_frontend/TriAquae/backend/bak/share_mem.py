from multiprocessing import Process, Manager

def f(d,n):
    d[i] = i

if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    #l = manager.list(range(10))

    for i in range(15):
     p = Process(target=f, args=(d,i))
     p.start()
     p.join()

    print d
