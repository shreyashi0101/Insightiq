learning_dna = {
    "distributive_property": 0.8,
    "variable_isolation": 0.8,
    "negative_numbers": 0.8,
    "fractions": 0.8,
    "combining_like_terms": 0.8
}


def update_skill(skill, is_correct):

    if is_correct:
        learning_dna[skill] += 0.05

    else:
        learning_dna[skill] -= 0.10

    learning_dna[skill] = max(
        0,
        min(1, learning_dna[skill])
    )

    return learning_dna


def get_learning_dna():
    return learning_dna