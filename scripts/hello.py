import simpy


def car(env):
    while True:
        print(f"Start parking at {env.now}")
        parking_duration = 5
        yield env.timeout(parking_duration)

        print(f"Start driving at {env.now}")
        trip_duration = 2
        yield env.timeout(trip_duration)


def main():
    env = simpy.Environment()
    env.process(car(env))
    env.run(until=15)


if __name__ == "__main__":
    main()
