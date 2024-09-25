def generate_sequence(modulus: int,
                      multiplier: int,
                      increment: int,
                      start_val: int,
                      iterations: int = 1000) -> list[int]:
    """
    Generates a sequence of random numbers using *linear congruential generator*.
    :param modulus: The modulus value (m) which defines the range of the numbers.
    :param multiplier: The multiplier (a) used in the LCG formula.
    :param increment: The increment (c) added in the LCG formula.
    :param start_val: The initial value (X_0) of the sequence.
    :param iterations: Number of iterations to generate, defaults to 1000.
    :return: A list of integers representing the generated sequence.
    """
    if modulus <= 0:
        raise ValueError(f"The modulus has to be greater than 0, got {modulus} instead")
    if not 0 <= multiplier < modulus:
        raise ValueError(f"The multiplier has to be in range [0; {modulus}), got {multiplier} instead")
    if not 0 <= increment < modulus:
        raise ValueError(f"The increment has to be in range [0; {modulus}), got {increment} instead")
    if not 0 <= start_val < modulus:
        raise ValueError(f"The start value has to be in range [0; {modulus}), got {start_val} instead")

    values: list[int] = [start_val] + [0] * (iterations-1)
    current_value: int = start_val
    for i in range(1, iterations):
        current_value = (multiplier * current_value + increment) % modulus
        values[i] = current_value

    return values


def measure_period(values: list[int] | tuple[int]) -> int:
    """
    Measures the period of repeated elements in a sequence.
    :param values: Sequence where the check is performed.
    :return: Period of the elements if present, -1 otherwise
    """
    aux_struct: list = []

    for i, v in enumerate(values):
        if v in aux_struct:  # If the same number found twice, period is present
            prev_ind: int = aux_struct.index(v)
            return i - prev_ind
        aux_struct.append(v)

    return -1


if __name__ == "__main__":
    result = generate_sequence(2 ** 25 - 1, 12 ** 3, 987, 11)
    print(result)
    print(f"Period: {measure_period(result)}, len: {len(result)}")
