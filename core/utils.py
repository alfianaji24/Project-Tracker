from decimal import Decimal


def format_rupiah(value: Decimal | int | float | None) -> str:
    if value is None:
        return "-"
    amount = Decimal(value)
    formatted = f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"Rp {formatted}"
