import re
import threading

import sublime
import sublime_plugin

from .kavel_api import KavelError, generate

SETTINGS = "Kavel.sublime-settings"


class KavelGenerateImageCommand(sublime_plugin.TextCommand):
    """Ask for a prompt (prefilled with the selection), generate in the background,
    then insert the image's Markdown link where the cursor was."""

    def run(self, edit):
        sel = self.view.sel()
        selected = self.view.substr(sel[0]).strip() if len(sel) else ""
        self.view.window().show_input_panel(
            "Kavel image prompt:", selected, self.on_prompt, None, None)

    def on_prompt(self, prompt):
        prompt = prompt.strip()
        if not prompt:
            return
        point = self.view.sel()[0].end() if len(self.view.sel()) else self.view.size()
        settings = sublime.load_settings(SETTINGS)
        threading.Thread(target=self.work, args=(prompt, point, settings), daemon=True).start()

    def work(self, prompt, point, settings):
        ticks = [0]

        def on_wait():
            ticks[0] += 1
            self.view.set_status("kavel", "Kavel: generating" + "." * (ticks[0] % 4))

        self.view.set_status("kavel", "Kavel: generating")
        try:
            url = generate(
                prompt,
                api_key=settings.get("api_key", ""),
                model=settings.get("model", ""),
                aspect_ratio=settings.get("aspect_ratio", "1:1"),
                on_wait=on_wait,
            )
        except KavelError as e:
            self.view.erase_status("kavel")
            sublime.error_message("Kavel: %s" % e)
            return
        self.view.erase_status("kavel")
        alt = re.sub(r"[\[\]]", "", prompt)
        link = "![%s](%s)" % (alt, url)
        sublime.set_clipboard(url)
        if settings.get("insert_link", True):
            self.view.run_command("kavel_insert_text", {"point": point, "text": link})
            sublime.status_message("Kavel: image ready - link inserted, URL copied")
        else:
            sublime.status_message("Kavel: image ready - URL copied")


class KavelInsertTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, point, text):
        self.view.insert(edit, min(point, self.view.size()), "\n" + text + "\n")
