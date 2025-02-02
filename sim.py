from playground import Playground

env = Playground()
env.set_target(point=(200,200))
env.set_machine(
    [
        ((255,0,0), (300,400), (300,300)),
        ((255,0,0), (300,300), (300,200)),
        ((255,0,0), (300,200), (300,100)),
    ]
)
env.run()
