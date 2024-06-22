from .game import Player, Game
from .painter import present_6_die_name
from .recorder import RunRecord, MakeRecord
from os import linesep


class CLIGame():

    def __init__(self):
        self.prompt_end = "> "
        self.game = Game()
        self.prompted_for_pawn = False
        self.record_maker = MakeRecord()
        self.record_runner = None

    def validate_input(self, prompt, desire_type, allawed_input=None, error_mess="Invalid Option!"
                       , str_len=None):
        prompt += linesep + self.prompt_end
        while True:
            choice = input(prompt)
            if not choice:
                print(linesep + error_mess)
                continue
            try:
                choice = desire_type(choice)
            except ValueError:
                print(linesep + error_mess)
                continue
            if allawed_input:
                if choice in allawed_input:
                    break
                else:
                    print("Invalid Option!")
                    continue
            elif str_len:
                min_len, max_len = str_len
                if min_len < len(choice) < max_len:
                    break
                else:
                    print(linesep + error_mess)
            else:
                break
        print()
        return choice

    def get_user_initial_choice(self):
        text = linesep.join(["choose option",
                             "0 - start new game",
                             "1 - continue game",
                             "2 - run (review) recorded game"])
        choice = self.validate_input(text, int, (0, 1, 2))
        return choice

    def prompt_for_file(self, mode="rb"):
        text = "Enter filename (name of the record)"
        while True:
            filename = self.validate_input(text, str)
            try:
                file_descr = open(filename, mode=mode)
                return file_descr
            except IOError as e:
                print(e)
                print("Try again")

    def does_user_want_save_game(self):
        text = linesep.join(["Save game?",
                             "0 - No",
                             "1 - Yes"])
        choice = self.validate_input(text, int, (0, 1))
        return choice == 1

    def prompt_for_player(self):
        available_colours = self.game.get_available_colours()
        text = linesep.join(["choose type of player",
                             "0 - computer",
                             "1 - human"])
        choice = self.validate_input(text, int, (0, 1))

        if choice == 1:
            name = self.validate_input("Enter name for player",
                                       str, str_len=(1, 30))
            available_options = range(len(available_colours))
            if len(available_options) > 1:
                # show available colours
                options = ["{} - {}".format(index, colour)
                           for index, colour in
                           zip(available_options,
                           available_colours)]
                text = "choose colour" + linesep
                text += linesep.join(options)
                choice = self.validate_input(text, int, available_options)
                colour = available_colours.pop(choice)
            else:
                # only one colour left
                colour = available_colours.pop()
            player = Player(colour, name, self.prompt_choose_pawn)
        elif choice == 0:
            # automatically assign colours
            colour = available_colours.pop()
            player = Player(colour)
        self.game.add_palyer(player)
