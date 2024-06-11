def format_metrics(metrics):
    if not metrics:
        return "You have not recorded any water metrics yet."
    return "Your water metrics:\n" + "\n".join([f"{amount} {unit}" for amount, unit in metrics])
