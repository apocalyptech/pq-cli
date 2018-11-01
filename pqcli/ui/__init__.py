import typing as T

import urwid

from pqcli.game_state import Roster
from pqcli.ui.exit_view import ExitView
from pqcli.ui.new_game_view import NewGameView
from pqcli.ui.roster_view import RosterView


urwid.command_map["k"] = "cursor up"
urwid.command_map["K"] = "cursor up"
urwid.command_map["j"] = "cursor down"
urwid.command_map["J"] = "cursor down"
urwid.command_map["h"] = "cursor left"
urwid.command_map["H"] = "cursor left"
urwid.command_map["l"] = "cursor right"
urwid.command_map["L"] = "cursor right"


class Ui:
    def __init__(self, roster: Roster) -> None:
        self.roster = roster
        self.loop = urwid.MainLoop(None, unhandled_input=self.unhandled_input)
        self.old_view: T.Optional[urwid.Widget] = None

        self.switch_to_roster_view()

    def run(self) -> None:
        self.loop.run()

    def unhandled_input(self, key: str) -> bool:
        callback = getattr(self.loop.widget, "unhandled_input", None)
        if callback and callback(key):
            return True

        if key == "ctrl q":
            self.old_view = self.loop.widget
            self.switch_to_exit_view()
            return True

        return False

    def switch_to_roster_view(self) -> None:
        self.loop.widget = RosterView(
            self.roster,
            self.loop,
            on_exit=self.switch_to_exit_view,
            on_new_game=self.switch_to_new_game_view,
            on_resume_game=self.switch_to_game_view,
        )

    def switch_to_exit_view(self) -> None:
        self.old_view = self.loop.widget
        self.loop.widget = ExitView(
            self.old_view, on_exit=self.exit, on_cancel=self.cancel_exit
        )

    def switch_to_new_game_view(self) -> None:
        self.loop.widget = NewGameView(
            on_confirm=self.switch_to_game_view,
            on_cancel=self.switch_to_roster_view,
        )

    def switch_to_game_view(self, player_name: str) -> None:
        ...

    def exit(self) -> None:
        raise urwid.ExitMainLoop()

    def cancel_exit(self) -> None:
        assert self.old_view is not None
        self.loop.widget = self.old_view
        self.old_view = None
