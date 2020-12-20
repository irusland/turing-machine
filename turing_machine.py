from enum import Enum


class Tape:
    def __init__(self, tape):
        self.tape = dict((enumerate(tape)))

    def __str__(self):
        st = []
        for i, c in sorted(self.tape.items(), key=lambda kv: kv[0]):
            st.append(c)
        return "".join(st)

    def __getitem__(self, index: int) -> str:
        if index in self.tape:
            return self.tape[index]
        else:
            self.tape[index] = '_'
            return self.tape[index]

    def __setitem__(self, i, char):
        self.tape[i] = char

    def get_alphabet(self) -> [str]:
        return self.tape.values()


class State:
    def __repr__(self) -> str:
        return self.name

    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, State) and obj.name == self.name

    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return self.name.__hash__()


class Heading(Enum):
    def __repr__(self):
        return self.name

    UP = 'S'
    LEFT = 'L'
    RIGHT = 'R'


class StepFunction:
    def __init__(self, steps: {(State, str): (State, str, Heading)}):
        self.function = dict()
        for step in steps.items():
            (state, letter), (state_next, letter_next, heading) = step
            self.function[(state, letter)] = (state_next, letter_next, heading)

    def get_step(self, step: (State, str)) -> (State, str, Heading):
        if step in self.function:
            return self.function[step]


class TuringMachine:
    def __init__(self,
                 tape: Tape,
                 alphabet: [str],
                 empty: str,
                 step_function: StepFunction,
                 states: {State},
                 state_initial: State,
                 states_final: {State},
                 is_debug_mode=False):
        self.tape = tape
        self.alphabet = alphabet
        self.state_initial = state_initial
        self.states = states
        self.states_final = states_final
        self.step_function = step_function

        self.position = 0
        self.empty = empty
        self.state = state_initial
        self.symbol = None
        self.step_count = 0
        self.IS_DEBUG_MODE = is_debug_mode

    def get_tape(self) -> str:
        return str(self.tape)

    def make_step(self) -> bool:
        self.symbol = self.tape[self.position]
        if self.symbol is None:
            self.symbol = self.empty
        step = self.step_function.get_step((self.state, self.symbol))
        if step is not None:
            if self.IS_DEBUG_MODE:
                print(self.state, self.symbol, '>', *step, sep='\t')
                print(self.get_tape())
                print(' ' * self.position + '^')
            state_next, symbol_next, heading = step
            self.tape[self.position] = symbol_next
            if heading == Heading.RIGHT:
                self.position += 1
            elif heading == Heading.LEFT:
                self.position += -1
            self.state = state_next
            self.step_count += 1
            if self.IS_DEBUG_MODE:
                print(self.get_tape())

                print(' ' * (self.position if self.position >= 0 else -(
                        len(self.get_tape()) + self.position)) + '^')
                print()
            return True
        else:
            if self.IS_DEBUG_MODE:
                print(self.state, self.symbol, '>', '?', sep='\t')
                print(self.get_tape())
                print(' ' * self.position + '^')
            return False

    def is_final(self) -> bool:
        return self.state in self.states_final
