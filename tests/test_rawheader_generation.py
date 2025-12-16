from conftest import INPUT_DIR, OUTPUT_DIR, check_header, generate_header


def test_array_c():
    generated = generate_header(INPUT_DIR / "array.rdl", "c")
    check_header(generated, OUTPUT_DIR / "array.h")
