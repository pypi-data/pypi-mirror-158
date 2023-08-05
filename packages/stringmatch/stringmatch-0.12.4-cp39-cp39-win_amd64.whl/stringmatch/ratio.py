import Levenshtein  # type: ignore

from stringmatch.scorer import BaseScorer, LevenshteinScorer
from stringmatch.strings import Strings


class Ratio:
    """Contains functions for calculating the ratio of similarity between two strings."""

    def __init__(
        self,
        *,
        scorer: type[BaseScorer] = LevenshteinScorer,
        latinise: bool = False,
        ignore_case: bool = True,
        remove_punctuation: bool = False,
        alphanumeric: bool = False,
        include_partial: bool = False,
        **kwargs,
    ) -> None:
        """Initialise the Match class with the correct scoring algorithm,
        to be passed along to the Ratio class.

        Parameters
        ----------
        scorer : type[BaseScorer], optional
            The scoring algorithm to use, by default LevenshteinScorer
            Available scorers: LevenshteinScorer, JaroScorer, JaroWinklerScorer.
        latinise : bool, optional
            If special unicode characters should be removed from the strings, by default False.
        ignore_case : bool, optional
            If the strings should be compared ignoring case, by default True.
        remove_punctuation : bool, optional
            If punctuation should be removed from the strings, by default False.
        alphanumeric : bool, optional
            If the strings should only be compared by their latin letters, by default False.
        include_partial : bool, optional
            If partial substring matches should be included, by default False.
        """
        self.scorer = scorer
        self.latinise = latinise
        self.ignore_case = ignore_case
        self.remove_punctuation = remove_punctuation
        self.alphanumeric = alphanumeric
        self.include_partial = include_partial

    def _prepare_strings(self, string1: str, string2: str) -> tuple[str, str]:
        """Modifies the strings to be ready for comparison, according to the settings.
        Only meant for internal usage.
        """
        if self.latinise:
            string1, string2 = Strings().latinise(string1), Strings().latinise(string2)

        if self.ignore_case:
            string1, string2 = Strings().ignore_case(string1), Strings().ignore_case(
                string2
            )

        if self.remove_punctuation:
            string1, string2 = Strings().remove_punctuation(
                string1
            ), Strings().remove_punctuation(string2)

        if self.alphanumeric:
            string1, string2 = Strings().alphanumeric(string1), Strings().alphanumeric(
                string2
            )

        return (string1, string2)

    def ratio(self, string1: str, string2: str) -> int:
        """Returns the similarity score between two strings.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.

        Returns
        -------
        int
            The score between 0 and 100.
        """
        if self.include_partial:
            return self.partial_ratio(string1, string2)

        # If you happen to pass in a non-string we will just return 0 instead of raising an error.
        # Could happen if you have an incredibly large list of strings and something sneaks in i guess.
        if not all(isinstance(s, str) for s in [string1, string2]):
            return 0

        string1, string2 = self._prepare_strings(string1, string2)

        # If either string is empty after modifying we also wanna return 0.
        if not string1 or not string2:
            return 0

        return round(self.scorer().score(string1, string2) * 100)

    def ratio_list(self, string: str, string_list: list[str]) -> list[int]:
        """Returns the similarity score between a string and a list of strings.

        Parameters
        ----------
        string : str
            The string to compare.
        string_list : list[str]
            The list of strings to compare to.

        Returns
        -------
        list[int]
            The scores between 0 and 100.
        """

        return [self.ratio(string, s) for s in string_list]

    def partial_ratio(self, string1: str, string2: str) -> int:
        """Returns the similarity score between subsections of strings.

        Parameters
        ----------
        string1 : str
            The first string to compare.
        string2 : str
            The second string to compare.

        Returns
        -------
        int
            The score between 0 and 100.
        """
        if not all(isinstance(s, str) for s in [string1, string2]):
            return 0

        string1, string2 = self._prepare_strings(string1, string2)

        if not string1 or not string2:
            return 0

        if len(string1) >= len(string2):
            longer_string, shorter_string = string1, string2
        else:
            longer_string, shorter_string = string2, string1

        blocks = [
            b
            for b in Levenshtein.matching_blocks(
                Levenshtein.editops(longer_string, shorter_string),
                longer_string,
                shorter_string,
            )
            # Doesn't make too much sense to me to match substrings with a length of 1,
            # except when they are at the start of a string, so we filter those out.
            if (b[2] > 1 or (b[2] == 1 and b[0] == 0))
        ]

        # Gets the correct multiplier for the partial ratio.
        # The longer the strings are apart in length, the smaller the multiplier.
        diff = len(longer_string) - len(shorter_string)

        if diff >= 20:
            # Since the default cutoff score is 70, this would not show up on default settings.
            multiplier = 65
        elif diff >= 10:
            multiplier = 75
        elif diff >= 4:
            multiplier = 85
        elif diff >= 1:
            # We want to reserve a score of 100 for perfect matches.
            multiplier = 95
        else:
            multiplier = 100

        scores = []

        for block in blocks:
            start = max((block[0] - block[1]), 0)
            substring = longer_string[start : start + len(shorter_string)]

            scores.append(
                round(
                    self.scorer().score(
                        substring,
                        shorter_string,
                    )
                    * multiplier
                ),
            )

        # Also gets the "normal score" for both starting strings,
        # and returns whichever one is higher.
        scores.append(round(self.scorer().score(string1, string2) * 100))

        return max(scores, default=0)
