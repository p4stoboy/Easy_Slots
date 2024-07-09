from multiprocessing import Pool, Lock
from random import seed

from machine import spin

# threaded RTP test
def test(iters = 100000000):
    payout = 0
    with Pool() as p:
        for res in p.imap_unordered(spin, [1] * iters, chunksize=iters//100):
            payout += res
        p.close()
        p.join()
    print()
    print(f"payout: {payout}")
    print(f"RTP: {(payout / iters) * 100}%")
    return payout

# normal test
def test2(iters = 100000, _seed=51):
    seed(_seed)
    payout = 0
    for i in range(iters):
        payout += spin()
    print(f"RTP: {(payout / iters) * 100}%")
