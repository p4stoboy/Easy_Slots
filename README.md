#### Python slot machine implementation with linear program derived payout coefficients

###### by Oscar Harris

---

*Disclaimer: This code is not to be re-used or re-distributed and certainly not utilised in any commercial project. The author reserves all rights.*



**Testing RTP**

`test_rtp.py` has a threaded function (`test()` (default 100,000,000 spins)) which can be called to confirm the payout coefficients derived from the linear optimisation outlined below actually determine the RTP set against the optimisation (note: this LP is a bit basic and the RTP error margin over 100,000,000 spins is at around 1.5% currently).



**Basic Info**

- 3 reel machine.

- 5 pay lines (3 horizontal, 2 diagonal).

- 5 symbols (this is arbitrary, the symbol and reel sets can be mutated on the fly and new payout coefficients derived from LP implementation.

- RTP @ 0.9 which can also be adjusted and new coefficients derived.

- Win = 3 of the same symbol across any line.



**Current implementation**

$N=number\ of\ symbols$

$S:=set\ of\ symbols\ s_n=\{A,B,C,D,Z\},\ n\in\{1,...,N\}$



$R:=set\ of\ reels\ r_i,\ i\in\{1,2,3\}$

$r_1=\{A,A,A,A,B,B,C,D,Z\}$

$r_2=\{A,A,A,A,B,B,C,C,D,D,Z\}$

$r_3=\{A,A,B,C,C,D,Z\}$

$k_{in}=number\ of\ symbol\ s_n\ on\ reel\ r_i$

$l_i=total\ length\ of\ reel\ r_i$



$P:=set\ of\ independent\ probabilities\ p_n\ of\ symbol\ s_n\ winning\ on\ any\ given\ line$

$p_n=\frac{k_{1n}k_{2n}k_{3n}}{l_1l_2l_3}$



$A:=set\ of\ absolute\ probabilities\ a_n\ of\ any\ given\ symbol\ s_n\ paying\ across\ all\ lines$

$a_n=1-(1-p_n)^5$



$C:=set\ of\ payout\ coefficients\ c_n\ pertaining\ to\ a\ winning\ line\ against\ s_n\ where\ payout=c_n\times\ bet$

$RTP=0.9$



**Derive $C$ from LP**

$max:\sum\limits^5_{n=1}c_n$

$s.t.$

$\sum\limits^5_{n=1}c_na_n\leq RTP$

$c_n\geq 0.8,\ n=1,...,5$

$c_n\geq \frac{13}{10}c_{n-1},\ n=2,...,5$



The bottom two constraints are fairly arbitrary, they exist purely to ensure that we don't end up with 4 symbols which have payout multipliers $<1$ and one huge one, and also to ensure the multiplier increases as the chance of win decreases.

This implementation allows us to change the number of symbols and state of each reel haphazardly without having to manually adjust the win multipliers.


