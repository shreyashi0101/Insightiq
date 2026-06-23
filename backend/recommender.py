from backend.learning_dna import (
    learning_dna
)


def get_weakest_skill():

    return min(
        learning_dna,
        key=learning_dna.get
    )