from playground import Playground

mach_config = [
    [[255, 0, 0], [300, 400]],
    [[255, 0, 0], [300, 300]],
    [[255, 0, 0], [300, 200]],
]
env = Playground()
env.set_target(point=(200, 200))
env.set_machine(mach_config)
env.run()