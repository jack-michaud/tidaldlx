from tidaldlx.lib.tidal.login.session import Session
from tidaldlx.lib.ui.notify import Notify


class PromptForLogin:
    def __init__(self, notify: Notify) -> None:
        self.notify = notify

    def needs_login(self, session: Session) -> bool:
        return not session.check_login()

    def prompt_for_login(self, session: Session) -> bool:
        login, future = session.login_oauth()

        self.notify.notify("Open the URL to log in", login.verification_uri_complete)

        future.result()

        if not self.needs_login(session):
            print("Logged in")
            return True
        else:
            print("Failed to log in")
            return False
