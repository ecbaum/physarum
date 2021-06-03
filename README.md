# physarum agent simulation
The core premise of this simulation is as follows; Autonomous cells deposit a trail at their position which diffuses over time. This trail is scented by other cells and they stochastically choose to move in the direction in which the trail is the strongest.

These sets of traits and conditions, published in a paper on [physarum patterns](https://uwe-repository.worktribe.com/output/980579) by Jeff Jones and explored further in a blog post by [Sage Jenson](https://sagejenson.com/physarum), cause the cells to form structures and patterns similar to that of the Physarum Polycephalum, a unicellular slime mold species.

<p align="center">
  <img width="489" height="490" src="/images/image1.png">
</p>


### installation
```
virtualenv venv 
source venv/bin/activate
pip install -r requirements.txt
```

for windows
```source venv/bin/activate``` becomes ```venv\Scripts\activate ``` 

