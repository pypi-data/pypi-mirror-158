"""
Generate useful user or group names
"""

# vim: foldmethod=indent : tw=100
# pylint: disable=invalid-name, superfluous-parens
# pylint: disable=logging-fstring-interpolation, logging-not-lazy, logging-format-interpolation
# pylint: disable=raise-missing-from, missing-docstring, too-few-public-methods

import logging
from .config import CONFIG

logger = logging.getLogger(__name__)


class NameGenerator:
    """
    Meta class that returns one of the actual classes, depending on preference
    """

    def __init__(self, generator_mode: str = "friendly", **kwargs):
        if generator_mode == "friendly":
            self.generator = FriendlyNameGenerator(kwargs["userinfo"])
        else:
            self.generator = PooledNameGenerator(kwargs["pool_prefix"])

    def suggest_name(self, *args, **kwargs) -> str:
        return self.generator.suggest_name(*args, **kwargs)

    def tried_names(self) -> list:
        if isinstance(
            self.generator,
            FriendlyNameGenerator,
        ):
            return self.generator.tried_names()
        return []


class FriendlyNameGenerator:
    """
    Create Names from UserInfo.
    Don't return the same name twice per run
    """

    strategies = [
        "{self.userinfo.preferred_username}",
        "{self.userinfo.given_name}",
        "{self.userinfo.given_name:.3}{self.userinfo.family_name:.3}",
        "{self.userinfo.family_name}",
        "{self.userinfo.given_name:.4}{self.userinfo.family_name:.3}",
        "{self.userinfo.given_name:.5}{self.userinfo.family_name:.3}",
        "{self.userinfo.given_name:.2}{self.userinfo.family_name:.3}",
        "{self.userinfo.given_name:.4}{self.userinfo.family_name:.4}",
        "{self.userinfo.given_name:.5}{self.userinfo.family_name:.4}",
        "{self.userinfo.given_name:.2}{self.userinfo.family_name:.4}",
        "{self.userinfo.given_name:.4}{self.userinfo.family_name:.5}",
        "{self.userinfo.given_name:.5}{self.userinfo.family_name:.5}",
        "{self.userinfo.given_name:.2}{self.userinfo.family_name:.5}",
        "{self.userinfo.given_name:.4}{self.userinfo.family_name:.2}",
        "{self.userinfo.given_name:.5}{self.userinfo.family_name:.2}",
        "{self.userinfo.given_name:.2}{self.userinfo.family_name:.2}",
        "{self.userinfo.email}",
    ]
    next_strategy_idx = -1

    def __init__(self, userinfo):
        """Generate a useful name"""
        self.userinfo = userinfo
        self.dont_use_these_names = []

    def suggest_name(self, forbidden_names: list = None) -> str:
        """suggest a valid username"""
        # Copy forbidden names:
        for name in forbidden_names or []:
            if name.lower() not in self.dont_use_these_names:
                self.dont_use_these_names.append(name.lower())

        while True:

            self.next_strategy_idx += 1
            try:
                candidate_name = (
                    self.strategies[self.next_strategy_idx]
                    .format(**locals())
                    .lower()
                    .replace("@", "-")
                )
            except KeyError:
                continue
            except AttributeError as e:
                print(f"ATTRIBUTE ERROR: {e}")
                continue
            except IndexError:
                NL = "\n    "
                logger.error("Ran out of strategies for generating a friendly username")
                logger.error(
                    f"The list of tried usernames is: \n {NL.join(self.dont_use_these_names)}"
                )
                raise

            if candidate_name.lower() not in self.dont_use_these_names:
                self.dont_use_these_names.append(candidate_name)
                if CONFIG.getboolean("messages", "log_username_creation", fallback=False):
                    logger.info(f"Potential username: '{candidate_name}'")
                return candidate_name.lower()
            else:
                self.dont_use_these_names.append(candidate_name.lower())

    def tried_names(self) -> list:
        return self.dont_use_these_names


class PooledNameGenerator:
    """Name Generator for Pooled Accounts"""

    index = 0
    digits = CONFIG.getint("username_generator", "pool_digits", fallback=3)
    username_prefix = ""

    def __init__(self, pool_prefix: str = "pool"):
        self.username_prefix = CONFIG.get("username_generator", "pool_prefix", fallback=pool_prefix)
        if self.username_prefix is None:
            self.username_prefix = "pool"

    def suggest_name(self) -> str:
        """suggest a valid username"""
        self.index += 1
        candidate_name = f"{self.username_prefix}%0{self.digits}d" % self.index
        return candidate_name
