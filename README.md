# physarum agent simulation
The core premise of this simulation is as follows; Autonomous cells deposits a trail at their position which diffuses over time. This trail is scented by other cells and stochastiaclly chooses to move in direction in which the trail is the strongest.

These sets of traits and conditions, published in a paper on [physarum patterns](https://uwe-repository.worktribe.com/output/980579) by Jeff Jones and explored further in a blog post by [Sage Jenson](https://sagejenson.com/physarum), causes the cells to form structures and patterns similar to that of the Physarum Polycephalum, a unicellular slime mold species.

<p align="center">
  <img width="489" height="490" src="/images/image1.png">
</p>


### installation windows
```
virtualenv venv 
venv\Scripts\activate
pip install -r requirements.txt
```
### Background
The physarum slime mold as been widely studies because it seemingly inhibits a form of [collective intelligence](https://www.nature.com/news/how-brainless-slime-molds-redefine-intelligence-1.11811), which which it can solve optimization problems such as solving [mazes](https://www.nature.com/articles/35035159), [shortest path problems](https://arxiv.org/abs/1106.0423) and [mimicking the Tokyo rail system](https://science.sciencemag.org/content/327/5964/439). More over, the slime mold can also be configured in such ways as to make [logical gates](https://www.sciencedirect.com/science/article/pii/S136970211400025X) and have been used for [dark matter simulations](https://www.nasa.gov/feature/goddard/2020/slime-mold-simulations-used-to-map-dark-matter-holding-universe-together).

These characteristics of unicellular collective intelligence has inspired a variety of [optimization algorithms](https://arxiv.org/pdf/1712.02910.pdf) which tries to capture the traits of the physarum by modelling different aspects of the slime mold ranging from fluid dynamics to graph theory. 

### Objective
This a project in which I wish to use the system stipulated by Jeff Jones as a stepping stone to explore aspects of its possible traits of intelligence, approach it from a evolutionary simulation context and analyze it from a systems theory perspective to my best ability.


![Multiple species](/images/image2.png)
