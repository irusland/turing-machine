from turing_machine import TuringMachine, State, StepFunction, Tape, Heading


def main():
    states_count = int(input())
    states = [map(State, input().split())]
    state_initial, state_final = (map(State, input().split()))
    states_final = {state_final}
    steps_count = int(input())
    steps = dict()
    for _ in range(steps_count):
        state, symbol, _, state_next, symbol_next, heading = input().split()
        state = State(state)
        state_next = State(state_next)
        heading = Heading(heading)
        steps[(state, symbol)] = (state_next, symbol_next, heading)
    tape = Tape(input())

    machine = TuringMachine(tape=tape,
                            alphabet=tape.get_alphabet(),
                            empty='_',
                            step_function=StepFunction(steps),
                            states=states,
                            state_initial=state_initial,
                            states_final=states_final)

    while True:
        is_running = machine.make_step()
        if machine.is_final():
            print(f'STOP after {machine.step_count} transitions')
            break
        if is_running:
            if machine.step_count >= 10 ** 5:
                print(f'MADE 100000 transitions')
                break
        else:
            print(f'FAIL after {machine.step_count} transitions')
            break
    # todo ___00___
    # todo        ^index
    # todo ___00___
    # todo ^index

    start = next((k for k, v in machine.tape.tape.items() if v != '_'), None)
    if start is not None:
        stop = next(
            (k for k, v in reversed(machine.tape.tape.items()) if v != '_'),
            None)
        tape = []
        for i in range(start, stop + 1):
            tape.append(machine.tape.tape[i])
        print(''.join(tape))
        print(machine.state, machine.position - start)
    else:
        print()
        print(machine.state, 0)


if __name__ == '__main__':
    main()
