import sys
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import string
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from heapq import nlargest

punctuations = string.punctuation
from spacy.language import Language

nlp = English()
nlp.add_pipe('sentencizer')  # updated
parser = English()


def pre_process(document):
    clean_tokens = [token.lemma_.lower().strip() for token in document]
    clean_tokens = [token for token in clean_tokens if token not in STOP_WORDS and token not in punctuations]
    tokens = [token.text for token in document]
    lower_case_tokens = list(map(str.lower, tokens))

    return lower_case_tokens


def generate_numbers_vector(tokens):
    frequency = [tokens.count(token) for token in tokens]
    token_dict = dict(list(zip(tokens, frequency)))
    maximum_frequency = sorted(token_dict.values())[-1]
    normalised_dict = {token_key: token_dict[token_key] / maximum_frequency for token_key in token_dict.keys()}
    return normalised_dict


def sentences_importance(text, normalised_dict):
    importance = {}
    for sentence in nlp(text).sents:
        for token in sentence:
            target_token = token.text.lower()
            if target_token in normalised_dict.keys():
                if sentence in importance.keys():
                    importance[sentence] += normalised_dict[target_token]
                else:
                    importance[sentence] = normalised_dict[target_token]
    return importance


def generate_summary(rank, text):
    target_document = parser(text)
    importance = sentences_importance(text, generate_numbers_vector(pre_process(target_document)))
    summary = nlargest(rank, importance, key=importance.get)
    return summary


if __name__ == '__main__':
    summary = generate_summary(3, "Rewards totaling $33,000 are being offered for information leading to 7-year-old "
                                  "Harmony Montgomery. "
                                  "She was last seen at a Manchester home in October 2019, when she was 5."
                                  "Adam Montgomery, 31, was arrested Tuesday on charges including second-degree "
                                  "assault connected to an incident in 2019 involving the missing girl, interference "
                                  "with custody and endangering the welfare of a child. "
                                  "The assault charge is a felony. Although an arrest has been made, the search for "
                                  "Harmony continues, New Hampshire Attorney General John M. Formella wrote in a "
                                  "statement. "
                                  "Adam Montgomery waived his arraignment Wednesday in the Hillsborough County "
                                  "Superior Court North. He had not guilty pleas entered on his behalf by his lawyer "
                                  "and has been jailed without bail. "
                                  "According to an affidavit, Adam Montgomery is suspected of hitting his daughter in "
                                  "the face and claimed that he brought her to live with her mother, who lived in "
                                  "Lowell, Massachusetts. "
                                  "Manchester Police Chief Allen Aldenberg said Harmony was in the child welfare "
                                  "system in Massachusetts and New Hampshire. "
                                  "It was New Hampshire's Division of Children, Youth and Families that notified "
                                  "police last week that Harmony was missing and last seen two years ago, "
                                  "the chief said. "
                                  "A source told WCVB sister station WMUR that Harmony had been reunited with her "
                                  "father after spending time in foster care in Massachusetts. "
                                  "An affidavit from the case indicates that Harmony's mother called Manchester "
                                  "Police Department to report the girl missing on Nov. 18, 2021. She originally told "
                                  "officers she hadn't seen her in over six months, but then said it had been since "
                                  "Easter 2019 when she video chatted with Adam Montgomery and Harmony, according to "
                                  "the affidavit. "
                                  "Harmony's mother told police she had lost custody of the girl to the state in "
                                  "2018, in part to a substance abuse issue. According to the affidavit, "
                                  "she told police that since Easter 2019, she attempts to find Harmony by contacting "
                                  "various schools and driving by addresses associated with Adam Montgomery, "
                                  "but those efforts were unsuccessful. Harmony's mother said last year, "
                                  "Adam Montgomery and his partner had blocked all communication from her. A "
                                  "boyfriend who lived with Harmony's mother in 2019 said he never met Harmony in "
                                  "person. "
                                  "The Manchester Police Department contacted DCYF to get contact information about "
                                  "the father, but was unable to find him at the addresses provided. More than a "
                                  "month later, on Dec. 27, 2021, DCYF contacted police to report they were unable to "
                                  "locate Harmony. The affidavit says that was when the department initiated its "
                                  "investigation.")
    print(summary)
